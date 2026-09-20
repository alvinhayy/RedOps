---
title: "Control.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Control/
fetched_at: 2026-09-20T17:09:44Z
license: unspecified
category: windows
---

Binary used to launch controlpanel items in Windows

## Paths
- C:\Windows\System32\control.exe
- C:\Windows\SysWOW64\control.exe

## Resources
- [https://pentestlab.blog/2017/05/24/applocker-bypass-control-panel/](https://pentestlab.blog/2017/05/24/applocker-bypass-control-panel/)
- [https://www.contextis.com/resources/blog/applocker-bypass-registry-key-manipulation/](https://www.contextis.com/resources/blog/applocker-bypass-registry-key-manipulation/)
- [https://twitter.com/bohops/status/955659561008017409](https://twitter.com/bohops/status/955659561008017409)
- [https://docs.microsoft.com/en-us/windows/desktop/shell/executing-control-panel-items](https://docs.microsoft.com/en-us/windows/desktop/shell/executing-control-panel-items)
- [https://bohops.com/2018/01/23/loading-alternate-data-stream-ads-dll-cpl-binaries-to-bypass-applocker/](https://bohops.com/2018/01/23/loading-alternate-data-stream-ads-dll-cpl-binaries-to-bypass-applocker/)

## Acknowledgements
- Jimmy ([@bohops](https://twitter.com/@bohops))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules-emerging-threats/2021/Exploits/CVE-2021-40444/proc_creation_win_exploit_cve_2021_40444.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules-emerging-threats/2021/Exploits/CVE-2021-40444/proc_creation_win_exploit_cve_2021_40444.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_control_dll_load.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_control_dll_load.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_network_connection_from_windows_binary.toml](https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_network_connection_from_windows_binary.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/0875c1e4c4370ab9fbf453c8160bb5abc8ad95e7/rules/windows/defense_evasion_execution_control_panel_suspicious_args.toml](https://github.com/elastic/detection-rules/blob/0875c1e4c4370ab9fbf453c8160bb5abc8ad95e7/rules/windows/defense_evasion_execution_control_panel_suspicious_args.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_unusual_dir_ads.toml](https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_unusual_dir_ads.toml)
- IOC: Control.exe executing files from alternate data streams
- IOC: Control.exe executing library file without cpl extension
- IOC: Suspicious network connections from control.exe

## Alternate data streams

1. Execute evil.dll which is stored in an Alternate Data Stream (ADS).

```
control.exe {PATH_ABSOLUTE}:evil.dll
```

   - Use case: Can be used to evade defensive countermeasures or to hide as a persistence mechanism

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.002

   - Tags: Execute: DLL

2. Execute .cpl file. A CPL is a DLL file with CPlApplet export function)

```
control.exe {PATH_ABSOLUTE:.cpl}
```

   - Use case: Use to execute code and bypass application whitelisting

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.002

   - Tags: Execute: DLL
