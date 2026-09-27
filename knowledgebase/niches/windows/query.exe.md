---
title: "Query.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Query/
fetched_at: 2026-09-20T17:11:09Z
license: unspecified
category: windows
---

Remote Desktop Services MultiUser Query Utility

## Paths
- c:\windows\system32\query.exe
- c:\windows\syswow64\query.exe

## Acknowledgements
- Idan Lerman ([@IdanLerman](https://twitter.com/@IdanLerman))

## Detections
- IOC: query.exe being executed and executes a child process outside of its normal path of c:\windows\system32\ or c:\windows\syswow64\

## Execute

1. Once executed, query.exe will execute quser.exe in the same folder. Thus, if query.exe is copied to a folder and an arbitrary executable is renamed to quser.exe, query.exe will spawn it. Instead of user, it is also possible to use session, termsession or process as command-line option.

```
query.exe user
```

   - Use case: Execute an arbitrary executable via trusted system executable.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: EXERequires: Rename
