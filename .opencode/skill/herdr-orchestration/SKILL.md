---
name: herdr-orchestration
description: Spawn and coordinate scoped OpenCode specialists in Herdr.
---

The primary `redops` agent coordinates specialists; it does not run target commands.
Use this sequence for each worker:

1. Discover or reuse the engagement workspace.
2. Create an `ai-<role>` tab with the engagement directory as its working directory.
3. Start the matching OpenCode agent with `--agent <role>` and a unique name.
4. Read the role's `.opencode/tools.json` profile and prompt it with only the target
   allowlist, phase approval, relevant knowledge paths, allowed MCPs, binary manifest
   policy, exact `engagements/<name>/notes.md` path, evidence, and deliverable.
5. Wait for idle, then read the durable ledger and route the next phase.

Retry a prompt once after a transient TUI stall. Keep recon and independent research
parallel, but serialize exploit, post-exploit, lateral movement, and persistence behind
their explicit approval gates. Never close or split the operator's primary tab.
