---
title: "Mshtml.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Mshtml/
fetched_at: 2026-09-20T17:16:14Z
license: unspecified
category: windows
---

Microsoft HTML Viewer

## Paths
- c:\windows\system32\mshtml.dll
- c:\windows\syswow64\mshtml.dll

## Resources
- [https://twitter.com/pabraeken/status/998567549670477824](https://twitter.com/pabraeken/status/998567549670477824)
- [https://windows10dll.nirsoft.net/mshtml_dll.html](https://windows10dll.nirsoft.net/mshtml_dll.html)

## Acknowledgements
- Pierre-Alexandre Braeken ([@pabraeken](https://twitter.com/@pabraeken))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)

## Execute

1. Invoke an HTML Application via mshta.exe (note: pops a security warning and a print dialogue box).

```
rundll32.exe Mshtml.dll,PrintHTML {PATH_ABSOLUTE:.hta}
```

   - Use case: Launch an HTA application.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: HTA
