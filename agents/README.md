# RedOps agent profiles

This directory defines routing profiles for the RedOps knowledge base. Profiles are
organized by the technical niche of the corpus, not by source website. The canonical
machine-readable registry is [`registry.yaml`](registry.yaml).
Tool availability, required/optional status, source, and health checks are in
[`tools.md`](tools.md).

## Routing model

Every profile requires written authorization and an explicitly scoped engagement. The
normal execution order is Exegol, then an approved specialist MCP, then the bounded
terminal connector. Retrieval can still run without an execution connector; lack of a
connector must never be treated as permission to use an unrestricted host shell.

All reports should retain the document path, source URL, relevant heading, target hash or
request identifier, and a clear distinction between observed evidence and a hypothesis.
Secrets, credentials, cookies, tokens, private keys, and raw identity exports belong in
the private engagement workspace—not in `knowledge/` or agent configuration.

## Profiles and real corpus mapping

| Agent | Primary knowledge niches | Specialist connectors |
|---|---|---|
| `ad_agent` | `ad/`, `windows/`, `database/`, `methodology/`, `tools/` | Exegol, BloodHound, bounded terminal |
| `windows_redteam_agent` | `windows/`, `redteam/`, `tools/`, `vulnerabilities/`, `ad/` | Exegol, bounded terminal |
| `web_agent` | `web/`, `vulnerabilities/`, `network/`, `methodology/` | Exegol, Burp, Camoufox |
| `cloud_agent` | `cloud/`, `ad/`, `container/`, `devops/`, `network/` | Exegol, bounded terminal |
| `mobile_agent` | `mobile/android/`, `mobile/ios/`, `mobile/flutter/`, `mobile/react-native/`, `reversing/` | Exegol, Burp, uiautomator2, Ghidra, radare2 |
| `reversing_tools_agent` | `reversing/`, `malware/`, `tools/`, `windows/`, `linux/`, `mobile/` | Exegol, Ghidra, radare2 |
| `network_agent` | `network/`, `wireless/`, `linux/`, `windows/`, `web/` | Exegol, bounded terminal |
| `container_devops_agent` | `container/`, `devops/`, `cloud/`, `linux/`, `vulnerabilities/` | Exegol, bounded terminal |
| `web3_agent` | `web3/`, `web/`, `vulnerabilities/`, `reversing/`, `network/` | Exegol, Burp, Ghidra, radare2 |
| `rag_curator_agent` | all direct `knowledge/*` niches | bounded terminal only |

The mapping reflects the current repository layout: categories are direct children of
`knowledge/`, with mobile-specific subdirectories. `misc/` is intentionally not a
primary offensive routing target; it is a fallback for material that cannot yet be
classified. `database/`, `methodology/`, `tools/`, and `vulnerabilities/` are shared
cross-cutting niches.

## Important connector boundary

BloodHound is exclusive to `ad_agent`. It is not a mobile connector and must not be
used by `mobile_agent`, even when an Android or iOS engagement involves an enterprise
identity provider. Mobile identity observations are handled as application/API findings
and routed through the web/mobile profiles; AD graph analysis is a separate authorized
scope.

The mobile profile is limited to Android/iOS artifacts and disposable authorized devices.
Static analysis must not launch target apps. Ghidra and radare2 receive local authorized
files, while Burp and Camoufox may handle only explicitly scoped traffic and flows.

## Output contract

Agents should produce Markdown for human review and JSON for automation. A finding must
include: `title`, `niche`, `target_scope`, `authorization_basis`, `evidence`,
`reproduction_status`, `impact`, `severity`, `remediation`, and `sources`. Curator
outputs additionally include manifest/provenance and index QA results.

Tool requirements: [`tools.md`](tools.md). Machine-readable MCP profiles:
[`mcp-profiles.yaml`](mcp-profiles.yaml).

Individual profiles: [AD](ad.md), [Windows/red team](windows-redteam.md),
[Web](web.md), [Cloud](cloud.md), [Mobile](mobile.md), [Reversing](reversing-tools.md),
[Network](network.md), [Container/DevOps](container-devops.md), [Web3](web3.md),
and [RAG curator](rag-curator.md).

Skill-to-tool/MCP audit: [`skill-tool-matrix.yaml`](skill-tool-matrix.yaml) and
[`docs/skill-tool-wiring.md`](../docs/skill-tool-wiring.md).
