---
title: "Nmcap.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Nmcap/
fetched_at: 2026-09-20T17:15:09Z
license: unspecified
category: windows
---

Command-line packet capture utility from Microsoft Network Monitor 3.x.

## Paths
- C:\Program Files\Microsoft Network Monitor 3\nmcap.exe
- C:\Program Files (x86)\Microsoft Network Monitor 3\nmcap.exe

## Resources
- [https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/network-monitor-3](https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/network-monitor-3)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Reconnaissance

1. Start capture on all network adapters and save to specified .cap (circular) file. Optionally, one can add:

```
nmcap.exe /network * /capture /file {PATH_ABSOLUTE:.cap}
```

   - Use case: Capture network traffic on windows to collect sensitive data.

   - Privileges required: Administrator

   - Operating systems: Windows

   - ATT&CK® technique: T1040
