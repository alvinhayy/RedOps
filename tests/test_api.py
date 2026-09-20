from fastapi.testclient import TestClient

from redops_rag.api import app


def test_health_and_query_endpoints(tmp_path, monkeypatch) -> None:
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "smb.md").write_text(
        """---
title: SMB Basics
source_url: https://docs.example.test/smb
---
# SMB Basics

Enumerate dialects and signing requirements before authenticated testing.
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("REDOPS_DB_PATH", str(tmp_path / "api.db"))
    monkeypatch.setenv("REDOPS_KNOWLEDGE_DIR", str(knowledge))
    client = TestClient(app)

    ingest = client.post("/v1/ingest", json={})
    health = client.get("/health")
    query = client.post(
        "/v1/query", json={"question": "SMB signing", "top_k": 3, "generate": False}
    )

    assert ingest.status_code == 200
    assert health.json()["documents"] == 1
    assert query.status_code == 200
    assert query.json()["sources"][0]["title"] == "SMB Basics"
