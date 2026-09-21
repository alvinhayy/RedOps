from pathlib import Path

from redops_rag.config import Settings
from redops_rag.service import RagService


def settings(tmp_path: Path) -> Settings:
    return Settings(
        db_path=tmp_path / "index.db",
        knowledge_dir=tmp_path / "knowledge",
        writeups_dir=tmp_path / "writeups",
        chunk_size=300,
        chunk_overlap=20,
    )


def test_ingest_and_retrieve_with_provenance(tmp_path: Path) -> None:
    config = settings(tmp_path)
    config.knowledge_dir.mkdir()
    (config.knowledge_dir / "ldap.md").write_text(
        """---
title: LDAP Enumeration
source_url: https://docs.example.test/ldap
---
# LDAP Enumeration

Use ldapsearch to query the directory root DSE and inspect naming contexts.
""",
        encoding="utf-8",
    )

    service = RagService(config)
    report = service.ingest()
    result = service.query("ldapsearch naming contexts")

    assert report["indexed"] == 1
    assert result["sources"][0]["title"] == "LDAP Enumeration"
    assert result["sources"][0]["source_url"] == "https://docs.example.test/ldap"
    assert "[S1]" in result["answer"]


def test_ingest_is_idempotent(tmp_path: Path) -> None:
    config = settings(tmp_path)
    config.knowledge_dir.mkdir()
    (config.knowledge_dir / "one.md").write_text("# One\n\nKerberos ticket.", encoding="utf-8")
    service = RagService(config)

    assert service.ingest()["indexed"] == 1
    second = service.ingest()
    assert second["indexed"] == 0
    assert second["skipped"] == 1
    assert service.store.stats()["documents"] == 1


def test_stale_document_is_removed(tmp_path: Path) -> None:
    config = settings(tmp_path)
    config.knowledge_dir.mkdir()
    document = config.knowledge_dir / "old.md"
    document.write_text("# Old\n\nLegacy content.", encoding="utf-8")
    service = RagService(config)
    service.ingest()
    document.unlink()

    report = service.ingest()
    assert report["removed"] == 1
    assert service.store.stats()["documents"] == 0


def test_document_that_becomes_empty_is_removed(tmp_path: Path) -> None:
    config = settings(tmp_path)
    config.knowledge_dir.mkdir()
    document = config.knowledge_dir / "old.md"
    document.write_text("# Old\n\nLegacy content.", encoding="utf-8")
    service = RagService(config)
    service.ingest()
    document.write_text("", encoding="utf-8")

    report = service.ingest()
    assert report["empty"] == 1
    assert report["removed"] == 1
    assert service.store.stats()["documents"] == 0


def test_query_with_fts_syntax_characters_is_safe(tmp_path: Path) -> None:
    config = settings(tmp_path)
    config.knowledge_dir.mkdir()
    (config.knowledge_dir / "cve.md").write_text(
        "# CVE Notes\n\nCheck the affected version first.", encoding="utf-8"
    )
    service = RagService(config)
    service.ingest()

    result = service.query('CVE-2026:* OR "quoted"?', generate=False)
    assert result["answer"] is None
    assert len(result["sources"]) == 1


def test_identical_documents_do_not_collide(tmp_path: Path) -> None:
    config = settings(tmp_path)
    config.knowledge_dir.mkdir()
    content = "# Shared\n\nThe same reusable guidance."
    (config.knowledge_dir / "a.md").write_text(content, encoding="utf-8")
    (config.knowledge_dir / "b.md").write_text(content, encoding="utf-8")
    service = RagService(config)

    report = service.ingest()
    assert report["indexed"] == 2
    assert service.store.stats()["documents"] == 2


def test_knowledge_and_writeups_are_separate_corpora(tmp_path: Path) -> None:
    config = settings(tmp_path)
    config.knowledge_dir.mkdir()
    config.writeups_dir.mkdir()
    (config.knowledge_dir / "method.md").write_text(
        "# Method\n\nLDAP enumeration methodology.", encoding="utf-8"
    )
    (config.writeups_dir / "case.md").write_text(
        "# Case\n\nA solved LDAP enumeration writeup.", encoding="utf-8"
    )
    service = RagService(config)

    report = service.ingest()
    assert report["indexed"] == 2
    assert service.query("LDAP enumeration", generate=False, corpus="knowledge")["sources"][0]["corpus"] == "knowledge"
    assert service.query("LDAP enumeration", generate=False, corpus="writeups")["sources"][0]["corpus"] == "writeups"
    assert service.store.stats()["documents_by_corpus"] == {"knowledge": 1, "writeups": 1}
