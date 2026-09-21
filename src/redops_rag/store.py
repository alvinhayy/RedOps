from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from .models import Chunk, Document, SearchResult


class IndexStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self.connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY,
                    path TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    source_url TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                    chunk_index INTEGER NOT NULL,
                    heading TEXT NOT NULL,
                    content TEXT NOT NULL,
                    token_count INTEGER NOT NULL,
                    embedding_json TEXT NOT NULL,
                    UNIQUE(document_id, chunk_index)
                );
                CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                    chunk_id UNINDEXED, heading, content, tokenize='unicode61'
                );
                """
            )

    def get_metadata(self, key: str) -> str | None:
        with self.connect() as db:
            row = db.execute("SELECT value FROM metadata WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None

    def set_metadata(self, key: str, value: str) -> None:
        with self.connect() as db:
            db.execute(
                "INSERT INTO metadata(key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, value),
            )

    def document_hash(self, path: str) -> str | None:
        with self.connect() as db:
            row = db.execute("SELECT content_hash FROM documents WHERE path = ?", (path,)).fetchone()
        return row["content_hash"] if row else None

    def upsert_document(
        self, document: Document, chunks: list[Chunk], embeddings: list[list[float]]
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("every chunk must have one embedding")
        with self.connect() as db:
            old_ids = [
                row["id"]
                for row in db.execute(
                    "SELECT c.id FROM chunks c JOIN documents d ON d.id=c.document_id WHERE d.path=?",
                    (document.path,),
                )
            ]
            if old_ids:
                db.executemany("DELETE FROM chunks_fts WHERE chunk_id = ?", [(item,) for item in old_ids])
            db.execute("DELETE FROM documents WHERE path = ?", (document.path,))
            cursor = db.execute(
                "INSERT INTO documents(path,title,source_url,content_hash,metadata_json) VALUES(?,?,?,?,?)",
                (
                    document.path,
                    document.title,
                    document.source_url,
                    document.content_hash,
                    json.dumps(document.metadata, sort_keys=True),
                ),
            )
            document_id = cursor.lastrowid
            for chunk, embedding in zip(chunks, embeddings, strict=True):
                path_hash = hashlib.sha256(document.path.encode()).hexdigest()[:16]
                chunk_id = f"{path_hash}:{document.content_hash[:16]}:{chunk.index}"
                db.execute(
                    "INSERT INTO chunks VALUES(?,?,?,?,?,?,?)",
                    (
                        chunk_id,
                        document_id,
                        chunk.index,
                        chunk.heading,
                        chunk.content,
                        chunk.token_count,
                        json.dumps(embedding, separators=(",", ":")),
                    ),
                )
                db.execute(
                    "INSERT INTO chunks_fts(chunk_id,heading,content) VALUES(?,?,?)",
                    (chunk_id, chunk.heading, chunk.content),
                )

    def delete_missing(self, active_paths: set[str]) -> int:
        with self.connect() as db:
            rows = db.execute("SELECT path FROM documents").fetchall()
            missing = [row["path"] for row in rows if row["path"] not in active_paths]
            for path in missing:
                ids = db.execute(
                    "SELECT c.id FROM chunks c JOIN documents d ON d.id=c.document_id WHERE d.path=?",
                    (path,),
                ).fetchall()
                db.executemany("DELETE FROM chunks_fts WHERE chunk_id=?", [(row["id"],) for row in ids])
                db.execute("DELETE FROM documents WHERE path=?", (path,))
        return len(missing)

    def search(
        self,
        query: str,
        query_vector: list[float],
        limit: int,
        vector_weight: float,
        corpus: str | None = None,
    ) -> list[SearchResult]:
        if not 0 <= vector_weight <= 1:
            raise ValueError("vector_weight must be between zero and one")
        with self.connect() as db:
            all_rows = db.execute(
                """SELECT c.id, c.heading, c.content, c.embedding_json,
                          d.title, d.source_url, d.path, d.metadata_json
                   FROM chunks c JOIN documents d ON d.id=c.document_id"""
            ).fetchall()
            rows = [
                row
                for row in all_rows
                if corpus is None or json.loads(row["metadata_json"]).get("corpus", "knowledge") == corpus
            ]
            vector_ranked = sorted(
                rows,
                key=lambda row: _cosine(query_vector, json.loads(row["embedding_json"])),
                reverse=True,
            )[: max(limit * 8, 40)]
            terms = re.findall(r"[\w]+", query.lower(), flags=re.UNICODE)
            lexical_rows: list[sqlite3.Row] = []
            if terms:
                fts_query = " OR ".join(f'"{term}"' for term in terms[:20])
                lexical_rows = db.execute(
                    "SELECT chunk_id FROM chunks_fts WHERE chunks_fts MATCH ? ORDER BY bm25(chunks_fts) LIMIT ?",
                    (fts_query, max(limit * 8, 40)),
                ).fetchall()

        scores: dict[str, float] = {}
        row_by_id = {row["id"]: row for row in rows}
        for rank, row in enumerate(vector_ranked, start=1):
            scores[row["id"]] = scores.get(row["id"], 0.0) + vector_weight / (60 + rank)
        for rank, row in enumerate(lexical_rows, start=1):
            chunk_id = row["chunk_id"]
            if chunk_id not in row_by_id:
                continue
            scores[chunk_id] = scores.get(chunk_id, 0.0) + (1 - vector_weight) / (60 + rank)

        ranked = sorted(scores, key=scores.get, reverse=True)[:limit]
        return [
            SearchResult(
                chunk_id=chunk_id,
                title=row_by_id[chunk_id]["title"],
                source_url=row_by_id[chunk_id]["source_url"],
                path=row_by_id[chunk_id]["path"],
                heading=row_by_id[chunk_id]["heading"],
                content=row_by_id[chunk_id]["content"],
                score=scores[chunk_id],
                corpus=json.loads(row_by_id[chunk_id]["metadata_json"]).get("corpus", "knowledge"),
            )
            for chunk_id in ranked
        ]

    def stats(self) -> dict[str, object]:
        with self.connect() as db:
            documents = db.execute("SELECT COUNT(*) AS count FROM documents").fetchone()["count"]
            chunks = db.execute("SELECT COUNT(*) AS count FROM chunks").fetchone()["count"]
            corpus_rows = db.execute("SELECT metadata_json FROM documents").fetchall()
            fingerprint = db.execute(
                "SELECT value FROM metadata WHERE key='embedding_fingerprint'"
            ).fetchone()
        by_corpus: dict[str, int] = {}
        for row in corpus_rows:
            corpus = json.loads(row["metadata_json"]).get("corpus", "knowledge")
            by_corpus[corpus] = by_corpus.get(corpus, 0) + 1
        return {
            "documents": documents,
            "chunks": chunks,
            "documents_by_corpus": by_corpus,
            "embedding_fingerprint": fingerprint["value"] if fingerprint else None,
        }


def _cosine(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        return -1.0
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return sum(a * b for a, b in zip(left, right, strict=True)) / (left_norm * right_norm)
