---
title: "Mpiexec.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Mpiexec/
fetched_at: 2026-09-20T17:14:58Z
license: unspecified
category: windows
---

Command-line tool for running Message Passing Interface (MPI) applications.

## Paths
- C:\Program Files\Microsoft MPI\Bin\mpiexec.exe
- C:\Program Files (x86)\Microsoft MPI\Bin\mpiexec.exe

## Resources
- [https://learn.microsoft.com/en-us/powershell/high-performance-computing/mpiexec](https://learn.microsoft.com/en-us/powershell/high-performance-computing/mpiexec)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Execute

1. Executes a command via MPI command-line tool.

```
mpiexec.exe {CMD}
```

   - Use case: Executes commands under a trusted, Microsoft signed binary.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: CMD
