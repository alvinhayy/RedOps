---
title: "Tracker.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Tracker/
fetched_at: 2026-09-20T17:15:33Z
license: unspecified
category: windows
---

Tool included with Microsoft .Net Framework.

## Paths
- no default

## Resources
- [https://twitter.com/subTee/status/793151392185589760](https://twitter.com/subTee/status/793151392185589760)
- [https://attack.mitre.org/wiki/Execution](https://attack.mitre.org/wiki/Execution)

## Acknowledgements
- Casey Smith ([@subTee](https://twitter.com/@subTee))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_tracker.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_tracker.yml)

## Execute

1. Use tracker.exe to proxy execution of an arbitrary DLL into another process. Since tracker.exe is also signed it can be used to bypass application whitelisting solutions.

```
Tracker.exe /d {PATH:.dll} /c C:\Windows\write.exe
```

   - Use case: Injection of locally stored DLL file into target process.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: DLL

2. Use tracker.exe to proxy execution of an arbitrary DLL into another process. Since tracker.exe is also signed it can be used to bypass application whitelisting solutions.

```
Tracker.exe /d {PATH:.dll} /c C:\Windows\write.exe
```

   - Use case: Injection of locally stored DLL file into target process.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: DLL
