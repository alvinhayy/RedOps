#!/usr/bin/env python3
"""Report host tool availability for the OpenCode agent roles; never run target tools."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLE_MCP = {
    "exegol", "burp", "camoufox", "uiautomator2", "ghidra", "radare2",
    "bloodhound", "notion", "open-figma-mcp", "figma-rest",
}
ALIASES = {
    "impacket": ["impacket-smbclient", "impacket-GetUserSPNs"],
    "bloodhound-python": ["bloodhound-python", "bloodhound-ce-python"],
    "winpeas": ["winPEAS.exe", "winpeas"],
    "linpeas": ["linpeas.sh", "linpeas"],
    "camoufox": ["camoufox", "camoufox-mcp"],
}


def check_wiring(manifest: dict) -> dict:
    """Validate local paths and report MCP configuration without exposing credentials."""
    resources = manifest["resources"]
    for key in ("index", "knowledgebase", "binary_manifest", "engagement_template"):
        if not (ROOT / resources[key]).exists():
            raise SystemExit(f"Missing RedOps resource: {resources[key]}")
    binary_manifest = json.loads((ROOT / resources["binary_manifest"]).read_text())
    if not isinstance(binary_manifest.get("artifacts"), list):
        raise SystemExit("Binary manifest must contain an artifacts list")
    for artifact in binary_manifest["artifacts"]:
        path = Path(artifact["path"])
        digest = artifact.get("sha256", "")
        if path.is_absolute() or ".." in path.parts or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            raise SystemExit(f"Unsafe or unhashed binary manifest entry: {path}")
        binary_root = (ROOT / "precompiled-binaries").resolve()
        candidate = (binary_root / path).resolve()
        if not candidate.is_relative_to(binary_root) or not candidate.is_file():
            raise SystemExit(f"Listed binary is missing: {path}")
        actual = hashlib.sha256()
        with candidate.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                actual.update(block)
        if actual.hexdigest().lower() != digest.lower():
            raise SystemExit(f"SHA-256 mismatch for listed binary: {path}")

    agent_files = {path.stem for path in (ROOT / ".opencode/agent").glob("*.md")}
    profiles = manifest["agents"]
    if agent_files != set(profiles):
        raise SystemExit(f"Agent/profile mismatch: {sorted(agent_files ^ set(profiles))}")
    niche_root = ROOT / resources["knowledgebase"]
    public_niches = {path.name for path in niche_root.iterdir() if path.is_dir() and path.name != "api"}
    routed_niches = {
        niche for profile in profiles.values() for niche in profile["knowledge"]
        if not niche.startswith("knowledgebase/")
    }
    if public_niches - routed_niches:
        raise SystemExit(f"Unrouted knowledge niches: {sorted(public_niches - routed_niches)}")
    config = json.loads((ROOT / ".opencode/opencode.json").read_text())
    resolved = None
    if shutil.which("opencode"):
        try:
            result = subprocess.run(["opencode", "debug", "config"], cwd=ROOT,
                                    capture_output=True, text=True, timeout=15, check=False)
            if result.returncode == 0:
                resolved = json.loads(result.stdout)
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
            pass
    mcp_names = set((resolved or config).get("mcp", {}))
    report = {}
    for role, profile in profiles.items():
        guidance = (ROOT / ".opencode/agent" / f"{role}.md").read_text()
        heading = "## Knowledge-based dispatch" if role == "redops" else "## Knowledge route"
        if heading not in guidance or ".opencode/tools.json" not in guidance:
            raise SystemExit(f"Missing role-specific knowledge guidance: {role}")
        for niche in profile["knowledge"]:
            source = ROOT / niche if niche.startswith("knowledgebase/") else ROOT / resources["knowledgebase"] / niche
            if not source.exists():
                raise SystemExit(f"Missing {role} knowledge: {source.relative_to(ROOT)}")
        for niche in profile.get("optional_knowledge", []):
            if niche != "api":
                raise SystemExit(f"Unrecognized opt-in knowledge: {niche}")
        if not isinstance(profile["binaries"], bool):
            raise SystemExit(f"Invalid binary policy: {role}")
        permissions = (resolved or {}).get("agent", {}).get(role, {}).get("permission", {})
        assigned = profile["mcp"]
        if set(assigned) - ROLE_MCP:
            raise SystemExit(f"Unknown MCP assignment for {role}: {sorted(set(assigned) - ROLE_MCP)}")
        if permissions:
            for server in ROLE_MCP:
                action = permissions.get(f"{server}_*")
                if server in assigned and action not in ("allow", "ask"):
                    raise SystemExit(f"MCP permission missing for {role}: {server}")
                if server not in assigned and action != "deny":
                    raise SystemExit(f"Unassigned MCP not denied for {role}: {server}")
        report[role] = {
            "knowledge": profile["knowledge"],
            "binary_access": profile["binaries"],
            "engagement_ledger": resources["engagement_ledger"],
            "mcp_assigned": assigned,
            "mcp_configured": sorted(set(assigned) & mcp_names),
            "mcp_unconfigured": sorted(set(assigned) - mcp_names),
            "permissions_verified": bool(permissions),
        }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    parser.add_argument("--wiring", action="store_true", help="validate role resources and MCP wiring")
    args = parser.parse_args()
    manifest = json.loads((ROOT / ".opencode/tools.json").read_text())
    if args.wiring:
        report = check_wiring(manifest)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            for role, details in report.items():
                mcp = ", ".join(details["mcp_configured"]) or "none"
                missing = ", ".join(details["mcp_unconfigured"]) or "none"
                verified = "yes" if details["permissions_verified"] else "no"
                print(f"{role:18} knowledge={len(details['knowledge'])} MCP configured={mcp}; missing={missing}; permissions={verified}")
            print("Configured does not mean connected; use `opencode mcp list` for runtime health.")
        return
    report = {}
    for role, groups in manifest["agents"].items():
        report[role] = {
            group: {tool: any(shutil.which(cmd) for cmd in ALIASES.get(tool, [tool]))
                    for tool in groups[group]}
            for group in ("required", "optional")
        }
    if args.json:
        print(json.dumps(report, indent=2))
        return
    for role, groups in report.items():
        missing = [tool for tool, found in groups["required"].items() if not found]
        optional = [tool for tool, found in groups["optional"].items() if not found]
        state = "ready" if not missing else "missing " + ", ".join(missing)
        print(f"{role:18} {state}")
        if optional:
            print(f"{'':18} optional: {', '.join(optional)}")
    print("Host-only check; specialist tools may be available inside Exegol.")


if __name__ == "__main__":
    main()
