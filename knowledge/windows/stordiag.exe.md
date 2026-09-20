---
title: "Stordiag.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Stordiag/
fetched_at: 2026-09-20T17:11:43Z
license: unspecified
category: windows
---

Storage diagnostic tool

## Paths
- c:\windows\system32\stordiag.exe
- c:\windows\syswow64\stordiag.exe

## Resources
- [https://twitter.com/eral4m/status/1451112385041911809](https://twitter.com/eral4m/status/1451112385041911809)

## Acknowledgements
- Eral4m ([@eral4m](https://twitter.com/@eral4m))
- Ekitji ([@eki_erk](https://twitter.com/@eki_erk))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_stordiag_susp_child_process.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_stordiag_susp_child_process.yml)
- IOC: systeminfo.exe, fltmc.exe or schtasks.exe or powershell.exe being executed outside of their normal path of c:\windows\system32\ or c:\windows\syswow64\

## Execute

1. Once executed, Stordiag.exe will execute schtasks.exe systeminfo.exe and fltmc.exe - if stordiag.exe is copied to a folder and an arbitrary executable is renamed to one of these names, stordiag.exe will execute it.

```
stordiag.exe
```

   - Use case: Possible defence evasion purposes.

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1218

   - Tags: Execute: EXE

2. Once executed, Stordiag.exe will execute schtasks.exe and powershell.exe - if stordiag.exe is copied to a folder and an arbitrary executable is renamed to one of these names, stordiag.exe will execute it.

```
stordiag.exe
```

   - Use case: Possible defence evasion purposes.

   - Privileges required: User

   - Operating systems: Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: EXE
