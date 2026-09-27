---
title: "Msbuild.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Msbuild/
fetched_at: 2026-09-20T17:10:41Z
license: unspecified
category: windows
---

Used to compile and execute code

## Paths
- C:\Windows\Microsoft.NET\Framework\v2.0.50727\Msbuild.exe
- C:\Windows\Microsoft.NET\Framework64\v2.0.50727\Msbuild.exe
- C:\Windows\Microsoft.NET\Framework\v3.5\Msbuild.exe
- C:\Windows\Microsoft.NET\Framework64\v3.5\Msbuild.exe
- C:\Windows\Microsoft.NET\Framework\v4.0.30319\Msbuild.exe
- C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Msbuild.exe
- C:\Program Files (x86)\MSBuild\14.0\bin\MSBuild.exe

## Resources
- [https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1127/T1127.md](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1127/T1127.md)
- [https://github.com/Cn33liz/MSBuildShell](https://github.com/Cn33liz/MSBuildShell)
- [https://pentestlab.blog/2017/05/29/applocker-bypass-msbuild/](https://pentestlab.blog/2017/05/29/applocker-bypass-msbuild/)
- [https://oddvar.moe/2017/12/13/applocker-case-study-how-insecure-is-it-really-part-1/](https://oddvar.moe/2017/12/13/applocker-case-study-how-insecure-is-it-really-part-1/)
- [https://gist.github.com/bohops/4ffc43a281e87d108875f07614324191](https://gist.github.com/bohops/4ffc43a281e87d108875f07614324191)
- [https://github.com/LOLBAS-Project/LOLBAS/issues/165](https://github.com/LOLBAS-Project/LOLBAS/issues/165)
- [https://docs.microsoft.com/en-us/visualstudio/msbuild/msbuild-response-files](https://docs.microsoft.com/en-us/visualstudio/msbuild/msbuild-response-files)
- [https://www.daveaglick.com/posts/msbuild-loggers-and-logging-events](https://www.daveaglick.com/posts/msbuild-loggers-and-logging-events)

## Acknowledgements
- Casey Smith ([@subtee](https://twitter.com/@subtee))
- Cn33liz ([@Cneelis](https://twitter.com/@Cneelis))
- Jimmy ([@bohops](https://twitter.com/@bohops))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/file/file_event/file_event_win_shell_write_susp_directory.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/file/file_event/file_event_win_shell_write_susp_directory.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_msbuild_susp_parent_process.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_msbuild_susp_parent_process.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/network_connection/net_connection_win_silenttrinity_stager_msbuild_activity.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/network_connection/net_connection_win_silenttrinity_stager_msbuild_activity.yml)
- Splunk: [https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/suspicious_msbuild_spawn.yml](https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/suspicious_msbuild_spawn.yml)
- Splunk: [https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/suspicious_msbuild_rename.yml](https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/suspicious_msbuild_rename.yml)
- Splunk: [https://github.com/splunk/security_content/blob/a1afa0fa605639cbef7d528dec46ce7c8112194a/detections/endpoint/msbuild_suspicious_spawned_by_script_process.yml](https://github.com/splunk/security_content/blob/a1afa0fa605639cbef7d528dec46ce7c8112194a/detections/endpoint/msbuild_suspicious_spawned_by_script_process.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_msbuild_beacon_sequence.toml](https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_msbuild_beacon_sequence.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_msbuild_making_network_connections.toml](https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_msbuild_making_network_connections.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/ef7548f04c4341e0d1a172810330d59453f46a21/rules/windows/defense_evasion_execution_msbuild_started_by_script.toml](https://github.com/elastic/detection-rules/blob/ef7548f04c4341e0d1a172810330d59453f46a21/rules/windows/defense_evasion_execution_msbuild_started_by_script.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_execution_msbuild_started_by_office_app.toml](https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_execution_msbuild_started_by_office_app.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_execution_msbuild_started_renamed.toml](https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_execution_msbuild_started_renamed.toml)
- BlockRule: [https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)
- IOC: Msbuild.exe should not normally be executed on workstations

## AWL bypass

1. Build and execute a C# project stored in the target XML file.

```
msbuild.exe {PATH:.xml}
```

   - Use case: Compile and run code

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1127.001

   - Tags: Execute: CSharp

2. Build and execute a C# project stored in the target csproj file.

```
msbuild.exe {PATH:.csproj}
```

   - Use case: Compile and run code

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1127.001

   - Tags: Execute: CSharp

3. Executes generated Logger DLL file with TargetLogger export.

```
msbuild.exe /logger:TargetLogger,{PATH_ABSOLUTE:.dll};MyParameters,Foo
```

   - Use case: Execute DLL

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1127.001

   - Tags: Execute: DLL

4. Execute JScript/VBScript code through XML/XSL Transformation. Requires Visual Studio MSBuild v14.0+.

```
msbuild.exe {PATH:.proj}
```

   - Use case: Execute project file that contains XslTransformation tag parameters

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1127.001

   - Tags: Execute: XSL

5. By putting any valid msbuild.exe command-line options in an RSP file and calling it as above will interpret the options as if they were passed on the command line.

```
msbuild.exe @{PATH:.rsp}
```

   - Use case: Bypass command-line based detections

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1036

   - Tags: Execute: CMD
