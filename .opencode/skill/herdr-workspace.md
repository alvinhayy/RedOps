---
name: herdr-workspace
description: Use Herdr as the persistent terminal and session layer around RedOps.
---

Keep one Herdr workspace/session per authorized engagement. The primary RedOps agent
runs in the operator's `opencode` tab; specialists run in separate `ai-*` tabs.
Discover the workspace when needed, then create a tab and start an OpenCode agent with
the matching role prompt. Use durable files under `engagements/<name>/` as the source
of truth rather than terminal scrollback.

The expected handoff pattern is:

```text
herdr workspace list
herdr tab create --workspace <id> --cwd /workspace/engagements/<name> --label ai-<role> --no-focus
herdr agent start <role>-<engagement> --kind opencode --pane <pane-id> -- --agent <role>
herdr agent prompt <role>-<engagement> "<scoped task>" --wait
```

If a prompt stalls while the TUI renders, wait for the agent to become idle and retry
once. Collect results from `notes.md`; `agent read` is only a liveness check.

Herdr is an execution/session convenience, not an authorization boundary. Exegol and
the RedOps phase gates remain authoritative for target actions.
