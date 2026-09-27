---
name: shell
description: Handle authorized shells and evidence without leaking secrets.
---

Use only shells obtained inside the target allowlist and approved Exegol session. Keep
commands bounded and reversible, preserve stdout/stderr in the engagement ledger, and
redact credentials before sharing them with other agents. Shell access is evidence of a
phase result, not permission to expand scope or establish persistence.
