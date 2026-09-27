---
title: "Sigverif.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Sigverif/
fetched_at: 2026-09-20T17:11:40Z
license: unspecified
category: windows
---

File Signature Verification utility to verify digital signatures of files

## Paths
- C:\Windows\System32\sigverif.exe
- C:\Windows\SysWOW64\sigverif.exe

## Resources
- [https://twitter.com/0gtweet/status/1457676633809330184](https://twitter.com/0gtweet/status/1457676633809330184)
- [https://www.hexacorn.com/blog/2018/04/27/i-shot-the-sigverif-exe-the-gui-based-lolbin/](https://www.hexacorn.com/blog/2018/04/27/i-shot-the-sigverif-exe-the-gui-based-lolbin/)

## Acknowledgements
- Grzegorz Tworek ([@0gtweet](https://twitter.com/@0gtweet))
- Adam ([@Hexacorn](https://twitter.com/@Hexacorn))

## Detections
- IOC: sigverif.exe spawning unexpected child processes

## Execute

1. Launch sigverif.exe GUI, click ‘Advanced’, specify arbitrary executable path as ‘log file name’, then click ‘View Log’ to execute the binary.

```
sigverif.exe
```

   - Use case: Execute arbitrary programs through a trusted Microsoft-signed binary to bypass application whitelisting.

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: EXEApplication: GUI
