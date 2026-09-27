# Knowledge niche index

Use `redops stats` for the current indexed counts. The active corpus is the direct
`knowledge/` tree; this index is a stable map for agents and OpenCode prompts.

| Niche | Typical specialist |
|---|---|
| `ad` | `ad-enum`, `ad-exploit` |
| `cloud` | cloud profile |
| `container`, `devops` | container/DevOps profile |
| `linux` | `linux-privesc` |
| `mobile` | mobile profile |
| `network`, `wireless` | `recon` |
| `reversing`, `malware` | reversing profile |
| `vulnerabilities`, `redteam`, `tools` | assessment and exploit phases |
| `web` | `web-recon`, `web-exploit` |
| `web3` | Web3 profile |
| `windows` | `windows-privesc` |
| `api` | excluded book corpus; never indexed by default |

Refresh the index after source changes:

```bash
redops ingest
redops stats
```
