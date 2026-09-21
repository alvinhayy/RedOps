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
redops workflow \"<authorized task>\"
redops orchestrate \"<authorized task>\"
redops exegol status
```

Use `redops workflow` to plan the phase-gated lifecycle before routing niche agents.
Use `redops exegol exec -- <argv...>` only after confirming written scope and
the configured Exegol container. Keep active web/mobile/WAF checks to approved
local, staging, or lab targets; do not submit destructive payloads or create
load. Knowledge lives in Markdown and should be refreshed with `redops ingest`.

When a provider is unavailable, use `redops query --no-generate` for a local,
extractive answer. Provider credentials must remain in environment variables,
never in prompts, reports, or the shared corpus.
"""

CODEX_SKILL_TEXT = """---
name: redops-rag
description: Source-grounded authorized pentest RAG workflow.
---

""" + INTEGRATION_TEXT

ENGAGEMENT_WORKFLOW_SKILL_TEXT = """---
name: engagement-workflow
description: Phase-gated authorized penetration-testing lifecycle for RedOps.
---

# RedOps engagement workflow

Use the RedOps phase graph for authorized assessments. Start with pre-engagement
scope and written authorization, then hand off evidence through information gathering,
vulnerability assessment, approved exploitation, post-exploitation impact validation,
lateral-movement validation, proof-of-concept packaging, and post-engagement reporting.

Call the `plan_engagement` tool from the `redops-rag` MCP or run:

```bash
redops workflow "<authorized task>"
```

Call `route_task` to select technical niche agents. Active phases remain blocked until
written scope, exact target allowlists, phase approval, and Exegol/runtime health are
confirmed. Every handoff includes evidence, source citations, scope, artifacts, and
open questions. Never include credentials or claim a command ran without output.
"""

ORCHESTRATOR_COMMAND_TEXT = (
    "Act as the RedOps orchestrator for $ARGUMENTS. First call `plan_engagement` "
    "from the redops-rag MCP (or run `redops workflow`) to create the phase-gated "
    "lifecycle: pre-engagement, information gathering, vulnerability assessment, "
    "exploitation, post-exploitation, lateral movement, proof-of-concept, and "
    "post-engagement. Then call `route_task` for niche specialists, retrieve context "
    "with `search_knowledge`/`search_writeups`, and delegate each phase to the matching "
    "phase agent and niche agent using the provider's native agent/task mechanism. "
    "Stop active phases until written scope and exact approval are confirmed. Pass each "
    "worker only its scoped evidence and handoff contract, preserve [S#] citations and "
    "source URLs, and never claim a command ran without its output. Execution remains "
    "Exegol-first and belongs to the approved phase specialist."
)


_COMMAND_NAME = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def _manifest_commands() -> list[dict[str, str]]:
    manifest = Path(__file__).resolve().parents[2] / "agents" / "skill-commands.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [
            {
                "name": "redops-rag",
                "skill": "redops-rag",
                "description": "RedOps orchestrator entry point",
                "content": ORCHESTRATOR_COMMAND_TEXT,
            }
        ]
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
            discovered.append(
                {
                    "name": name,
                    "skill": owner,
                    "description": _frontmatter_field(content, "description"),
                    "content": content,
                }
            )
            seen_names.add(name)
    return discovered


def _frontmatter_field(content: str, field: str) -> str:
    """Read a simple scalar from a Markdown YAML frontmatter block."""

    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for line in lines[1:]:
        if line.strip() == "---":
            break
        prefix = f"{field}:"
        if line.startswith(prefix):
            return line[len(prefix) :].strip().strip("'\"")
    return ""


def _slash_commands(skill_paths: Iterable[str | Path] | None = None) -> list[dict[str, str]]:
    """Combine discovered skill commands with the built-in RedOps fallbacks."""

    manifest = _manifest_commands()
    discovered = _discover_skill_commands(skill_paths)
    # Built-in commands are canonical when scanning default locations. An
    # explicit --skill-path/REDOPS_SKILL_PATHS opts into external skill content.
    external_source = skill_paths is not None or bool(os.getenv("REDOPS_SKILL_PATHS"))
    combined = discovered if external_source else manifest
    seen = {item["name"] for item in combined}
    additions = manifest if external_source else discovered
    for item in additions:
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


def _gemini_command(item: dict[str, str]) -> str:
    description = item.get("description", "") or item["name"]
    body = item["content"]
    if body.startswith("---"):
        parts = body.split("---", 2)
        if len(parts) == 3:
            body = parts[2].lstrip()
    body = body.replace("\\", "\\\\").replace('"', '\\"')
    body = body.replace("$ARGUMENTS", "{{args}}")
    if "{{args}}" not in body:
        body = f"{body.rstrip()}\n\nArguments: {{{{args}}}}"
    description = description.replace("\\", "\\\\").replace('"', '\\"')
    return (
        "# Generated by RedOps; edit the source skill command instead.\n"
        f'description = "{description}"\n\n'
        f'prompt = """\n{body}\n"""\n'
    )


def _skill_file(target: str, root: Path) -> IntegrationFile:
    return IntegrationFile(target, root / "skills" / "redops-rag" / "SKILL.md", CODEX_SKILL_TEXT)


def _workflow_skill_file(target: str, root: Path) -> IntegrationFile:
    return IntegrationFile(
        target,
        root / "skills" / "engagement-workflow" / "SKILL.md",
        ENGAGEMENT_WORKFLOW_SKILL_TEXT,
    )


def integration_files(
    target: str,
    *,
    skill_paths: Iterable[str | Path] | None = None,
    workspace: str | Path | None = None,
) -> list[IntegrationFile]:
    normalized = target.lower()
    if normalized == "codex":
        root = _home("CODEX_HOME", Path.home() / ".codex")
        return [_skill_file(target, root), _workflow_skill_file(target, root)]
    if normalized == "claude":
        root = _home("CLAUDE_HOME", Path.home() / ".claude")
        files = [_skill_file(target, root), _workflow_skill_file(target, root)]
        files.extend(
            IntegrationFile(target, root / "commands" / f"{item['name']}.md", item["content"])
            for item in _slash_commands(skill_paths)
        )
        return files
    if normalized == "opencode":
        root = _home("OPENCODE_HOME", Path.home() / ".config" / "opencode")
        commands = [
            IntegrationFile(target, root / "commands" / f"{item['name']}.md", item["content"])
            for item in _slash_commands(skill_paths)
        ]
        commands.append(_skill_file(target, root))
        commands.append(_workflow_skill_file(target, root))
        # OpenCode also follows the cross-agent .agents/skills convention.
        commands.append(_skill_file(target, _home("AGENTS_HOME", Path.home() / ".agents")))
        commands.append(_workflow_skill_file(target, _home("AGENTS_HOME", Path.home() / ".agents")))
        return commands
    if normalized in {"zcode", "cursor", "gemini", "copilot", "windsurf", "amp", "crush"}:
        agents_root = _home("AGENTS_HOME", Path.home() / ".agents")
        files = [_skill_file(target, agents_root), _workflow_skill_file(target, agents_root)]
        commands = _slash_commands(skill_paths)
        if normalized == "zcode":
            files.extend(IntegrationFile(target, agents_root / "commands" / f"{item['name']}.md", item["content"]) for item in commands)
        elif normalized == "cursor":
            root = _home("CURSOR_HOME", Path.home() / ".cursor")
            files.extend(IntegrationFile(target, root / "commands" / f"{item['name']}.md", item["content"]) for item in commands)
        elif normalized == "gemini":
            root = _home("GEMINI_HOME", Path.home() / ".gemini")
            files.extend(IntegrationFile(target, root / "commands" / f"{item['name']}.toml", _gemini_command(item)) for item in commands)
        elif workspace is not None and normalized == "copilot":
            root = Path(workspace).expanduser()
            files.extend(IntegrationFile(target, root / ".github" / "prompts" / f"{item['name']}.prompt.md", item["content"]) for item in commands)
        elif workspace is not None and normalized == "windsurf":
            root = Path(workspace).expanduser()
            files.extend(IntegrationFile(target, root / ".windsurf" / "workflows" / f"{item['name']}.md", item["content"]) for item in commands)
        return files
    raise ValueError(
        "target must be one of: codex, claude, opencode, zcode, cursor, gemini, "
        "copilot, windsurf, amp, crush, all"
    )


def install_integrations(
    target: str,
    *,
    dry_run: bool = False,
    force: bool = False,
    skill_paths: Iterable[str | Path] | None = None,
    workspace: str | Path | None = None,
) -> list[dict[str, str]]:
    target = target.lower()
    targets = (
        ("codex", "claude", "opencode", "zcode", "cursor", "gemini", "copilot", "windsurf", "amp", "crush")
        if target == "all"
        else (target,)
    )
    normalized_skill_paths = tuple(skill_paths) if skill_paths is not None else None
    results: list[dict[str, str]] = []
    seen_paths: set[Path] = set()
    for item_target in targets:
        for item in integration_files(item_target, skill_paths=normalized_skill_paths, workspace=workspace):
            if item.path in seen_paths:
                continue
            seen_paths.add(item.path)
            if item.path.exists() and not force:
                results.append({"target": item.target, "path": str(item.path), "status": "exists"})
                continue
            if not dry_run:
                item.path.parent.mkdir(parents=True, exist_ok=True)
                item.path.write_text(item.content, encoding="utf-8")
            results.append({"target": item.target, "path": str(item.path), "status": "planned" if dry_run else "installed"})
    return results
