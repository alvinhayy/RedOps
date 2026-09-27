---
title: "Reset.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Reset/
fetched_at: 2026-09-20T17:11:23Z
license: unspecified
category: windows
---

Remote Desktop Services Reset Utility

## Paths
- c:\windows\system32\reset.exe
- c:\windows\syswow64\reset.exe

## Acknowledgements
- Matan Bahar ([@Bl4ckShad3](https://twitter.com/@Bl4ckShad3))

## Detections
- IOC: reset.exe being executed and executes rwinsta.exe outside of its normal path of c:\windows\system32\ or c:\windows\syswow64\

## Execute

1. Once executed, reset.exe will execute rwinsta.exe in the same folder. Thus, if reset.exe is copied to a folder and an arbitrary executable is renamed to rwinsta.exe, reset.exe will spawn it.

```
reset.exe session
```

   - Use case: Execute an arbitrary executable via trusted system executable.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: EXERequires: Rename
