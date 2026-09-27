---
title: "Logger.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Logger/
fetched_at: 2026-09-20T17:14:54Z
license: unspecified
category: windows
---

A logging configuration tool from the Windows Kits used to start and manage process logging.

## Paths
- C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\logger.exe
- C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\logger.exe
- C:\Program Files\Windows Kits\10\Debuggers\x86\logger.exe
- C:\Program Files\Windows Kits\10\Debuggers\x64\logger.exe

## Resources
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/logger](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/logger)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Execute

1. Executes the command specified after the RUN parameter as a child of logger.exe.

```
logger.exe RUN "{CMD}"
```

   - Use case: Executes an abitrary command via a signed binary to evade detection.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD

2. Executes the command specified after the RUNW parameter as a child of logger.exe.

```
logger.exe RUNW "{CMD}"
```

   - Use case: Executes an abitrary command via a signed binary to evade detection.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD

3. Executes the command specified as a child of logger.exe.

```
logger.exe "{CMD}"
```

   - Use case: Executes an abitrary command via a signed binary to evade detection.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD
