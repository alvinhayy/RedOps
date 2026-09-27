"""Safe, credential-free RedOps status reporting."""

from __future__ import annotations

import shutil
from typing import Any

from .config import Settings
from .execution import CommandRunner, ExecutionError
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
    exegol_cli_available = shutil.which("exegol") is not None
    exegol_runtime = "not_configured"
    exegol_error = None
    if settings.execution_backend == "exegol":
        if not exegol_cli_available:
            exegol_runtime = "cli_missing"
        else:
            try:
                # Probe only; never return Exegol's stdout because it can contain
                # generated container credentials.
                CommandRunner(settings).status()
                exegol_runtime = "ready"
            except ExecutionError as exc:
                exegol_runtime = "unavailable"
                exegol_error = exc.code
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
        "exegol_cli_available": exegol_cli_available,
        "exegol_runtime": exegol_runtime,
        "exegol_error": exegol_error,
    }


def render_status(status: dict[str, Any]) -> str:
    key_state = "configured" if status["api_key_configured"] else "not configured"
    index_state = "ready" if status["index_exists"] else "not initialized"
    if status["execution_backend"] == "exegol":
        exegol_state = {
            "ready": "ready",
            "unavailable": "unavailable",
            "cli_missing": "CLI not found",
        }.get(status["exegol_runtime"], status["exegol_runtime"])
        if status.get("exegol_error"):
            exegol_state += f" ({status['exegol_error']})"
    else:
        exegol_state = "not selected"
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
