---
title: "Fsutil.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Fsutil/
fetched_at: 2026-09-20T17:10:14Z
license: unspecified
category: windows
---

File System Utility

## Paths
- C:\Windows\System32\fsutil.exe
- C:\Windows\SysWOW64\fsutil.exe

## Resources
- [https://twitter.com/0gtweet/status/1720724516324704404](https://twitter.com/0gtweet/status/1720724516324704404)

## Acknowledgements
- Elliot Killick ([@elliotkillick](https://twitter.com/@elliotkillick))
- Jimmy ([@bohops](https://twitter.com/@bohops))
- Grzegorz Tworek ([@0gtweet](https://twitter.com/@0gtweet))

## Detections
- IOC: fsutil.exe should not be run on a normal workstation
- IOC: file setZeroData (not case-sensitive) in the process arguments
- IOC: Sysmon Event ID 1
- IOC: Execution of process fsutil.exe with trace decode could be suspicious
- IOC: Non-Windows netsh.exe execution
- Sigma: [https://github.com/SigmaHQ/sigma/blob/ff5102832031425f6eed011dd3a2e62653008c94/rules/windows/process_creation/proc_creation_win_susp_fsutil_usage.yml](https://github.com/SigmaHQ/sigma/blob/ff5102832031425f6eed011dd3a2e62653008c94/rules/windows/process_creation/proc_creation_win_susp_fsutil_usage.yml)

## Tamper

1. Zero out a file

```
fsutil.exe file setZeroData offset=0 length=9999999999 {PATH_ABSOLUTE}
```

   - Use case: Can be used to forensically erase a file

   - Privileges required: User

   - Operating systems: Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10

   - ATT&CK® technique: T1485

2. Delete the USN journal volume to hide file creation activity

```
fsutil.exe usn deletejournal /d c:
```

   - Use case: Can be used to hide file creation activity

   - Privileges required: User

   - Operating systems: Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10

   - ATT&CK® technique: T1485

3. Executes a pre-planted binary named netsh.exe from the current directory.

```
fsutil.exe trace decode
```

   - Use case: Spawn a pre-planted executable from fsutil.exe.

   - Privileges required: User

   - Operating systems: Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: EXE
