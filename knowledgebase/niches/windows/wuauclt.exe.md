---
title: "wuauclt.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Wuauclt/
fetched_at: 2026-09-20T17:12:08Z
license: unspecified
category: windows
---

Windows Update Client

## Paths
- C:\Windows\System32\wuauclt.exe
- C:\Windows\UUS\amd64\wuauclt.exe

## Resources
- [https://dtm.uk/wuauclt/](https://dtm.uk/wuauclt/)

## Acknowledgements
- David Middlehurst ([@dtmsecurity](https://twitter.com/@dtmsecurity))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/network_connection/net_connection_win_wuauclt_network_connection.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/network_connection/net_connection_win_wuauclt_network_connection.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_wuauclt.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_wuauclt.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_wuauclt_execution.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_wuauclt_execution.yml)
- IOC: wuauclt run with a parameter of a DLL path
- IOC: Suspicious wuauclt Internet/network connections

## Execute

1. Loads and executes DLL code on attach.

```
wuauclt.exe /UpdateDeploymentProvider {PATH_ABSOLUTE:.dll} /RunHandlerComServer
```

   - Use case: Execute dll via attach/detach methods

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1218

   - Tags: Execute: DLL
