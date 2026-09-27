---
title: Cross-domain enumeration
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/cross-domain-enumeration
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

## Domain trusts explained

Active Directory Domain Services (AD DS) provides security across multiple domains or forests through domain and forest trust relationships. Before authentication can occur across trusts, Windows must first check if the domain being requested by a user, computer, or service has a trust relationship with the domain of the requesting account.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F2h0S71AkSkFOG0au5sSI%2Ftrust-relationships.png?alt=media&amp;token=3c8fca43-cc04-4fa8-bbed-a2a5208bc784" alt=""><figcaption></figcaption></figure>

## Enumerating domain trust

```
Get-NetForest [-Forest megacorp.local]
Get-Forest [-Forest megacorp.local]
```

Need PowerView\.ps1 for this:

```
Get-NetForestDomain [-Forest megacorp.local]
Get-ForestDomain [-Forest megacorp.local]
```

## Enumerate from one to another domain

If you have a valid account for the child/parent domain and there is a trust between the domains, you can enumerate the other domain using the authentication of the compromised domain.

A great tool can me powershell empire, but you will need to do all enumeration from the compromised DC and run powershell empire. This can trigger AV. A better way is to use BloodyAD. BloodyAD is a remote tool that uses LDAP to enumerate the domain.

### Get all domain users

```
bloodyAD -d compromised-domain.local -u Administrator -p :<nt-hash-or-password> --host ip-of-target-domain get children 'DC=bloody,DC=local' --type user
```

### Get all writable objects

```
bloodyAD -d compromised-domain.local -u Administrator -p :<nt-hash-or-password> --host ip-of-target-domain get writable
```

### More Bloody-AD examples:
