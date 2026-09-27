---
title: "Jsc.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Jsc/
fetched_at: 2026-09-20T17:10:30Z
license: unspecified
category: windows
---

Binary file used by .NET to compile JavaScript code to .exe or .dll format

## Paths
- C:\Windows\Microsoft.NET\Framework\v4.0.30319\Jsc.exe
- C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Jsc.exe
- C:\Windows\Microsoft.NET\Framework\v2.0.50727\Jsc.exe
- C:\Windows\Microsoft.NET\Framework64\v2.0.50727\Jsc.exe

## Resources
- [https://twitter.com/DissectMalware/status/998797808907046913](https://twitter.com/DissectMalware/status/998797808907046913)
- [https://www.phpied.com/make-your-javascript-a-windows-exe/](https://www.phpied.com/make-your-javascript-a-windows-exe/)

## Acknowledgements
- Malwrologist ([@DissectMalware](https://twitter.com/@DissectMalware))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/35a7244c62820fbc5a832e50b1e224ac3a1935da/rules/windows/process_creation/proc_creation_win_lolbin_jsc.yml](https://github.com/SigmaHQ/sigma/blob/35a7244c62820fbc5a832e50b1e224ac3a1935da/rules/windows/process_creation/proc_creation_win_lolbin_jsc.yml)
- IOC: Jsc.exe should normally not run a system unless it is used for development.

## Compile

1. Use jsc.exe to compile JavaScript code stored in the provided .JS file and generate a .EXE file with the same name.

```
jsc.exe {PATH:.js}
```

   - Use case: Compile attacker code on system. Bypass defensive counter measures.

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: JScript

2. Use jsc.exe to compile JavaScript code stored in the .JS file and generate a DLL file with the same name.

```
jsc.exe /t:library {PATH:.js}
```

   - Use case: Compile attacker code on system. Bypass defensive counter measures.

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: JScript
