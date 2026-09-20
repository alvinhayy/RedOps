---
title: "Advpack.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Advpack/
fetched_at: 2026-09-20T17:16:07Z
license: unspecified
category: windows
---

Utility for installing software and drivers with rundll32.exe

## Paths
- c:\windows\system32\advpack.dll
- c:\windows\syswow64\advpack.dll

## Resources
- [https://bohops.com/2018/02/26/leveraging-inf-sct-fetch-execute-techniques-for-bypass-evasion-persistence/](https://bohops.com/2018/02/26/leveraging-inf-sct-fetch-execute-techniques-for-bypass-evasion-persistence/)
- [https://twitter.com/ItsReallyNick/status/967859147977850880](https://twitter.com/ItsReallyNick/status/967859147977850880)
- [https://twitter.com/bohops/status/974497123101179904](https://twitter.com/bohops/status/974497123101179904)
- [https://twitter.com/moriarty_meng/status/977848311603380224](https://twitter.com/moriarty_meng/status/977848311603380224)

## Acknowledgements
- Jimmy (LaunchINFSection) ([@bohops](https://twitter.com/@bohops))
- Fabrizio (RegisterOCX - DLL) ([@0rbz_](https://twitter.com/@0rbz_))
- Moriarty (RegisterOCX - CMD) ([@moriarty_meng](https://twitter.com/@moriarty_meng))
- Nick Carr (Threat Intel) ([@ItsReallyNick](https://twitter.com/@ItsReallyNick))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)
- Splunk: [https://github.com/splunk/security_content/blob/86a5b644a44240f01274c8b74d19a435c7dae66e/detections/endpoint/detect_rundll32application_control_bypass__advpack.yml](https://github.com/splunk/security_content/blob/86a5b644a44240f01274c8b74d19a435c7dae66e/detections/endpoint/detect_rundll32_application_control_bypass___advpack.yml)

## AWL bypass

1. Execute the specified (local or remote) .wsh/.sct script with scrobj.dll in the .inf file by calling an information file directive (section name specified).

```
rundll32.exe advpack.dll,LaunchINFSection {PATH:.inf},DefaultInstall_SingleUser,1,
```

   - Use case: Run local or remote script(let) code through INF file specification.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: INF

2. Execute the specified (local or remote) .wsh/.sct script with scrobj.dll in the .inf file by calling an information file directive (DefaultInstall section implied).

```
rundll32.exe advpack.dll,LaunchINFSection {PATH:.inf},,1,
```

   - Use case: Run local or remote script(let) code through INF file specification.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: INF

3. Launch a DLL payload by calling the RegisterOCX function.

```
rundll32.exe advpack.dll,RegisterOCX {PATH:.dll}
```

   - Use case: Load a DLL payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: DLL

4. Launch an executable by calling the RegisterOCX function.

```
rundll32.exe advpack.dll,RegisterOCX {PATH:.exe}
```

   - Use case: Run an executable payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: EXE

5. Launch command line by calling the RegisterOCX function.

```
rundll32 advpack.dll, RegisterOCX {CMD}
```

   - Use case: Run an executable payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: CMD
