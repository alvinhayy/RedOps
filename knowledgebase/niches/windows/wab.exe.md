---
title: "Wab.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Wab/
fetched_at: 2026-09-20T17:11:55Z
license: unspecified
category: windows
---

Windows address book manager

## Paths
- C:\Program Files\Windows Mail\wab.exe
- C:\Program Files (x86)\Windows Mail\wab.exe

## Resources
- [https://twitter.com/Hexacorn/status/991447379864932352](https://twitter.com/Hexacorn/status/991447379864932352)
- [http://www.hexacorn.com/blog/2018/05/01/wab-exe-as-a-lolbin/](http://www.hexacorn.com/blog/2018/05/01/wab-exe-as-a-lolbin/)

## Acknowledgements
- Adam ([@Hexacorn](https://twitter.com/@Hexacorn))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/registry/registry_set/registry_set_wab_dllpath_reg_change.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/registry/registry_set/registry_set_wab_dllpath_reg_change.yml)
- IOC: WAB.exe should normally never be used

## Execute

1. Change HKLM\Software\Microsoft\WAB\DLLPath and execute DLL of choice

```
wab.exe
```

   - Use case: Execute dll file. Bypass defensive counter measures

   - Privileges required: Administrator

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: DLL
