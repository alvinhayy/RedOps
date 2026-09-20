---
title: "Volatility - CheatSheet"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/basic-forensic-methodology/memory-dump-analysis/volatility-cheatsheet.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: tools
---

```
# Full scan (runs all plugins)
python3 autovol3.py -f MEMFILE -o OUT_DIR -s full
# Minimal scan (runs a limited set of plugins)
python3 autovol3.py -f MEMFILE -o OUT_DIR -s minimal
# Normal scan (runs a balanced set of plugins)
python3 autovol3.py -f MEMFILE -o OUT_DIR -s normal
```
```
python autoVolatility.py -f MEMFILE -d OUT_DIRECTORY -e /home/user/tools/volatility/vol.py # It will use the most important plugins (could use a lot of space depending on the size of the memory)
```
## Installation

### volatility3

```
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3
python3 setup.py install
python3 vol.py —h
```
### volatility2

```
Download the executable from https://www.volatilityfoundation.org/26
```
## Volatility Commands

Access the official doc in [Volatility command reference](https://github.com/volatilityfoundation/volatility/wiki/Command-Reference#kdbgscan)

### A note on “list” vs. “scan” plugins

`list` plugins walk kernel-maintained structures, so they are fast but may miss objects that malware unlinks. `scan` plugins such as `psscan` search memory for object signatures; they can recover terminated or unlinked processes, but are slower and can produce false positives when residual structures are damaged.[\[8\]](#references)

## OS Profiles

### Volatility3

Volatility 3 requires symbol tables for the target operating system. The project README lists Windows, Mac, and Linux packs; place them in `volatility3/symbols` or in a `symbols` directory beside the executable. Windows symbols that are missing may be fetched and generated automatically, while Mac and Linux tables may need to be produced separately.[\[9\]](#references)

Symbol table packs for the various operating systems are available for **download** at:

- [https://downloads.volatilityfoundation.org/volatility3/symbols/windows.zip](https://downloads.volatilityfoundation.org/volatility3/symbols/windows.zip)
- [https://downloads.volatilityfoundation.org/volatility3/symbols/mac.zip](https://downloads.volatilityfoundation.org/volatility3/symbols/mac.zip)
- [https://downloads.volatilityfoundation.org/volatility3/symbols/linux.zip](https://downloads.volatilityfoundation.org/volatility3/symbols/linux.zip)

### Volatility2

#### External Profile

You can get the list of supported profiles doing:

```
./volatility_2.6_lin64_standalone --info | grep "Profile"
```
If you want to use a **new profile you have downloaded** (for example a linux one) you need to create somewhere the following folder structure: *plugins/overlays/linux* and put inside this folder the zip file containing the profile. Then, get the number of the profiles using:

```
./vol --plugins=/home/kali/Desktop/ctfs/final/plugins --info
Volatility Foundation Volatility Framework 2.6
Profiles
--------
LinuxCentOS7_3_10_0-123_el7_x86_64_profilex64 - A Profile for Linux CentOS7_3.10.0-123.el7.x86_64_profile x64
VistaSP0x64                                   - A Profile for Windows Vista SP0 x64
VistaSP0x86                                   - A Profile for Windows Vista SP0 x86
```
You can **download Linux and Mac profiles** from [https://github.com/volatilityfoundation/profiles](https://github.com/volatilityfoundation/profiles)

In the previous chunk you can see that the profile is called `LinuxCentOS7_3_10_0-123_el7_x86_64_profilex64`, and you can use it to execute something like:

```
./vol -f file.dmp --plugins=. --profile=LinuxCentOS7_3_10_0-123_el7_x86_64_profilex64 linux_netscan
```
#### Discover Profile

```
volatility imageinfo -f file.dmp
volatility kdbgscan -f file.dmp
```
#### **Differences between imageinfo and kdbgscan**

**Differences between imageinfo and kdbgscan**

[Andrea Fortuna’s image-identification notes](https://www.andreafortuna.org/2017/06/25/volatility-my-own-cheatsheet-part-1-image-identification/) explain that `imageinfo` produces profile suggestions, while `kdbgscan` scans for KDBG signatures and applies sanity checks to identify candidate profiles and KDBG addresses. Its output depends in part on whether Volatility can locate a DTB, so pass a known or suggested profile when running it.[\[1\]](#references)

When multiple candidates are returned, compare their process and module counts: a candidate with zero processes or modules is less credible than one with populated lists. Treat this as a sanity check rather than proof that a profile is correct.[\[1\]](#references)

```
# GOOD
PsActiveProcessHead           : 0xfffff800011977f0 (37 processes)
PsLoadedModuleList            : 0xfffff8000119aae0 (116 modules)
```
```
# BAD
PsActiveProcessHead           : 0xfffff800011947f0 (0 processes)
PsLoadedModuleList            : 0xfffff80001197ac0 (0 modules)
```
#### KDBG

`KdDebuggerDataBlock`, known to Volatility as KDBG, is a `_KDDEBUGGER_DATA64` structure that includes `PsActiveProcessHead`, the head of the process list used for process enumeration.[\[2\]](#references)

## OS Information

```
#vol3 has a plugin to give OS information (note that imageinfo from vol2 will give you OS info)
./vol.py -f file.dmp windows.info.Info
```
The plugin `banners.Banners` can be used in **vol3 to try to find linux banners** in the dump.

## Hashes/Passwords

Extract SAM hashes, [domain cached credentials](../../../windows-hardening/stealing-credentials/credentials-protections.html#cached-credentials) and [lsa secrets](../../../windows-hardening/authentication-credentials-uac-and-efs/index.html#lsa-secrets).

```
./vol.py -f file.dmp windows.hashdump.Hashdump #Grab common windows hashes (SAM+SYSTEM)
./vol.py -f file.dmp windows.cachedump.Cachedump #Grab domain cache hashes inside the registry
./vol.py -f file.dmp windows.lsadump.Lsadump #Grab lsa secrets
```
## Memory Dump

The memory dump of a process will **extract everything** of the current status of the process. The **procdump** module will only **extract** the **code**.

```
volatility -f file.dmp --profile=Win7SP1x86 memdump -p 2168 -D conhost/
```
## Processes

### List processes

Try to find **suspicious** processes (by name) or **unexpected** child **processes** (for example a cmd.exe as a child of iexplorer.exe).

It could be interesting to **compare** the result of pslist with the one of psscan to identify hidden processes.

```
python3 vol.py -f file.dmp windows.pstree.PsTree # Get processes tree (not hidden)
python3 vol.py -f file.dmp windows.pslist.PsList # Get process list (EPROCESS)
python3 vol.py -f file.dmp windows.psscan.PsScan # Get hidden process list(malware)
```
### Dump proc

```
./vol.py -f file.dmp windows.dumpfiles.DumpFiles --pid <pid> #Dump the .exe and dlls of the process in the current directory
```
### Command line

Anything suspicious was executed?

```
python3 vol.py -f file.dmp windows.cmdline.CmdLine #Display process command-line arguments
```
Commands executed in `cmd.exe` are managed by **`conhost.exe`** (or `csrss.exe` on systems before Windows 7). This means that if **`cmd.exe`** is terminated by an attacker before a memory dump is obtained, it’s still possible to recover the session’s command history from the memory of **`conhost.exe`**. To do this, if unusual activity is detected within the console’s modules, the memory of the associated **`conhost.exe`** process should be dumped. Then, by searching for **strings** within this dump, command lines used in the session can potentially be extracted.

### Environment

Get the env variables of each running process. There could be some interesting values.

```
python3 vol.py -f file.dmp windows.envars.Envars [--pid <pid>] #Display process environment variables
```
### Token privileges

Check for privileges tokens in unexpected services.

It could be interesting to list the processes using some privileged token.

```
#Get enabled privileges of some processes
python3 vol.py -f file.dmp windows.privileges.Privs [--pid <pid>]
#Get all processes with interesting privileges
python3 vol.py -f file.dmp windows.privileges.Privs | grep "SeImpersonatePrivilege\|SeAssignPrimaryPrivilege\|SeTcbPrivilege\|SeBackupPrivilege\|SeRestorePrivilege\|SeCreateTokenPrivilege\|SeLoadDriverPrivilege\|SeTakeOwnershipPrivilege\|SeDebugPrivilege"
```
### SIDs

Check each SSID owned by a process.

It could be interesting to list the processes using a privileges SID (and the processes using some service SID).

```
./vol.py -f file.dmp windows.getsids.GetSIDs [--pid <pid>] #Get SIDs of processes
./vol.py -f file.dmp windows.getservicesids.GetServiceSIDs #Get the SID of services
```
### Handles

Useful to know to which other files, keys, threads, processes… a **process has a handle** for (has opened)

```
vol.py -f file.dmp windows.handles.Handles [--pid <pid>]
```
### DLLs

```
./vol.py -f file.dmp windows.dlllist.DllList [--pid <pid>] #List dlls used by each
./vol.py -f file.dmp windows.dumpfiles.DumpFiles --pid <pid> #Dump the .exe and dlls of the process in the current directory process
```
### Strings per processes

Volatility allows us to check which process a string belongs to.

```
strings file.dmp > /tmp/strings.txt
./vol.py -f /tmp/file.dmp windows.strings.Strings --strings-file /tmp/strings.txt
```
It also allows to search for strings inside a process using the yarascan module:

```
./vol.py -f file.dmp windows.vadyarascan.VadYaraScan --yara-rules "https://" --pid 3692 3840 3976 3312 3084 2784
./vol.py -f file.dmp yarascan.YaraScan --yara-rules "https://"
```
### UserAssist

`UserAssist` registry values record programs launched through Windows Explorer, including execution counts and last-run timestamps; command-line launches are not recorded in these keys.[\[3\]](#references)

```
./vol.py -f file.dmp windows.registry.userassist.UserAssist
```
## Services

```
./vol.py -f file.dmp windows.svcscan.SvcScan #List services
./vol.py -f file.dmp windows.getservicesids.GetServiceSIDs #Get the SID of services
```
## Network

```
./vol.py -f file.dmp windows.netscan.NetScan
#For network info of linux use volatility2
```
## Registry hive

### Print available hives

```
./vol.py -f file.dmp windows.registry.hivelist.HiveList #List roots
./vol.py -f file.dmp windows.registry.printkey.PrintKey #List roots and get initial subkeys
```
### Get a value

```
./vol.py -f file.dmp windows.registry.printkey.PrintKey --key "Software\Microsoft\Windows NT\CurrentVersion"
```
### Dump

```
#Dump a hive
volatility --profile=Win7SP1x86_23418 hivedump -o 0x9aad6148 -f file.dmp #Offset extracted by hivelist
#Dump all hives
volatility --profile=Win7SP1x86_23418 hivedump -f file.dmp
```
## Filesystem

### Mount

```
#See vol2
```
### Scan/dump

```
./vol.py -f file.dmp windows.filescan.FileScan #Scan for files inside the dump
./vol.py -f file.dmp windows.dumpfiles.DumpFiles --physaddr <0xAAAAA> #Offset from previous command
```
### Master File Table

```
# I couldn't find any plugin to extract this information in volatility3
```
On NTFS, the MFT has at least one entry per file on the volume, including itself. File metadata and contents are stored in MFT entries or in locations those entries describe; see the [Microsoft documentation](https://learn.microsoft.com/en-us/windows/win32/fileio/master-file-table).[\[4\]](#references)

### SSL Keys/Certs

```
#vol3 allows to search for certificates inside the registry
./vol.py -f file.dmp windows.registry.certificates.Certificates
```
## Malware

```
./vol.py -f file.dmp windows.malfind.Malfind [--dump] #Find hidden and injected code, [dump each suspicious section]
#Malfind will search for suspicious structures related to malware
./vol.py -f file.dmp windows.driverirp.DriverIrp #Driver IRP hook detection
./vol.py -f file.dmp windows.ssdt.SSDT #Check system call address from unexpected addresses
./vol.py -f file.dmp linux.check_afinfo.Check_afinfo #Verifies the operation function pointers of network protocols
./vol.py -f file.dmp linux.check_creds.Check_creds #Checks if any processes are sharing credential structures
./vol.py -f file.dmp linux.check_idt.Check_idt #Checks if the IDT has been altered
./vol.py -f file.dmp linux.check_syscall.Check_syscall #Check system call table for hooks
./vol.py -f file.dmp linux.check_modules.Check_modules #Compares module list to sysfs info, if available
./vol.py -f file.dmp linux.tty_check.tty_check #Checks tty devices for hooks
```
### Scanning with yara

Use this script to download and merge all the yara malware rules from github: [https://gist.github.com/andreafortuna/29c6ea48adf3d45a979a78763cdc7ce9](https://gist.github.com/andreafortuna/29c6ea48adf3d45a979a78763cdc7ce9)

Create the ***rules*** directory and execute it. This will create a file called ***malware_rules.yar*** which contains all the yara rules for malware.

```
wget https://gist.githubusercontent.com/andreafortuna/29c6ea48adf3d45a979a78763cdc7ce9/raw/4ec711d37f1b428b63bed1f786b26a0654aa2f31/malware_yara_rules.py
mkdir rules
python malware_yara_rules.py
#Only Windows
./vol.py -f file.dmp windows.vadyarascan.VadYaraScan --yara-file /tmp/malware_rules.yar
#All
./vol.py -f file.dmp yarascan.YaraScan --yara-file /tmp/malware_rules.yar
```
## MISC

### External plugins

If you want to use external plugins make sure that the folders related to the plugins are the first parameter used.

```
./vol.py --plugin-dirs "/tmp/plugins/" [...]
```
#### Autoruns

Download it from [https://github.com/tomchop/volatility-autoruns](https://github.com/tomchop/volatility-autoruns)

```
 volatility --plugins=volatility-autoruns/ --profile=WinXPSP2x86 -f file.dmp autoruns
```
### Mutexes

```
./vol.py -f file.dmp windows.mutantscan.MutantScan
```
### Symlinks

```
./vol.py -f file.dmp windows.symlinkscan.SymlinkScan
```
### Bash

It’s possible to **read from memory the bash history.** You could also dump the *.bash_history* file, but it was disabled you will be glad you can use this volatility module

```
./vol.py -f file.dmp linux.bash.Bash
```
### TimeLine

```
./vol.py -f file.dmp timeLiner.TimeLiner
```
### Drivers

```
./vol.py -f file.dmp windows.driverscan.DriverScan
```
### Get clipboard

```
#Just vol2
volatility --profile=Win7SP1x86_23418 clipboard -f file.dmp
```
### Get IE history

```
#Just vol2
volatility --profile=Win7SP1x86_23418 iehistory -f file.dmp
```
### Get notepad text

```
#Just vol2
volatility --profile=Win7SP1x86_23418 notepad -f file.dmp
```
### Screenshot

```
#Just vol2
volatility --profile=Win7SP1x86_23418 screenshot -f file.dmp
```
### Master Boot Record (MBR)

```
volatility --profile=Win7SP1x86_23418 mbrparser -f file.dmp
```
On BIOS-based systems, the MBR at sector 0 contains master boot code and the partition table. Microsoft documents that `bootsect /mbr` updates the code without changing that table.[\[7\]](#references)

## References

- [1] [Volatility, my own cheatsheet (Part 1): Image Identification](https://andreafortuna.org/2017/06/25/volatility-my-own-cheatsheet-part-1-image-identification/)
- [2] [Finding the Kernel Debugger Block](https://scudette.blogspot.com/2012/11/finding-kernel-debugger-block.html)
- [3] [Windows UserAssist Keys](https://www.aldeid.com/wiki/Windows-userassist-keys)
- [4] [Master File Table (Local File Systems) - Win32 apps](https://learn.microsoft.com/en-us/windows/win32/fileio/master-file-table)
- [5] [UEFI-based PC, protective MBR: what is it? - Microsoft Community](https://answers.microsoft.com/en-us/windows/forum/all/uefi-based-pc-protective-mbr-what-is-it/0fc7b558-d8d4-4a7d-bae2-395455bb19aa)
- [6] [Tutorial: Volatility plugins for malware analysis](http://tomchop.me/2016/11/21/tutorial-volatility-plugins-malware-analysis/)
- [7] [Bootsect Command-Line Options](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/bootsect-command-line-options?view=windows-11)
- [8] [Tutorial - Volatility plugins & malware analysis](https://tomchop.me/posts/volatility-plugin-malware-analysis/)
- [9] [Volatility 3 README](https://github.com/volatilityfoundation/volatility3/blob/develop/README.md)
