---
title: "VSIISExeLauncher.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/VSIISExeLauncher/
fetched_at: 2026-09-20T17:15:37Z
license: unspecified
category: windows
---

Binary will execute specified binary. Part of VS/VScode installation.

## Paths
- C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\Extensions\Microsoft\Web Tools\ProjectSystem\VSIISExeLauncher.exe

## Resources
- [https://github.com/timwhitez](https://github.com/timwhitez)

## Acknowledgements
- timwhite

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_vsiisexelauncher.yml](https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_vsiisexelauncher.yml)
- IOC: VSIISExeLauncher.exe spawned an unknown process

## Execute

1. The above binary will execute other binary.

```
VSIISExeLauncher.exe -p {PATH:.exe} -a "{CMD:args}"
```

   - Use case: Execute any binary with given arguments.

   - Privileges required: User

   - Operating systems: Windows 10 and up with VS/VScode installed

   - ATT&CK® technique: T1218

   - Tags: Execute: EXE
