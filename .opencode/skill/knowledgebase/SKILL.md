---
name: knowledgebase
description: Navigate the source-grounded RedOps knowledge and writeup references.
---

Resolve the repository root first (a Herdr worker may start below
`engagements/`). Read `knowledgebase/INDEX.md` and the current role's `knowledge` list in
`.opencode/tools.json`, then open only relevant files under those mapped niches.
Search the selected niche when the index is insufficient. Other niches require a
reasoned handoff from RedOps, not bulk traversal.
Keep source URLs, document paths, headings, and evidence references in handoffs.
Prefer the narrowest niche matching the observed service or artifact, and label
uncertainty.

`knowledgebase/niches/api/` is an optional user-added collection. Read it only when
the operator explicitly opts in for that engagement. Never put credentials, tokens, cookies, raw
identity exports, or target loot in the knowledge tree.
