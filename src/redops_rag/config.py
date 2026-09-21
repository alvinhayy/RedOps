from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .providers import get_provider


def _env_float(name: str, default: float) -> float:
    return float(os.getenv(name, str(default)))


def _env_int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean (true/false)")


@dataclass(frozen=True, slots=True)
class Settings:
    db_path: Path = Path("data/redops.db")
    knowledge_dir: Path = Path("knowledge")
    writeups_dir: Path = Path("writeups")
    embedding_provider: str = "hash"
    embedding_model: str = "redops-hash-v1"
    embedding_dimension: int = 384
    llm_provider: str = "extractive"
    llm_model: str = "gpt-4.1-mini"
    api_base_url: str = "https://api.openai.com/v1"
    api_key: str | None = None
    embedding_api_base_url: str = "https://api.openai.com/v1"
    embedding_api_key: str | None = None
    top_k: int = 6
    vector_weight: float = 0.65
    chunk_size: int = 1400
    chunk_overlap: int = 180
    execution_backend: str = "local"
    exegol_container: str = "redops"
    exegol_image: str = "full"
    exegol_tmp: bool = False
    exegol_verbose: bool = False
    exegol_timeout: float = 120.0

    @classmethod
    def from_env(cls) -> Settings:
        llm_provider = os.getenv("REDOPS_LLM_PROVIDER", "extractive").strip().lower()
        provider = get_provider(llm_provider)
        api_key = os.getenv("REDOPS_API_KEY")
        if not api_key and provider.api_key_env:
            api_key = os.getenv(provider.api_key_env)
        base_url = os.getenv("REDOPS_API_BASE_URL")
        if not base_url:
            base_url = os.getenv(f"REDOPS_{llm_provider.upper()}_BASE_URL")
        base_url = base_url or provider.default_base_url or "https://api.openai.com/v1"
        model = os.getenv("REDOPS_LLM_MODEL") or provider.default_chat_model or "gpt-4.1-mini"
        embedding_provider = os.getenv("REDOPS_EMBEDDING_PROVIDER", "hash").strip().lower()
        embedding_spec = get_provider(embedding_provider) if embedding_provider != "hash" else None
        embedding_key = os.getenv("REDOPS_EMBEDDING_API_KEY") or (
            os.getenv(embedding_spec.api_key_env) if embedding_spec and embedding_spec.api_key_env else None
        ) or api_key
        embedding_base = os.getenv("REDOPS_EMBEDDING_API_BASE_URL") or (
            embedding_spec.default_base_url if embedding_spec else None
        ) or base_url
        return cls(
            db_path=Path(os.getenv("REDOPS_DB_PATH", "data/redops.db")),
            knowledge_dir=Path(os.getenv("REDOPS_KNOWLEDGE_DIR", "knowledge")),
            writeups_dir=Path(os.getenv("REDOPS_WRITEUPS_DIR", "writeups")),
            embedding_provider=os.getenv("REDOPS_EMBEDDING_PROVIDER", "hash"),
            embedding_model=os.getenv("REDOPS_EMBEDDING_MODEL", "redops-hash-v1"),
            embedding_dimension=_env_int("REDOPS_EMBEDDING_DIMENSION", 384),
            llm_provider=llm_provider,
            llm_model=model,
            api_base_url=base_url.rstrip("/"),
            api_key=api_key,
            embedding_api_base_url=embedding_base.rstrip("/"),
            embedding_api_key=embedding_key,
            top_k=_env_int("REDOPS_TOP_K", 6),
            vector_weight=_env_float("REDOPS_VECTOR_WEIGHT", 0.65),
            chunk_size=_env_int("REDOPS_CHUNK_SIZE", 1400),
            chunk_overlap=_env_int("REDOPS_CHUNK_OVERLAP", 180),
            execution_backend=os.getenv("REDOPS_EXECUTION_BACKEND", "local").strip().lower(),
            exegol_container=os.getenv("REDOPS_EXEGOL_CONTAINER", "redops"),
            exegol_image=os.getenv("REDOPS_EXEGOL_IMAGE", "full"),
            exegol_tmp=_env_bool("REDOPS_EXEGOL_TMP", False),
            exegol_verbose=_env_bool("REDOPS_EXEGOL_VERBOSE", False),
            exegol_timeout=_env_float("REDOPS_EXEGOL_TIMEOUT", 120.0),
        )

    @property
    def embedding_fingerprint(self) -> str:
        return f"{self.embedding_provider}:{self.embedding_model}:{self.embedding_dimension}"
