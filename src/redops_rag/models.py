from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Document:
    path: str
    title: str
    source_url: str
    content: str
    content_hash: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class Chunk:
    index: int
    heading: str
    content: str
    token_count: int


@dataclass(slots=True)
class SearchResult:
    chunk_id: str
    title: str
    source_url: str
    path: str
    heading: str
    content: str
    score: float

    def as_dict(self) -> dict[str, object]:
        return {
            "chunk_id": self.chunk_id,
            "title": self.title,
            "source_url": self.source_url,
            "path": self.path,
            "heading": self.heading,
            "content": self.content,
            "score": round(self.score, 6),
        }

