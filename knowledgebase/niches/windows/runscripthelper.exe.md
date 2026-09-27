---
title: "Runscripthelper.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Runscripthelper/
fetched_at: 2026-09-20T17:11:30Z
license: unspecified
category: windows
---

Execute target PowerShell script

## Paths
- C:\Windows\WinSxS\amd64_microsoft-windows-u..ed-telemetry-client_31bf3856ad364e35_10.0.16299.15_none_c2df1bba78111118\Runscripthelper.exe
- C:\Windows\WinSxS\amd64_microsoft-windows-u..ed-telemetry-client_31bf3856ad364e35_10.0.16299.192_none_ad4699b571e00c4a\Runscripthelper.exe

## Resources
- [https://posts.specterops.io/bypassing-application-whitelisting-with-runscripthelper-exe-1906923658fc](https://posts.specterops.io/bypassing-application-whitelisting-with-runscripthelper-exe-1906923658fc)

## Acknowledgements
- Matt Graeber ([@mattifestation](https://twitter.com/@mattifestation))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_runscripthelper.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_runscripthelper.yml)
- BlockRule: [https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)
- IOC: Event ID 4104 - Microsoft-Windows-PowerShell/Operational
- IOC: Event ID 400 - Windows PowerShell

## Execute

1. Execute the PowerShell script with .txt extension

```
runscripthelper.exe surfacecheck \\?\{PATH_ABSOLUTE:.txt} {PATH_ABSOLUTE:folder}
```

   - Use case: Bypass constrained language mode and execute Powershell script

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10

   - ATT&CK® technique: T1218

   - Tags: Execute: PowerShell
