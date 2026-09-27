---
title: "Expand.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Expand/
fetched_at: 2026-09-20T17:10:03Z
license: unspecified
category: windows
---

Binary that expands one or more compressed files

## Paths
- C:\Windows\System32\Expand.exe
- C:\Windows\SysWOW64\Expand.exe

## Resources
- [https://twitter.com/infosecn1nja/status/986628482858807297](https://twitter.com/infosecn1nja/status/986628482858807297)
- [https://twitter.com/Oddvarmoe/status/986709068759949319](https://twitter.com/Oddvarmoe/status/986709068759949319)

## Acknowledgements
- Rahmat Nurfauzi ([@infosecn1nja](https://twitter.com/@infosecn1nja))
- Oddvar Moe ([@oddvarmoe](https://twitter.com/@oddvarmoe))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_expand_cabinet_files.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_expand_cabinet_files.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/defense_evasion_misc_lolbin_connecting_to_the_internet.toml](https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/defense_evasion_misc_lolbin_connecting_to_the_internet.toml)

## Download

1. Copies source file to destination.

```
expand {PATH_SMB:.bat} {PATH_ABSOLUTE:.bat}
```

   - Use case: Use to copies the source file to the destination file

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

2. Copies source file to destination.

```
expand {PATH_ABSOLUTE:.source.ext} {PATH_ABSOLUTE:.dest.ext}
```

   - Use case: Copies files from A to B

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

3. Copies source file to destination Alternate Data Stream (ADS)

```
expand {PATH_SMB:.bat} {PATH_ABSOLUTE}:file.bat
```

   - Use case: Copies files from A to B

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004
