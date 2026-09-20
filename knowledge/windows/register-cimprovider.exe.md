---
title: "Register-cimprovider.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Register-cimprovider/
fetched_at: 2026-09-20T17:11:18Z
license: unspecified
category: windows
---

Used to register new wmi providers

## Paths
- C:\Windows\System32\Register-cimprovider.exe
- C:\Windows\SysWOW64\Register-cimprovider.exe

## Resources
- [https://twitter.com/PhilipTsukerman/status/992021361106268161](https://twitter.com/PhilipTsukerman/status/992021361106268161)

## Acknowledgements
- Philip Tsukerman ([@PhilipTsukerman](https://twitter.com/@PhilipTsukerman))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/35a7244c62820fbc5a832e50b1e224ac3a1935da/rules/windows/process_creation/proc_creation_win_susp_register_cimprovider.yml](https://github.com/SigmaHQ/sigma/blob/35a7244c62820fbc5a832e50b1e224ac3a1935da/rules/windows/process_creation/proc_creation_win_susp_register_cimprovider.yml)
- IOC: Register-cimprovider.exe execution and cmdline DLL load may be supsicious

## Execute

1. Load the target .DLL.

```
Register-cimprovider -path {PATH_ABSOLUTE:.dll}
```

   - Use case: Execute code within dll file

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: DLL
