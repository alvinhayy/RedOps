# Knowledgebase index

The canonical Markdown corpus is [`niches/`](niches/). Pick a niche first and open relevant files. Each document retains its original `source_url`. Source-family directories are maps, not duplicate copies.

| Task | Niche directory |
|---|---|
| Active Directory | [`niches/ad/`](niches/ad/) |
| Windows privilege escalation | [`niches/windows/`](niches/windows/) |
| Linux server | [`niches/linux/`](niches/linux/) |
| Web and API | [`niches/web/`](niches/web/), [`niches/vulnerabilities/`](niches/vulnerabilities/) |
| Mobile | [`niches/mobile/`](niches/mobile/) |
| Reversing | [`niches/reversing/`](niches/reversing/) |
| Cloud / containers | [`niches/cloud/`](niches/cloud/), [`niches/container/`](niches/container/) |
| Network / pivoting | [`niches/network/`](niches/network/) |
| Web3 | [`niches/web3/`](niches/web3/) |
| Red-team methodology | [`niches/redteam/`](niches/redteam/) |

Source-family maps: [`PayloadsAllTheThings/`](PayloadsAllTheThings/), [`InternalAllTheThings/`](InternalAllTheThings/), and [`HackerRecipes/`](HackerRecipes/). These point into the niche corpus and do not determine storage category.

`niches/api/` is optional user-provided book material excluded from Git. Opt it into an engagement explicitly.

## Agent routes

The authoritative routing profile is [`.opencode/tools.json`](../.opencode/tools.json).
OpenCode agent prompts specify when each niche applies and how to hand off evidence.
These are **role lanes**, not one agent per niche:

| Agent | Default niches |
|---|---|
| `recon` | network, wireless, cloud, container, devops, methodology |
| `web-recon` | web, network, database; API book only by opt-in |
| `web-exploit` | web, vulnerabilities, database; API book only by opt-in |
| `cve-research` | vulnerabilities, malware, reversing, tools, misc, mobile, web3 (research only) |
| `ad-enum` | ad, windows, network |
| `ad-exploit` | ad, windows, redteam |
| `linux-privesc` | linux, container, devops, misc |
| `windows-privesc` | windows, ad, redteam, misc |
| `persistence` | redteam, windows, linux, cloud, methodology (separate approval) |

The `redops` primary agent reads this index, assigns the narrowest role and
passes only relevant source paths plus observed target evidence. There is no
separate `knowledge/` tree; `knowledgebase/niches/` is canonical.
