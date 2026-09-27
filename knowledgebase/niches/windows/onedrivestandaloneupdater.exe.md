---
title: "OneDriveStandaloneUpdater.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/OneDriveStandaloneUpdater/
fetched_at: 2026-09-20T17:10:55Z
license: unspecified
category: windows
---

OneDrive Standalone Updater

## Paths
- C:\Users\<username>\AppData\Local\Microsoft\OneDrive\OneDriveStandaloneUpdater.exe
- C:\Program Files\Microsoft OneDrive\OneDriveStandaloneUpdater.exe
- C:\Program Files (x86)\Microsoft OneDrive\OneDriveStandaloneUpdater.exe

## Resources
- [https://github.com/LOLBAS-Project/LOLBAS/pull/153](https://github.com/LOLBAS-Project/LOLBAS/pull/153)

## Acknowledgements
- Elliot Killick ([@elliotkillick](https://twitter.com/@elliotkillick))

## Detections
- IOC: HKCU\Software\Microsoft\OneDrive\UpdateOfficeConfig\UpdateRingSettingURLFromOC being set to a suspicious non-Microsoft controlled URL
- IOC: Reports of downloading from suspicious URLs in %localappdata%\OneDrive\setup\logs\StandaloneUpdate_*.log files
- Sigma: [https://github.com/SigmaHQ/sigma/blob/ff5102832031425f6eed011dd3a2e62653008c94/rules/windows/registry/registry_set/registry_set_lolbin_onedrivestandaloneupdater.yml](https://github.com/SigmaHQ/sigma/blob/ff5102832031425f6eed011dd3a2e62653008c94/rules/windows/registry/registry_set/registry_set_lolbin_onedrivestandaloneupdater.yml)

## Download

1. Download a file from the web address specified in HKCU\Software\Microsoft\OneDrive\UpdateOfficeConfig\UpdateRingSettingURLFromOC. ODSUUpdateXMLUrlFromOC and UpdateXMLUrlFromOC must be equal to non-empty string values in that same registry key. UpdateOfficeConfigTimestamp is a UNIX epoch time which must be set to a large QWORD such as 99999999999 (in decimal) to indicate the URL cache is good. The downloaded file will be in %localappdata%\OneDrive\StandaloneUpdater\PreSignInSettingsConfig.json.

```
OneDriveStandaloneUpdater
```

   - Use case: Download a file from the Internet without executing any anomalous executables with suspicious arguments

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1105
