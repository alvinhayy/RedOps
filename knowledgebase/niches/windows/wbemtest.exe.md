---
title: "wbemtest.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Wbemtest/
fetched_at: 2026-09-20T17:11:58Z
license: unspecified
category: windows
---

WMI/WBEM Test Binary

## Paths
- c:\windows\system32\wbem\wbemtest.exe

## Resources
- [https://saulpanders.github.io/2025/01/20/lolbas-wbemtest.html](https://saulpanders.github.io/2025/01/20/lolbas-wbemtest.html)

## Acknowledgements
- Paul Sanders ([@saulpanders](https://twitter.com/@saulpanders))

## Detections
- IOC: wbemtest.exe binary spawned

## Execute

1. Execute arbitary commands through WMI through a GUI managment interface for Web Based Enterprise Management testing (WBEM). Uses WMI to Create and instance of a Win32_Process WMI class with a commandline argument of the target command to spawn. Spawns a GUI so it requires interactive access. For a demo, see link to blog in resources.

```
wbemtest.exe
```

   - Use case: Execute arbitrary commands through WMI classes

   - Privileges required: Any

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1047

   - Tags: Application: GUIExecute: CMD
