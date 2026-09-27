---
title: "vbc.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Vbc/
fetched_at: 2026-09-20T17:11:51Z
license: unspecified
category: windows
---

Binary file used for compile vbs code

## Paths
- C:\Windows\Microsoft.NET\Framework\v4.0.30319\vbc.exe
- C:\Windows\Microsoft.NET\Framework\v3.5\vbc.exe
- C:\Windows\Microsoft.NET\Framework\v2.0.50727\vbc.exe
- C:\Windows\Microsoft.NET\Framework64\v4.0.30319\vbc.exe
- C:\Windows\Microsoft.NET\Framework64\v3.5\vbc.exe
- C:\Windows\Microsoft.NET\Framework64\v2.0.50727\vbc.exe

## Acknowledgements
- Lior Adar
- Hai Vaknin(Lux)

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_visual_basic_compiler.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_visual_basic_compiler.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_dotnet_compiler_parent_process.toml](https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_dotnet_compiler_parent_process.toml)

## Compile

1. Binary file used by .NET to compile Visual Basic code to an executable.

```
vbc.exe /target:exe {PATH_ABSOLUTE:.vb}
```

   - Use case: Compile attacker code on system. Bypass defensive counter measures.

   - Privileges required: User

   - Operating systems: Windows 7, Windows 10, Windows 11

   - ATT&CK® technique: T1127

2. Binary file used by .NET to compile Visual Basic code to an executable.

```
vbc -reference:Microsoft.VisualBasic.dll {PATH_ABSOLUTE:.vb}
```

   - Use case: Compile attacker code on system. Bypass defensive counter measures.

   - Privileges required: User

   - Operating systems: Windows 7, Windows 10, Windows 11

   - ATT&CK® technique: T1127
