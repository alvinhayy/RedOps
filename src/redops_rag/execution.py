"""Safe command execution through the local host or an Exegol container.

The runner deliberately accepts an argv list and never invokes a shell.  It is
intended for authorized testing environments only; it is not a sandbox.
"""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass

from .config import Settings


class ExecutionError(RuntimeError):
    def __init__(self, code: str, message: str, *, details: dict | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}

    def as_dict(self) -> dict:
        return {"error": self.code, "message": self.message, **self.details}


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    def as_dict(self) -> dict:
        return {
            "command": self.command,
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


class CommandRunner:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_env()
        if self.settings.execution_backend not in {"local", "exegol"}:
            raise ExecutionError(
                "invalid_backend",
                "REDOPS_EXECUTION_BACKEND must be 'local' or 'exegol'",
            )

    @property
    def backend(self) -> str:
        return self.settings.execution_backend

    def _command(self, args: Sequence[str]) -> list[str]:
        values = [str(arg) for arg in args]
        # argparse.REMAINDER keeps the conventional ``--`` separator.
        while values and values[0] == "--":
            values.pop(0)
        if not values or not values[0].strip():
            raise ExecutionError("empty_command", "A command is required after 'exec --'")
        if self.backend == "local":
            return values
        command = ["exegol", "exec"]
        if self.settings.exegol_verbose:
            command.append("-v")
        if self.settings.exegol_tmp:
            command.append("--tmp")
            command.extend([self.settings.exegol_image, *values])
        else:
            command.extend([self.settings.exegol_container, *values])
        return command

    def run(self, args: Sequence[str], *, timeout: float | None = None) -> ExecutionResult:
        command = self._command(args)
        executable = command[0]
        if shutil.which(executable) is None:
            raise ExecutionError(
                "missing_executable",
                f"Executable not found: {executable}",
                details={"executable": executable, "backend": self.backend},
            )
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout if timeout is not None else self.settings.exegol_timeout,
                check=False,
                shell=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise ExecutionError(
                "timeout",
                f"Command timed out after {exc.timeout} seconds",
                details={"command": command, "timeout": exc.timeout},
            ) from exc
        except OSError as exc:
            raise ExecutionError(
                "execution_failed", str(exc), details={"command": command}
            ) from exc
        result = ExecutionResult(command, completed.returncode, completed.stdout, completed.stderr)
        if completed.returncode != 0:
            raise ExecutionError(
                "nonzero_exit",
                f"Command exited with status {completed.returncode}",
                details=result.as_dict(),
            )
        return result

    def status(self) -> ExecutionResult:
        if self.backend != "exegol":
            return ExecutionResult([], 0, "local backend active", "")
        return self._run_command(
            ["exegol", "info", self.settings.exegol_container],
            timeout=self.settings.exegol_timeout,
        )

    def _run_command(self, command: list[str], *, timeout: float) -> ExecutionResult:
        """Run an already assembled Exegol command (used by read-only status)."""
        if shutil.which(command[0]) is None:
            raise ExecutionError(
                "missing_executable",
                f"Executable not found: {command[0]}",
                details={"executable": command[0], "backend": self.backend},
            )
        try:
            completed = subprocess.run(
                command, capture_output=True, text=True, timeout=timeout, check=False, shell=False
            )
        except subprocess.TimeoutExpired as exc:
            raise ExecutionError(
                "timeout", f"Command timed out after {exc.timeout} seconds",
                details={"command": command, "timeout": exc.timeout},
            ) from exc
        result = ExecutionResult(command, completed.returncode, completed.stdout, completed.stderr)
        if completed.returncode != 0:
            raise ExecutionError(
                "nonzero_exit", f"Command exited with status {completed.returncode}",
                details=result.as_dict(),
            )
        return result
