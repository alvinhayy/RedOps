---
title: "Ieadvpack.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Ieadvpack/
fetched_at: 2026-09-20T17:16:11Z
license: unspecified
category: windows
---

INF installer for Internet Explorer. Has much of the same functionality as advpack.dll.

## Paths
- c:\windows\system32\ieadvpack.dll
- c:\windows\syswow64\ieadvpack.dll

## Resources
- [https://bohops.com/2018/03/10/leveraging-inf-sct-fetch-execute-techniques-for-bypass-evasion-persistence-part-2/](https://bohops.com/2018/03/10/leveraging-inf-sct-fetch-execute-techniques-for-bypass-evasion-persistence-part-2/)
- [https://twitter.com/pabraeken/status/991695411902599168](https://twitter.com/pabraeken/status/991695411902599168)
- [https://twitter.com/0rbz_/status/974472392012689408](https://twitter.com/0rbz_/status/974472392012689408)

## Acknowledgements
- Jimmy (LaunchINFSection) ([@bohops](https://twitter.com/@bohops))
- Fabrizio (RegisterOCX - DLL) ([@0rbz_](https://twitter.com/@0rbz_))
- Pierre-Alexandre Braeken (RegisterOCX - CMD) ([@pabraeken](https://twitter.com/@pabraeken))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)
- Splunk: [https://github.com/splunk/security_content/blob/86a5b644a44240f01274c8b74d19a435c7dae66e/detections/endpoint/detect_rundll32application_control_bypass__advpack.yml](https://github.com/splunk/security_content/blob/86a5b644a44240f01274c8b74d19a435c7dae66e/detections/endpoint/detect_rundll32_application_control_bypass___advpack.yml)

## AWL bypass

1. Execute the specified (local or remote) .wsh/.sct script with scrobj.dll in the .inf file by calling an information file directive (section name specified).

```
rundll32.exe ieadvpack.dll,LaunchINFSection {PATH_ABSOLUTE:.inf},DefaultInstall_SingleUser,1,
```

   - Use case: Run local or remote script(let) code through INF file specification.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: INF

2. Execute the specified (local or remote) .wsh/.sct script with scrobj.dll in the .inf file by calling an information file directive (DefaultInstall section implied).

```
rundll32.exe ieadvpack.dll,LaunchINFSection {PATH_ABSOLUTE:.inf},,1,
```

   - Use case: Run local or remote script(let) code through INF file specification.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: INF

3. Launch a DLL payload by calling the RegisterOCX function.

```
rundll32.exe ieadvpack.dll,RegisterOCX {PATH:.dll}
```

   - Use case: Load a DLL payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: DLL

4. Launch an executable by calling the RegisterOCX function.

```
rundll32.exe ieadvpack.dll,RegisterOCX {PATH:.exe}
```

   - Use case: Run an executable payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: EXE

5. Launch command line by calling the RegisterOCX function.

```
rundll32 ieadvpack.dll, RegisterOCX {CMD}
```

   - Use case: Run an executable payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: CMD
