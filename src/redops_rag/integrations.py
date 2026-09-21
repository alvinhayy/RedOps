"""Install small, non-secret RedOps adapters for popular agent CLIs."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

INTEGRATION_TEXT = """# RedOps RAG integration

Use RedOps as the source-grounded knowledge and execution layer for authorized
security work. Start with retrieval, cite the returned source paths/URLs, and
never claim a command ran unless its output is present.

## Core commands

```bash
redops providers
redops stats
redops query \"<question>\"
redops query \"<question>\" --no-generate
redops exegol status
```

Use `redops exegol exec -- <argv...>` only after confirming written scope and
the configured Exegol container. Keep active web/mobile/WAF checks to approved
local, staging, or lab targets; do not submit destructive payloads or create
load. Knowledge lives in Markdown and should be refreshed with `redops ingest`.

When a provider is unavailable, use `redops query --no-generate` for a local,
extractive answer. Provider credentials must remain in environment variables,
never in prompts, reports, or the shared corpus.
"""


def _slash_commands() -> list[dict[str, str]]:
    manifest = Path(__file__).resolve().parents[2] / "agents" / "skill-commands.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [{"name": "redops-rag", "skill": "redops-rag", "description": "", "content": INTEGRATION_TEXT}]
    return data.get("commands", [])


@dataclass(frozen=True, slots=True)
class IntegrationFile:
    target: str
    path: Path
    content: str


def _home(name: str, default: Path) -> Path:
    value = os.getenv(name)
    return Path(value).expanduser() if value else default.expanduser()


def integration_files(target: str) -> list[IntegrationFile]:
    normalized = target.lower()
    if normalized == "codex":
        root = _home("CODEX_HOME", Path.home() / ".codex")
        return [IntegrationFile(target, root / "skills" / "redops-rag" / "SKILL.md", 
                                "---\nname: redops-rag\ndescription: Source-grounded authorized pentest RAG workflow.\n---\n\n" + INTEGRATION_TEXT)]
    if normalized == "claude":
        root = _home("CLAUDE_HOME", Path.home() / ".claude")
        return [
            IntegrationFile(target, root / "commands" / f"{item['name']}.md", item["content"])
            for item in _slash_commands()
        ]
    if normalized == "opencode":
        root = _home("OPENCODE_HOME", Path.home() / ".config" / "opencode")
        commands = [
            IntegrationFile(target, root / "commands" / f"{item['name']}.md", item["content"])
            for item in _slash_commands()
        ]
        commands.append(IntegrationFile(target, root / "skills" / "redops-rag" / "SKILL.md", INTEGRATION_TEXT))
        return commands
    raise ValueError("target must be one of: codex, claude, opencode, all")


def install_integrations(target: str, *, dry_run: bool = False, force: bool = False) -> list[dict[str, str]]:
    targets = ("codex", "claude", "opencode") if target == "all" else (target,)
    results: list[dict[str, str]] = []
    for item_target in targets:
        for item in integration_files(item_target):
            if item.path.exists() and not force:
                results.append({"target": item.target, "path": str(item.path), "status": "exists"})
                continue
            if not dry_run:
                item.path.parent.mkdir(parents=True, exist_ok=True)
                item.path.write_text(item.content, encoding="utf-8")
            results.append({"target": item.target, "path": str(item.path), "status": "planned" if dry_run else "installed"})
    return results
