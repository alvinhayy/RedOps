---
title: "powerview enumeration"
source_url: https://www.bordergate.co.uk/powerview/
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: ad
---

PowerView is a PowerShell script to perform common Active Directory enumeration and exploitation tasks. This article lists some common PowerView enumeration commands.

You can obtain a copy of PowerView here; [https://github.com/ZeroDayLab/PowerSploit/blob/master/Recon/PowerView.ps1](https://github.com/ZeroDayLab/PowerSploit/blob/master/Recon/PowerView.ps1).

There is also a .NET port of PowerView, called SharpView in case usage of PowerShell isn’t an option. This can be downloaded here; [https://github.com/tevora-threat/SharpView](https://github.com/tevora-threat/SharpView)

#### ADModule

In addition to PowerView commands, I’ve also listed the equivalent commands using Microsoft.ActiveDirectory.Management.dll.

This is a DLL created by Microsoft to query Active Directory, and is normally used as part of the Microsoft Remote Server Administration Tools (RSAT). RSAT typically requires administrator privileges to install, but we can use the DLL on it’s own.

The benefit of this approach over PowerView is we’re using a Microsoft signed executable, which reduces our chance of getting detected on disk. Unfortunately, the DLL can’t perform all the tasks that PowerView can.

A copy of this DLL can be obtained here; [https://github.com/samratashok/ADModule](https://github.com/samratashok/ADModule)

To access it’s cmdlet’s, import it using the following commands;

```
Import-Module C:\AD\Tools\ADModule-master\Microsoft.ActiveDirectory.Management.dll
Import-Module C:\AD\Tools\ADModule-master\ActiveDirectory\ActiveDirectory.psd1
```
### PowerView Commands

#### Domain Information

| PowerView Command | ADModule | Purpose |
|---|---|---|
| Get-Domain | Get-ADDomain | Find the current domain |
| Get-DomainSID | (Get-ADDomain).DomainSID | Find the current domain’s SID |
| Get-DomainPolicyData | (Get-DomainPolicyData).systemaccess | Returns the default domain policy or the domain controller policy for the current domain |
| Get-DomainController | Get-ADDomainController | Find the current domain controllers |
| Get-DomainOU | Get-ADOrganizationalUnit -Filter * -Properties * | List organisational units in the domain |

#### Enumerating Users, Groups & Computers

| PowerView Command | ADModule | Purpose |
|---|---|---|
| Get-DomainUser \| select samaccountname | Get-ADUser -Filter * -Properties * | List users in current domain |
| Get-DomainComputer | Get-ADComputer -Filter * \| select Name | List computers in the domain |
| Get-DomainGroup \| select Name | Get-ADGroup -Filter * \| select Name | List groups in the domain |
| Get-DomainGroupMember -Identity “Domain Admins” -Recurse | Get-ADGroupMember -Identity “Domain Admins” -Recursive | Find members of the domain admin group |
| Get-NetLocalGroup -ComputerName Computer1 -ListGroups |  | List local groups on remote computer (requires admin privileges) |

#### Domain Trust Enumeration

| PowerView Command | ADModule | Purpose |
|---|---|---|
| Get-NetDomainTrust | Get-ADDomain | Get trusts for the current domain |
| Get-NetForest | Get-ADForest | List forest details |
| Get-NetForestDomain |  | List all domains in forest |
| Get-NetForestTrust |  | Map forest trusts |

#### Share Enumeration

| PowerView Command | Purpose |
|---|---|
| Get-NetShare -ComputerName sqlserver | List shares on a machine |
| Invoke-ShareFinder | Search for shares on the network |
| Invoke-FileFinder | Search for files on the network |
| Get-NetFileServer | List file servers in the domain |

#### User Hunting

| PowerView Command | Purpose |
|---|---|
| Get-NetLoggedonLocal -ComputerName Computer1 | Find logged in users using the remote registry service (which is started by default on Windows server). Does not require admin privileges. |
| Invoke-UserHunter -CheckAccess | Check if domain administrators are logged into workstations |

#### GPO Enumeration

| PowerView Command | Purpose |
|---|---|
| Get-DomainGPO | List group policy objects in a domain |
| Get-DomainGPOLocalGroup | Returns all GPOs in a domain that modify local group memberships through ‘Restricted Groups’ or Group Policy preferences |

#### ACL Enumeration

| PowerView Command | Purpose |
|---|---|
| Get-DomainObjectAcl -SamAccountName test -ResolveGUIDs | Get an ACL for a specific object |
| Find-InterestingDomainAcl -ResolveGUIDs | Find interesting domain ACL’s |

#### Kerberos Delegation

| PowerView Command | Purpose |
|---|---|
| Get-DomainComputer -Unconstrained | Check for unconstrained delegation hosts |
| Get-DomainUser -TrustedToAuth | Check for constrained delegation hosts |

## Automating PowerView ACL Enumeration

The below PowerShell code can be used to check for exploitable ACL’s from the context of the current user.

```
Function Invoke-ACLChecks {
Write-Host ("Checking for GenericALL ACL's")
Get-DomainUser | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}}
Get-DomainGroup | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq$("$env:UserDomain\$env:Username")) {$_}}
Write-Host ("Checking for WriteDACL's")
Get-DomainUser | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}}
Write-Host ("Checking for unconstrained delegation")
Get-DomainComputer -Unconstrained
Write-Host ("Checking for constrained delegation")
Get-DomainUser -TrustedToAuth
Write-Host ("Checks done")
}
```
