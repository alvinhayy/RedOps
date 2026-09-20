---
title: "Shell32.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Shell32/
fetched_at: 2026-09-20T17:16:22Z
license: unspecified
category: windows
---

Windows Shell Common Dll

## Paths
- c:\windows\system32\shell32.dll
- c:\windows\syswow64\shell32.dll

## Resources
- [https://twitter.com/Hexacorn/status/885258886428725250](https://twitter.com/Hexacorn/status/885258886428725250)
- [https://twitter.com/pabraeken/status/991768766898941953](https://twitter.com/pabraeken/status/991768766898941953)
- [https://twitter.com/mattifestation/status/776574940128485376](https://twitter.com/mattifestation/status/776574940128485376)
- [https://twitter.com/KyleHanslovan/status/905189665120149506](https://twitter.com/KyleHanslovan/status/905189665120149506)
- [https://windows10dll.nirsoft.net/shell32_dll.html](https://windows10dll.nirsoft.net/shell32_dll.html)
- [https://www.hexacorn.com/blog/2025/05/18/shell32-dll-44-lolbin/](https://www.hexacorn.com/blog/2025/05/18/shell32-dll-44-lolbin/)

## Acknowledgements
- Adam (Control_RunDLL, Control_RunDLLNoFallback) ([@hexacorn](https://twitter.com/@hexacorn))
- Pierre-Alexandre Braeken (ShellExec_RunDLL) ([@pabraeken](https://twitter.com/@pabraeken))
- Matt Graeber (ShellExec_RunDLL) ([@mattifestation](https://twitter.com/@mattifestation))
- Kyle Hanslovan (ShellExec_RunDLL) ([@KyleHanslovan](https://twitter.com/@KyleHanslovan))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)
- Splunk: [https://github.com/splunk/security_content/blob/a1afa0fa605639cbef7d528dec46ce7c8112194a/detections/endpoint/rundll32_control_rundll_hunt.yml](https://github.com/splunk/security_content/blob/a1afa0fa605639cbef7d528dec46ce7c8112194a/detections/endpoint/rundll32_control_rundll_hunt.yml)

## Execute

1. Launch a DLL payload by calling the Control_RunDLL function.

```
rundll32.exe shell32.dll,Control_RunDLL {PATH_ABSOLUTE:.dll}
```

   - Use case: Load a DLL payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: DLL

2. Launch an executable by calling the ShellExec_RunDLL function.

```
rundll32.exe shell32.dll,ShellExec_RunDLL {PATH:.exe}
```

   - Use case: Run an executable payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: EXE

3. Launch command line by calling the ShellExec_RunDLL function.

```
rundll32 SHELL32.DLL,ShellExec_RunDLL {PATH:.exe} {CMD:args}
```

   - Use case: Run an executable payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: CMD

4. Load a DLL/CPL by calling undocumented Control_RunDLLNoFallback function.

```
rundll32.exe shell32.dll,#44 {PATH:.dll}
```

   - Use case: Load a DLL/CPL payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: DLL
