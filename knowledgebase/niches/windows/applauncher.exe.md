---
title: "AppLauncher.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/AppLauncher/
fetched_at: 2026-09-20T17:14:21Z
license: unspecified
category: windows
---

User Experience Virtualization tool that launches applications under monitoring to capture and synchronize user settings.

## Paths
- C:\Program Files\Windows Kits\10\Microsoft User Experience Virtualization\Management\AppLauncher.exe
- C:\Program Files (x86)\Windows Kits\10\Microsoft User Experience Virtualization\Management\AppLauncher.exe

## Resources
- [https://learn.microsoft.com/en-us/microsoft-desktop-optimization-pack/ue-v/uev-getting-started](https://learn.microsoft.com/en-us/microsoft-desktop-optimization-pack/ue-v/uev-getting-started)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Execute

1. Launches an executable via User Experience Virtualization tool.

```
AppLauncher.exe {PATH_ABSOLUTE:.exe}
```

   - Use case: Executes an executable under a trusted, Microsoft signed binary.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE
