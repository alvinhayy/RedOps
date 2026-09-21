from pathlib import Path

from redops_rag.config import Settings
from redops_rag.status import collect_status, render_status


def test_status_does_not_expose_credentials(tmp_path: Path) -> None:
    settings = Settings(db_path=tmp_path / "missing.db", api_key="secret-value")
    status = collect_status(settings)
    assert status["api_key_configured"] is True
    assert "secret-value" not in render_status(status)
    assert status["documents"] == 0
    assert status["index_exists"] is False
