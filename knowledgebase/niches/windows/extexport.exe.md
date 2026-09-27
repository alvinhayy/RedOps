---
title: "Extexport.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Extexport/
fetched_at: 2026-09-20T17:10:06Z
license: unspecified
category: windows
---

Load a DLL located in the c:\test folder with a specific name.

## Paths
- C:\Program Files\Internet Explorer\Extexport.exe
- C:\Program Files (x86)\Internet Explorer\Extexport.exe

## Resources
- [http://www.hexacorn.com/blog/2018/04/24/extexport-yet-another-lolbin/](http://www.hexacorn.com/blog/2018/04/24/extexport-yet-another-lolbin/)

## Acknowledgements
- Adam ([@hexacorn](https://twitter.com/@hexacorn))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_extexport.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_extexport.yml)
- IOC: Extexport.exe loads dll and is execute from other folder the original path

## Execute

1. Load a DLL located in the specified folder with one of the following names mozcrt19.dll, mozsqlite3.dll, or sqlite.dll.

```
Extexport.exe {PATH_ABSOLUTE:folder} foo bar
```

   - Use case: Execute dll file

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: DLL
