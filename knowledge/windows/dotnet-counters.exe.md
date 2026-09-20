---
title: "dotnet-counters.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/dotnet-counters/
fetched_at: 2026-09-20T17:15:58Z
license: unspecified
category: windows
---

.NET diagnostic tool for monitoring performance counters of .NET applications in real-time. Installed via ‘dotnet tool install –global dotnet-counters’ (.NET SDK required).

## Paths
- C:\Users\<user>\.dotnet\tools\dotnet-counters.exe

## Resources
- [https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters)
- [https://github.com/dotnet/diagnostics](https://github.com/dotnet/diagnostics)

## Acknowledgements
- Iván Cabrera ([@ivancabrera02](https://twitter.com/@ivancabrera02))

## Detections
- IOC: Process creation with command line containing "dotnet-counters collect" and "–"

## Execute

1. Launches the specified executable as a child process while collecting performance counter data for 1 second.

```
dotnet-counters.exe collect --duration 1 -- {PATH:.exe}
```

   - Use case: Execute a child process under the guise of a legitimate .NET diagnostic tool.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE
