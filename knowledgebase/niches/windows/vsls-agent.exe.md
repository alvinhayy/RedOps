---
title: "vsls-agent.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/vsls-agent/
fetched_at: 2026-09-20T17:16:01Z
license: unspecified
category: windows
---

Agent for Visual Studio Live Share (Code Collaboration)

## Paths
- c:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\IDE\Extensions\Microsoft\LiveShare\Agent\vsls-agent.exe

## Resources
- [https://twitter.com/bohops/status/1583916360404729857](https://twitter.com/bohops/status/1583916360404729857)

## Acknowledgements
- Jimmy ([@bohops](https://twitter.com/@bohops))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_vslsagent_agentextensionpath_load.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_vslsagent_agentextensionpath_load.yml)

## Execute

1. Load a library payload using the –agentExtensionPath parameter (32-bit)

```
vsls-agent.exe --agentExtensionPath {PATH_ABSOLUTE:.dll}
```

   - Use case: Execute proxied payload with Microsoft signed binary

   - Privileges required: User

   - Operating systems: Windows 10 21H2 (likely previous and newer versions with modern versions of Visual Studio installed)

   - ATT&CK® technique: T1218

   - Tags: Execute: DLL
