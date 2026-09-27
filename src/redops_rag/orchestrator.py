"""Deterministic, read-only routing for the RedOps specialist-agent registry."""
from __future__ import annotations

import re

from .workflow import plan_engagement

WORD_RE = re.compile(r"[a-z0-9][a-z0-9+.#_-]*")

# Operator-facing names used by the Exegol → Herdr → OpenCode graph.  The
# registry profile remains the policy source; these aliases are only spawn labels.
WORKSPACE_AGENT_ALIASES: dict[str, tuple[str, ...]] = {
    "recon_agent": ("recon",),
    "web_agent": ("web-recon", "web-exploit"),
    "ad_agent": ("ad-enum", "ad-exploit"),
    "windows_redteam_agent": ("windows-privesc",),
    "assessment_agent": ("cve-research",),
    "exploitation_agent": ("web-exploit",),
    "post_exploitation_agent": ("persistence",),
    "lateral_movement_agent": ("ad-exploit",),
}


# Keep routing conservative and explainable. The registry remains the source of
# truth for detailed guardrails; this table only supplies a dependency-free index
# usable from an installed CLI/MCP process. Lab and workflow vocabulary keeps
# readiness/recon tasks away from a zero-score fallback.
ROUTES: tuple[tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]], ...] = (
    (
        "scope_agent",
        (
            "scope",
            "authorization",
            "rules of engagement",
            "engagement packet",
            "workflow",
            "readiness",
            "pre-engagement",
            "success criteria",
        ),
        ("methodology", "misc"),
        ("redops-rag",),
    ),
    (
        "recon_agent",
        (
            "recon",
            "reconnaissance",
            "information gathering",
            "asset inventory",
            "htb",
            "hack the box",
            "lab machine",
            "ctf",
            "user.txt",
            "root.txt",
        ),
        ("network", "web", "ad", "cloud", "mobile", "methodology", "tools"),
        ("redops-rag", "redops-exegol", "terminal-bounded"),
    ),
    (
        "ad_agent",
        (
            "active directory", "entra", "azure ad", "ldap", "kerberos", "bloodhound", "adcs",
            "domain", "acl", "dacl", "genericwrite", "forcechangepassword",
            "ntsecuritydescriptor", "signed ldap",
        ),
        ("ad", "windows", "database", "methodology", "tools"),
        ("redops-rag", "redops-exegol", "terminal-bounded"),
    ),
    (
        "windows_redteam_agent",
        (
            "windows", "winrm", "powershell", "lolbas", "seatbelt", "winpeas", "dll hijack",
            "vsix", "vscode", "visual studio code", "extension", "devdrop", "supply chain",
        ),
        ("windows", "redteam", "tools", "vulnerabilities", "ad", "methodology", "devops"),
        ("redops-rag", "redops-exegol", "terminal-bounded"),
    ),
    (
        "web_agent",
        ("web", "api", "http", "https", "xss", "sqli", "ssrf", "csrf", "waf", "browser", "xsrf"),
        ("web", "api", "vulnerabilities", "network", "methodology", "tools", "redteam"),
        ("redops-rag", "redops-exegol", "burp", "camoufox", "terminal-bounded"),
    ),
    (
        "cloud_agent",
        ("aws", "azure", "gcp", "cloud", "iam", "s3", "lambda", "kubernetes", "terraform"),
        ("cloud", "ad", "container", "devops", "network", "vulnerabilities", "methodology", "tools"),
        ("redops-rag", "redops-exegol", "terminal-bounded"),
    ),
    (
        "mobile_agent",
        ("android", "ios", "iphone", "apk", "ipa", "flutter", "frida", "mobile", "react native"),
        ("mobile", "reversing", "vulnerabilities", "web", "network", "tools", "methodology"),
        ("redops-rag", "redops-exegol", "burp", "uiautomator2", "ghidra", "radare2", "terminal-bounded"),
    ),
    (
        "reversing_tools_agent",
        ("reverse", "reversing", "malware", "binary", "elf", "pe file", "ghidra", "radare2", "disassembly"),
        ("reversing", "malware", "tools", "vulnerabilities", "windows", "linux", "mobile", "methodology"),
        ("redops-rag", "redops-exegol", "ghidra", "radare2", "terminal-bounded"),
    ),
    (
        "network_agent",
        ("network", "nmap", "port scan", "pcap", "tshark", "wireless", "wifi", "pivot"),
        ("network", "wireless", "linux", "windows", "web", "vulnerabilities", "tools", "methodology"),
        ("redops-rag", "redops-exegol", "terminal-bounded"),
    ),
    (
        "container_devops_agent",
        ("docker", "container", "kubernetes", "k8s", "cicd", "devops", "supply chain", "trivy"),
        ("container", "devops", "cloud", "linux", "vulnerabilities", "tools", "methodology"),
        ("redops-rag", "redops-exegol", "terminal-bounded"),
    ),
    (
        "web3_agent",
        ("web3", "smart contract", "solidity", "defi", "ethereum", "evm", "wallet", "dapp", "blockchain"),
        ("web3", "web", "vulnerabilities", "reversing", "network", "tools", "methodology"),
        ("redops-rag", "redops-exegol", "burp", "ghidra", "radare2", "terminal-bounded"),
    ),
    (
        "rag_curator_agent",
        ("knowledge", "rag", "corpus", "scrape", "scraping", "noise", "deduplicate", "ingest", "writeup"),
        ("knowledge", "writeups", "methodology"),
        ("redops-rag", "terminal-bounded"),
    ),
)

