from __future__ import annotations

import re

from .models import Chunk

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
WORD_RE = re.compile(r"[\w./:@-]+", re.UNICODE)


def _blocks(markdown: str) -> list[tuple[str, str]]:
    """Split Markdown into heading-aware blocks without breaking fenced code."""
    result: list[tuple[str, str]] = []
    heading = "Document"
    buffer: list[str] = []
    in_fence = False

    def flush() -> None:
        nonlocal buffer
        text = "\n".join(buffer).strip()
        if text:
            result.append((heading, text))
        buffer = []

    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            buffer.append(line)
            continue
        match = HEADING_RE.match(line) if not in_fence else None
        if match:
            flush()
            heading = match.group(2).strip()
            buffer.append(line)
        elif not line.strip() and buffer and not in_fence:
            flush()
        else:
            buffer.append(line)
    flush()
    return result


def chunk_markdown(markdown: str, max_chars: int = 1400, overlap: int = 180) -> list[Chunk]:
    if max_chars < 200:
        raise ValueError("max_chars must be at least 200")
    if overlap < 0 or overlap >= max_chars:
        raise ValueError("overlap must be non-negative and smaller than max_chars")

    chunks: list[Chunk] = []
    current_heading = "Document"
    current = ""

    def emit(text: str, heading: str) -> None:
        cleaned = text.strip()
        if cleaned:
            chunks.append(
                Chunk(
                    index=len(chunks),
                    heading=heading,
                    content=cleaned,
                    token_count=len(WORD_RE.findall(cleaned)),
                )
            )

    for heading, block in _blocks(markdown):
        if len(block) > max_chars:
            if current:
                emit(current, current_heading)
                current = ""
            start = 0
            while start < len(block):
                end = min(start + max_chars, len(block))
                if end < len(block):
                    boundary = block.rfind("\n", start + max_chars // 2, end)
                    if boundary > start:
                        end = boundary
                emit(block[start:end], heading)
                if end >= len(block):
                    break
                start = max(end - overlap, start + 1)
            continue

        separator = "\n\n" if current else ""
        if current and len(current) + len(separator) + len(block) > max_chars:
            emit(current, current_heading)
            tail = current[-overlap:].lstrip() if overlap else ""
            current = f"{tail}\n\n{block}" if tail else block
            current_heading = heading
        else:
            if not current:
                current_heading = heading
            current = f"{current}{separator}{block}"
    emit(current, current_heading)
    return chunks
