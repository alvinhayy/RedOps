---
title: "ComputerDefaults.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/ComputerDefaults/
fetched_at: 2026-09-20T17:09:40Z
license: unspecified
category: windows
---

ComputerDefaults.exe is a Windows system utility for managing default applications for tasks like web browsing, emailing, and media playback.

## Paths
- C:\Windows\System32\ComputerDefaults.exe
- C:\Windows\SysWOW64\ComputerDefaults.exe

## Resources
- [https://gist.github.com/havoc3-3/812547525107bd138a1a839118a3a44b](https://gist.github.com/havoc3-3/812547525107bd138a1a839118a3a44b)

## Acknowledgements
- Eron Clarke

## Detections
- IOC: Event ID 10
- IOC: A binary or script spawned as a child process of ComputerDefaults.exe
- IOC: Changes to HKEY_CURRENT_USER\Software\Classes\ms-settings\Shell\open\command
- Sigma: [https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_uac_bypass_computerdefaults.yml](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_uac_bypass_computerdefaults.yml)

## UAC bypass

1. Upon execution, ComputerDefaults.exe checks two registry values at HKEY_CURRENT_USER\Software\Classes\ms-settings\Shell\open\command; if these are set by an attacker, the set command will be executed as a high-integrity process without a UAC prompt being displayed to the user. See ‘resources’ for which registry keys/values to set.

```
ComputerDefaults.exe
```

   - Use case: Execute a binary or script as a high-integrity process without a UAC prompt.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1548.002