_NO_MATCH_FALLBACK: dict[str, object] = {
    "agent": "rag_curator_agent",
    "workspace_agents": ["redops"],
    "score": 0,
    "rationale": "no niche keyword matched; retrieve context before selecting a specialist",
    "knowledge": ["methodology"],
    "allowed_mcp": ["redops-rag", "terminal-bounded"],
}


def _terms(task: str) -> set[str]:
    return set(WORD_RE.findall(task.lower()))


def rank_routes(
    task: str, limit: int = 3, boost_terms: tuple[str, ...] = ()
) -> list[dict[str, object]]:
    """Explainable keyword ranking over ROUTES; routing only, never execution.

    ``boost_terms`` (for example an OS hint supplied with lab context) double-weight
    their matches so the matching specialist ranks first without changing gates.
    """

    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("limit must be a positive integer")
    lowered = task.strip().lower()
    terms = _terms(lowered)
    boosted = {term.lower() for term in boost_terms if isinstance(term, str) and term}
    ranked: list[dict[str, object]] = []
    for agent, keywords, knowledge, mcp in ROUTES:
        matches = [keyword for keyword in keywords if keyword in lowered or keyword in terms]
        if not matches:
            continue
        score = sum(2 if keyword in boosted else 1 for keyword in matches)
        ranked.append(
            {
                "agent": agent,
                "workspace_agents": list(WORKSPACE_AGENT_ALIASES.get(agent, (agent,))),
                "score": score,
                "rationale": "matched: " + ", ".join(matches[:5]),
                "matched": matches[:5],
                "knowledge": list(knowledge),
                "allowed_mcp": list(mcp),
            }
        )
    ranked.sort(key=lambda item: (-int(item["score"]), str(item["agent"])))
    return ranked[:limit]


def route_task(
    task: str,
    limit: int = 3,
    *,
    lab: str | None = None,
    os_hint: str = "unknown",
) -> dict[str, object]:
    """Return an explainable delegation plan; never executes a target command.

    ``lab``/``os_hint`` attach the same read-only lab context as the workflow
    planner: routing hints are enriched with the lab's tags and the embedded
    workflow becomes the lab engagement plan, but scope gates are delegated
    untouched and can never be confirmed by lab metadata.
    """

    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 5:
        raise ValueError("limit must be an integer between 1 and 5")
    normalized = task.strip()
    if lab is None:
        workflow = plan_engagement(normalized)
        enriched = normalized
        boost: tuple[str, ...] = ()
    else:
        # Deferred import: labs imports this module for ROUTES/rank_routes.
        from .labs import describe_lab, lab_engagement, normalize_os_hint

        normalized_os = normalize_os_hint(os_hint)
        workflow = lab_engagement(normalized, lab=lab, os_hint=normalized_os)
        tags = " ".join(str(tag) for tag in describe_lab(lab)["routing_tags"])
        enriched = " ".join(part for part in (normalized, tags) if part)
        boost = (normalized_os,) if normalized_os != "unknown" else ()
    selected = rank_routes(enriched, limit, boost)
    if not selected:
        selected = [dict(_NO_MATCH_FALLBACK)]
    return {
        "task": normalized,
        "workflow": workflow,
        "authorization_required": True,
        "execution_policy": "orchestrator routes only; specialist executes via Exegol after scope confirmation",
        "workspace_agent_graph": [
            "recon", "web-recon", "web-exploit", "cve-research", "ad-enum",
            "ad-exploit", "linux-privesc", "windows-privesc", "persistence",
        ],
        "selected_agents": selected,
        "delegation_contract": {
            "include": ["written_scope", "retrieved_sources", "artifacts", "expected_output"],
            "exclude": ["credentials", "tokens", "unscoped_targets", "claims_without_command_output"],
        },
    }
