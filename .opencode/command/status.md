---
description: Show RedOps, RAG, Exegol and specialist-session readiness.
---

Use the native OpenCode references and Herdr read-only session inspection to report:

- active Herdr workspace and `ai-*` specialist tabs;
- whether the Exegol workspace/session is reachable;
- knowledge/reference and RAG MCP availability;
- missing tools or MCP capabilities from `agents/registry.yaml`.

Do not start scans, mutate a target, expose credentials, or infer authorization from a
healthy runtime. A RedOps CLI status command is optional maintenance, not a prerequisite
for this command.
