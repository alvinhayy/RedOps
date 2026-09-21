"""Deterministic engagement workflow planning for the RedOps orchestrator."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class WorkflowPhase:
    id: str
    agent: str
    purpose: str
    knowledge: tuple[str, ...]
    required_artifacts: tuple[str, ...]
    gate: str
    next_phases: tuple[str, ...]


PHASES: tuple[WorkflowPhase, ...] = (
    WorkflowPhase(
        "pre_engagement",
        "scope_agent",
        "Confirm authorization, targets, exclusions, timing, and success criteria.",
        ("methodology", "misc"),
        ("written_scope", "target_inventory", "rules_of_engagement"),
        "written authorization and in-scope target are mandatory",
        ("information_gathering",),
    ),
    WorkflowPhase(
        "information_gathering",
        "recon_agent",
        "Build an evidence-backed asset, identity, service, and application inventory.",
        ("network", "web", "ad", "cloud", "mobile", "methodology", "tools"),
        ("scope_reference", "asset_inventory", "service_or_artifact_evidence"),
        "scope_agent output and rate limits must be accepted",
        ("vulnerability_assessment", "post_exploitation"),
    ),
    WorkflowPhase(
        "vulnerability_assessment",
        "assessment_agent",
        "Correlate observations with vulnerabilities, misconfigurations, and hypotheses.",
        ("vulnerabilities", "tools", "methodology", "linux", "windows", "web", "ad"),
        ("recon_evidence", "finding_hypotheses", "severity_rationale"),
        "each hypothesis needs a source and observed evidence",
        ("information_gathering", "exploitation", "post_exploitation"),
    ),
    WorkflowPhase(
        "exploitation",
        "exploitation_agent",
        "Perform minimal, reversible validation of an approved vulnerability.",
        ("vulnerabilities", "redteam", "tools", "methodology"),
        ("approved_finding", "exploit_test_plan", "rollback_plan"),
        "explicit exploit approval, target scope, and Exegol/runtime health are required",
        ("post_exploitation", "lateral_movement"),
    ),
    WorkflowPhase(
        "post_exploitation",
        "post_exploitation_agent",
        "Measure impact, collect minimal evidence, and preserve a clean rollback state.",
        ("redteam", "ad", "cloud", "windows", "linux", "methodology"),
        ("validated_access", "impact_evidence", "cleanup_record"),
        "only approved test accounts and minimum necessary data may be collected",
        ("information_gathering", "lateral_movement", "proof_of_concept"),
    ),
    WorkflowPhase(
        "lateral_movement",
        "lateral_movement_agent",
        "Validate explicitly approved movement paths and segmentation controls.",
        ("ad", "network", "windows", "cloud", "methodology", "tools"),
        ("movement_scope", "source_access", "destination_allowlist"),
        "source and destination must both be explicitly in scope",
        ("vulnerability_assessment", "post_exploitation", "proof_of_concept"),
    ),
    WorkflowPhase(
        "proof_of_concept",
        "poc_agent",
        "Reduce validated behavior to a minimal reproducible proof without destructive payloads.",
        ("vulnerabilities", "methodology", "tools"),
        ("reproduction_steps", "sanitized_output", "impact_statement"),
        "PoC must be reproducible, sanitized, and limited to the approved fixture",
        ("post_engagement",),
    ),
    WorkflowPhase(
        "post_engagement",
        "reporting_agent",
        "Consolidate evidence, remediation, residual risk, and cleanup confirmation.",
        ("methodology", "vulnerabilities", "misc"),
        ("finding_records", "source_citations", "remediation", "cleanup_record"),
        "report distinguishes observed evidence from hypotheses and missing evidence",
        (),
    ),
)

_PHASE_BY_ID = {phase.id: phase for phase in PHASES}


def _validate_task(task: str) -> str:
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")
    return task.strip()


def _niche_hints(task: str) -> tuple[str, ...]:
    terms = set(re.findall(r"[a-z0-9][a-z0-9+.#_-]*", task.lower()))
    candidates = (
        ("ad", ("active directory", "entra", "ldap", "kerberos", "bloodhound", "adcs")),
        ("windows", ("windows", "winrm", "powershell", "lolbas", "iis", "smb")),
        ("linux", ("linux", "ssh", "sudo", "suid", "systemd", "nfs")),
        ("web", ("web", "api", "http", "https", "xss", "sqli", "ssrf", "waf")),
        ("cloud", ("aws", "azure", "gcp", "cloud", "iam", "s3")),
        ("mobile", ("android", "ios", "apk", "ipa", "flutter", "frida")),
        ("network", ("network", "nmap", "pcap", "wireless", "vpn", "pivot")),
        ("container", ("docker", "kubernetes", "k8s", "container", "trivy")),
        ("web3", ("web3", "solidity", "defi", "ethereum", "smart contract")),
    )
    result = []
    lowered = task.lower()
    for niche, keywords in candidates:
        if any(keyword in lowered or keyword in terms for keyword in keywords):
            result.append(niche)
    return tuple(result) or ("methodology",)


def plan_engagement(
    task: str,
    *,
    scope_confirmed: bool = False,
    include_active: bool = False,
) -> dict[str, object]:
    """Return a read-only phase plan; this function never executes a target action."""

    normalized = _validate_task(task)
    if not isinstance(scope_confirmed, bool) or not isinstance(include_active, bool):
        raise TypeError("scope_confirmed and include_active must be booleans")
    active_allowed = scope_confirmed and include_active
    phases = []
    for phase in PHASES:
        row = asdict(phase)
        row["status"] = "planned"
        if phase.id == "pre_engagement":
            row["status"] = "required"
        elif phase.id in {"exploitation", "post_exploitation", "lateral_movement"} and not active_allowed:
            row["status"] = "blocked_until_scope_and_approval"
        phases.append(row)
    return {
        "task": normalized,
        "niche_hints": list(_niche_hints(normalized)),
        "authorization_required": True,
        "scope_confirmed": scope_confirmed,
        "active_execution_enabled": active_allowed,
        "execution_policy": "phase agents coordinate; approved execution remains Exegol-first",
        "entry_phase": "pre_engagement",
        "terminal_phase": "post_engagement",
        "phases": phases,
        "handoff_contract": {
            "include": ["phase_output", "source_citations", "target_scope", "open_questions"],
            "exclude": ["credentials", "tokens", "unscoped_targets", "unsupported_claims"],
        },
    }


def phase(phase_id: str) -> WorkflowPhase:
    """Return a phase definition for integrations/tests without exposing mutable state."""

    try:
        return _PHASE_BY_ID[phase_id]
    except KeyError as exc:
        raise ValueError(f"unknown workflow phase: {phase_id}") from exc
