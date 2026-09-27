---
title: "ntdsutil.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Ntdsutil/
fetched_at: 2026-09-20T17:15:10Z
license: unspecified
category: windows
---

Command line utility used to export Active Directory.

## Paths
- C:\Windows\System32\ntdsutil.exe

## Resources
- [https://adsecurity.org/?p=2398#CreateIFM](https://adsecurity.org/?p=2398#CreateIFM)

## Acknowledgements
- Sean Metcalf ([@PyroTek3](https://twitter.com/@PyroTek3))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_ntdsutil_usage.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_ntdsutil_usage.yml)
- Splunk: [https://github.com/splunk/security_content/blob/2b87b26bdc2a84b65b1355ffbd5174bdbdb1879c/detections/endpoint/ntdsutil_export_ntds.yml](https://github.com/splunk/security_content/blob/2b87b26bdc2a84b65b1355ffbd5174bdbdb1879c/detections/endpoint/ntdsutil_export_ntds.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/5bdf70e72c6cd4547624c521108189af994af449/rules/windows/credential_access_cmdline_dump_tool.toml](https://github.com/elastic/detection-rules/blob/5bdf70e72c6cd4547624c521108189af994af449/rules/windows/credential_access_cmdline_dump_tool.toml)
- IOC: ntdsutil.exe with command line including "ifm"

## Dump

1. Dump NTDS.dit into folder

```
ntdsutil.exe "ac i ntds" "ifm" "create full c:\" q q
```

   - Use case: Dumping of Active Directory NTDS.dit database

   - Privileges required: Administrator

   - Operating systems: Windows

   - ATT&CK® technique: T1003.003
