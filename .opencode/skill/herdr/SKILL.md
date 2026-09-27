---
name: herdr
description: Operate persistent Herdr workspaces and OpenCode agent sessions.
---

Herdr is the workspace/session layer around the primary OpenCode agent. Keep the
operator's `opencode` tab untouched and create uniquely named `ai-<role>` tabs for
specialists. One authorized engagement gets one durable workspace and one
`engagements/<name>/notes.md` ledger.

Use Herdr's workspace, tab, agent, and read-only inspection commands to manage sessions.
Terminal scrollback is not durable evidence; agents must append findings, commands,
and output references to the ledger. Idle or disconnected does not mean completed.

Herdr does not grant authorization. Exegol health, written scope, and RedOps phase
gates remain mandatory before any target action.
