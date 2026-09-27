---
name: knowledgebase
description: Navigate the source-grounded RedOps knowledge and writeup references.
---

Use local niche directories and the read-only RAG MCP to ground recommendations. Keep
source URLs, document paths, headings, and evidence references in handoffs. Prefer the
narrowest niche matching the observed service or artifact, and label uncertainty.

`knowledge/api/` is an optional user-added corpus. It is excluded from the active index
by default; do not traverse or cite it unless the operator explicitly enables it with
the knowledge-exclude setting. Never put credentials, tokens, cookies, raw identity
exports, or target loot in the knowledge tree.
