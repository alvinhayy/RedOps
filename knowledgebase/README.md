# RedOps knowledge-base contract

The canonical source files live in [`../knowledge/`](../knowledge/), organized by niche
(`ad`, `cloud`, `linux`, `mobile`, `network`, `web`, `windows`, `web3`, and others).
`redops ingest` indexes Markdown from that tree and preserves source URL, path and
heading provenance.

The book-derived API corpus at [`../knowledge/api/`](../knowledge/api/) is deliberately
excluded by default via `REDOPS_KNOWLEDGE_EXCLUDE=api` and ignored by Git. Its files are
left intact for local archival use, but they must not enter the active RedOps index.

Do not place secrets, credentials, cookies, raw identity exports or engagement loot in
this tree. Use `writeups/` for sanitized case evidence and `engagements/` for private
session artifacts.
