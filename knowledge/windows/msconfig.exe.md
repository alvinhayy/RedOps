---
title: "Msconfig.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Msconfig/
fetched_at: 2026-09-20T17:10:42Z
license: unspecified
category: windows
---

MSConfig is a troubleshooting tool which is used to temporarily disable or re-enable software, device drivers or Windows services that run during startup process to help the user determine the cause of a problem with Windows

## Paths
- C:\Windows\System32\msconfig.exe

## Resources
- [https://twitter.com/pabraeken/status/991314564896690177](https://twitter.com/pabraeken/status/991314564896690177)

## Acknowledgements
- Pierre-Alexandre Braeken ([@pabraeken](https://twitter.com/@pabraeken))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_uac_bypass_msconfig_gui.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_uac_bypass_msconfig_gui.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/file/file_event/file_event_win_uac_bypass_msconfig_gui.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/file/file_event/file_event_win_uac_bypass_msconfig_gui.yml)
- IOC: mscfgtlc.xml changes in system32 folder

## Execute

1. Executes command embeded in crafted c:\windows\system32\mscfgtlc.xml.

```
Msconfig.exe -5
```

   - Use case: Code execution using Msconfig.exe

   - Privileges required: Administrator

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10

   - ATT&CK® technique: T1218

   - Tags: Execute: CMD
