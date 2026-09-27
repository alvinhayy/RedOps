---
title: "Ldifde.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Ldifde/
fetched_at: 2026-09-20T17:10:31Z
license: unspecified
category: windows
---

Creates, modifies, and deletes LDAP directory objects.

## Paths
- c:\windows\system32\ldifde.exe
- c:\windows\syswow64\ldifde.exe

## Resources
- [https://twitter.com/0gtweet/status/1564968845726580736](https://twitter.com/0gtweet/status/1564968845726580736)

## Acknowledgements
- Grzegorz Tworek ([@0gtweet](https://twitter.com/@0gtweet))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/3d172914f6c2bd5c2b5ed471bf0657a662d395af/rules/windows/process_creation/proc_creation_win_ldifde_export.yml](https://github.com/SigmaHQ/sigma/blob/3d172914f6c2bd5c2b5ed471bf0657a662d395af/rules/windows/process_creation/proc_creation_win_ldifde_export.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/3d172914f6c2bd5c2b5ed471bf0657a662d395af/rules/windows/process_creation/proc_creation_win_ldifde_file_load.yml](https://github.com/SigmaHQ/sigma/blob/3d172914f6c2bd5c2b5ed471bf0657a662d395af/rules/windows/process_creation/proc_creation_win_ldifde_file_load.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/3d172914f6c2bd5c2b5ed471bf0657a662d395af/rules-emerging-threats/2019/TA/APT31/proc_creation_win_apt_apt31_judgement_panda.yml](https://github.com/SigmaHQ/sigma/blob/3d172914f6c2bd5c2b5ed471bf0657a662d395af/rules-emerging-threats/2019/TA/APT31/proc_creation_win_apt_apt31_judgement_panda.yml)

## Download

1. Import specified .ldf file into LDAP. If the file contains http-based attrval-spec such as thumbnailPhoto:< http://example.org/somefile.txt, the file will be downloaded into IE temp folder.

```
Ldifde -i -f {PATH:.ldf}
```

   - Use case: Download file from Internet

   - Privileges required: Administrator

   - Operating systems: Windows Server with AD Domain Services role, Windows 10 with AD LDS role.

   - ATT&CK® technique: T1105
