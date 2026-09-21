"""Deterministic, read-only routing for the RedOps specialist-agent registry."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from .workflow import plan_engagement


@dataclass(frozen=True, slots=True)
class AgentRoute:
    agent: str
    score: int
    rationale: str
    knowledge: tuple[str, ...]
    allowed_mcp: tuple[str, ...]


# Keep routing conservative and explainable. The registry remains the source of
# truth for detailed guardrails; this table only supplies a dependency-free index
# usable from an installed CLI/MCP process.
ROUTES: tuple[tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]], ...] = (
    (
        "ad_agent",
        ("active directory", "entra", "azure ad", "ldap", "kerberos", "bloodhound", "adcs", "domain"),
        ("ad", "windows", "database", "methodology", "tools"),
        ("redops-rag", "redops-exegol", "terminal-bounded"),
    ),
    (
        "windows_redteam_agent",
        ("windows", "winrm", "powershell", "lolbas", "seatbelt", "winpeas", "dll hijack"),
        ("windows", "redteam", "tools", "vulnerabilities", "ad", "methodology"),
        ("redops-rag", "redops-exegol", "terminal-bounded"),
    ),
    (
        "web_agent",
        ("web", "api", "http", "https", "xss", "sqli", "ssrf", "csrf", "waf", "browser", "xsrf"),
        ("web", "vulnerabilities", "network", "methodology", "tools", "redteam"),
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


def _terms(task: str) -> set[str]:
    return set(re.findall(r"[a-z0-9][a-z0-9+.#_-]*", task.lower()))


def route_task(task: str, limit: int = 3) -> dict[str, object]:
    """Return an explainable delegation plan; never executes a target command."""

    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 5:
        raise ValueError("limit must be an integer between 1 and 5")
    normalized = task.strip()
    terms = _terms(normalized)
    ranked: list[AgentRoute] = []
    for agent, keywords, knowledge, mcp in ROUTES:
        matches = [keyword for keyword in keywords if keyword in normalized.lower() or keyword in terms]
        if matches:
            ranked.append(
                AgentRoute(
                    agent=agent,
                    score=len(matches),
                    rationale="matched: " + ", ".join(matches[:5]),
                    knowledge=knowledge,
                    allowed_mcp=mcp,
                )
            )
    ranked.sort(key=lambda item: (-item.score, item.agent))
    selected = ranked[:limit]
    if not selected:
        selected = [
            AgentRoute(
                agent="rag_curator_agent",
                score=0,
                rationale="no niche keyword matched; retrieve context before selecting a specialist",
                knowledge=("methodology",),
                allowed_mcp=("redops-rag", "terminal-bounded"),
            )
        ]
    return {
        "task": normalized,
        "workflow": plan_engagement(normalized),
        "authorization_required": True,
        "execution_policy": "orchestrator routes only; specialist executes via Exegol after scope confirmation",
        "selected_agents": [asdict(item) for item in selected],
        "delegation_contract": {
            "include": ["written_scope", "retrieved_sources", "artifacts", "expected_output"],
            "exclude": ["credentials", "tokens", "unscoped_targets", "claims_without_command_output"],
        },
    }
