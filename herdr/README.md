# Herdr workspace layer

Herdr owns the persistent terminal/session layer around RedOps and OpenCode. It is the
place where operators keep one workspace per engagement and monitor long-running agents.
RedOps does not reimplement Herdr; it supplies the agent prompts, handoff contract and
status information that run inside those sessions.

Recommended layout:

```text
Herdr workspace
└── RedOps checkout
    └── engagements/<engagement-name>/
        ├── notes.md
        ├── recon/
        ├── evidence/
        ├── static/
        └── report/
```

Keep live sessions, terminal logs, credentials, VPN material and loot outside Git.
See <https://herdr.dev/> for the Herdr runtime and connection setup.
