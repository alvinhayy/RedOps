---
title: "Csc.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Csc/
fetched_at: 2026-09-20T17:09:45Z
license: unspecified
category: windows
---

Binary file used by .NET Framework to compile C# code

## Paths
- C:\Windows\Microsoft.NET\Framework\v4.0.30319\Csc.exe
- C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Csc.exe
- C:\Windows\Microsoft.NET\Framework\v3.5\csc.exe
- C:\Windows\Microsoft.NET\Framework64\v3.5\csc.exe
- C:\Windows\Microsoft.NET\Framework\v2.0.50727\csc.exe
- C:\Windows\Microsoft.NET\Framework64\v2.0.50727\csc.exe

## Resources
- [https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/)

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_csc_susp_parent.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_csc_susp_parent.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_csc_susp_folder.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_csc_susp_folder.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_dotnet_compiler_parent_process.toml](https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_dotnet_compiler_parent_process.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/82ec6ac1eeb62a1383792719a1943b551264ed16/rules/windows/defense_evasion_execution_msbuild_started_unusal_process.toml](https://github.com/elastic/detection-rules/blob/82ec6ac1eeb62a1383792719a1943b551264ed16/rules/windows/defense_evasion_execution_msbuild_started_unusal_process.toml)
- IOC: Csc.exe should normally not run as System account unless it is used for development.

## Compile

1. Use csc.exe to compile C# code, targeting the .NET Framework, stored in the specified .cs file and output the compiled version to the specified .exe path.

```
csc.exe -out:{PATH:.exe} {PATH:.cs}
```

   - Use case: Compile attacker code on system. Bypass defensive counter measures.

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1127

2. Use csc.exe to compile C# code, targeting the .NET Framework, stored in the specified .cs file and output the compiled version to a DLL file with the same name.

```
csc -target:library {PATH:.cs}
```

   - Use case: Compile attacker code on system. Bypass defensive counter measures.

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1127
