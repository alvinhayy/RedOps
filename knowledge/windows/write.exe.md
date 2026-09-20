---
title: "write.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/write/
fetched_at: 2026-09-20T17:12:16Z
license: unspecified
category: windows
---

Windows Write

## Paths
- C:\Windows\write.exe
- C:\Windows\System32\write.exe
- C:\Windows\SysWOW64\write.exe

## Resources
- [https://gist.github.com/mblzk/b8c5ff7c2bd0fb2b385cc2fdd119874b](https://gist.github.com/mblzk/b8c5ff7c2bd0fb2b385cc2fdd119874b)

## Acknowledgements
- Michal Belzak

## Detections
- IOC: Changes to HKCU:\Software\Microsoft\Windows\CurrentVersion\App Paths\wordpad.exe
- Sigma: [https://github.com/SigmaHQ/sigma/blob/master/rules/windows/registry/registry_set/registry_set_persistence_app_paths.yml](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/registry/registry_set/registry_set_persistence_app_paths.yml)

## Execute

1. Executes a binary provided in default value of HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\wordpad.exe.

```
write.exe
```

   - Use case: Execute binary through legitimate proxy. This might be utilized to confuse detection solutions that rely on parent-child relationships.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11 (before 24H2)

   - ATT&CK® technique: T1218

   - Tags: Execute: EXERequires: Registry Change
