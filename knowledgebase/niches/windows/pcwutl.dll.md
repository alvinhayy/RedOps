---
title: "Pcwutl.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Pcwutl/
fetched_at: 2026-09-20T17:16:15Z
license: unspecified
category: windows
---

Microsoft HTML Viewer

## Paths
- c:\windows\system32\pcwutl.dll
- c:\windows\syswow64\pcwutl.dll

## Resources
- [https://twitter.com/harr0ey/status/989617817849876488](https://twitter.com/harr0ey/status/989617817849876488)
- [https://windows10dll.nirsoft.net/pcwutl_dll.html](https://windows10dll.nirsoft.net/pcwutl_dll.html)

## Acknowledgements
- Matt harr0ey ([@harr0ey](https://twitter.com/@harr0ey))

## Detections
- Analysis: [https://redcanary.com/threat-detection-report/techniques/rundll32/](https://redcanary.com/threat-detection-report/techniques/rundll32/)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)

## Execute

1. Launch executable by calling the LaunchApplication function.

```
rundll32.exe pcwutl.dll,LaunchApplication {PATH:.exe}
```

   - Use case: Launch an executable.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: EXE
