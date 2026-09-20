---
title: "dotnet-trace.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/dotnet-trace/
fetched_at: 2026-09-20T17:15:59Z
license: unspecified
category: windows
---

.NET diagnostic tool for collecting runtime traces from .NET applications. Installed via ‘dotnet tool install –global dotnet-trace’ (.NET SDK required).

## Paths
- C:\Users\<user>\.dotnet\tools\dotnet-trace.exe

## Resources
- [https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace)
- [https://github.com/dotnet/diagnostics](https://github.com/dotnet/diagnostics)

## Acknowledgements
- Iván Cabrera ([@ivancabrera02](https://twitter.com/@ivancabrera02))

## Detections
- IOC: Process creation with command line containing "dotnet-trace collect" and "–"

## Execute

1. Launches the specified executable as a child process while collecting runtime trace data for 1 second during execution.

```
dotnet-trace.exe collect --duration 00:00:01 -- {PATH:.exe}
```

   - Use case: Execute a child process under the guise of a legitimate .NET diagnostic tool.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE
