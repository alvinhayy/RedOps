---
title: "vsjitdebugger.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Vsjitdebugger/
fetched_at: 2026-09-20T17:15:43Z
license: unspecified
category: windows
---

Just-In-Time (JIT) debugger included with Visual Studio

## Paths
- c:\windows\system32\vsjitdebugger.exe

## Resources
- [https://twitter.com/pabraeken/status/990758590020452353](https://twitter.com/pabraeken/status/990758590020452353)

## Acknowledgements
- Pierre-Alexandre Braeken ([@pabraeken](https://twitter.com/@pabraeken))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_susp_use_of_vsjitdebugger_bin.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_susp_use_of_vsjitdebugger_bin.yml)

## Execute

1. Executes specified executable as a subprocess of Vsjitdebugger.exe.

```
Vsjitdebugger.exe {PATH:.exe}
```

   - Use case: Execution of local PE file as a subprocess of Vsjitdebugger.exe.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE
