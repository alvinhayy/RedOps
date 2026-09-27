---
title: "iediagcmd.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Iediagcmd/
fetched_at: 2026-09-20T17:10:22Z
license: unspecified
category: windows
---

Diagnostics Utility for Internet Explorer

## Paths
- C:\Program Files\Internet Explorer\iediagcmd.exe

## Resources
- [https://twitter.com/Hexacorn/status/1507516393859731456](https://twitter.com/Hexacorn/status/1507516393859731456)

## Acknowledgements
- Adam ([@hexacorn](https://twitter.com/@hexacorn))

## Detections
- Sigma: [https://github.com/manasmbellani/mycode_public/blob/master/sigma/rules/win_proc_creation_lolbin_iediagcmd.yml](https://github.com/manasmbellani/mycode_public/blob/master/sigma/rules/win_proc_creation_lolbin_iediagcmd.yml)
- IOC: Sysmon Event ID 1
- IOC: Execution of process iediagcmd.exe with /out could be suspicious

## Execute

1. Executes binary that is pre-planted at C:\test\system32\netsh.exe.

```
set windir=c:\test& cd "C:\Program Files\Internet Explorer\" & iediagcmd.exe /out:{PATH_ABSOLUTE:.cab}
```

   - Use case: Spawn a pre-planted executable from iediagcmd.exe.

   - Privileges required: User

   - Operating systems: Windows 10 1803, Windows 10 1703, Windows 10 22H1, Windows 10 22H2, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: EXE
