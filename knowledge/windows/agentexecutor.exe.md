---
title: "AgentExecutor.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Agentexecutor/
fetched_at: 2026-09-20T17:14:19Z
license: unspecified
category: windows
---

Intune Management Extension included on Intune Managed Devices

## Paths
- C:\Program Files (x86)\Microsoft Intune Management Extension\AgentExecutor.exe

## Acknowledgements
- Eleftherios Panos ([@lefterispan](https://twitter.com/@lefterispan))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_agentexecutor.yml](https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_agentexecutor.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_agentexecutor_susp_usage.yml](https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_agentexecutor_susp_usage.yml)

## Execute

1. Spawns powershell.exe and executes a provided powershell script with ExecutionPolicy Bypass argument

```
AgentExecutor.exe -powershell "{PATH_ABSOLUTE:.ps1}" "{PATH_ABSOLUTE:.1.log}" "{PATH_ABSOLUTE:.2.log}" "{PATH_ABSOLUTE:.3.log}" 60000 "C:\Windows\SysWOW64\WindowsPowerShell\v1.0" 0 1
```

   - Use case: Execute unsigned powershell scripts

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1218

   - Tags: Execute: PowerShell

2. If we place a binary named powershell.exe in the specified folder path, agentexecutor.exe will execute it successfully

```
AgentExecutor.exe -powershell "{PATH_ABSOLUTE:.ps1}" "{PATH_ABSOLUTE:.1.log}" "{PATH_ABSOLUTE:.2.log}" "{PATH_ABSOLUTE:.3.log}" 60000 "{PATH_ABSOLUTE:folder}" 0 1
```

   - Use case: Execute a provided EXE

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1218

   - Tags: Execute: EXE
