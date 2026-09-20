---
title: "WinDbg.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/WinDbg/
fetched_at: 2026-09-20T17:15:47Z
license: unspecified
category: windows
---

Windows Debugger for advanced user-mode and kernel-mode debugging.

## Paths
- C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\windbg.exe
- C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\windbg.exe
- C:\Program Files (x86)\Windows Kits\10\Debuggers\arm\windbg.exe
- C:\Program Files (x86)\Windows Kits\10\Debuggers\arm64\windbg.exe

## Resources
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/windbg-command-line-options](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/windbg-command-line-options)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Execute

1. Launches a command line through the debugging process; optionally add -G to exit the debugger automatically.

```
windbg.exe -g {CMD}
```

   - Use case: Executes an executable under a trusted microsoft signed binary.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: CMD
