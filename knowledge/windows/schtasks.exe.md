---
title: "Schtasks.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Schtasks/
fetched_at: 2026-09-20T17:11:32Z
license: unspecified
category: windows
---

Schedule periodic tasks

## Paths
- c:\windows\system32\schtasks.exe
- c:\windows\syswow64\schtasks.exe

## Resources
- [https://isc.sans.edu/forums/diary/Adding+Persistence+Via+Scheduled+Tasks/23633/](https://isc.sans.edu/forums/diary/Adding+Persistence+Via+Scheduled+Tasks/23633/)

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_schtasks_creation.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_schtasks_creation.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/ef7548f04c4341e0d1a172810330d59453f46a21/rules/windows/persistence_local_scheduled_task_creation.toml](https://github.com/elastic/detection-rules/blob/ef7548f04c4341e0d1a172810330d59453f46a21/rules/windows/persistence_local_scheduled_task_creation.toml)
- Splunk: [https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/schtasks_scheduling_job_on_remote_system.yml](https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/schtasks_scheduling_job_on_remote_system.yml)
- IOC: Suspicious task creation events

## Execute

1. Create a recurring task to execute every minute.

```
schtasks /create /sc minute /mo 1 /tn "Reverse shell" /tr "{CMD}"
```

   - Use case: Create a recurring task to keep reverse shell session(s) alive

   - Privileges required: User

   - Operating systems: Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1053.005

   - Tags: Execute: CMD

2. Create a scheduled task on a remote computer for persistence/lateral movement

```
schtasks /create /s targetmachine /tn "MyTask" /tr "{CMD}" /sc daily
```

   - Use case: Create a remote task to run daily relative to the the time of creation

   - Privileges required: Administrator

   - Operating systems: Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1053.005

   - Tags: Execute: CMD
