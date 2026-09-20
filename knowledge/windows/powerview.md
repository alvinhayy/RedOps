---
title: Powerview
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/tools/powerview
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---
Powerview is a powerful powershell script from powershell empire that can be used for enumerating a domain after you have already gained a shell in the system. Powerview is a script part of PowerSploit, which is not a supported project anymore, but still a powerfull post-exploitation tool.

***

Load Powerview module in powershell

```jsx
. .\Downloads\PowerView.ps1
```

Next, we can use powerview to get domain users for example:

```jsx
Get-NetUser | select cn
```

By piping the output of Get-NetUser to select cn, we only select the cnames of the users:

```jsx
**PS C:\Users\Administrator> Get-NetUser | select cn**

cn
--
Administrator
Guest
krbtgt
Machine-1
Admin2
Machine-2
SQL Service
POST{P0W3RV13W_FTW}
sshd
```

We can also find every domain group with the word “Admin” in it:

```jsx
**PS C:\Users\Administrator> Get-NetGroup -GroupName *Admin***
Administrators
Hyper-V Administrators
Storage Replica Administrators
Schema Admins
Enterprise Admins
Domain Admins
Key Admins
Enterprise Key Admins
DnsAdmins
```

List all network shares:

```jsx
**PS C:\Users\Administrator> Invoke-ShareFinder**
\\Domain-Controller.CONTROLLER.local\ADMIN$     - Remote Admin
\\Domain-Controller.CONTROLLER.local\C$         - Default share
\\Domain-Controller.CONTROLLER.local\IPC$       - Remote IPC
\\Domain-Controller.CONTROLLER.local\NETLOGON   - Logon server share
\\Domain-Controller.CONTROLLER.local\Share      -
\\Domain-Controller.CONTROLLER.local\SYSVOL     - Logon server share
PS C:\Users\Administrator>
```

Find OS in network:

```jsx
**PS C:\Users\Administrator> Get-NetComputer -fulldata | select operatingsystem**

operatingsystem
---------------
Windows Server 2019 Standard
Windows 10 Enterprise Evaluation
Windows 10 Enterprise Evaluation
```

More commands & cheatsheet:

<https://gist.github.com/HarmJ0y/184f9822b195c52dd50c379ed3117993#file-powerview-3-0-tricks-ps1-L7>
