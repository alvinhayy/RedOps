---
title: "FsiAnyCpu.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/FsiAnyCpu/
fetched_at: 2026-09-20T17:14:51Z
license: unspecified
category: windows
---

32/64-bit FSharp (F#) Interpreter included with Visual Studio.

## Paths
- c:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\FSharp\fsianycpu.exe

## Resources
- [https://bohops.com/2020/11/02/exploring-the-wdac-microsoft-recommended-block-rules-part-ii-wfc-fsi/](https://bohops.com/2020/11/02/exploring-the-wdac-microsoft-recommended-block-rules-part-ii-wfc-fsi/)

## Acknowledgements
- Nick Tyrer ([@NickTyrer](https://twitter.com/@NickTyrer))
- Jimmy ([@bohops](https://twitter.com/@bohops))

## Detections
- BlockRule: [https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)
- IOC: FsiAnyCpu.exe execution may be suspicious on non-developer machines
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6b34764215b0e97e32cbc4c6325fc933d2695c3a/rules/windows/process_creation/proc_creation_win_lolbin_fsharp_interpreters.yml](https://github.com/SigmaHQ/sigma/blob/6b34764215b0e97e32cbc4c6325fc933d2695c3a/rules/windows/process_creation/proc_creation_win_lolbin_fsharp_interpreters.yml)

## AWL bypass

1. Execute F# code via script file

```
fsianycpu.exe {PATH:.fsscript}
```

   - Use case: Execute payload with Microsoft signed binary to bypass WDAC policies

   - Privileges required: User

   - Operating systems: Windows 10 2004 (likely previous and newer versions as well)

   - ATT&CK® technique: T1059

   - Tags: Execute: FSharp

2. Execute F# code via interactive command line

```
fsianycpu.exe
```

   - Use case: Execute payload with Microsoft signed binary to bypass WDAC policies

   - Privileges required: User

   - Operating systems: Windows 10 2004 (likely previous and newer versions as well)

   - ATT&CK® technique: T1059

   - Tags: Execute: FSharp
