"""Optional mobile runtime MCP configuration.

The Android device automation server is intentionally not vendored.  This small
config object builds a safe stdio argv for the upstream uiautomator2-mcp server
and validates its local launcher without importing optional dependencies.
"""
from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class MobileMcpConfig:
    python: str = ""
    server_script: str = ""
    device_serial: str | None = None

    @classmethod
    def from_env(cls) -> MobileMcpConfig:
        return cls(
            python=os.getenv("REDOPS_MOBILE_MCP_PYTHON", "").strip(),
            server_script=os.getenv("REDOPS_MOBILE_MCP_SERVER", "").strip(),
            device_serial=os.getenv("REDOPS_MOBILE_DEVICE_SERIAL") or None,
        )

    def command(self) -> list[str]:
        """Return the stdio launcher argv, or an empty list when unconfigured."""
        if not self.python and not self.server_script:
            return []
        if not self.python or not self.server_script:
            raise ValueError(
                "REDOPS_MOBILE_MCP_PYTHON and REDOPS_MOBILE_MCP_SERVER must be set together"
            )
        return [self.python, self.server_script]

    def validate(self) -> list[str]:
        """Return non-fatal local setup issues; no process or device is contacted."""
        issues: list[str] = []
        command = self.command()
        if not command:
            return issues
        if shutil.which(command[0]) is None and not Path(command[0]).is_file():
            issues.append(f"MCP Python executable not found: {command[0]}")
        if not Path(command[1]).is_file():
            issues.append(f"MCP server script not found: {command[1]}")
        return issues
