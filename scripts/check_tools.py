#!/usr/bin/env python3
"""Check agent tool capabilities without requiring PyYAML or executing targets."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

# Capability names that do not exactly match their usual executable/module name.
ALIASES = {
    "impacket": ("impacket-smbclient", "impacket-GetUserSPNs"),
    "frida": ("frida", "frida-ps"),
    "markdown-tools": ("pandoc", "markdownlint"),
    "ripgrep": ("rg",),
}

PIP_PACKAGES = {
    "androguard": "androguard",
    "bloodhound-python": "bloodhound-ce",
    "frida": "frida-tools",
    "impacket": "impacket",
    "netexec": "NetExec",
    "objection": "objection",
    "semgrep": "semgrep",
}


def _manifest(path: Path) -> dict[str, dict[str, list[str]]]:
    agents: dict[str, dict[str, list[str]]] = {}
    current_agent: str | None = None
    current_kind: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if raw_line.startswith("  ") and not raw_line.startswith("    ") and line.endswith(":"):
            current_agent = line[:-1]
            agents[current_agent] = {"required": [], "optional": []}
            current_kind = None
        elif current_agent and raw_line.startswith("    ") and line in {"required:", "optional:"}:
            current_kind = line[:-1]
        elif current_agent and current_kind and raw_line.startswith("    - "):
            agents[current_agent][current_kind].append(line[2:])
    return agents


def _available(name: str, extra_bin: Path | None) -> bool:
    candidates = ALIASES.get(name, (name,))
    search_path = None
    if extra_bin:
        search_path = f"{extra_bin}{os.pathsep}{os.environ.get('PATH', '')}"
    if any(shutil.which(candidate, path=search_path) for candidate in candidates):
        return True
    if name == "impacket" and extra_bin:
        probe = subprocess.run(
            [str(extra_bin / "python"), "-c", "import impacket"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return probe.returncode == 0
    return False


def check(path: Path, extra_bin: Path | None) -> dict[str, object]:
    agents = _manifest(path)
    rows: dict[str, object] = {}
    for agent, tools in agents.items():
        rows[agent] = {
            kind: {
                tool: _available(tool, extra_bin) for tool in values
            }
            for kind, values in tools.items()
        }
    return {"manifest": str(path), "agents": rows}


def missing(report: dict[str, object], *, required_only: bool = False) -> list[str]:
    result: set[str] = set()
    for tools in report["agents"].values():  # type: ignore[union-attr]
        for kind in ("required",) if required_only else ("required", "optional"):
            result.update(tool for tool, present in tools[kind].items() if not present)  # type: ignore[index]
    return sorted(result)


def install(packages: list[str], python: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for tool in packages:
        package = PIP_PACKAGES.get(tool)
        if not package:
            result[tool] = "manual-or-exegol"
            continue
        completed = subprocess.run(
            [str(python), "-m", "pip", "install", package],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        result[tool] = "installed" if completed.returncode == 0 else "failed"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--venv-bin", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--install", action="store_true", help="install supported missing Python tools")
    args = parser.parse_args()
    report = check(args.manifest, args.venv_bin)
    install_result: dict[str, str] | None = None
    if args.install:
        if not args.venv_bin:
            raise SystemExit("--install requires --venv-bin")
        packages = missing(report, required_only=False)
        install_result = install(packages, args.venv_bin / "python")
        report = check(args.manifest, args.venv_bin)
        report["install"] = install_result
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        required_missing = missing(report, required_only=True)
        all_missing = missing(report)
        optional_missing = [tool for tool in all_missing if tool not in required_missing]
        print(f"required missing: {', '.join(required_missing) if required_missing else 'none'}")
        print(f"optional missing: {', '.join(optional_missing) or 'none'}")
        if install_result is not None:
            for tool, state in sorted(install_result.items()):
                print(f"install {tool}: {state}")


if __name__ == "__main__":
    main()
