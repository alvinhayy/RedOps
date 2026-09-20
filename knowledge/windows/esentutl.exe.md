---
title: "Esentutl.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Esentutl/
fetched_at: 2026-09-20T17:09:59Z
license: unspecified
category: windows
---

Binary for working with Microsoft Joint Engine Technology (JET) database

## Paths
- C:\Windows\System32\esentutl.exe
- C:\Windows\SysWOW64\esentutl.exe

## Resources
- [https://twitter.com/egre55/status/985994639202283520](https://twitter.com/egre55/status/985994639202283520)
- [https://dfironthemountain.wordpress.com/2018/12/06/locked-file-access-using-esentutl-exe/](https://dfironthemountain.wordpress.com/2018/12/06/locked-file-access-using-esentutl-exe/)
- [https://twitter.com/bohops/status/1094810861095534592](https://twitter.com/bohops/status/1094810861095534592)

## Acknowledgements
- egre55 ([@egre55](https://twitter.com/@egre55))
- Mike Cary ([@grayfold3d](https://twitter.com/@grayfold3d))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_esentutl_params.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_esentutl_params.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_esentutl_webcache.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_esentutl_webcache.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/registry/registry_event/registry_event_esentutl_volume_shadow_copy_service_keys.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/registry/registry_event/registry_event_esentutl_volume_shadow_copy_service_keys.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_esentutl_sensitive_file_copy.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_esentutl_sensitive_file_copy.yml)
- Splunk: [https://github.com/splunk/security_content/blob/86a5b644a44240f01274c8b74d19a435c7dae66e/detections/endpoint/esentutl_sam_copy.yml](https://github.com/splunk/security_content/blob/86a5b644a44240f01274c8b74d19a435c7dae66e/detections/endpoint/esentutl_sam_copy.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/f6421d8c534f295518a2c945f530e8afc4c8ad1b/rules/windows/credential_access_copy_ntds_sam_volshadowcp_cmdline.toml](https://github.com/elastic/detection-rules/blob/f6421d8c534f295518a2c945f530e8afc4c8ad1b/rules/windows/credential_access_copy_ntds_sam_volshadowcp_cmdline.toml)

## Copy

1. Copies the source VBS file to the destination VBS file.

```
esentutl.exe /y {PATH_ABSOLUTE:.source.vbs} /d {PATH_ABSOLUTE:.dest.vbs} /o
```

   - Use case: Copies files from A to B

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1105

2. Copies a (locked) file using Volume Shadow Copy

```
esentutl.exe /y /vss c:\windows\ntds\ntds.dit /d {PATH_ABSOLUTE:.dit}
```

   - Use case: Copy/extract a locked file such as the AD Database

   - Privileges required: Admin

   - Operating systems: Windows 10, Windows 11, Windows 2016 Server, Windows 2019 Server

   - ATT&CK® technique: T1003.003

3. Copies the source EXE to an Alternate Data Stream (ADS) of the destination file.

```
esentutl.exe /y {PATH_ABSOLUTE:.exe} /d {PATH_ABSOLUTE}:file.exe /o
```

   - Use case: Copy file and hide it in an alternate data stream as a defensive counter measure

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

4. Copies the source Alternate Data Stream (ADS) to the destination EXE.

```
esentutl.exe /y {PATH_ABSOLUTE}:file.exe /d {PATH_ABSOLUTE:.exe} /o
```

   - Use case: Extract hidden file within alternate data streams

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

5. Copies the remote source EXE to the destination Alternate Data Stream (ADS) of the destination file.

```
esentutl.exe /y {PATH_SMB:.exe} /d {PATH_ABSOLUTE}:file.exe /o
```

   - Use case: Copy file and hide it in an alternate data stream as a defensive counter measure

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

6. Copies the source EXE to the destination EXE file

```
esentutl.exe /y {PATH_SMB:.source.exe} /d {PATH_SMB:.dest.exe} /o
```

   - Use case: Use to copy files from one unc path to another

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004
