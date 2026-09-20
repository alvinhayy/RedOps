from pathlib import Path

import pytest

from redops_rag.mobile_mcp import MobileMcpConfig


def test_mobile_mcp_is_optional_and_builds_argv(tmp_path: Path):
    python = tmp_path / "python"
    server = tmp_path / "server.py"
    python.touch()
    server.touch()
    config = MobileMcpConfig(str(python), str(server), "emulator-5554")
    assert config.command() == [str(python), str(server)]
    assert config.validate() == []


def test_mobile_mcp_rejects_partial_configuration():
    with pytest.raises(ValueError, match="must be set together"):
        MobileMcpConfig(python="python3").command()


def test_mobile_mcp_default_is_graceful():
    config = MobileMcpConfig()
    assert config.command() == []
    assert config.validate() == []
