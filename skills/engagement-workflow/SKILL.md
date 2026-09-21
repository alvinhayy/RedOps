---
name: engagement-workflow
description: Phase-gated authorized penetration-testing lifecycle for RedOps.
---

# RedOps engagement workflow

Use the RedOps phase graph for authorized assessments. Start with pre-engagement
scope and written authorization, then hand off evidence through information gathering,
vulnerability assessment, approved exploitation, post-exploitation impact validation,
lateral-movement validation, proof-of-concept packaging, and post-engagement reporting.

Call the `plan_engagement` tool from the `redops-rag` MCP or run:

```bash
redops workflow "<authorized task>"
```

Call `route_task` to select technical niche agents. Active phases remain blocked until
written scope, exact target allowlists, phase approval, and Exegol/runtime health are
confirmed. Every handoff includes evidence, source citations, scope, artifacts, and
open questions. Never include credentials or claim a command ran without output.
