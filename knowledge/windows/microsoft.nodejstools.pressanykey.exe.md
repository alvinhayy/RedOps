---
title: "Microsoft.NodejsTools.PressAnyKey.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Microsoft.NodejsTools.PressAnyKey/
fetched_at: 2026-09-20T17:14:57Z
license: unspecified
category: windows
---

Part of the NodeJS Visual Studio tools.

## Paths
- C:\Program Files\Microsoft Visual Studio\<version>\Community\Common7\IDE\Extensions\Microsoft\NodeJsTools\NodeJsTools\Microsoft.NodejsTools.PressAnyKey.exe
- C:\Program Files (x86)\Microsoft Visual Studio\<version>\Community\Common7\IDE\Extensions\Microsoft\NodeJsTools\NodeJsTools\Microsoft.NodejsTools.PressAnyKey.exe

## Resources
- [https://twitter.com/mrd0x/status/1463526834918854661](https://twitter.com/mrd0x/status/1463526834918854661)

## Acknowledgements
- mr.d0x ([@mrd0x](https://twitter.com/@mrd0x))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/b02e3b698afbaae143ac4fb36236eb0b41122ed7/rules/windows/process_creation/proc_creation_win_renamed_pressanykey.yml](https://github.com/SigmaHQ/sigma/blob/b02e3b698afbaae143ac4fb36236eb0b41122ed7/rules/windows/process_creation/proc_creation_win_renamed_pressanykey.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/b02e3b698afbaae143ac4fb36236eb0b41122ed7/rules/windows/process_creation/proc_creation_win_pressanykey_lolbin_execution.yml](https://github.com/SigmaHQ/sigma/blob/b02e3b698afbaae143ac4fb36236eb0b41122ed7/rules/windows/process_creation/proc_creation_win_pressanykey_lolbin_execution.yml)

## Execute

1. Launch specified executable as a subprocess of Microsoft.NodejsTools.PressAnyKey.exe.

```
Microsoft.NodejsTools.PressAnyKey.exe normal 1 {PATH:.exe}
```

   - Use case: Spawn a new process via Microsoft.NodejsTools.PressAnyKey.exe.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE
