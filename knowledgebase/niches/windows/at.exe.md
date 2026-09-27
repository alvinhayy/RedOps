---
title: "At.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/At/
fetched_at: 2026-09-20T17:09:21Z
license: unspecified
category: windows
---

Schedule periodic tasks

## Paths
- C:\WINDOWS\System32\At.exe
- C:\WINDOWS\SysWOW64\At.exe

## Resources
- [https://freddiebarrsmith.com/at.txt](https://freddiebarrsmith.com/at.txt)
- [https://sushant747.gitbooks.io/total-oscp-guide/privilege_escalation_windows.html](https://sushant747.gitbooks.io/total-oscp-guide/privilege_escalation_windows.html)
- [https://www.secureworks.com/blog/where-you-at-indicators-of-lateral-movement-using-at-exe-on-windows-7-systems](https://www.secureworks.com/blog/where-you-at-indicators-of-lateral-movement-using-at-exe-on-windows-7-systems)

## Acknowledgements
- Freddie Barr-Smith
- Riccardo Spolaor
- Mariano Graziano
- Xabier Ugarte-Pedrero

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_at_interactive_execution.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_at_interactive_execution.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/network/zeek/zeek_smb_converted_win_atsvc_task.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/network/zeek/zeek_smb_converted_win_atsvc_task.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/builtin/security/win_security_atsvc_task.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/builtin/security/win_security_atsvc_task.yml)
- IOC: C:\Windows\System32\Tasks\At1 (substitute 1 with subsequent number of at job)
- IOC: C:\Windows\Tasks\At1.job
- IOC: Registry Key - Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\At1.

## Execute

1. Create a recurring task to execute every day at a specific time.

```
C:\Windows\System32\at.exe 09:00 /interactive /every:m,t,w,th,f,s,su {CMD}
```

   - Use case: Create a recurring task, to eg. to keep reverse shell session(s) alive

   - Privileges required: Local Admin

   - Operating systems: Windows 7 or older

   - ATT&CK® technique: T1053.002

   - Tags: Execute: CMD
