from redops_rag.chunking import chunk_markdown


def test_chunking_preserves_fenced_code() -> None:
    markdown = """# LDAP

Use the following command:

```bash
ldapsearch -x -H ldap://target
```

## Notes

Validate authorization first.
"""
    chunks = chunk_markdown(markdown, max_chars=300, overlap=20)
    combined = "\n".join(chunk.content for chunk in chunks)
    assert "ldapsearch -x" in combined
    assert "```bash" in combined
    assert chunks[0].token_count > 0


def test_chunking_rejects_invalid_overlap() -> None:
    try:
        chunk_markdown("hello", max_chars=200, overlap=200)
    except ValueError as exc:
        assert "overlap" in str(exc)
    else:
        raise AssertionError("expected ValueError")

