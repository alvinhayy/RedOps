import subprocess

import pytest

from redops_rag.config import Settings
from redops_rag.execution import CommandRunner, ExecutionError


def settings(**kwargs):
    values = {"execution_backend": "exegol", "exegol_container": "redops"}
    values.update(kwargs)
    return Settings(**values)


def test_exegol_uses_argv_and_no_shell(monkeypatch):
    seen = {}
    monkeypatch.setattr("redops_rag.execution.shutil.which", lambda _: "/usr/bin/exegol")

    def fake_run(command, **kwargs):
        seen.update(command=command, kwargs=kwargs)
        return subprocess.CompletedProcess(command, 0, "ok", "")

    monkeypatch.setattr("redops_rag.execution.subprocess.run", fake_run)
    result = CommandRunner(settings(exegol_verbose=True, exegol_tmp=True)).run(["nmap", "-sV"])
    assert result.stdout == "ok"
    assert seen["command"] == ["exegol", "exec", "-v", "--tmp", "full", "nmap", "-sV"]
    assert seen["kwargs"]["shell"] is False


def test_empty_command_is_clear():
    with pytest.raises(ExecutionError, match="command is required"):
        CommandRunner(settings()).run([])


def test_missing_executable(monkeypatch):
    monkeypatch.setattr("redops_rag.execution.shutil.which", lambda _: None)
    with pytest.raises(ExecutionError) as exc:
        CommandRunner(settings()).run(["id"])
    assert exc.value.code == "missing_executable"


def test_timeout(monkeypatch):
    monkeypatch.setattr("redops_rag.execution.shutil.which", lambda _: "/usr/bin/exegol")
    monkeypatch.setattr(
        "redops_rag.execution.subprocess.run",
        lambda *args, **kwargs: (_ for _ in ()).throw(subprocess.TimeoutExpired(args[0], 3)),
    )
    with pytest.raises(ExecutionError) as exc:
        CommandRunner(settings()).run(["id"])
    assert exc.value.code == "timeout"


def test_nonzero_exit(monkeypatch):
    monkeypatch.setattr("redops_rag.execution.shutil.which", lambda _: "/usr/bin/exegol")
    monkeypatch.setattr(
        "redops_rag.execution.subprocess.run",
        lambda command, **kwargs: subprocess.CompletedProcess(command, 7, "", "bad"),
    )
    with pytest.raises(ExecutionError) as exc:
        CommandRunner(settings()).run(["id"])
    assert exc.value.code == "nonzero_exit"


def test_local_backend_does_not_prefix_exegol(monkeypatch):
    monkeypatch.setattr("redops_rag.execution.shutil.which", lambda _: "/usr/bin/id")
    calls = []
    monkeypatch.setattr(
        "redops_rag.execution.subprocess.run",
        lambda command, **kwargs: (calls.append(command) or subprocess.CompletedProcess(command, 0, "", "")),
    )
    CommandRunner(Settings()).run(["id", "-u"])
    assert calls == [["id", "-u"]]


def test_status_is_read_only_info(monkeypatch):
    monkeypatch.setattr("redops_rag.execution.shutil.which", lambda _: "/usr/bin/exegol")
    calls = []
    monkeypatch.setattr(
        "redops_rag.execution.subprocess.run",
        lambda command, **kwargs: (calls.append(command) or subprocess.CompletedProcess(command, 0, "", "")),
    )
    CommandRunner(settings()).status()
    assert calls == [["exegol", "info", "redops"]]
