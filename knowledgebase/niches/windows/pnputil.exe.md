---
title: "Pnputil.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Pnputil/
fetched_at: 2026-09-20T17:11:01Z
license: unspecified
category: windows
---

Used for installing drivers

## Paths
- C:\Windows\system32\pnputil.exe

## Acknowledgements
- Hai Vaknin(Lux) ([@LuxNoBulIshit](https://twitter.com/@LuxNoBulIshit))
- Avihay eldad ([@aloneliassaf](https://twitter.com/@aloneliassaf))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_susp_driver_installed_by_pnputil.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_susp_driver_installed_by_pnputil.yml)

## Execute

1. Used for installing drivers

```
pnputil.exe -i -a {PATH_ABSOLUTE:.inf}
```

   - Use case: Add malicious driver

   - Privileges required: Administrator

   - Operating systems: Windows 7, Windows 10, Windows 11

   - ATT&CK® technique: T1547

   - Tags: Execute: INF
