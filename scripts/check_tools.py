#!/usr/bin/env python3
"""Report host tool availability for the OpenCode agent roles; never run target tools."""

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALIASES = {
    "impacket": ["impacket-smbclient", "impacket-GetUserSPNs"],
    "bloodhound-python": ["bloodhound-python", "bloodhound-ce-python"],
    "winpeas": ["winPEAS.exe", "winpeas"],
    "linpeas": ["linpeas.sh", "linpeas"],
    "camoufox": ["camoufox", "camoufox-mcp"],
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    args = parser.parse_args()
    manifest = json.loads((ROOT / ".opencode/tools.json").read_text())
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
