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
    first = install_integrations("all")
    second = install_integrations("all")
    assert all(item["status"] == "installed" for item in first)
    assert all(item["status"] == "exists" for item in second)


def test_skill_slash_commands_are_installed_for_supported_clients(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_HOME", str(tmp_path / "claude"))
    monkeypatch.setenv("OPENCODE_HOME", str(tmp_path / "opencode"))
    install_integrations("all")
    for root in (tmp_path / "claude" / "commands", tmp_path / "opencode" / "commands"):
        assert (root / "mobile-vuln-hunt.md").exists()
        assert (root / "reverse-engineer.md").exists()
        assert (root / "afl-fuzzing.md").exists()
