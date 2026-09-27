# Precompiled binaries

This directory intentionally contains only documentation and
[`MANIFEST.json`](MANIFEST.json). Its `artifacts` list is empty: no local binary is
currently installed or implied by an agent profile. Pentest binaries and Windows/AD
tools should normally come from the configured Exegol image.

If the operator adds a local binary, record its relative path, platform, version,
provenance and SHA-256 in `MANIFEST.json` before use. Agents must verify the digest
and engagement approval. Never treat a manifest entry as permission to execute.

Do not commit executables, credentials, raw payloads, or target-specific loot here.
