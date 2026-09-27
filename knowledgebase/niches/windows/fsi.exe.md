---
title: "Fsi.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Fsi/
fetched_at: 2026-09-20T17:14:50Z
license: unspecified
category: windows
---

64-bit FSharp (F#) Interpreter included with Visual Studio and DotNet Core SDK.

## Paths
- C:\Program Files\dotnet\sdk\<version>\FSharp\fsi.exe
- C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\FSharp\fsi.exe

## Resources
- [https://twitter.com/NickTyrer/status/904273264385589248](https://twitter.com/NickTyrer/status/904273264385589248)
- [https://bohops.com/2020/11/02/exploring-the-wdac-microsoft-recommended-block-rules-part-ii-wfc-fsi/](https://bohops.com/2020/11/02/exploring-the-wdac-microsoft-recommended-block-rules-part-ii-wfc-fsi/)

## Acknowledgements
- Nick Tyrer ([@NickTyrer](https://twitter.com/@NickTyrer))
- Jimmy ([@bohops](https://twitter.com/@bohops))

## Detections
- Elastic: [https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_unusual_process_network_connection.toml](https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_unusual_process_network_connection.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_network_connection_from_windows_binary.toml](https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_network_connection_from_windows_binary.toml)
- BlockRule: [https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)
- IOC: Fsi.exe execution may be suspicious on non-developer machines
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6b34764215b0e97e32cbc4c6325fc933d2695c3a/rules/windows/process_creation/proc_creation_win_lolbin_fsharp_interpreters.yml](https://github.com/SigmaHQ/sigma/blob/6b34764215b0e97e32cbc4c6325fc933d2695c3a/rules/windows/process_creation/proc_creation_win_lolbin_fsharp_interpreters.yml)

## AWL bypass

1. Execute F# code via script file

```
fsi.exe {PATH:.fsscript}
```

   - Use case: Execute payload with Microsoft signed binary to bypass WDAC policies

   - Privileges required: User

   - Operating systems: Windows 10 2004 (likely previous and newer versions as well)

   - ATT&CK® technique: T1059

   - Tags: Execute: FSharp

2. Execute F# code via interactive command line

```
fsi.exe
```

   - Use case: Execute payload with Microsoft signed binary to bypass WDAC policies

   - Privileges required: User

   - Operating systems: Windows 10 2004 (likely previous and newer versions as well)

   - ATT&CK® technique: T1059

   - Tags: Execute: FSharp
