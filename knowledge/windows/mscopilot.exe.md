---
title: "Mscopilot.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Mscopilot/
fetched_at: 2026-09-20T17:15:01Z
license: unspecified
category: windows
---

Microsoft Copilot app

## Paths
- C:\Program Files (x86)\Microsoft\Copilot\Application\mscopilot.exe

## Resources
- [https://github.com/4n4s4zi/tour-de-mscopilot](https://github.com/4n4s4zi/tour-de-mscopilot)

## Acknowledgements
- 4n4s4zi ([@4n4s4zi](https://twitter.com/@4n4s4zi))

## Execute

1. mscopilot.exe will spawn the provided command. Parent mscopilot.exe process needs to be killed to avoid command being executed an infinite number of times.

```
mscopilot.exe --no-startup-window --disable-gpu-sandbox --gpu-launcher="{CMD} && taskkill /f /im mscopilot.exe &&"
```

   - Use case: Executes a process under a trusted Microsoft signed binary

   - Privileges required: User

   - Operating systems: Windows 11

   - ATT&CK® technique: T1218.015

   - Tags: Execute: CMD
