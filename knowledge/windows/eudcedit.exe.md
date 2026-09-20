---
title: "Eudcedit.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Eudcedit/
fetched_at: 2026-09-20T17:10:01Z
license: unspecified
category: windows
---

Private Character Editor Windows Utility

## Paths
- c:\windows\system32\eudcedit.exe
- c:\windows\syswow64\eudcedit.exe

## Resources
- [https://medium.com/@matanb707/windows-fonts-exploitation-in-2025-bypassing-uac-with-eudcedit-915599705639](https://medium.com/@matanb707/windows-fonts-exploitation-in-2025-bypassing-uac-with-eudcedit-915599705639)

## Acknowledgements
- Matan Bahar ([@Bl4ckShad3](https://twitter.com/@Bl4ckShad3))

## Detections
- IOC: Processes spawned by eudcedit.exe.

## UAC bypass

1. Once executed, the Private Charecter Editor will be opened - click OK, then click File -> Font Links. In the next window choose the option “Link with Selected Fonts” and click on Save As, then in the opened enter the command you want to execute.

```
eudcedit
```

   - Use case: Execute a binary or script as a high-integrity process without a UAC prompt.

   - Privileges required: Administrator

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1548.002

   - Tags: Execute: CMDApplication: GUI
