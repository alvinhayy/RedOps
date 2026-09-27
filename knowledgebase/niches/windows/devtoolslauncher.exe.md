---
title: "Devtoolslauncher.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Devtoolslauncher/
fetched_at: 2026-09-20T17:14:37Z
license: unspecified
category: windows
---

Binary will execute specified binary. Part of VS/VScode installation.

## Paths
- c:\windows\system32\devtoolslauncher.exe

## Resources
- [https://twitter.com/_felamos/status/1179811992841797632](https://twitter.com/_felamos/status/1179811992841797632)
- [https://www.virustotal.com/gui/file/84877a507af8b70c145777a87eaf28a8327c50a1563fe650f34572bef8a42ff6/details](https://www.virustotal.com/gui/file/84877a507af8b70c145777a87eaf28a8327c50a1563fe650f34572bef8a42ff6/details)

## Acknowledgements
- felamos ([@_felamos](https://twitter.com/@_felamos))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_devtoolslauncher.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_devtoolslauncher.yml)
- IOC: DeveloperToolsSvc.exe spawned an unknown process

## Execute

1. The above binary will execute other binary.

```
devtoolslauncher.exe LaunchForDeploy {PATH_ABSOLUTE:.exe} "{CMD:args}" test
```

   - Use case: Execute any binary with given arguments and it will call developertoolssvc.exe. developertoolssvc is actually executing the binary.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: CMD

2. The above binary will execute other binary.

```
devtoolslauncher.exe LaunchForDebug {PATH_ABSOLUTE:.exe} "{CMD:args}" test
```

   - Use case: Execute any binary with given arguments.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: CMD
