# RedOps Knowledgebase Index

Reference map for the OpenCode agents. The active RedOps corpus remains in
`../knowledge/`, organized by pentest niche (`ad`, `web`, `linux`, `windows`,
`mobile`, `cloud`, `network`, `web3`, and others). `redops ingest` indexes that
niche tree; this file is only the quick navigation layer used by agents.

## Reference namespaces

- `PayloadsAllTheThings/` — web/API payload and exploitation reference map.
- `InternalAllTheThings/` — Active Directory, Windows/Linux privilege escalation,
  persistence, pivoting, and internal-network reference map.
- `HackerRecipes/` — theory, methodology, and service walkthrough reference map.

Each namespace README points to the corresponding niche paths and source URLs. Do
not duplicate the corpus here. The optional user-added `../knowledge/api/` archive
is excluded from the active index by default.

## Specialist routing

| Task | Active niche paths |
|---|---|
| Web/API | `../knowledge/web`, `../knowledge/vulnerabilities` |
| AD/Windows | `../knowledge/ad`, `../knowledge/windows`, `../knowledge/redteam` |
| Linux | `../knowledge/linux`, `../knowledge/container` |
| Mobile/reversing | `../knowledge/mobile`, `../knowledge/reversing` |
| Cloud/DevOps | `../knowledge/cloud`, `../knowledge/devops`, `../knowledge/container` |
| Network/pivoting | `../knowledge/network`, `../knowledge/wireless` |
| Web3 | `../knowledge/web3`, `../knowledge/reversing` |

Refresh the active index after source changes:

```text
redops ingest → data/redops.db → RAG/OpenCode retrieval
```
