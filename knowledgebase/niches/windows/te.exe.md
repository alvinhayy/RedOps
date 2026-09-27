---
title: "te.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Te/
fetched_at: 2026-09-20T17:15:29Z
license: unspecified
category: windows
---

Testing tool included with Microsoft Test Authoring and Execution Framework (TAEF).

## Paths
- no default

## Resources
- [https://twitter.com/gn3mes1s/status/927680266390384640](https://twitter.com/gn3mes1s/status/927680266390384640)
- [https://github.com/LOLBAS-Project/LOLBAS/pull/359](https://github.com/LOLBAS-Project/LOLBAS/pull/359)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/taef/authoring-tests](https://learn.microsoft.com/en-us/windows-hardware/drivers/taef/authoring-tests)

## Acknowledgements
- Giuseppe N3mes1s ([@gN3mes1s](https://twitter.com/@gN3mes1s))
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_susp_use_of_te_bin.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_susp_use_of_te_bin.yml)

## Execute

1. Run COM Scriptlets (e.g. VBScript) by calling a Windows Script Component (WSC) file.

```
te.exe {PATH:.wsc}
```

   - Use case: Execute Visual Basic script stored in local Windows Script Component file.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: WSH

2. Execute commands from a DLL file with Test Authoring and Execution Framework (TAEF) tests. See resources section for required structures.

```
te.exe {PATH:.dll}
```

   - Use case: Execute DLL file.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: DLLInput: Custom Format
