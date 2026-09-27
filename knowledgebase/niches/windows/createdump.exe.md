---
title: "Createdump.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Createdump/
fetched_at: 2026-09-20T17:14:30Z
license: unspecified
category: windows
---

Microsoft .NET Runtime Crash Dump Generator (included in .NET Core)

## Paths
- C:\Program Files\dotnet\shared\Microsoft.NETCore.App\<version>\createdump.exe
- C:\Program Files (x86)\dotnet\shared\Microsoft.NETCore.App\<version>\createdump.exe
- C:\Program Files\Microsoft Visual Studio\<version>\Community\dotnet\runtime\shared\Microsoft.NETCore.App\6.0.0\createdump.exe
- C:\Program Files (x86)\Microsoft Visual Studio\<version>\Community\dotnet\runtime\shared\Microsoft.NETCore.App\6.0.0\createdump.exe

## Resources
- [https://twitter.com/bopin2020/status/1366400799199272960](https://twitter.com/bopin2020/status/1366400799199272960)
- [https://docs.microsoft.com/en-us/troubleshoot/developer/webapps/aspnetcore/practice-troubleshoot-linux/lab-1-3-capture-core-crash-dumps](https://docs.microsoft.com/en-us/troubleshoot/developer/webapps/aspnetcore/practice-troubleshoot-linux/lab-1-3-capture-core-crash-dumps)

## Acknowledgements
- bopin ([@bopin2020](https://twitter.com/@bopin2020))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_proc_dump_createdump.yml](https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_proc_dump_createdump.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_renamed_createdump.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_renamed_createdump.yml)
- IOC: createdump.exe process with a command line containing the lsass.exe process id

## Dump

1. Dump process by PID and create a minidump file. If “-f dump.dmp” is not specified, the file is created as ‘%TEMP%\dump.%p.dmp’ where %p is the PID of the target process.

```
createdump.exe -n -f {PATH:.dmp} {PID}
```

   - Use case: Dump process memory contents using PID.

   - Privileges required: SYSTEM

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1003
