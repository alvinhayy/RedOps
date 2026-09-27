---
title: "Explorer.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Explorer/
fetched_at: 2026-09-20T17:10:05Z
license: unspecified
category: windows
---

Binary used for managing files and system components within Windows

## Paths
- C:\Windows\explorer.exe
- C:\Windows\SysWOW64\explorer.exe

## Resources
- [https://twitter.com/CyberRaiju/status/1273597319322058752?s=20](https://twitter.com/CyberRaiju/status/1273597319322058752?s=20)
- [https://twitter.com/bohops/status/1276356245541335048](https://twitter.com/bohops/status/1276356245541335048)
- [https://twitter.com/bohops/status/986984122563391488](https://twitter.com/bohops/status/986984122563391488)

## Acknowledgements
- Jai Minton ([@CyberRaiju](https://twitter.com/@CyberRaiju))
- Jimmy ([@bohops](https://twitter.com/@bohops))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_explorer_break_process_tree.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_explorer_break_process_tree.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_explorer_lolbin_execution.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_explorer_lolbin_execution.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/f2bc0c685d83db7db395fc3dc4b9729759cd4329/rules/windows/initial_access_via_explorer_suspicious_child_parent_args.toml](https://github.com/elastic/detection-rules/blob/f2bc0c685d83db7db395fc3dc4b9729759cd4329/rules/windows/initial_access_via_explorer_suspicious_child_parent_args.toml)
- IOC: Multiple instances of explorer.exe or explorer.exe using the /root command line is suspicious.

## Execute

1. Execute specified .exe with the parent process spawning from a new instance of explorer.exe

```
explorer.exe /root,"{PATH_ABSOLUTE:.exe}"
```

   - Use case: Performs execution of specified file with explorer parent process breaking the process tree, can be used for defense evasion.

   - Privileges required: User

   - Operating systems: Windows XP, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: EXE

2. Execute notepad.exe with the parent process spawning from a new instance of explorer.exe

```
explorer.exe {PATH_ABSOLUTE:.exe}
```

   - Use case: Performs execution of specified file with explorer parent process breaking the process tree, can be used for defense evasion.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: EXE
