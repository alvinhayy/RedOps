---
title: "Setres.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Setres/
fetched_at: 2026-09-20T17:11:36Z
license: unspecified
category: windows
---

Configures display settings

## Paths
- c:\windows\system32\setres.exe

## Resources
- [https://twitter.com/0gtweet/status/1583356502340870144](https://twitter.com/0gtweet/status/1583356502340870144)

## Acknowledgements
- Grzegorz Tworek ([@0gtweet](https://twitter.com/@0gtweet))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_setres.yml](https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_setres.yml)
- IOC: Unusual location for choice.exe file
- IOC: Process created from choice.com binary
- IOC: Existence of choice.cmd file

## Execute

1. Sets the resolution and then launches ‘choice’ command from the working directory.

```
setres.exe -w 800 -h 600
```

   - Use case: Executes arbitrary code

   - Privileges required: User

   - Operating systems: Windows Server 2012, Windows Server 2016, Windows Server 2019, Windows Server 2022

   - ATT&CK® technique: T1218

   - Tags: Execute: EXE
