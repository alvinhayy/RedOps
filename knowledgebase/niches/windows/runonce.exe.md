---
title: "Runonce.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Runonce/
fetched_at: 2026-09-20T17:11:28Z
license: unspecified
category: windows
---

Executes a Run Once Task that has been configured in the registry

## Paths
- C:\Windows\System32\runonce.exe
- C:\Windows\SysWOW64\runonce.exe

## Resources
- [https://twitter.com/pabraeken/status/990717080805789697](https://twitter.com/pabraeken/status/990717080805789697)
- [https://cmatskas.com/configure-a-runonce-task-on-windows/](https://cmatskas.com/configure-a-runonce-task-on-windows/)

## Acknowledgements
- Pierre-Alexandre Braeken ([@pabraeken](https://twitter.com/@pabraeken))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/registry/registry_event/registry_event_runonce_persistence.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/registry/registry_event/registry_event_runonce_persistence.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_runonce_execution.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_runonce_execution.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/2926e98c5d998706ef7e248a63fb0367c841f685/rules/windows/persistence_run_key_and_startup_broad.toml](https://github.com/elastic/detection-rules/blob/2926e98c5d998706ef7e248a63fb0367c841f685/rules/windows/persistence_run_key_and_startup_broad.toml)
- IOC: Registy key add - HKLM\SOFTWARE\Microsoft\Active Setup\Installed Components\YOURKEY

## Execute

1. Executes a Run Once Task that has been configured in the registry.

```
Runonce.exe /AlternateShellStartup
```

   - Use case: Persistence, bypassing defensive counter measures

   - Privileges required: Administrator

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: CMD
