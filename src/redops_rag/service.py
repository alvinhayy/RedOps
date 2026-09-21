from __future__ import annotations

from .config import Settings
from .embeddings import Embedder, HashingEmbedder, OpenAICompatibleEmbedder
from .ingest import Ingestor
from .llm import ExtractiveGenerator, Generator, OpenAICompatibleGenerator
from .providers import get_provider
from .store import IndexStore


class RagService:
    def __init__(
        self,
        settings: Settings | None = None,
        embedder: Embedder | None = None,
        generator: Generator | None = None,
    ) -> None:
        self.settings = settings or Settings.from_env()
        self.store = IndexStore(self.settings.db_path)
        self.embedder = embedder or self._build_embedder()
        self.generator = generator or self._build_generator()

    def _build_embedder(self) -> Embedder:
        if self.settings.embedding_provider == "hash":
            return HashingEmbedder(self.settings.embedding_dimension)
        if self.settings.embedding_provider != "hash":
            provider = get_provider(self.settings.embedding_provider)
            if provider.kind != "openai-compatible" or not self.settings.embedding_api_key:
                raise ValueError(
                    f"an API key is required for the {provider.id} embedding provider "
                    f"(set REDOPS_EMBEDDING_API_KEY or its provider key)"
                )
            return OpenAICompatibleEmbedder(
                self.settings.embedding_api_base_url,
                self.settings.embedding_api_key,
                self.settings.embedding_model,
            )
        raise ValueError(f"unsupported embedding provider: {self.settings.embedding_provider}")

    def _build_generator(self) -> Generator:
        if self.settings.llm_provider == "extractive":
            return ExtractiveGenerator()
        provider = get_provider(self.settings.llm_provider)
        if provider.kind == "openai-compatible":
            if not self.settings.api_key:
                key_env = provider.api_key_env or "REDOPS_API_KEY"
                raise ValueError(f"API key is required for {provider.id} ({key_env})")
            return OpenAICompatibleGenerator(
                self.settings.api_base_url, self.settings.api_key, self.settings.llm_model
            )
        raise ValueError(f"unsupported LLM provider: {self.settings.llm_provider}")

    def ingest(self, force: bool = False) -> dict[str, int]:
        return Ingestor(self.settings, self.store, self.embedder).run(force=force)

    def retrieve(self, question: str, top_k: int | None = None, corpus: str | None = None):
        if corpus is not None and corpus not in {"knowledge", "writeups"}:
            raise ValueError("corpus must be knowledge or writeups")
        requested_limit = top_k if top_k is not None else self.settings.top_k
        if not 1 <= requested_limit <= 100:
            raise ValueError("top_k must be between 1 and 100")
        fingerprint = self.store.get_metadata("embedding_fingerprint")
        if fingerprint and fingerprint != self.settings.embedding_fingerprint:
            raise RuntimeError("index embedding configuration differs; rebuild with ingest --force")
        vector = self.embedder.embed([question])[0]
        return self.store.search(
            question,
            vector,
            requested_limit,
            self.settings.vector_weight,
            corpus=corpus,
        )

    def query(
        self,
        question: str,
        top_k: int | None = None,
        generate: bool = True,
        corpus: str | None = None,
    ) -> dict:
        sources = self.retrieve(question, top_k, corpus=corpus)
        answer = self.generator.generate(question, sources) if generate else None
        return {
            "question": question,
            "answer": answer,
            "sources": [source.as_dict() for source in sources],
        }
