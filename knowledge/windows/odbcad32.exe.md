---
title: "odbcad32.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/odbcad32/
fetched_at: 2026-09-20T17:12:13Z
license: unspecified
category: windows
---

ODBC Data Source Administrator to manage User/System DSNs and ODBC drivers.

## Paths
- c:\windows\system32\odbcad32.exe
- c:\windows\syswow64\odbcad32.exe

## Resources
- [https://medium.com/@thebinaryhashira/living-off-the-land-and-living-above-uac-6a66738d225c](https://medium.com/@thebinaryhashira/living-off-the-land-and-living-above-uac-6a66738d225c)

## Acknowledgements
- amonitoring
- Ekitji ([@eki_erk](https://twitter.com/@eki_erk))

## Detections
- IOC: odbcad32.exe spawning unexpected child processes.

## UAC bypass

1. Launch odbcad32.exe GUI, click ‘Tracing’ tab, click ‘Browsing’ button, enter abitrary command in the File Dialog’s path, press enter.

```
odbcad32.exe
```

   - Use case: Execute a binary as a high-integrity process without a UAC prompt.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1548.002

   - Tags: Execute: CMDApplication: GUI
