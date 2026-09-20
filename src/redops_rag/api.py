from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .service import RagService

app = FastAPI(
    title="RedOps RAG",
    version="0.1.0",
    description="Source-grounded retrieval for authorized pentesting knowledge.",
)


class QueryRequest(BaseModel):
    question: str = Field(min_length=2, max_length=4000)
    top_k: int = Field(default=6, ge=1, le=20)
    generate: bool = True


class IngestRequest(BaseModel):
    force: bool = False


def get_service() -> RagService:
    return RagService()


@app.get("/health")
def health() -> dict:
    service = get_service()
    return {"status": "ok", **service.store.stats()}


@app.post("/v1/ingest")
def ingest(request: IngestRequest) -> dict:
    try:
        return get_service().ingest(force=request.force)
    except (ValueError, RuntimeError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/query")
def query(request: QueryRequest) -> dict:
    try:
        return get_service().query(request.question, request.top_k, request.generate)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

