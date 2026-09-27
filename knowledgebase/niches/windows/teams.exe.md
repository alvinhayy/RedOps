---
title: "Teams.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Teams/
fetched_at: 2026-09-20T17:15:30Z
license: unspecified
category: windows
---

Electron runtime binary which runs the Teams application

## Paths
- C:\Users\<username>\AppData\Local\Microsoft\Teams\current\Teams.exe

## Resources
- [https://l--k.uk/2022/01/16/microsoft-teams-and-other-electron-apps-as-lolbins/](https://l--k.uk/2022/01/16/microsoft-teams-and-other-electron-apps-as-lolbins/)

## Acknowledgements
- Andrew Kisliakov
- mr.d0x ([@mrd0x](https://twitter.com/@mrd0x))

## Detections
- IOC: %LOCALAPPDATA%\Microsoft\Teams\current\app directory created
- IOC: %LOCALAPPDATA%\Microsoft\Teams\current\app.asar file created/modified by non-Teams installer/updater
- Sigma: [https://github.com/SigmaHQ/sigma/blob/43277f26fc1c81fc98fc79147b711189e901b757/rules/windows/process_creation/proc_creation_win_susp_electron_exeuction_proxy.yml](https://github.com/SigmaHQ/sigma/blob/43277f26fc1c81fc98fc79147b711189e901b757/rules/windows/process_creation/proc_creation_win_susp_electron_exeuction_proxy.yml)

## Execute

1. Generate JavaScript payload and package.json, and save to “%LOCALAPPDATA%\Microsoft\Teams\current\app\” before executing.

```
teams.exe
```

   - Use case: Execute JavaScript code

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.015

   - Tags: Execute: Node.JS

2. Generate JavaScript payload and package.json, archive in ASAR file and save to “%LOCALAPPDATA%\Microsoft\Teams\current\app.asar” before executing.

```
teams.exe
```

   - Use case: Execute JavaScript code

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.015

   - Tags: Execute: Node.JS

3. Teams spawns cmd.exe as a child process of teams.exe and executes the ping command

```
teams.exe --disable-gpu-sandbox --gpu-launcher="{CMD} &&"
```

   - Use case: Executes a process under a trusted Microsoft signed binary

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.015

   - Tags: Execute: CMD
