---
title: "XBootMgr.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/XBootMgr/
fetched_at: 2026-09-20T17:15:54Z
license: unspecified
category: windows
---

Windows Performance Toolkit binary used to start performance traces.

## Paths
- C:\Program Files\Windows Kits\10\Windows Performance Toolkit\xbootmgr.exe
- C:\Program Files (x86)\Windows Kits\10\Windows Performance Toolkit\xbootmgr.exe

## Resources
- [https://learn.microsoft.com/en-us/previous-versions/windows/desktop/xperf/reference](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/xperf/reference)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))
- Tommy Warren

## Execute

1. Executes an executable after the trace is complete using the callBack parameter.

```
xbootmgr.exe -trace "{boot|hibernate|standby|shutdown|rebootCycle}" -callBack {PATH:.exe}
```

   - Use case: Executes code as part of post-trace automation flow.

   - Privileges required: Administrator

   - Operating systems: Windows

   - ATT&CK® technique: T1202

   - Tags: Execute: EXE

2. Executes an executable before each trace run using the preTraceCmd parameter.

```
xbootmgr.exe -trace "{boot|hibernate|standby|shutdown|rebootCycle}" -preTraceCmd {PATH:.exe}
```

   - Use case: Executes code as part of pre-trace automation or staging.

   - Privileges required: Administrator

   - Operating systems: Windows

   - ATT&CK® technique: T1202

   - Tags: Execute: EXE
