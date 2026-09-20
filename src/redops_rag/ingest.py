from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .chunking import chunk_markdown
from .config import Settings
from .embeddings import Embedder
from .models import Document
from .store import IndexStore

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def _parse_front_matter(content: str) -> tuple[dict[str, str], str]:
    match = FRONT_MATTER_RE.match(content)
    if not match:
        return {}, content
    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip().strip('"\'')
    return metadata, content[match.end() :]


def load_document(path: Path, root: Path) -> Document:
    raw = path.read_text(encoding="utf-8")
    metadata, body = _parse_front_matter(raw)
    title_match = TITLE_RE.search(body)
    title = metadata.get("title") or (title_match.group(1).strip() if title_match else path.stem)
    source_url = (
        metadata.get("source_url")
        or metadata.get("source")
        or metadata.get("url")
        or path.resolve().as_uri()
    )
    relative = path.relative_to(root).as_posix()
    return Document(
        path=relative,
        title=title,
        source_url=source_url,
        content=body,
        content_hash=hashlib.sha256(raw.encode()).hexdigest(),
        metadata=metadata,
    )


class Ingestor:
    def __init__(self, settings: Settings, store: IndexStore, embedder: Embedder) -> None:
        self.settings = settings
        self.store = store
        self.embedder = embedder

    def run(self, source_dir: Path | None = None, force: bool = False) -> dict[str, int]:
        root = (source_dir or self.settings.knowledge_dir).resolve()
        if not root.is_dir():
            raise FileNotFoundError(f"knowledge directory does not exist: {root}")

        existing_fingerprint = self.store.get_metadata("embedding_fingerprint")
        fingerprint = self.settings.embedding_fingerprint
        if existing_fingerprint and existing_fingerprint != fingerprint and not force:
            raise RuntimeError(
                "embedding configuration changed; run ingest with --force to rebuild the index"
            )

        files = sorted(path for path in root.rglob("*.md") if path.is_file())
        active_paths: set[str] = set()
        indexed = skipped = empty = 0
        for path in files:
            document = load_document(path, root)
            if not document.content.strip():
                empty += 1
                continue
            active_paths.add(document.path)
            if not force and self.store.document_hash(document.path) == document.content_hash:
                skipped += 1
                continue
            chunks = chunk_markdown(
                document.content,
                max_chars=self.settings.chunk_size,
                overlap=self.settings.chunk_overlap,
            )
            embeddings = self.embedder.embed(
                [f"{chunk.heading}\n{chunk.content}" for chunk in chunks]
            )
            self.store.upsert_document(document, chunks, embeddings)
            indexed += 1

        removed = self.store.delete_missing(active_paths)
        self.store.set_metadata("embedding_fingerprint", fingerprint)
        return {
            "discovered": len(files),
            "indexed": indexed,
            "skipped": skipped,
            "empty": empty,
            "removed": removed,
        }
