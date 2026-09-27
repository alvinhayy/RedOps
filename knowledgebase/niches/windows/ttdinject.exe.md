---
title: "Ttdinject.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Ttdinject/
fetched_at: 2026-09-20T17:11:47Z
license: unspecified
category: windows
---

Used by Windows 1809 and newer to Debug Time Travel (Underlying call of tttracer.exe)

## Paths
- C:\Windows\System32\ttdinject.exe
- C:\Windows\Syswow64\ttdinject.exe

## Resources
- [https://twitter.com/Oddvarmoe/status/1196333160470138880](https://twitter.com/Oddvarmoe/status/1196333160470138880)

## Acknowledgements
- Oddvar Moe ([@oddvarmoe](https://twitter.com/@oddvarmoe))
- Maxime Nadeau ([@m_nad0](https://twitter.com/@m_nad0))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/create_remote_thread/create_remote_thread_win_ttdinjec.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/create_remote_thread/create_remote_thread_win_ttdinjec.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/7ea6ed3db65e0bd812b051d9bb4fffd27c4c4d0a/rules/windows/process_creation/proc_creation_win_lolbin_ttdinject.yml](https://github.com/SigmaHQ/sigma/blob/7ea6ed3db65e0bd812b051d9bb4fffd27c4c4d0a/rules/windows/process_creation/proc_creation_win_lolbin_ttdinject.yml)
- IOC: Parent child relationship. Ttdinject.exe parent for executed command
- IOC: Multiple queries made to the IFEO registry key of an untrusted executable (Ex. "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\payload.exe") from the ttdinject.exe process

## Execute

1. Execute a program using ttdinject.exe. Requires administrator privileges. A log file will be created in tmp.run. The log file can be changed, but the length (7) has to be updated.

```
TTDInject.exe /ClientParams "7 tmp.run 0 0 0 0 0 0 0 0 0 0" /Launch "{PATH:.exe}"
```

   - Use case: Spawn process using other binary

   - Privileges required: Administrator

   - Operating systems: Windows 10 2004 and above, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE

2. Execute a program using ttdinject.exe. Requires administrator privileges. A log file will be created in tmp.run. The log file can be changed, but the length (7) has to be updated.

```
ttdinject.exe /ClientScenario TTDRecorder /ddload 0 /ClientParams "7 tmp.run 0 0 0 0 0 0 0 0 0 0" /launch "{PATH:.exe}"
```

   - Use case: Spawn process using other binary

   - Privileges required: Administrator

   - Operating systems: Windows 10 1909 and below

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE
