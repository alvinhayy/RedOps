---
title: "Pcalua.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Pcalua/
fetched_at: 2026-09-20T17:10:57Z
license: unspecified
category: windows
---

Program Compatibility Assistant

## Paths
- C:\Windows\System32\pcalua.exe

## Resources
- [https://twitter.com/KyleHanslovan/status/912659279806640128](https://twitter.com/KyleHanslovan/status/912659279806640128)

## Acknowledgements
- Kyle Hanslovan ([@kylehanslovan](https://twitter.com/@kylehanslovan))
- Fab ([@0rbz_](https://twitter.com/@0rbz_))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_pcalua.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_pcalua.yml)

## Execute

1. Open the target .EXE using the Program Compatibility Assistant.

```
pcalua.exe -a {PATH:.exe}
```

   - Use case: Proxy execution of binary

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: EXE

2. Open the target .DLL file with the Program Compatibilty Assistant.

```
pcalua.exe -a {PATH_SMB:.dll}
```

   - Use case: Proxy execution of remote dll file

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10

   - ATT&CK® technique: T1202

   - Tags: Execute: DLLExecute: Remote

3. Open the target .CPL file with the Program Compatibility Assistant.

```
pcalua.exe -a {PATH_ABSOLUTE:.cpl} -c Java
```

   - Use case: Execution of CPL files

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: DLL
