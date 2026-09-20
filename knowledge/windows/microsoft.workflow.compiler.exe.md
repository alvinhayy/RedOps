---
title: "Microsoft.Workflow.Compiler.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Microsoft.Workflow.Compiler/
fetched_at: 2026-09-20T17:10:35Z
license: unspecified
category: windows
---

A utility included with .NET that is capable of compiling and executing C# or VB.net code.

## Paths
- C:\Windows\Microsoft.Net\Framework64\v4.0.30319\Microsoft.Workflow.Compiler.exe

## Resources
- [https://twitter.com/mattifestation/status/1030445200475185154](https://twitter.com/mattifestation/status/1030445200475185154)
- [https://posts.specterops.io/arbitrary-unsigned-code-execution-vector-in-microsoft-workflow-compiler-exe-3d9294bc5efb](https://posts.specterops.io/arbitrary-unsigned-code-execution-vector-in-microsoft-workflow-compiler-exe-3d9294bc5efb)
- [https://gist.github.com/mattifestation/3e28d391adbd7fe3e0c722a107a25aba#file-workflowcompilerdetectiontests-ps1](https://gist.github.com/mattifestation/3e28d391adbd7fe3e0c722a107a25aba#file-workflowcompilerdetectiontests-ps1)
- [https://gist.github.com/mattifestation/7ba8fc8f724600a9f525714c9cf767fd#file-createcompilerinputxml-ps1](https://gist.github.com/mattifestation/7ba8fc8f724600a9f525714c9cf767fd#file-createcompilerinputxml-ps1)
- [https://www.forcepoint.com/blog/security-labs/using-c-post-powershell-attacks](https://www.forcepoint.com/blog/security-labs/using-c-post-powershell-attacks)
- [https://www.fortynorthsecurity.com/microsoft-workflow-compiler-exe-veil-and-cobalt-strike/](https://www.fortynorthsecurity.com/microsoft-workflow-compiler-exe-veil-and-cobalt-strike/)
- [https://medium.com/@Bank_Security/undetectable-c-c-reverse-shells-fab4c0ec4f15](https://medium.com/@Bank_Security/undetectable-c-c-reverse-shells-fab4c0ec4f15)

## Acknowledgements
- Matt Graeber ([@mattifestation](https://twitter.com/@mattifestation))
- John Bergbom ([@BergbomJohn](https://twitter.com/@BergbomJohn))
- FortyNorth Security ([@FortyNorthSec](https://twitter.com/@FortyNorthSec))
- Bank Security ([@Bank_Security](https://twitter.com/@Bank_Security))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_workflow_compiler.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_workflow_compiler.yml)
- Splunk: [https://github.com/splunk/security_content/blob/961a81d4a5cb5c5febec4894d6d812497171a85c/detections/endpoint/suspicious_microsoft_workflow_compiler_usage.yml](https://github.com/splunk/security_content/blob/961a81d4a5cb5c5febec4894d6d812497171a85c/detections/endpoint/suspicious_microsoft_workflow_compiler_usage.yml)
- Splunk: [https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/suspicious_microsoft_workflow_compiler_rename.yml](https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/suspicious_microsoft_workflow_compiler_rename.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_unusual_process_network_connection.toml](https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_unusual_process_network_connection.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_network_connection_from_windows_binary.toml](https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_network_connection_from_windows_binary.toml)
- BlockRule: [https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)
- IOC: Microsoft.Workflow.Compiler.exe would not normally be run on workstations.
- IOC: The presence of csc.exe or vbc.exe as child processes of Microsoft.Workflow.Compiler.exe
- IOC: Presence of "<CompilerInput" in a text file.

## Execute

1. Compile and execute C# or VB.net code in a XOML file referenced in the first argument (any extension accepted).

```
Microsoft.Workflow.Compiler.exe {PATH} {PATH:.log}
```

   - Use case: Compile and run code

   - Privileges required: User

   - Operating systems: Windows 10S, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: VB.NetExecute: Csharp

2. Compile and execute C# or VB.net code in a XOML file referenced in the test.txt file.

```
Microsoft.Workflow.Compiler.exe {PATH} {PATH:.log}
```

   - Use case: Compile and run code

   - Privileges required: User

   - Operating systems: Windows 10S, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: XOML

3. Compile and execute C# or VB.net code in a XOML file referenced in the test.txt file.

```
Microsoft.Workflow.Compiler.exe {PATH} {PATH:.log}
```

   - Use case: Compile and run code

   - Privileges required: User

   - Operating systems: Windows 10S, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: XOML
