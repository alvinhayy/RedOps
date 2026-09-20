---
title: "Diskshadow.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Diskshadow/
fetched_at: 2026-09-20T17:09:56Z
license: unspecified
category: windows
---

Diskshadow.exe is a tool that exposes the functionality offered by the volume shadow copy Service (VSS).

## Paths
- C:\Windows\System32\diskshadow.exe
- C:\Windows\SysWOW64\diskshadow.exe

## Resources
- [https://bohops.com/2018/03/26/diskshadow-the-return-of-vss-evasion-persistence-and-active-directory-database-extraction/](https://bohops.com/2018/03/26/diskshadow-the-return-of-vss-evasion-persistence-and-active-directory-database-extraction/)

## Acknowledgements
- Jimmy ([@bohops](https://twitter.com/@bohops))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_lolbin_diskshadow.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_lolbin_diskshadow.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_susp_shadow_copies_deletion.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_susp_shadow_copies_deletion.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/5bdf70e72c6cd4547624c521108189af994af449/rules/windows/credential_access_cmdline_dump_tool.toml](https://github.com/elastic/detection-rules/blob/5bdf70e72c6cd4547624c521108189af994af449/rules/windows/credential_access_cmdline_dump_tool.toml)
- IOC: Child process from diskshadow.exe

## Dump

1. Execute commands using diskshadow.exe from a prepared diskshadow script.

```
diskshadow.exe /s {PATH:.txt}
```

   - Use case: Use diskshadow to exfiltrate data from VSS such as NTDS.dit

   - Privileges required: User

   - Operating systems: Windows server

   - ATT&CK® technique: T1003.003

   - Tags: Execute: CMD

2. Execute commands using diskshadow.exe to spawn child process

```
diskshadow> exec {PATH:.exe}
```

   - Use case: Use diskshadow to bypass defensive counter measures

   - Privileges required: User

   - Operating systems: Windows server

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD
