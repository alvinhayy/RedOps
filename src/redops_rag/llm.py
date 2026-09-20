from __future__ import annotations

from typing import Protocol

import httpx

from .models import SearchResult

SYSTEM_PROMPT = """You are RedOps, a retrieval-grounded assistant for authorized security testing.
Use only the supplied sources for factual claims. Cite sources inline as [S1], [S2], and so on.
If sources are insufficient, say what is missing. Never claim a command was executed.
Assume testing is limited to systems the operator is explicitly authorized to assess.
Prefer concise, verifiable steps and call out destructive or disruptive operations."""


class Generator(Protocol):
    def generate(self, question: str, sources: list[SearchResult]) -> str: ...


class ExtractiveGenerator:
    def generate(self, question: str, sources: list[SearchResult]) -> str:
        del question
        if not sources:
            return "Tidak ada konteks yang cukup di knowledge base untuk menjawab pertanyaan ini."
        lines = ["Konteks paling relevan yang ditemukan:"]
        for index, source in enumerate(sources[:4], start=1):
            excerpt = " ".join(source.content.split())
            if len(excerpt) > 420:
                excerpt = f"{excerpt[:417]}..."
            lines.append(f"- [S{index}] **{source.title} — {source.heading}**: {excerpt}")
        return "\n".join(lines)


class OpenAICompatibleGenerator:
    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def generate(self, question: str, sources: list[SearchResult]) -> str:
        context = "\n\n".join(
            f"[S{index}] {source.title} | {source.heading} | {source.source_url}\n{source.content}"
            for index, source in enumerate(sources, start=1)
        )
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "temperature": 0.1,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Question:\n{question}\n\nRetrieved sources:\n{context}",
                    },
                ],
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

