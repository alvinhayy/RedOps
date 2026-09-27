---
title: "Syssetup.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Syssetup/
fetched_at: 2026-09-20T17:16:25Z
license: unspecified
category: windows
---

Windows NT System Setup

## Paths
- c:\windows\system32\syssetup.dll
- c:\windows\syswow64\syssetup.dll

## Resources
- [https://twitter.com/pabraeken/status/994392481927258113](https://twitter.com/pabraeken/status/994392481927258113)
- [https://twitter.com/harr0ey/status/975350238184697857](https://twitter.com/harr0ey/status/975350238184697857)
- [https://twitter.com/bohops/status/975549525938135040](https://twitter.com/bohops/status/975549525938135040)
- [https://windows10dll.nirsoft.net/syssetup_dll.html](https://windows10dll.nirsoft.net/syssetup_dll.html)

## Acknowledgements
- Pierre-Alexandre Braeken (Execute) ([@pabraeken](https://twitter.com/@pabraeken))
- Matt harr0ey (Execute) ([@harr0ey](https://twitter.com/@harr0ey))
- Jimmy (Scriptlet) ([@bohops](https://twitter.com/@bohops))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)
- Splunk: [https://github.com/splunk/security_content/blob/86a5b644a44240f01274c8b74d19a435c7dae66e/detections/endpoint/detect_rundll32application_control_bypass__syssetup.yml](https://github.com/splunk/security_content/blob/86a5b644a44240f01274c8b74d19a435c7dae66e/detections/endpoint/detect_rundll32_application_control_bypass___syssetup.yml)

## AWL bypass

1. Execute the specified (local or remote) .wsh/.sct script with scrobj.dll in the .inf file by calling an information file directive (section name specified).

```
rundll32 syssetup.dll,SetupInfObjectInstallAction DefaultInstall 128 {PATH_ABSOLUTE:.inf}
```

   - Use case: Run local or remote script(let) code through INF file specification (Note May pop an error window).

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: INF

2. Launch an executable file via the SetupInfObjectInstallAction function and .inf file section directive.

```
rundll32 syssetup.dll,SetupInfObjectInstallAction DefaultInstall 128 {PATH_ABSOLUTE:.inf}
```

   - Use case: Load an executable payload.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: INF
