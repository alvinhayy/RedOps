---
title: "WorkFolders.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/WorkFolders/
fetched_at: 2026-09-20T17:12:04Z
license: unspecified
category: windows
---

Work Folders

## Paths
- C:\Windows\System32\WorkFolders.exe

## Resources
- [https://www.ctus.io/2021/04/12/exploading/](https://www.ctus.io/2021/04/12/exploading/)
- [https://twitter.com/ElliotKillick/status/1449812843772227588](https://twitter.com/ElliotKillick/status/1449812843772227588)

## Acknowledgements
- John Carroll ([@YoSignals](https://twitter.com/@YoSignals))
- Elliot Killick ([@elliotkillick](https://twitter.com/@elliotkillick))
- Naor Evgi ([@ghosts621](https://twitter.com/@ghosts621))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_susp_workfolders.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_susp_workfolders.yml)
- IOC: WorkFolders.exe should not be run on a normal workstation
- IOC: Registry modification to HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\control.exe

## Execute

1. Execute control.exe in the current working directory

```
WorkFolders
```

   - Use case: Can be used to evade defensive countermeasures or to hide as a persistence mechanism

   - Privileges required: User

   - Operating systems: Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: EXERequires: Rename

2. WorkFolders attempts to execute control.exe. By modifying the default value of the App Paths registry key for control.exe in HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\control.exe, an attacker can achieve proxy execution.

```
WorkFolders
```

   - Use case: Proxy execution of a malicious payload via App Paths registry hijacking.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: EXERequires: Registry change
