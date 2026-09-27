# RedOps layered architecture

RedOps follows the runtime separation used by the Makima reference design, while
keeping RedOps' source-grounded retrieval and phase gates authoritative.

```text
Exegol - Pentest Environment
│   pentest tools · precompiled binaries · runtime knowledge
│
└── Herdr - Workspace / Sessions
    │   persistent terminals · resumable sessions · shared engagement workspace
    │
    └── OpenCode - AI Harness
        │   agent prompts · slash commands · provider/model selection
        │
        └── RedOps - Orchestrator ──► authorized target
            │   plan · retrieve · route · spawn · verify · hand off
            │
            ├── recon
            ├── web-recon
            ├── web-exploit
            ├── cve-research
            ├── ad-enum
            ├── ad-exploit
            ├── linux-privesc
            ├── windows-privesc
            └── persistence
```

## Layer responsibilities

| Layer | RedOps responsibility | Boundary |
|---|---|---|
| Exegol | Tool/runtime boundary for approved commands and precompiled binaries | No command is implied by a plan; health must be verified first |
| Herdr | Long-lived terminals, workspaces and resumable sessions | Session state belongs under the private engagement workspace |
| OpenCode | Model/provider harness and agent process lifecycle | Provider credentials stay in environment/configuration, never in prompts or corpus |
| RedOps | Phase planning, RAG provenance, routing, handoffs and safety gates | The orchestrator does not directly probe or exploit targets |
| Specialist agents | Narrow technical work and evidence collection | Each agent receives only its scoped artifacts and allowed connectors |

Herdr is designed as a persistent runtime for coding-agent terminals: agents can keep
working when the operator disconnects, and the workspace can be viewed from another
machine. RedOps treats that persistence as an operational layer, not as authorization.
See [herdr.dev](https://herdr.dev/) for installation and session management.

## Repository layout

```text
.
├── .opencode/                 # OpenCode-native agent prompts and slash commands
├── agents/                    # canonical RedOps registry, phase graph and tool matrix
├── engagements/               # private per-target ledgers and sanitized templates
├── herdr/                     # workspace/session conventions (runtime state stays private)
├── knowledge/                 # canonical niche-organized RAG corpus
│   └── api/                   # book-derived corpus; excluded from Git and indexing
├── knowledgebase/             # corpus contract and generated index documentation
├── precompiled-binaries/      # manifest only; binaries are supplied by Exegol
├── skills/                    # reusable RedOps skills and slash-command sources
└── src/redops_rag/            # CLI, RAG, workflow, router and MCP adapters
```

The existing `agents/` registry remains the machine-readable source of truth for
tool/MCP wiring. `.opencode/agent/` contains the OpenCode-facing role prompts and maps
to those profiles; this avoids duplicating tool permissions in two independent policy
files.

| OpenCode role | RedOps policy profile |
|---|---|
| `recon` | `recon_agent` |
| `web-recon`, `web-exploit` | `web_agent` plus phase gate |
| `cve-research` | `assessment_agent` |
| `ad-enum`, `ad-exploit` | `ad_agent` plus phase gate |
| `linux-privesc` | `exploitation_agent` plus Linux niche |
| `windows-privesc` | `windows_redteam_agent` |
| `persistence` | `post_exploitation_agent` plus explicit persistence approval |

## Engagement flow

```text
scope → recon → assessment → approved exploit validation
  ↘          ↘              ↘
   writeups   niche agents   PoC/report/cleanup
```

`redops-rag` is an optional read-only retrieval/plan MCP; local OpenCode references can
be used when it is not configured. Exegol is the execution boundary, but all active
phases remain blocked until the scope and per-phase approval gates are satisfied. The
standalone RedOps CLI is a maintenance/offline fallback, not a prerequisite for an
OpenCode/Herdr engagement.

## Reference design

The layered runtime model is adapted from the private Makima repository's architecture
(Exegol → Herdr → OpenCode → orchestrator → specialist agents). RedOps intentionally
adds explicit provenance, non-destructive defaults, separate knowledge/writeup corpora,
and an API-book exclusion so a large imported book cannot silently dominate retrieval.
