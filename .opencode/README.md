# OpenCode layer

OpenCode is the AI harness in the RedOps runtime stack. The primary `redops` agent
spawns and coordinates specialist OpenCode agents through Herdr, following the same
model as Makima. The operator can talk to the primary agent or use `/solve`; no RedOps
CLI command is required to run an engagement.

```text
.opencode/
├── opencode.json # default agent, references, and skill paths
├── agent/       # redops + narrow specialist prompts
├── command/     # /solve and /status
└── skill/       # harness-specific operating conventions
```

Start the primary `redops` agent from the RedOps checkout inside a Herdr session. Configure
the provider/model and optional MCP endpoints in the user's OpenCode configuration; do
not commit API keys here. The RAG MCP is optional when local references are available;
if enabled, register it through the provider's own MCP configuration rather than making
the engagement depend on a shell command.
