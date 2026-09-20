---
title: "devtunnel.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/devtunnels/
fetched_at: 2026-09-20T17:15:57Z
license: unspecified
category: windows
---

Binary to enable forwarded ports on windows operating systems.

## Paths
- C:\Users\<username>\AppData\Local\Temp\.net\devtunnel\devtunnel.exe
- C:\Users\<username>\AppData\Local\Temp\DevTunnels\devtunnel.exe

## Resources
- [https://code.visualstudio.com/docs/editor/port-forwarding](https://code.visualstudio.com/docs/editor/port-forwarding)

## Acknowledgements
- Kamran Saifullah ([@deFr0ggy](https://twitter.com/@deFr0ggy))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/dns_query/dns_query_win_devtunnels_communication.yml](https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/dns_query/dns_query_win_devtunnels_communication.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/network_connection/net_connection_win_domain_devtunnels.yml](https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/network_connection/net_connection_win_domain_devtunnels.yml)
- IOC: devtunnel.exe binary spawned
- IOC: *.devtunnels.ms
- IOC: ..devtunnels.ms
- Analysis: [https://cydefops.com/vscode-data-exfiltration](https://cydefops.com/vscode-data-exfiltration)

## Download

1. Enabling a forwarded port for locally hosted service at port 8080 to be exposed on the internet.

```
devtunnel.exe host -p 8080
```

   - Use case: Download Files, Upload Files, Data Exfiltration

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11, MacOS

   - ATT&CK® technique: T1105
