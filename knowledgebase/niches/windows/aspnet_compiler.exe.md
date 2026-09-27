---
title: "Aspnet_Compiler.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Aspnet_Compiler/
fetched_at: 2026-09-20T17:09:20Z
license: unspecified
category: windows
---

ASP.NET Compilation Tool

## Paths
- c:\Windows\Microsoft.NET\Framework\v4.0.30319\aspnet_compiler.exe
- c:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_compiler.exe

## Resources
- [https://ijustwannared.team/2020/08/01/the-curious-case-of-aspnet_compiler-exe/](https://ijustwannared.team/2020/08/01/the-curious-case-of-aspnet_compiler-exe/)
- [https://docs.microsoft.com/en-us/dotnet/api/system.web.compilation.buildprovider.generatecode?view=netframework-4.8](https://docs.microsoft.com/en-us/dotnet/api/system.web.compilation.buildprovider.generatecode?view=netframework-4.8)

## Acknowledgements
- cpl ([@cpl3h](https://twitter.com/@cpl3h))

## Detections
- BlockRule: [https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_lolbin_aspnet_compiler.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_lolbin_aspnet_compiler.yml)

## AWL bypass

1. Execute C# code with the Build Provider and proper folder structure in place.

```
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_compiler.exe -v none -p C:\users\cpl.internal\desktop\asptest\ -f C:\users\cpl.internal\desktop\asptest\none -u
```

   - Use case: Execute proxied payload with Microsoft signed binary to bypass application control solutions

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1127
