---
title: "Mscopilot_proxy.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Mscopilot_proxy/
fetched_at: 2026-09-20T17:15:02Z
license: unspecified
category: windows
---

Microsoft Copilot proxy launcher

## Paths
- C:\Program Files (x86)\Microsoft\Copilot\Application\mscopilot_proxy.exe

## Resources
- [https://github.com/4n4s4zi/tour-de-mscopilot](https://github.com/4n4s4zi/tour-de-mscopilot)

## Acknowledgements
- 4n4s4zi ([@4n4s4zi](https://twitter.com/@4n4s4zi))

## Execute

1. mscopilot_proxy.exe will spawn the provided command. Parent mscopilot_proxy.exe process needs to be killed to avoid command being executed an infinite number of times.

```
mscopilot_proxy.exe --no-startup-window --disable-gpu-sandbox --gpu-launcher="cmd.exe /c calc.exe && taskkill /f /im mscopilot.exe &&"
```

   - Use case: Executes a process under a trusted Microsoft signed binary

   - Privileges required: User

   - Operating systems: Windows 11

   - ATT&CK® technique: T1218.015

   - Tags: Execute: CMD
