# RedOps workspace contract

RedOps is the OpenCode orchestrator inside Exegol (tools) → Herdr (sessions) → OpenCode (AI harness).

Read `knowledgebase/INDEX.md` first. The canonical Markdown corpus is `knowledgebase/niches/`, organized by topic; retain and cite each document's source URL. The optional `knowledgebase/niches/api/` is user-supplied and excluded from Git.

For each target, create `engagements/<name>/notes.md` with scope, exclusions, phase approvals, commands, evidence, findings, and cleanup. Keep credentials, loot, VPN files, and raw exports out of Git. Confirm written authorization and exact target allowlists before active work. Gate exploitation, post-exploitation, lateral movement, and persistence separately.

The RedOps primary agent coordinates specialists in separate Herdr/OpenCode sessions. Give each worker only its scoped task and relevant evidence. Exegol is the preferred tool environment. Use `.opencode/tools.json` for role-specific tool/MCP requirements. Never claim a command ran without its output or invent findings.
