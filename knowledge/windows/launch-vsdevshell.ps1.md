---
title: "Launch-VsDevShell.ps1"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Scripts/Launch-VsDevShell/
fetched_at: 2026-09-20T17:16:35Z
license: unspecified
category: windows
---

Locates and imports a Developer PowerShell module and calls the Enter-VsDevShell cmdlet

## Paths
- C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\Launch-VsDevShell.ps1
- C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\Launch-VsDevShell.ps1

## Resources
- [https://twitter.com/nas_bench/status/1535981653239255040](https://twitter.com/nas_bench/status/1535981653239255040)

## Acknowledgements
- Nasreddine Bencherchali ([@nas_bench](https://twitter.com/@nas_bench))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6199a703221a98ae6ad343c79c558da375203e4e/rules/windows/process_creation/proc_creation_win_lolbin_launch_vsdevshell.yml](https://github.com/SigmaHQ/sigma/blob/6199a703221a98ae6ad343c79c558da375203e4e/rules/windows/process_creation/proc_creation_win_lolbin_launch_vsdevshell.yml)

## Execute

1. Execute binaries from the context of the signed script using the “VsWherePath” flag.

```
powershell -ep RemoteSigned -f .\Launch-VsDevShell.ps1 -VsWherePath {PATH_ABSOLUTE:.exe}
```

   - Use case: Proxy execution

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1216

   - Tags: Execute: EXE

2. Execute binaries and commands from the context of the signed script using the “VsInstallationPath” flag.

```
powershell -ep RemoteSigned -f .\Launch-VsDevShell.ps1 -VsInstallationPath "/../../../../../; {PATH:.exe} ;"
```

   - Use case: Proxy execution

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1216

   - Tags: Execute: EXE
