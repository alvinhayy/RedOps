"""Read-only lab target context for authorized practice engagements.

Laboratory platforms such as Hack The Box provide contractually authorized,
isolated targets. This module attaches lab metadata to an engagement plan so
operators can fill a complete packet: which platform the target lives on, how
it is isolated, which networks it typically uses, and which specialists a
given OS hints at.

Safety contract (mirrors :mod:`redops_rag.workflow`):

- read-only: nothing here executes a command or touches a target;
- gate-preserving: lab metadata never sets ``scope_confirmed`` nor
  ``include_active``; active phases stay blocked exactly as before;
- secret-free: VPN keys, platform API tokens, machine ``appid`` values, and
  passwords are never accepted, stored, or forwarded — they move out-of-band;
- Exegol-first: execution policy is unchanged and belongs to the approved
  phase specialist.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .orchestrator import rank_routes
from .workflow import plan_engagement

OS_HINTS: tuple[str, ...] = ("unknown", "windows", "linux")


@dataclass(frozen=True, slots=True)
class LabEnvironment:
    id: str
    platform: str
    kind: str
    description: str
    isolation: str
    typical_networks: tuple[str, ...]
    routing_tags: tuple[str, ...]
    authorization_basis: str


LABS: tuple[LabEnvironment, ...] = (
    LabEnvironment(
        "htb_lab",
        "Hack The Box",
        "released lab machines",
        "Released HTB machines reached over the lab VPN; boxes are single-target and resettable.",
        "VPN-isolated lab network; machines are disposable and reset by design.",
        ("10.10.10.0/24", "10.10.11.0/24"),
        (),
        "Platform terms of service cover lab machines only; each target still needs its own "
        "engagement-packet row before any active phase.",
    ),
    LabEnvironment(
        "htb_pro_lab",
        "Hack The Box Pro Labs",
        "multi-host scenario lab",
        "Tiered multi-host Pro Lab scenarios built around Windows domains and Active Directory.",
        "VPN-isolated lab network dedicated to the Pro Lab scenario.",
        ("10.10.10.0/24", "10.10.11.0/24"),
        ("active directory", "windows", "domain"),
        "Platform terms of service cover the Pro Lab scenario only; every host in the tiered "
        "domain still needs its own engagement-packet row before any active phase.",
    ),
    LabEnvironment(
        "htb_academy",
        "HTB Academy",
        "guided module instances",
        "Academy module sections with dedicated per-module target instances.",
        "Dedicated per-module instances; not part of the shared lab machine ranges.",
        (),
        (),
        "Platform terms of service cover Academy module instances only; each module target "
        "still needs its own engagement-packet row before any active phase.",
    ),
)

_LAB_BY_ID = {env.id: env for env in LABS}


def lab_ids() -> tuple[str, ...]:
    """Return registered lab identifiers for CLI choices and MCP schemas."""

    return tuple(_LAB_BY_ID)


def describe_lab(lab_id: str) -> dict[str, object]:
    """Return read-only metadata for a registered lab environment."""

    env = _LAB_BY_ID.get(lab_id)
    if env is None:
        raise ValueError(f"unknown lab: {lab_id}")
    return {
        "id": env.id,
        "platform": env.platform,
        "kind": env.kind,
        "description": env.description,
        "isolation": env.isolation,
        "typical_networks": list(env.typical_networks),
        "routing_tags": list(env.routing_tags),
        "authorization_basis": env.authorization_basis,
    }


def _validate_task(task: str) -> str:
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")
    return task.strip()


def normalize_os_hint(os_hint: str) -> str:
    """Validate and normalize an OS hint; public so callers share one canonical form."""

    if not isinstance(os_hint, str):
        raise TypeError("os_hint must be a string")
    normalized = os_hint.strip().lower()
    if not normalized or normalized in {"none", "n/a"}:
        return "unknown"
    if normalized not in OS_HINTS:
        raise ValueError(f"os_hint must be one of: {', '.join(OS_HINTS)}")
    return normalized


def _recommended_agents(task: str, os_hint: str, routing_tags: tuple[str, ...]) -> list[dict[str, object]]:
    """Explainable specialist hints for a lab target; routing only, never execution.

    Ranking is delegated to :func:`redops_rag.orchestrator.rank_routes` so lab
    hints and orchestrator routing cannot drift apart. The OS hint double-weights
    its matching specialist (mirroring ``route_task``), which keeps an OS-specific
    specialist above lexical ties such as a single ``htb`` keyword match.
    """

    effective = " ".join((task, " ".join(routing_tags), os_hint if os_hint != "unknown" else ""))
    boost = (os_hint,) if os_hint != "unknown" else ()
    keep = {"agent", "matched", "knowledge", "allowed_mcp"}
    return [{key: value for key, value in item.items() if key in keep} for item in rank_routes(effective, 3, boost)]


def lab_engagement(
    task: str,
    *,
    lab: str = "htb_lab",
    os_hint: str = "unknown",
    scope_confirmed: bool = False,
    include_active: bool = False,
    scope_record: str | Path | None = None,
) -> dict[str, object]:
    """Return a phase-gated plan enriched with read-only lab target context.

    The underlying gates are delegated to :func:`plan_engagement` untouched:
    lab metadata can never confirm scope or enable active phases on its own,
    and the returned payload carries no credential or token fields.
    """

    normalized = _validate_task(task)
    env = _LAB_BY_ID.get(lab)
    if env is None:
        raise ValueError(f"unknown lab: {lab}")
    if not isinstance(scope_confirmed, bool) or not isinstance(include_active, bool):
        raise TypeError("scope_confirmed and include_active must be booleans")
    normalized_os = normalize_os_hint(os_hint)

    plan = plan_engagement(
        normalized,
        scope_confirmed=scope_confirmed,
        include_active=include_active,
        scope_record=scope_record,
    )
    result = dict(plan)
    result["lab"] = {
        **describe_lab(env.id),
        "network_note": (
            "documentation hint only; the engagement packet target inventory remains "
            "the single source of truth for scope"
        ),
        "credential_policy": (
            "VPN keys, platform API tokens, machine appid values, and passwords stay "
            "out-of-band; they are never stored in plans, packets, or the corpus"
        ),
    }
    result["target_context"] = {
        "os_hint": normalized_os,
        "routing_tags": list(env.routing_tags),
        "recommended_agents": _recommended_agents(normalized, normalized_os, env.routing_tags),
    }
    result["lab_gate_note"] = (
        "lab metadata never confirms scope; the scope_confirmed/include_active gates "
        "above apply unchanged"
    )
    return result
