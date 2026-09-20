---
title: "Extrac32.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Extrac32/
fetched_at: 2026-09-20T17:10:07Z
license: unspecified
category: windows
---

Extract to ADS, copy or overwrite a file with Extrac32.exe

## Paths
- C:\Windows\System32\extrac32.exe
- C:\Windows\SysWOW64\extrac32.exe

## Resources
- [https://oddvar.moe/2018/04/11/putting-data-in-alternate-data-streams-and-how-to-execute-it-part-2/](https://oddvar.moe/2018/04/11/putting-data-in-alternate-data-streams-and-how-to-execute-it-part-2/)
- [https://gist.github.com/api0cradle/cdd2d0d0ec9abb686f0e89306e277b8f](https://gist.github.com/api0cradle/cdd2d0d0ec9abb686f0e89306e277b8f)
- [https://twitter.com/egre55/status/985994639202283520](https://twitter.com/egre55/status/985994639202283520)

## Acknowledgements
- egre55 ([@egre55](https://twitter.com/@egre55))
- Oddvar Moe ([@oddvarmoe](https://twitter.com/@oddvarmoe))
- Hai Vaknin(Lux ([@VakninHai](https://twitter.com/@VakninHai))
- Tamir Yehuda ([@tim8288](https://twitter.com/@tim8288))

## Detections
- Elastic: [https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/defense_evasion_misc_lolbin_connecting_to_the_internet.toml](https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/defense_evasion_misc_lolbin_connecting_to_the_internet.toml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_extrac32.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_extrac32.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_extrac32_ads.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_lolbin_extrac32_ads.yml)

## Alternate data streams

1. Extracts the source CAB file into an Alternate Data Stream (ADS) of the target file.

```
extrac32 {PATH_ABSOLUTE:.cab} {PATH_ABSOLUTE}:file.exe
```

   - Use case: Extract data from cab file and hide it in an alternate data stream.

   - Privileges required: User

   - Operating systems: Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

   - Tags: Type: Compression

2. Extracts the source CAB file on an unc path into an Alternate Data Stream (ADS) of the target file.

```
extrac32 {PATH_ABSOLUTE:.cab} {PATH_ABSOLUTE}:file.exe
```

   - Use case: Extract data from cab file and hide it in an alternate data stream.

   - Privileges required: User

   - Operating systems: Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

   - Tags: Type: Compression

3. Copy the source file to the destination file and overwrite it.

```
extrac32 /Y /C {PATH_SMB} {PATH_ABSOLUTE}
```

   - Use case: Download file from UNC/WEBDav

   - Privileges required: User

   - Operating systems: Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

4. Command for copying file from one folder to another

```
extrac32.exe /C {PATH_ABSOLUTE:.source.exe} {PATH_ABSOLUTE:.dest.exe}
```

   - Use case: Copy file

   - Privileges required: User

   - Operating systems: Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105
