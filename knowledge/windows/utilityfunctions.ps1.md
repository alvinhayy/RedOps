---
title: "UtilityFunctions.ps1"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Scripts/UtilityFunctions/
fetched_at: 2026-09-20T17:16:40Z
license: unspecified
category: windows
---

PowerShell Diagnostic Script

## Paths
- C:\Windows\diagnostics\system\Networking\UtilityFunctions.ps1

## Resources
- [https://twitter.com/nickvangilder/status/1441003666274668546](https://twitter.com/nickvangilder/status/1441003666274668546)

## Acknowledgements
- Nick VanGilder ([@nickvangilder](https://twitter.com/@nickvangilder))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/0.21-688-gd172b136b/rules/windows/process_creation/proc_creation_win_lolbas_utilityfunctions.yml](https://github.com/SigmaHQ/sigma/blob/0.21-688-gd172b136b/rules/windows/process_creation/proc_creation_win_lolbas_utilityfunctions.yml)

## Execute

1. Proxy execute Managed DLL with PowerShell

```
powershell.exe -ep bypass -command "set-location -path c:\windows\diagnostics\system\networking; import-module .\UtilityFunctions.ps1; RegSnapin ..\..\..\..\temp\unsigned.dll;[Program.Class]::Main()"
```

   - Use case: Execute proxied payload with Microsoft signed binary

   - Privileges required: User

   - Operating systems: Windows 10 21H1 (likely other versions as well), Windows 11

   - ATT&CK® technique: T1216

   - Tags: Execute: DLL (.NET)
