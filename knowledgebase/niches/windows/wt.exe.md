---
title: "wt.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/wt/
fetched_at: 2026-09-20T17:12:17Z
license: unspecified
category: windows
---

Windows Terminal

## Paths
- C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_<version_packageid>\wt.exe

## Resources
- [https://twitter.com/nas_bench/status/1552100271668469761](https://twitter.com/nas_bench/status/1552100271668469761)

## Acknowledgements
- Nasreddine Bencherchali ([@nas_bench](https://twitter.com/@nas_bench))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_windows_terminal_susp_children.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_windows_terminal_susp_children.yml)

## Execute

1. Execute a command via Windows Terminal.

```
wt.exe {CMD}
```

   - Use case: Use wt.exe as a proxy binary to evade defensive counter-measures

   - Privileges required: User

   - Operating systems: Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD
