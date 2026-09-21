"""Safe, credential-free RedOps status reporting."""

from __future__ import annotations

import shutil
from typing import Any

from .config import Settings
from .providers import get_provider
from .store import IndexStore


def collect_status(settings: Settings | None = None) -> dict[str, Any]:
    settings = settings or Settings.from_env()
    provider = get_provider(settings.llm_provider)
    index_exists = settings.db_path.exists()
    index = IndexStore(settings.db_path).stats() if index_exists else {
        "documents": 0,
        "chunks": 0,
        "embedding_fingerprint": None,
    }
    return {
        "provider": provider.id,
        "provider_name": provider.display_name,
        "model": settings.llm_model,
        "api_key_configured": bool(settings.api_key),
        "embedding": settings.embedding_fingerprint,
        "knowledge_dir": str(settings.knowledge_dir),
        "index_path": str(settings.db_path),
        "index_exists": index_exists,
        "documents": index["documents"],
        "chunks": index["chunks"],
        "execution_backend": settings.execution_backend,
        "exegol_container": settings.exegol_container,
        "exegol_cli_available": shutil.which("exegol") is not None,
    }


def render_status(status: dict[str, Any]) -> str:
    key_state = "configured" if status["api_key_configured"] else "not configured"
    index_state = "ready" if status["index_exists"] else "not initialized"
    exegol_state = "available" if status["exegol_cli_available"] else "not found"
    lines = [
        "RedOps status",
        "─────────────",
        f"Provider       {status['provider_name']} ({status['provider']})",
        f"Model          {status['model']}",
        f"API key        {key_state}",
        f"Embedding      {status['embedding']}",
        f"Knowledge      {status['knowledge_dir']}",
        f"Index          {index_state} · {status['documents']} documents · {status['chunks']} chunks",
        f"Execution      {status['execution_backend']}",
        f"Exegol         {exegol_state} · container {status['exegol_container']}",
    ]
    return "\n".join(lines)
