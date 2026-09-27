---
title: "CustomShellHost.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/CustomShellHost/
fetched_at: 2026-09-20T17:09:48Z
license: unspecified
category: windows
---

A host process that is used by custom shells when using Windows in Kiosk mode.

## Paths
- C:\Windows\System32\CustomShellHost.exe

## Resources
- [https://twitter.com/YoSignals/status/1381353520088113154](https://twitter.com/YoSignals/status/1381353520088113154)
- [https://docs.microsoft.com/en-us/windows/configuration/kiosk-shelllauncher](https://docs.microsoft.com/en-us/windows/configuration/kiosk-shelllauncher)

## Acknowledgements
- John Carroll ([@YoSignals](https://twitter.com/@YoSignals))

## Detections
- IOC: CustomShellHost.exe is unlikely to run on normal workstations
- Sigma: [https://github.com/SigmaHQ/sigma/blob/ff5102832031425f6eed011dd3a2e62653008c94/rules/windows/process_creation/proc_creation_win_lolbin_customshellhost.yml](https://github.com/SigmaHQ/sigma/blob/ff5102832031425f6eed011dd3a2e62653008c94/rules/windows/process_creation/proc_creation_win_lolbin_customshellhost.yml)

## Execute

1. Executes explorer.exe (with command-line argument /NoShellRegistrationCheck) if present in the current working folder.

```
CustomShellHost.exe
```

   - Use case: Can be used to evade defensive counter-measures

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: EXE
