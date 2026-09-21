from redops_rag.integrations import install_integrations


def test_install_cli_dry_run_does_not_write(tmp_path, monkeypatch):
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    result = install_integrations("codex", dry_run=True)
    assert result[0]["status"] == "planned"
    assert not (tmp_path / "codex").exists()


def test_install_all_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    monkeypatch.setenv("CLAUDE_HOME", str(tmp_path / "claude"))
    monkeypatch.setenv("OPENCODE_HOME", str(tmp_path / "opencode"))
    monkeypatch.setenv("AGENTS_HOME", str(tmp_path / "agents"))
    monkeypatch.setenv("CURSOR_HOME", str(tmp_path / "cursor"))
    monkeypatch.setenv("GEMINI_HOME", str(tmp_path / "gemini"))
    first = install_integrations("all")
    second = install_integrations("all")
    assert all(item["status"] == "installed" for item in first)
    assert all(item["status"] == "exists" for item in second)


def test_skill_slash_commands_are_installed_for_supported_clients(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_HOME", str(tmp_path / "claude"))
    monkeypatch.setenv("OPENCODE_HOME", str(tmp_path / "opencode"))
    monkeypatch.setenv("AGENTS_HOME", str(tmp_path / "agents"))
    monkeypatch.setenv("CURSOR_HOME", str(tmp_path / "cursor"))
    monkeypatch.setenv("GEMINI_HOME", str(tmp_path / "gemini"))
    install_integrations("all")
    for root in (tmp_path / "claude" / "commands", tmp_path / "opencode" / "commands"):
        assert (root / "mobile-vuln-hunt.md").exists()
        assert (root / "reverse-engineer.md").exists()
        assert (root / "afl-fuzzing.md").exists()
        assert "orchestrator" in (root / "redops-rag.md").read_text(encoding="utf-8")


def test_skill_repository_commands_are_discovered_and_copied(tmp_path, monkeypatch):
    skill_repo = tmp_path / "mobile-reverse-skill"
    command_dir = skill_repo / ".agents" / "commands"
    command_dir.mkdir(parents=True)
    command = command_dir / "observe-runtime.md"
    command.write_text("---\ndescription: observe\n---\n$ARGUMENTS\n", encoding="utf-8")
    duplicate_dir = skill_repo / ".claude" / "commands"
    duplicate_dir.mkdir(parents=True)
    (duplicate_dir / "observe-runtime.md").write_text("duplicate", encoding="utf-8")
    (command_dir / "README.md").write_text("not a command", encoding="utf-8")
    monkeypatch.setenv("CLAUDE_HOME", str(tmp_path / "claude"))
    monkeypatch.setenv("OPENCODE_HOME", str(tmp_path / "opencode"))

    result = install_integrations("claude", skill_paths=[skill_repo])

    assert any(item["path"].endswith("observe-runtime.md") for item in result)
    assert sum(item["path"].endswith("observe-runtime.md") for item in result) == 1
    root = tmp_path / "claude" / "commands"
    assert (root / "observe-runtime.md").read_text(encoding="utf-8") == command.read_text(encoding="utf-8")
    assert not (root / "README.md").exists()


def test_skill_command_does_not_replace_existing_file_without_force(tmp_path, monkeypatch):
    skill_repo = tmp_path / "skill"
    command_dir = skill_repo / "commands"
    command_dir.mkdir(parents=True)
    (command_dir / "custom.md").write_text("new", encoding="utf-8")
    claude = tmp_path / "claude"
    existing = claude / "commands" / "custom.md"
    existing.parent.mkdir(parents=True)
    existing.write_text("user-owned", encoding="utf-8")
    monkeypatch.setenv("CLAUDE_HOME", str(claude))

    install_integrations("claude", skill_paths=[skill_repo])

    assert existing.read_text(encoding="utf-8") == "user-owned"


def test_native_provider_formats_are_generated(tmp_path, monkeypatch):
    skill_repo = tmp_path / "skill"
    command_dir = skill_repo / "commands"
    command_dir.mkdir(parents=True)
    (command_dir / "demo.md").write_text(
        "---\ndescription: Demo command\n---\nRun the demo for $ARGUMENTS\n", encoding="utf-8"
    )
    monkeypatch.setenv("AGENTS_HOME", str(tmp_path / "agents"))
    monkeypatch.setenv("CURSOR_HOME", str(tmp_path / "cursor"))
    monkeypatch.setenv("GEMINI_HOME", str(tmp_path / "gemini"))

    install_integrations("all", skill_paths=[skill_repo], workspace=tmp_path / "workspace")

    assert (tmp_path / "agents/commands/demo.md").exists()
    assert (tmp_path / "cursor/commands/demo.md").exists()
    gemini = (tmp_path / "gemini/commands/demo.toml").read_text(encoding="utf-8")
    assert 'description = "Demo command"' in gemini
    assert "{{args}}" in gemini
    assert (tmp_path / "workspace/.github/prompts/demo.prompt.md").exists()
    assert (tmp_path / "workspace/.windsurf/workflows/demo.md").exists()
