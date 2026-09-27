---
title: "Vssadmin.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Vssadmin/
fetched_at: 2026-09-20T17:11:54Z
license: unspecified
category: windows
---

Volume Shadow Copy Service administrative command-line tool

## Paths
- C:\Windows\System32\vssadmin.exe

## Resources
- [https://attack.mitre.org/techniques/T1490/](https://attack.mitre.org/techniques/T1490/)
- [https://github.com/Neo23x0/Raccine](https://github.com/Neo23x0/Raccine)

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_susp_shadow_copies_deletion.yml](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_susp_shadow_copies_deletion.yml)

## Tamper

1. Delete all volume shadow copies on the host without prompting

```
vssadmin delete shadows /all /quiet
```

   - Use case: Destroy shadow copies to prevent file and system recovery, a technique commonly used by ransomware

   - Privileges required: Administrator

   - Operating systems: Windows 11, Windows 10, Windows Server

   - ATT&CK® technique: T1490
