# RedOps agent contract

RedOps is the orchestrator inside a layered authorized-testing workspace:

```text
Exegol (tools, binaries, knowledge runtime)
└── Herdr (persistent workspace and sessions)
    └── OpenCode (AI harness)
        └── RedOps (planning, routing, evidence and handoffs)
            └── scoped specialist agents
```

The orchestrator plans and delegates. It does not execute target commands itself.
Every task starts in the native OpenCode/Herdr workflow; the RedOps CLI is an optional
maintenance and offline-RAG tool, not a prerequisite. Active phases remain blocked until
written scope, exact target allowlists, phase approval, and Exegol/runtime health are
present.

## Shared workspace

- `engagements/<name>/` is the private session workspace for one authorized target.
- `notes.md` is the single handoff ledger; agents append under their own heading.
- Keep loot, credentials, tokens, cookies, hashes, raw identity exports, and VPN data
  outside the repository and outside `knowledge/`.
- `knowledge/` is the source-grounded technique corpus; `writeups/` is the case corpus.
- `knowledge/api/` contains book-derived API material and is intentionally excluded from
  the RedOps index and Git. Do not re-enable it without an explicit operator decision.

## Agent lifecycle

1. Confirm authorization, target allowlist, exclusions, timing and success criteria.
2. Retrieve source-grounded context and route the task to the narrowest specialists.
3. Run reconnaissance and assessment only inside the allowlist, preserving output and
   citations in the session ledger.
4. Gate exploitation, post-exploitation, lateral movement and persistence separately.
5. Produce a minimal reproducible PoC and a sanitized report with cleanup evidence.

The RedOps orchestrator must never claim a command ran without its command output. Use
Exegol first, then an explicitly approved MCP, then the bounded terminal connector.
