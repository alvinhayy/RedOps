---
title: "SettingSyncHost.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/SettingSyncHost/
fetched_at: 2026-09-20T17:11:38Z
license: unspecified
category: windows
---

Host Process for Setting Synchronization

## Paths
- C:\Windows\System32\SettingSyncHost.exe
- C:\Windows\SysWOW64\SettingSyncHost.exe

## Resources
- [https://www.hexacorn.com/blog/2020/02/02/settingsynchost-exe-as-a-lolbin/](https://www.hexacorn.com/blog/2020/02/02/settingsynchost-exe-as-a-lolbin/)

## Acknowledgements
- Adam ([@hexacorn](https://twitter.com/@hexacorn))
- Elliot Killick ([@elliotkillick](https://twitter.com/@elliotkillick))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_settingsynchost.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_settingsynchost.yml)
- IOC: SettingSyncHost.exe should not be run on a normal workstation

## Execute

1. Execute file specified in %COMSPEC%

```
SettingSyncHost -LoadAndRunDiagScript {PATH:.exe}
```

   - Use case: Can be used to evade defensive countermeasures or to hide as a persistence mechanism

   - Privileges required: User

   - Operating systems: Windows 8, Windows 8.1, Windows 10

   - ATT&CK® technique: T1218

   - Tags: Execute: EXE

2. Execute a batch script in the background (no window ever pops up) which can be subverted to running arbitrary programs by setting the current working directory to %TMP% and creating files such as reg.bat/reg.exe in that directory thereby causing them to execute instead of the ones in C:\Windows\System32.

```
SettingSyncHost -LoadAndRunDiagScriptNoCab {PATH:.bat}
```

   - Use case: Can be used to evade defensive countermeasures or to hide as a persistence mechanism. Additionally, effectively act as a -WindowStyle Hidden option (as there is in PowerShell) for any arbitrary batch file.

   - Privileges required: User

   - Operating systems: Windows 8, Windows 8.1, Windows 10

   - ATT&CK® technique: T1218

   - Tags: Execute: CMD
