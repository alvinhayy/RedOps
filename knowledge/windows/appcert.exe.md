---
title: "AppCert.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Appcert/
fetched_at: 2026-09-20T17:14:22Z
license: unspecified
category: windows
---

Windows App Certification Kit command-line tool.

## Paths
- C:\Program Files (x86)\Windows Kits\10\App Certification Kit\appcert.exe
- C:\Program Files\Windows Kits\10\App Certification Kit\appcert.exe

## Resources
- [https://learn.microsoft.com/windows/win32/win_cert/using-the-windows-app-certification-kit](https://learn.microsoft.com/windows/win32/win_cert/using-the-windows-app-certification-kit)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Execute

1. Execute an executable file via the Windows App Certification Kit command-line tool.

```
appcert.exe test -apptype desktop -setuppath {PATH_ABSOLUTE:.exe} -reportoutputpath {PATH_ABSOLUTE:.xml}
```

   - Use case: Performs execution of specified file, can be used as a defense evasion

   - Privileges required: Administrator

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE

2. Install an MSI file via an msiexec instance spawned via appcert.exe as parent process.

```
appcert.exe test -apptype desktop -setuppath {PATH_ABSOLUTE:.msi} -setupcommandline /q -reportoutputpath {PATH_ABSOLUTE:.xml}
```

   - Use case: Execute custom made MSI file with malicious code

   - Privileges required: Administrator

   - Operating systems: Windows

   - ATT&CK® technique: T1218.007

   - Tags: Execute: MSI
