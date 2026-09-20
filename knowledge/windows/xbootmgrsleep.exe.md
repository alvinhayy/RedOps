---
title: "XBootMgrSleep.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/XBootMgrSleep/
fetched_at: 2026-09-20T17:15:55Z
license: unspecified
category: windows
---

Windows Performance Toolkit binary used for tracing and analyzing system performance during sleep and resume transitions.

## Paths
- C:\Program Files\Windows Kits\10\Windows Performance Toolkit\xbootmgrsleep.exe
- C:\Program Files (x86)\Windows Kits\10\Windows Performance Toolkit\xbootmgrsleep.exe

## Resources
- [https://learn.microsoft.com/en-us/previous-versions/windows/desktop/xperf/reference](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/xperf/reference)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))
- Yuval Saban ([@yuvalsaban3](https://twitter.com/@yuvalsaban3))

## Execute

1. Execute executable via XBootMgrSleep, with a 1 second (=1000 milliseconds) delay. Alternatively, it is also possible to replace the delay with any string for immediate execution.

```
xbootmgrsleep.exe 1000 {PATH:.exe}
```

   - Use case: Performs execution of specified executable, can be used as a defense evasion

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1202

   - Tags: Execute: EXE
