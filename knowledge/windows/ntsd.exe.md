---
title: "Ntsd.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Ntsd/
fetched_at: 2026-09-20T17:15:11Z
license: unspecified
category: windows
---

Symbolic Debugger for Windows.

## Paths
- C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\ntsd.exe
- C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\ntsd.exe
- C:\Program Files (x86)\Windows Kits\10\Debuggers\arm\ntsd.exe
- C:\Program Files (x86)\Windows Kits\10\Debuggers\arm64\ntsd.exe

## Resources
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/cdb-command-line-options](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/cdb-command-line-options)
- [https://strontic.github.io/xcyclopedia/library/ntsd.exe-629EA12D527237B9CD945AC44C2DE80D.html](https://strontic.github.io/xcyclopedia/library/ntsd.exe-629EA12D527237B9CD945AC44C2DE80D.html)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Execute

1. Launches command through the debugging process; optionally add -G to exit the debugger automatically.

```
ntsd.exe -g {CMD}
```

   - Use case: Executes an executable under a trusted microsoft signed binary.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: CMD
