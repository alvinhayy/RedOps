---
title: "Mofcomp.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Mofcomp/
fetched_at: 2026-09-20T17:10:38Z
license: unspecified
category: windows
---

Compiler that parses a file containing MOF statements and adds the classes and class instances defined in the file to the WMI repository. Threat actors can leverage this binary to install malicious MOF scripts

## Paths
- C:\Windows\System32\wbem\mofcomp.exe
- C:\Windows\SysWOW64\wbem\mofcomp.exe

## Resources
- [https://docs.microsoft.com/en-us/windows/win32/wmisdk/mofcomp](https://docs.microsoft.com/en-us/windows/win32/wmisdk/mofcomp)
- [https://docs.microsoft.com/en-us/windows/win32/wmisdk/managed-object-format--mof-](https://docs.microsoft.com/en-us/windows/win32/wmisdk/managed-object-format--mof-)
- [https://thedfirreport.com/2022/07/11/select-xmrig-from-sqlserver/](https://thedfirreport.com/2022/07/11/select-xmrig-from-sqlserver/)
- [https://in.security/2019/04/03/an-intro-into-abusing-and-identifying-wmi-event-subscriptions-for-persistence/](https://in.security/2019/04/03/an-intro-into-abusing-and-identifying-wmi-event-subscriptions-for-persistence/)
- [https://medium.com/threatpunter/detecting-removing-wmi-persistence-60ccbb7dff96](https://medium.com/threatpunter/detecting-removing-wmi-persistence-60ccbb7dff96)

## Acknowledgements
- Daniel Gott ([@gott_cyber](https://twitter.com/@gott_cyber))
- The DFIR Report ([@TheDFIRReport](https://twitter.com/@TheDFIRReport))
- Nasreddine Bencherchali ([@nas_bench](https://twitter.com/@nas_bench))

## Detections
- IOC: strange parent processes spawning mofcomp.exe like cmd.exe or powershell.exe
- Sigma: [https://github.com/The-DFIR-Report/Sigma-Rules/blob/75260568a7ffe61b2458ca05f6f25914efb44337/win_mofcomp_execution.yml](https://github.com/The-DFIR-Report/Sigma-Rules/blob/75260568a7ffe61b2458ca05f6f25914efb44337/win_mofcomp_execution.yml)

## Execute

1. Abuse of mofcomp.exe to parse a file which contains MOF statements in order create new classes as part of the WMI repository

```
mofcomp.exe {PATH_ABSOLUTE:.mof}
```

   - Use case: Threat actors can use mofcomp.exe to register a malicious MOF file as a new class in the WMI repository

   - Privileges required: User

   - Operating systems: Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11, Windows Server 2008+

   - ATT&CK® technique: T1047

   - Tags: Execute: MOF
