#!/usr/bin/env python3
"""Merge agent tooling with tools required by the skills they own.

The registry and skill matrix remain the sources of truth. This script writes a
machine-readable merged file and replaces the marked README table idempotently.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- BEGIN GENERATED AGENT TOOLS -->"
END = "<!-- END GENERATED AGENT TOOLS -->"
TOOLS_START = "<!-- BEGIN GENERATED AGENT TOOL MATRIX -->"
TOOLS_END = "<!-- END GENERATED AGENT TOOL MATRIX -->"


def build(agents_path: Path, skills_path: Path) -> dict[str, dict[str, list[str]]]:
    agents = yaml.safe_load(agents_path.read_text(encoding="utf-8"))["agents"]
    skills = yaml.safe_load(skills_path.read_text(encoding="utf-8"))["skills"]
    merged: dict[str, dict[str, set[str]]] = {
        name: {
            "required": set(profile.get("tooling", {}).get("required", [])),
            "optional": set(profile.get("tooling", {}).get("optional", [])),
        }
        for name, profile in agents.items()
    }
    for skill in skills.values():
        executables = skill.get("executables", {})
        for owner in skill.get("owner_agents", []):
            if owner not in merged:
                continue
            merged[owner]["required"].update(executables.get("required", []))
            merged[owner]["optional"].update(executables.get("optional", []))
    return {
        agent: {
            "required": sorted(values["required"]),
            "optional": sorted(values["optional"] - values["required"]),
        }
        for agent, values in merged.items()
    }


def render_yaml(merged: dict[str, dict[str, list[str]]]) -> str:
    return yaml.safe_dump(
        {"version": 1, "description": "Generated union of registry and skill tooling", "agents": merged},
        sort_keys=False,
        allow_unicode=False,
    )


def render_table(merged: dict[str, dict[str, list[str]]]) -> str:
    lines = [
        START,
        "| Agent | Required tools (registry + owned skills) | Optional tools (registry + owned skills) |",
        "|---|---|---|",
    ]
    for agent, values in merged.items():
        required = ", ".join(f"`{tool}`" for tool in values["required"]) or "—"
        optional = ", ".join(f"`{tool}`" for tool in values["optional"]) or "—"
        lines.append(f"| `{agent}` | {required} | {optional} |")
    lines.append(END)
    return "\n".join(lines)


def update_marked_file(path: Path, table: str, start: str, end: str, anchor: str) -> None:
    content = path.read_text(encoding="utf-8")
    block = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if block.search(content):
        updated = block.sub(table, content, count=1)
    else:
        if anchor not in content:
            raise RuntimeError(f"{path} is missing the generated-table anchor")
        updated = content.replace(anchor, f"\n### Generated CLI tool union\n\n{table}\n{anchor}", 1)
    path.write_text(updated, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args()
    merged = build(ROOT / "agents/registry.yaml", ROOT / "agents/skill-tool-matrix.yaml")
    generated = ROOT / "agents/agent-tools.generated.yaml"
    table = render_table(merged)
    expected_yaml = render_yaml(merged)
    readme = ROOT / "README.md"
    tools_doc = ROOT / "agents/tools.md"
    content = readme.read_text(encoding="utf-8")
    block = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    tools_content = tools_doc.read_text(encoding="utf-8")
    tools_block = re.compile(re.escape(TOOLS_START) + r".*?" + re.escape(TOOLS_END), re.DOTALL)
    stale = generated.read_text(encoding="utf-8") != expected_yaml if generated.exists() else True
    stale = stale or not block.search(content) or block.search(content).group(0) != table
    tools_table = render_table(merged).replace(START, TOOLS_START).replace(END, TOOLS_END)
    stale = stale or not tools_block.search(tools_content) or tools_block.search(tools_content).group(0) != tools_table
    if args.check:
        if stale:
            raise SystemExit("generated agent tool files are stale; run scripts/sync_agent_tools.py")
        print("agent tool generation is up to date")
        return
    generated.write_text(expected_yaml, encoding="utf-8")
    update_marked_file(readme, table, START, END, "\n## Installation\n")
    update_marked_file(tools_doc, tools_table, TOOLS_START, TOOLS_END, "\n## Profiles\n")
    print(f"updated {generated}, {readme}, and {tools_doc}")


if __name__ == "__main__":
    main()
