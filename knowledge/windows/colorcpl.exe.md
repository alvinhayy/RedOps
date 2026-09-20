---
title: "Colorcpl.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Colorcpl/
fetched_at: 2026-09-20T17:09:39Z
license: unspecified
category: windows
---

Binary that handles color management

## Paths
- C:\Windows\System32\colorcpl.exe
- C:\Windows\SysWOW64\colorcpl.exe

## Resources
- [https://twitter.com/eral4m/status/1480468728324231172](https://twitter.com/eral4m/status/1480468728324231172)

## Acknowledgements
- eral4m ([@eral4m](https://twitter.com/@eral4m))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/master/rules/windows/file/file_event/file_event_win_susp_colorcpl.yml](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/file/file_event/file_event_win_susp_colorcpl.yml)
- IOC: colorcpl.exe writing files

## Copy

1. Copies the referenced file to C:\Windows\System32\spool\drivers\color.

```
colorcpl {PATH}
```

   - Use case: Copies file(s) to a subfolder of a generally trusted folder (c:\Windows\System32), which can be used to hide files or make them blend into the environment.

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1036.005
