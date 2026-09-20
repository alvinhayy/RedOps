---
title: "winfile.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/winfile/
fetched_at: 2026-09-20T17:16:04Z
license: unspecified
category: windows
---

Windows File Manager executable

## Paths
- C:\Windows\System32\winfile.exe
- C:\Windows\winfile.exe
- C:\Program Files\WinFile\winfile.exe
- C:\Program Files (x86)\WinFile\winfile.exe
- C:\Program Files\WindowsApps\Microsoft.WindowsFileManager_10.3.0.0_x64__8wekyb3d8bbwe\WinFile\winfile.exe

## Resources
- [https://github.com/microsoft/winfile](https://github.com/microsoft/winfile)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Execute

1. Execute an executable file with WinFile as a parent process.

```
winfile.exe {PATH:.exe}
```

   - Use case: Performs execution of specified file, can be used as a defense evasion

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: EXE
