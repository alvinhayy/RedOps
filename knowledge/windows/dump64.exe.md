---
title: "Dump64.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Dump64/
fetched_at: 2026-09-20T17:14:43Z
license: unspecified
category: windows
---

Memory dump tool that comes with Microsoft Visual Studio

## Paths
- C:\Program Files (x86)\Microsoft Visual Studio\Installer\Feedback\dump64.exe

## Resources
- [https://twitter.com/mrd0x/status/1460597833917251595](https://twitter.com/mrd0x/status/1460597833917251595)

## Acknowledgements
- mr.d0x ([@mrd0x](https://twitter.com/@mrd0x))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_dump64.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_dump64.yml)
- IOC: As a Windows SDK binary, execution on a system may be suspicious

## Dump

1. Creates a memory dump of the LSASS process.

```
dump64.exe {PID} out.dmp
```

   - Use case: Create memory dump and parse it offline to retrieve credentials.

   - Privileges required: Administrator

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1003.001
