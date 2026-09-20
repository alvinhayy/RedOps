---
title: "Cipher.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Cipher/
fetched_at: 2026-09-20T17:09:32Z
license: unspecified
category: windows
---

File Encryption Utility

## Paths
- c:\windows\system32\cipher.exe
- c:\windows\syswow64\cipher.exe

## Resources
- [https://www.volexity.com/blog/2024/11/22/the-nearest-neighbor-attack-how-a-russian-apt-weaponized-nearby-wi-fi-networks-for-covert-access/](https://www.volexity.com/blog/2024/11/22/the-nearest-neighbor-attack-how-a-russian-apt-weaponized-nearby-wi-fi-networks-for-covert-access/)

## Acknowledgements
- Ade Ogunsowo ([@i_am_tutu](https://twitter.com/@i_am_tutu))
- Alexander Sennhauser ([@conitrade](https://twitter.com/@conitrade))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/process_creation/proc_creation_win_cipher_overwrite_deleted_data.yml](https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/process_creation/proc_creation_win_cipher_overwrite_deleted_data.yml)
- IOC: cipher.exe process with /w on the command line

## Tamper

1. Zero out a file

```
cipher /w:{PATH_ABSOLUTE:folder}
```

   - Use case: Can be used to forensically erase a file.

   - Privileges required: User

   - Operating systems: Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1485

2. Encrypt a file

```
cipher.exe /e {PATH_ABSOLUTE}
```

   - Use case: Can be used to impair defences by e.g. encrypting a critical EDR solution file.

   - Privileges required: Admin

   - Operating systems: Windows 10

   - ATT&CK® technique: T1562
