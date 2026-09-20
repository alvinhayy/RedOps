---
title: "Pixtool.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Pixtool/
fetched_at: 2026-09-20T17:15:15Z
license: unspecified
category: windows
---

Command line utility for taking and analyzing PIX GPU captures.

## Paths
- C:\Program Files\Microsoft PIX\pixtool.exe
- C:\Program Files (x86)\Microsoft PIX\pixtool.exe

## Resources
- [https://devblogs.microsoft.com/pix/pixtool/](https://devblogs.microsoft.com/pix/pixtool/)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Execute

1. Launches an executable via PIX command-line utility.

```
pixtool.exe launch {PATH_ABSOLUTE:.exe}
```

   - Use case: Executes an executable under a trusted, Microsoft signed binary.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE
