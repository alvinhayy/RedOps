---
title: "OpenConsole.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/OpenConsole/
fetched_at: 2026-09-20T17:15:12Z
license: unspecified
category: windows
---

Console Window host for Windows Terminal

## Paths
- C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\CommonExtensions\Microsoft\Terminal\ServiceHub\os64\OpenConsole.exe
- C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\CommonExtensions\Microsoft\Terminal\ServiceHub\os86\OpenConsole.exe
- C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\Terminal\ServiceHub\os64\OpenConsole.exe
- C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_1.18.10301.0_x64__8wekyb3d8bbwe\OpenConsole.exe

## Resources
- [https://twitter.com/nas_bench/status/1537563834478645252](https://twitter.com/nas_bench/status/1537563834478645252)

## Acknowledgements
- Nasreddine Bencherchali ([@nas_bench](https://twitter.com/@nas_bench))

## Detections
- IOC: OpenConsole.exe spawning unexpected processes
- Sigma: [https://github.com/SigmaHQ/sigma/blob/9e0ef7251b075f15e7abafbbec16d3230c5fa477/rules/windows/process_creation/proc_creation_win_lolbin_openconsole.yml](https://github.com/SigmaHQ/sigma/blob/9e0ef7251b075f15e7abafbbec16d3230c5fa477/rules/windows/process_creation/proc_creation_win_lolbin_openconsole.yml)

## Execute

1. Execute specified process with OpenConsole.exe as parent process

```
OpenConsole.exe {PATH:.exe}
```

   - Use case: Use OpenConsole.exe as a proxy binary to evade defensive counter-measures

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: EXE
