---
title: "Pester.bat"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Scripts/pester/
fetched_at: 2026-09-20T17:16:43Z
license: unspecified
category: windows
---

Used as part of the Powershell pester

## Paths
- c:\Program Files\WindowsPowerShell\Modules\Pester\<VERSION>\bin\Pester.bat

## Resources
- [https://twitter.com/Oddvarmoe/status/993383596244258816](https://twitter.com/Oddvarmoe/status/993383596244258816)
- [https://twitter.com/_st0pp3r_/status/1560072680887525378](https://twitter.com/_st0pp3r_/status/1560072680887525378)
- [https://twitter.com/_st0pp3r_/status/1560072680887525378](https://twitter.com/_st0pp3r_/status/1560072680887525378)

## Acknowledgements
- Emin Atac ([@p0w3rsh3ll](https://twitter.com/@p0w3rsh3ll))
- Stamatis Chatzimangou ([@_st0pp3r_](https://twitter.com/@_st0pp3r_))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_pester_1.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_pester_1.yml)

## Execute

1. Execute code using Pester. The third parameter can be anything. The fourth is the payload.

```
Pester.bat [/help|?|-?|/?] "$null; {CMD}"
```

   - Use case: Proxy execution

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1216

   - Tags: Execute: EXE

2. Execute code using Pester. Example here executes specified executable.

```
Pester.bat ;{PATH:.exe}
```

   - Use case: Proxy execution

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1216

   - Tags: Execute: EXE
