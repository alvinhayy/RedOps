---
title: "iscsicpl.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Iscsicpl/
fetched_at: 2026-09-20T17:10:29Z
license: unspecified
category: windows
---

Microsoft iSCSI Initiator Control Panel tool

## Paths
- c:\windows\system32\iscsicpl.exe
- c:\windows\syswow64\iscsicpl.exe

## Resources
- [https://learn.microsoft.com/en-us/windows-server/storage/iscsi/iscsi-initiator-portal](https://learn.microsoft.com/en-us/windows-server/storage/iscsi/iscsi-initiator-portal)
- [https://github.com/hackerhouse-opensource/iscsicpl_bypassUAC](https://github.com/hackerhouse-opensource/iscsicpl_bypassUAC)

## Acknowledgements
- hacker.house
- Ekitji ([@eki_erk](https://twitter.com/@eki_erk))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/master/rules/windows/image_load/image_load_uac_bypass_iscsicpl.yml](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/image_load/image_load_uac_bypass_iscsicpl.yml)
- IOC: C:\Users\<username>\AppData\Local\Microsoft\WindowsApps\ISCSIEXE.dll
- IOC: Suspicious child process to iscsicpl.exe like cmd, powershell etc.

## UAC bypass

1. c:\windows\syswow64\iscsicpl.exe has a DLL injection through C:\Users\<username>\AppData\Local\Microsoft\WindowsApps\ISCSIEXE.dll, resulting in UAC bypass.

```
c:\windows\syswow64\iscsicpl.exe
```

   - Use case: Execute a custom DLL via a trusted high-integrity process without a UAC prompt.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1548.002

   - Tags: Execute: DLL

2. Both c:\windows\system32\iscsicpl.exe and c:\windows\system64\iscsicpl.exe have UAC bypass through launching iscicpl.exe, then navigating into the Configuration tab, clicking Report, then launching your custom command.

```
iscsicpl.exe
```

   - Use case: Execute a binary or script as a high-integrity process without a UAC prompt.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1548.002

   - Tags: Execute: CMDApplication: GUI
