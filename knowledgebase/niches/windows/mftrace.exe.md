---
title: "Mftrace.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Mftrace/
fetched_at: 2026-09-20T17:14:55Z
license: unspecified
category: windows
---

Trace log generation tool for Media Foundation Tools.

## Paths
- C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0\x86\mftrace.exe
- C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0\x64\mftrace.exe
- C:\Program Files (x86)\Windows Kits\10\bin\x86\mftrace.exe
- C:\Program Files (x86)\Windows Kits\10\bin\x64\mftrace.exe

## Resources
- [https://twitter.com/0rbz_/status/988911181422186496](https://twitter.com/0rbz_/status/988911181422186496)

## Acknowledgements
- fabrizio ([@0rbz_](https://twitter.com/@0rbz_))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_mftrace.yml](https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_mftrace.yml)

## Execute

1. Launch specified executable as a subprocess of Mftrace.exe.

```
Mftrace.exe {PATH:.exe}
```

   - Use case: Local execution of cmd.exe as a subprocess of Mftrace.exe.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE
