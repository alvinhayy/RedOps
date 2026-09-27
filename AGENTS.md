# RedOps workspace contract

RedOps is the OpenCode orchestrator inside Exegol (tools) → Herdr (sessions) → OpenCode (AI harness).

Read `knowledgebase/INDEX.md` first. The canonical Markdown corpus is `knowledgebase/niches/`, organized by topic; retain and cite each document's source URL. The optional `knowledgebase/niches/api/` is user-supplied and excluded from Git.

For each target, create `engagements/<name>/notes.md` with scope, exclusions, phase approvals, commands, evidence, findings, and cleanup. Keep credentials, loot, VPN files, and raw exports out of Git. Confirm written authorization and exact target allowlists before active work. Gate exploitation, post-exploitation, lateral movement, and persistence separately.

The RedOps primary agent coordinates specialists in separate Herdr/OpenCode sessions. Give each worker only its scoped task, mapped knowledge niches and relevant evidence. `.opencode/tools.json` is the role wiring contract: knowledge, local binary access, tool requirements, MCP assignments and the engagement ledger convention. Check `precompiled-binaries/MANIFEST.json` and SHA-256 before using any local artifact; the manifest currently lists none. An MCP may be configured but disconnected; confirm its runtime health. Exegol is the preferred tool environment. Never claim a command ran without its output or invent findings.

Each `.opencode/agent/*.md` prompt has a `Knowledge route` section. Follow it before reading a niche: select only files relevant to the observed target, cite the Markdown path/heading/`source_url`, and keep literature claims separate from command output. The `redops` primary prompt owns cross-role routing and approval gates.
