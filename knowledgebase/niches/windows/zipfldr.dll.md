---
title: "Zipfldr.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Zipfldr/
fetched_at: 2026-09-20T17:16:28Z
license: unspecified
category: windows
---

Compressed Folder library

## Paths
- c:\windows\system32\zipfldr.dll
- c:\windows\syswow64\zipfldr.dll

## Resources
- [https://twitter.com/moriarty_meng/status/977848311603380224](https://twitter.com/moriarty_meng/status/977848311603380224)
- [https://twitter.com/bohops/status/997896811904929792](https://twitter.com/bohops/status/997896811904929792)
- [https://windows10dll.nirsoft.net/zipfldr_dll.html](https://windows10dll.nirsoft.net/zipfldr_dll.html)

## Acknowledgements
- Moriarty (Execution) ([@moriarty_meng](https://twitter.com/@moriarty_meng))
- r0lan (Obfuscation) ([@r0lan](https://twitter.com/@r0lan))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)

## Execute

1. Launch an executable payload by calling RouteTheCall.

```
rundll32.exe zipfldr.dll,RouteTheCall {PATH:.exe}
```

   - Use case: Launch an executable.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: EXE

2. Launch an executable payload by calling RouteTheCall (obfuscated).

```
rundll32.exe zipfldr.dll,RouteTheCall file://^C^:^/^W^i^n^d^o^w^s^/^s^y^s^t^e^m^3^2^/^c^a^l^c^.^e^x^e
```

   - Use case: Launch an executable.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: EXE
