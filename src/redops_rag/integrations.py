"""Install small, non-secret RedOps adapters for popular agent CLIs."""

from __future__ import annotations

import json
import os
import re
from collections.abc import Iterable
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


_COMMAND_NAME = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def _manifest_commands() -> list[dict[str, str]]:
    manifest = Path(__file__).resolve().parents[2] / "agents" / "skill-commands.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [{"name": "redops-rag", "skill": "redops-rag", "description": "", "content": INTEGRATION_TEXT}]
    commands = data.get("commands", [])
    return [item for item in commands if isinstance(item, dict) and item.get("name") and item.get("content")]


def _skill_roots(skill_paths: Iterable[str | Path] | None = None) -> list[Path]:
    """Return roots where installed skills or skill repositories may expose commands.

    ``REDOPS_SKILL_PATHS`` is an os.pathsep-separated escape hatch for arbitrary
    skill repositories. The small default set covers the conventional local
    agent locations without scanning a user's whole home directory.
    """

    configured = list(skill_paths or ())
    if not configured:
        configured = [item for item in os.getenv("REDOPS_SKILL_PATHS", "").split(os.pathsep) if item]
    if not configured:
        project_root = Path(__file__).resolve().parents[2]
        working_dir = Path.cwd()
        configured = [
            str(project_root / "skills"),
            str(project_root / ".agents"),
            str(working_dir / "skills"),
            str(working_dir / ".agents"),
            str(Path.home() / ".agents"),
            str(Path.home() / ".codex"),
        ]

    roots: list[Path] = []
    seen: set[Path] = set()
    for raw in configured:
        root = Path(raw).expanduser()
        try:
            resolved = root.resolve()
        except OSError:
            continue
        if resolved in seen or not resolved.exists():
            continue
        seen.add(resolved)
        roots.append(resolved)
    return roots


def _command_candidates(root: Path) -> list[Path]:
    """Find common skill command layouts without recursively scanning a home dir."""

    patterns = ("commands/*.md", "*/commands/*.md", "*/*/commands/*.md")
    candidates: set[Path] = set()
    for pattern in patterns:
        candidates.update(path for path in root.glob(pattern) if path.is_file())
    return sorted(candidates, key=lambda path: str(path).lower())


def _discover_skill_commands(skill_paths: Iterable[str | Path] | None = None) -> list[dict[str, str]]:
    """Load slash command markdown shipped by installed skills.

    A command is simply a Markdown file under a ``commands`` directory. This
    matches the layout used by Claude/OpenCode skills and repositories such as
    Mobile-ReverseSkill (including ``.agents/commands`` and
    ``.claude/commands``). Invalid names and unreadable files are ignored.
    """

    discovered: list[dict[str, str]] = []
    seen_files: set[Path] = set()
    seen_names: set[str] = set()
    for root in _skill_roots(skill_paths):
        for path in _command_candidates(root):
            try:
                resolved = path.resolve()
            except OSError:
                continue
            if resolved in seen_files:
                continue
            seen_files.add(resolved)
            name = path.stem.lower()
            if name in {"readme", "index"} or not _COMMAND_NAME.fullmatch(name):
                continue
            # Skill repositories often vendor the same command for several
            # clients (.agents, .claude, .cursor, ...). Install one copy only.
            if name in seen_names:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            if not content.strip():
                continue
            # The nearest directory above ``commands`` is a useful provenance
            # label (``.agents``, ``mobile-vuln-hunt``, etc.), but command
            # execution never relies on it.
            owner = path.parent.parent.name or "skill"
            discovered.append({"name": name, "skill": owner, "description": "", "content": content})
            seen_names.add(name)
    return discovered


def _slash_commands(skill_paths: Iterable[str | Path] | None = None) -> list[dict[str, str]]:
    """Combine discovered skill commands with the built-in RedOps fallbacks."""

    # A real skill command wins over the short fallback wrapper with the same
    # name. This lets users install a richer command without editing RedOps.
    combined = _discover_skill_commands(skill_paths)
    seen = {item["name"] for item in combined}
    for item in _manifest_commands():
        name = str(item.get("name", "")).lower()
        if name and name not in seen:
            item = dict(item)
            item["name"] = name
            combined.append(item)
            seen.add(name)
    return combined


@dataclass(frozen=True, slots=True)
class IntegrationFile:
    target: str
    path: Path
    content: str


def _home(name: str, default: Path) -> Path:
    value = os.getenv(name)
    return Path(value).expanduser() if value else default.expanduser()


def integration_files(target: str, *, skill_paths: Iterable[str | Path] | None = None) -> list[IntegrationFile]:
    normalized = target.lower()
    if normalized == "codex":
        root = _home("CODEX_HOME", Path.home() / ".codex")
        return [IntegrationFile(target, root / "skills" / "redops-rag" / "SKILL.md", 
                                "---\nname: redops-rag\ndescription: Source-grounded authorized pentest RAG workflow.\n---\n\n" + INTEGRATION_TEXT)]
    if normalized == "claude":
        root = _home("CLAUDE_HOME", Path.home() / ".claude")
        return [
            IntegrationFile(target, root / "commands" / f"{item['name']}.md", item["content"])
            for item in _slash_commands(skill_paths)
        ]
    if normalized == "opencode":
        root = _home("OPENCODE_HOME", Path.home() / ".config" / "opencode")
        commands = [
            IntegrationFile(target, root / "commands" / f"{item['name']}.md", item["content"])
            for item in _slash_commands(skill_paths)
        ]
        commands.append(IntegrationFile(target, root / "skills" / "redops-rag" / "SKILL.md", INTEGRATION_TEXT))
        return commands
    raise ValueError("target must be one of: codex, claude, opencode, all")


def install_integrations(
    target: str,
    *,
    dry_run: bool = False,
    force: bool = False,
    skill_paths: Iterable[str | Path] | None = None,
) -> list[dict[str, str]]:
    targets = ("codex", "claude", "opencode") if target == "all" else (target,)
    normalized_skill_paths = tuple(skill_paths) if skill_paths is not None else None
    results: list[dict[str, str]] = []
    for item_target in targets:
        for item in integration_files(item_target, skill_paths=normalized_skill_paths):
            if item.path.exists() and not force:
                results.append({"target": item.target, "path": str(item.path), "status": "exists"})
                continue
            if not dry_run:
                item.path.parent.mkdir(parents=True, exist_ok=True)
                item.path.write_text(item.content, encoding="utf-8")
            results.append({"target": item.target, "path": str(item.path), "status": "planned" if dry_run else "installed"})
    return results
