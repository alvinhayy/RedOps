---
title: "Vshadow.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Vshadow/
fetched_at: 2026-09-20T17:15:42Z
license: unspecified
category: windows
---

VShadow is a command-line tool that can be used to create and manage volume shadow copies.

## Paths
- C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\vshadow.exe

## Resources
- [https://learn.microsoft.com/en-us/windows/win32/vss/vshadow-tool-and-sample](https://learn.microsoft.com/en-us/windows/win32/vss/vshadow-tool-and-sample)

## Acknowledgements
- Ayberk Halaç

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/process_creation/proc_creation_win_vshadow_exec.yml](https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/process_creation/proc_creation_win_vshadow_exec.yml)
- IOC: vshadow.exe usage with -exec parameter

## Execute

1. Executes specified executable from vshadow.exe.

```
vshadow.exe -nw -exec={PATH_ABSOLUTE:.exe} C:
```

   - Use case: Performs execution of specified executable file.

   - Privileges required: Administrator

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: EXE
