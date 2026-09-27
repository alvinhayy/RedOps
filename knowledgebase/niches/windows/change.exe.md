---
title: "Change.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Change/
fetched_at: 2026-09-20T17:09:31Z
license: unspecified
category: windows
---

Remote Desktop Services MultiUser Change Utility

## Paths
- c:\windows\system32\change.exe
- c:\windows\syswow64\change.exe

## Acknowledgements
- Idan Lerman ([@IdanLerman](https://twitter.com/@IdanLerman))

## Detections
- IOC: change.exe being executed and executes a child process outside of its normal path of c:\windows\system32\ or c:\windows\syswow64\

## Execute

1. Once executed, change.exe will execute chgusr.exe in the same folder. Thus, if change.exe is copied to a folder and an arbitrary executable is renamed to chgusr.exe, change.exe will spawn it. Instead of user, it is also possible to use port or logon as command-line option.

```
change.exe user
```

   - Use case: Execute an arbitrary executable via trusted system executable.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: EXERequires: Rename
