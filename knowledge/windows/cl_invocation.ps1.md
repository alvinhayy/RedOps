---
title: "CL_Invocation.ps1"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Scripts/Cl_invocation/
fetched_at: 2026-09-20T17:16:33Z
license: unspecified
category: windows
---

Aero diagnostics script

## Paths
- C:\Windows\diagnostics\system\AERO\CL_Invocation.ps1
- C:\Windows\diagnostics\system\Audio\CL_Invocation.ps1
- C:\Windows\diagnostics\system\WindowsUpdate\CL_Invocation.ps1

## Acknowledgements
- Jimmy ([@bohops](https://twitter.com/@bohops))
- Pierre-Alexandre Braeken ([@pabraeken](https://twitter.com/@pabraeken))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_cl_invocation.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_cl_invocation.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/powershell/powershell_script/posh_ps_cl_invocation_lolscript.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/powershell/powershell_script/posh_ps_cl_invocation_lolscript.yml)

## Execute

1. Import the PowerShell Diagnostic CL_Invocation script and call SyncInvoke to launch an executable.

```
. C:\Windows\diagnostics\system\AERO\CL_Invocation.ps1   \nSyncInvoke {CMD}
```

   - Use case: Proxy execution

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1216

   - Tags: Execute: CMD
