---
title: "fltMC.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/FltMC/
fetched_at: 2026-09-20T17:10:12Z
license: unspecified
category: windows
---

Filter Manager Control Program used by Windows

## Paths
- C:\Windows\System32\fltMC.exe

## Resources
- [https://www.darkoperator.com/blog/2018/10/5/operating-offensively-against-sysmon](https://www.darkoperator.com/blog/2018/10/5/operating-offensively-against-sysmon)

## Acknowledgements
- Carlos Perez ([@Carlos_Perez](https://twitter.com/@Carlos_Perez))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_fltmc_unload_driver_sysmon.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_fltmc_unload_driver_sysmon.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_via_filter_manager.toml](https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_via_filter_manager.toml)
- Splunk: [https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/unload_sysmon_filter_driver.yml](https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/unload_sysmon_filter_driver.yml)
- IOC: 4688 events with fltMC.exe

## Tamper

1. Unloads a driver used by security agents

```
fltMC.exe unload SysmonDrv
```

   - Use case: Defense evasion

   - Privileges required: Admin

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1562.001
