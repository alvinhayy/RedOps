---
title: "setupugc.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/setupugc/
fetched_at: 2026-09-20T17:12:14Z
license: unspecified
category: windows
---

Setup Unattend Generic Command Processor used during Windows deployment.

## Paths
- C:\Windows\System32\setupugc.exe
- C:\Windows\SysWOW64\setupugc.exe

## Resources
- [https://strontic.github.io/xcyclopedia/library/setupugc.exe-3CFE082E8656AD66B5B9FFEB28CF4EC3.html](https://strontic.github.io/xcyclopedia/library/setupugc.exe-3CFE082E8656AD66B5B9FFEB28CF4EC3.html)

## Acknowledgements
- Ang Kar Min ([@karminang](https://twitter.com/@karminang))

## Detections
- IOC: setupugc.exe spawning child processes outside of Windows Setup context. Legitimate parents are setuphost.exe or setup.exe.
- IOC: Registry writes to HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\UnattendSettings\Setup-Unattend-Settings\RunSynchronous\ on a deployed system.

## Execute

1. By first setting a command to a specific registry under Setup-Unattend-Settings, e.g. via: reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\UnattendSettings\Setup-Unattend-Settings\RunSynchronous\1" /v Path /d "{CMD}" /f, executing the following will cause it to execute the command.

```
setupugc.exe specialize
```

   - Use case: Execute binary through legitimate proxy

   - Privileges required: Administrator

   - Operating systems: Windows 10, Windows 11, Windows Server 2025

   - ATT&CK® technique: T1218

   - Tags: Execute: CMDRequires: Registry Change

2. Same technique as above, but using the auditUser command-line option.

```
setupugc.exe auditUser
```

   - Use case: Execute binary through legitimate proxy

   - Privileges required: Administrator

   - Operating systems: Windows 10, Windows 11, Windows Server 2025

   - ATT&CK® technique: T1218

   - Tags: Execute: CMDRequires: Registry Change
