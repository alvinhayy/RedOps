#!/usr/bin/env python3
"""Add the official Exegol MCP stdio server to the local OpenCode project config."""

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".opencode/opencode.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    binary = shutil.which("exegol-mcp")
    if not binary:
        raise SystemExit("exegol-mcp not found; install with: pipx install exegol-mcp")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    server = {"type": "local", "command": ["exegol-mcp", "--type", "stdio"], "enabled": True}
    existing = config.setdefault("mcp", {}).get("exegol")
    if existing and existing != server:
        raise SystemExit("Exegol MCP already configured differently; refusing to overwrite it")
    if existing == server:
        print("Exegol MCP already configured")
        return
    if args.dry_run:
        print(f"Would add project-local Exegol MCP: {binary} --type stdio")
        return
    config["mcp"]["exegol"] = server
    CONFIG.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print("Exegol MCP configured in .opencode/opencode.json; restart OpenCode")


if __name__ == "__main__":
    main()
