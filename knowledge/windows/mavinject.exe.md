---
title: "Mavinject.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Mavinject/
fetched_at: 2026-09-20T17:10:34Z
license: unspecified
category: windows
---

Used by App-v in Windows

## Paths
- C:\Windows\System32\mavinject.exe
- C:\Windows\SysWOW64\mavinject.exe

## Resources
- [https://twitter.com/gN3mes1s/status/941315826107510784](https://twitter.com/gN3mes1s/status/941315826107510784)
- [https://twitter.com/Hexcorn/status/776122138063409152](https://twitter.com/Hexcorn/status/776122138063409152)
- [https://oddvar.moe/2018/01/14/putting-data-in-alternate-data-streams-and-how-to-execute-it/](https://oddvar.moe/2018/01/14/putting-data-in-alternate-data-streams-and-how-to-execute-it/)

## Acknowledgements
- Giuseppe N3mes1s ([@gN3mes1s](https://twitter.com/@gN3mes1s))
- Oddvar Moe ([@oddvarmoe](https://twitter.com/@oddvarmoe))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_mavinject_process_injection.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_mavinject_process_injection.yml)
- IOC: mavinject.exe should not run unless APP-v is in use on the workstation

## Execute

1. Inject evil.dll into a process with PID 3110.

```
MavInject.exe 3110 /INJECTRUNNING {PATH_ABSOLUTE:.dll}
```

   - Use case: Inject dll file into running process

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.013

   - Tags: Execute: DLL

2. Inject file.dll stored as an Alternate Data Stream (ADS) into a process with PID 4172

```
Mavinject.exe 4172 /INJECTRUNNING {PATH_ABSOLUTE}:file.dll
```

   - Use case: Inject dll file into running process

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

   - Tags: Execute: DLL
