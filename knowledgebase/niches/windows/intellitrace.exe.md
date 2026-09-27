---
title: "IntelliTrace.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/IntelliTrace/
fetched_at: 2026-09-20T17:14:53Z
license: unspecified
category: windows
---

Visual Studio command-line tool for collecting and managing diagnostic trace files.

## Paths
- C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\IntelliTrace\IntelliTrace.exe
- C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\IntelliTrace\IntelliTrace.exe

## Resources
- [https://learn.microsoft.com/en-us/visualstudio/debugger/intellitrace](https://learn.microsoft.com/en-us/visualstudio/debugger/intellitrace)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Execute

1. Launches an executable via Visual Studio command line utility.

```
IntelliTrace.exe launch /cp:"collectionplan.xml" /f:"c:\users\public\log" "C:\Windows\System32\calc.exe"
```

   - Use case: Executes an executable under a trusted microsoft signed binary.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE
