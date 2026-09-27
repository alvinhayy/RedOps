---
title: "Recon - Domain Recon"
source_url: https://notes.qazeer.io/active-directory/recon-domain_recon
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: ad
---

### Active Directory recon tools

The tools presented below are usable through Pass-the-Hash attack using the `sekurlsa::pth` module of `mimikatz`:

`sekurlsa::pth /user:<USERNAME> /domain:<DOMAIN> /ntlm:<HASH> /run:<mmc.exe | powershell.exe>`
Refer to the `Windows - Lateral movement` note, section `Mimikatz Pass-The-Hash`, for more information.

The Microsoft `Remote Server Administration Tools (RSAT)` utilities and PowerShell cmdlets (except for the `Group Policy Management Editor` utility) and the PowerShell `PowerView` cmdlets can usually be used on out of domain computer by specifying `PSCredential` object:

```
$secpasswd = ConvertTo-SecureString "<PASSWORD>" -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential ("<DOMAIN>\<USERNAME>", $secpasswd)
<RSAT_AD_CMDLET> -Credential <PSCredential> -Server <DC_HOSTNAME | DC_IP>
```
**[GUI] Microsoft Management Console (mmc.exe)**

The `Microsoft Management Console (MMC)` utility allows for the loading of the `Remote Server Administration Tools (RSAT)` utilities, such as `Active Directory Users and Computers (dsa.msc)` and `Active Directory Domains and Trusts (domain.msc)`, under the same security context, possibly obtained through Pass-the-Hash.

The process to load an utility is as follow:

`File -> Add/Remove Snap-in (Ctrl + M) -> Selection of one or multiple chosen snap-in`
Once the utility is loaded, the Domain Controller queried by the snap-in may be specified by right clicking on the utility and going through the `Change Directory Server` / `Change Active Directory Domain Controller` form.

**[GUI] Sysinternals's AdExplorer**

`Active Directory Explorer (ADExplorer)`, part of the `Sysinternals` suite, is a standalone graphical utility that can be used to access and browse Active Directory domains. `AdExplorer` presents the advantage of being digitally signed by Microsoft and potentially legitimately used in the environment. `ADExplorer` rely on the `LDAP` protocol (port `TCP` 389) by default, and supports the `LDAPS` protocol (port `TCP` 636).

While `AdExplorer` connection prompt contains username and password fields, the current security context is used for the connection if both fields are left empty.

As one of it's most predominant feature, `AdExplorer` offers the ability to take "snapshots" of the Active Directory domain, allowing for off-target / offline viewing of Active Directory objects. For medium to large sized domains, a snapshot can weight hundreds of megabytes to a few gigabytes.

Once connected to an Active Directory domain, the procedure to take a snapshot is as follow:

`AdExplorer` snapshots can be used as an ingestor for `BloodHound` using the [`ADExplorerSnapshot.py`](https://github.com/c3c/ADExplorerSnapshot.py) Python script. Refer to the `[ActiveDirectory] Recon - AD scanners` note for more information.

**[CLI] Remote Server Administration Tools (RSAT) - PowerShell**

The `Remote Server Administration Tools (RSAT)` suite includes a number of utilities useful for Active Directory reconnaissance and notably the `Active-Directory` module for Windows PowerShell. The `Active-Directory` module consolidates a group of cmdlets, that can be used to retrieve information and manage Active Directory domains. The cmdlets of `ActiveDirectory` module rely on the `Active Directory Web Services (ADWS)` over port `TCP` 9389.

While the `RSAT` requires Administrator level-privileges to be installed, the `DLL` `Microsoft.ActiveDirectory.Management.dll` can be directly imported from an unprivileged user session. The `DLL` is usually located at the following path: `%SystemRoot%\Microsoft.NET\assembly\GAC_64\Microsoft.ActiveDirectory.Management\[...]` on a system with the `RSAT` installed.

Note however that all objects properties will not be retrieval following a direct import of **only** the `Microsoft.ActiveDirectory.Management.dll`. This can be addressed by importing the PowerShell Active Directory `module manifest`, with the necessary files available, after importing the module `DLL`. The files are usually located in `%SystemRoot%\System32\WindowsPowerShell\v1.0\Modules\ActiveDirectory\`.

Once the `DLL` has been uploaded to the target, or made accessible on a network share, the Active Directory module can be imported:

The [`Import-ActiveDirectory.ps1`](https://github.com/samratashok/ADModule) PowerShell script, in-lining the `Microsoft.ActiveDirectory.Management.dll`, may also be used to import the Active Directory module:

**[CLI] PowerSploit PowerView**

`PowerView` is a PowerShell tool to gain network situational awareness on Windows domains. It contains a set of pure-PowerShell replacements for various windows "net" commands, which utilize PowerShell AD hooks and underlying Win32 API functions to perform useful Windows domain functionality.

It also implements various useful metafunctions, including some custom-written user-hunting functions which will identify where on the network specific users are logged into. It can also check which machines on the domain the current user has local administrator access on. Several functions for the enumeration and abuse of domain trusts also exist.

The `dev` branch has the most up-to-date cmdlets: `git clone --single-branch --branch dev https://github.com/PowerShellMafia/PowerSploit.git`

`PowerSploit` can trigger antivirus software. To bypass such controls, inject it directly in memory:

`SharpView.exe` is a C# port of `PowerView` and support a number of the `PowerView`'s cmdlets.

**[CLI] AdFind**

`AdFind` is a command-line `C++` utility that can be used as a standalone binary for Active Directory reconnaissance. `AdFind` implements a number of aliases to facilitate enumeration as well as the possibility to make direct `LDAP` query.

**[CLI] Active Directory Services Interfaces (ADSI)**

`Active Directory Services Interfaces (ADSI)` is a set of interfaces built-in the Windows operating system. The `DirectoryEntry` and `DirectorySearcher` classes can be used on Windows system to query `AD Domain Services` with the advantage of not requiring any additional pre-requisite or tooling.

### Active Directory forest

To retrieve forest information, the following commands can be used:

### Active Directory domains

To retrieve domain information, the following commands can be used:

### Forest and domain trust relationships

Trust relationships define an administrative and security link between two Windows forests or domains. They enable a user to access resources that are located in a forest or domain that’s different from the user’s proper forest or domain.

*Directions*

A trust relationship can be:

- one-way, given by one forest or domain, the trusting object, to another domain or forest, the trusted object
- two-way, meaning permissions extend mutually from both objects.

*Transitivity*

A transitive trust is a trust that is extended not only to the directly trusted object, but also to each objects that the trusted object trusts.

*Default and configured trusts*

All domains in a forest trust each others by default. External trusts can also be configured between domains of different forests.

The following different types of trusts exist in Active Directory:

`Parent-Child`

Two-way

Transitive

Created automatically between a child domain and its domain parent

`Tree-Root`

Two-way

Transitive

Created automatically when a new Tree is added to a forest

`Shortcut`

One-way or two-way

Transitive

Created manually to improve performance between two domains in the same forest

`External`
`Forest`

One or two-way

Non-transitive by default

Manually created trusts between, respectively, domains of different forests or different forests

`Realm`

One-way or two way

Transitive or non-transitive

Manually created trusts between an Active Directory forest and a non-Windows Kerberos directory

To retrieve the trusts affecting a forest or domain, the following commands can be used:

### SID resolution

The PowerShell `Get-ADObject` cmdlet, of the `ActiveDirectory` module, `PowerView`'s `ConvertFrom-SID` and `AdFind.exe` can be used to resolve the `SID` associated with any object (user, group, computer, etc.):

### Organizational Units

### Computers

**Computer details**

To retrieve specific computer information or list the computers in the domain, the following commands can be used:

**Computer search**

To search for computers the following commands can be used:

**Domain Controllers**

To list the domain controllers in the current or specified domain or forest, the following commands can be used:

**Exchange servers**

To list the Exchange servers of the current or specified domain or forest, the following commands can be used:

**Sites and subnets**

The sites and subnets registered in Active Directory can provide information about the network topology and physical location of computers of the environment.

The sites and subnets can be listed, and exported in a text format, using the `Active Directory Sites and Services` snap-in (`dssite.msc`). The snap-in can be used for enumeration from domain-joined and non-domain joined machine.

The PowerShell cmdlet `Get-ADReplicationSubnet` of the `ActiveDirectory` module can also be used to enumerate the subnets:

**ADI DNS hostnames enumeration**

[`adidnsdump`](https://github.com/dirkjanm/adidnsdump) can be used to enumerate all `DNS records` in an Active Directory domain / forest by listing the child objects of the `DNS zones` containers and then using direct `DNS` queries to resolve the enumerated `DNS records`. Using a direct `DNS` resolution is required as the attributes of the `DNS record` object itself, including the associated `IP` address, may not be accessible to any authenticated users, while the name of the record (and thus the corresponding hostname) is.

Leveraging `DNS` records instead of retrieving the `dNSHostName` attribute of machine account objects provide the advantage of allowing enumeration of systems that may have a DNS entry in the domain but are not directly joined to it.

**Network scan**

AD queries can be used in combination with a network scan tool, such as nmap, to quickly identity computers running specific services.

Example for quickly gathering the servers and computers running SMB, which could be used for lateral movement:

### Users

**User details**

To retrieve specific user information or list the users in the domain, the following commands can be used:

**User search**

To search for users the following commands can be used:

**Enterprise and Domain Admins**

The following queries list the `Domain Administrators` and / or the current and past privileged users (users that have their `adminCount` attribute set to `1`) of the domain:

To check if the current user is a Domain Admin, a listing of the "C:" drive of a domain controller can be attempted:

**Privileged users**

The PowerShell script below can be used to list the members of the privileged domain groups.

The members of these groups can ultimately compromise the domain. Refer to the `[ActiveDirectory] Operators to Domain Admins` note for more information on the privilege escalation possibilities.

### Groups

**Enumerate groups**

The following commands can be used to enumerate the domain groups and the members of a specific group:

**User's groups**

The following commands can be used to retrieve the groups the specified user is member of:

**Local groups**

The following commands can be used to enumerate the local groups on a specific computer:

### Unconstrained Kerberos delegation

The following commands can be used to retrieve the computers and service account making uses of unconstrained Kerberos delegation:

### Search by Security Identifier

Active Directory objects can be searched by their `Security Identifier (SID)` using the following PowerShell cmdlets:

### Group Policy (GPO)

The `Grouper2` C# application can be used to enumerate a number of sensible parameters as well as access rights on the GPO object themselves and the associated GPO files (in the `SYSVOL` directory of Domain Controllers):

The following PowerShell script can be used to generate `XML` and `HTML` reports of all the `GPO` defined in the current domain:

### References

https://www.alitajran.com/get-organizational-units-with-powershell/

Last updated
