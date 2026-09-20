---
title: "Kerberos Authentication"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/active-directory-methodology/kerberos-authentication.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: ad
---

## TL;DR for attackers

- Kerberos is the default AD auth protocol; most lateral-movement chains will touch it.
- Think in **three operator phases** :<sup>[\[3\]](#references)</sup>  - **AS-REQ / AS-REP** → password/hash/certificate to obtain a**TGT** . This is where**AS-REP roasting** ,**over-pass-the-hash / pass-the-key** , and**PKINIT** live.
  - **TGS-REQ / TGS-REP** → use a TGT to obtain**service tickets** . This is where**Kerberoasting** ,**S4U abuse** ,**delegation abuse** , and most**ticket-forging tradecraft** become relevant.
  - **AP-REQ / AP-REP** → present the ticket to the service. This is where**pass-the-ticket** and service-specific lateral movement happen.
- For hands-on cheatsheets (AS-REP/Kerberoasting, ticket forgery, delegation abuse, etc.) see:
[88tcp/udp - Pentesting Kerberos](../../network-services-pentesting/pentesting-kerberos-88/index.html)
- Use this page as the **overview / “what changed recently”** index, then jump to the dedicated pages for[Kerberoast](kerberoast.html) ,[Resource-Based Constrained Delegation](resource-based-constrained-delegation.html) ,[AD Certificates / PKINIT abuse](ad-certificates.html) , or[BadSuccessor / dMSA abuse](acl-persistence-abuse/BadSuccessor.html) .

## Fresh attack notes (2024-2026)

- **RC4 hardening changed the defaults, not Kerberos itself** – modern DC hardening focuses on the**default assumed encryption types** for accounts that do**not** explicitly set`msDS-SupportedEncryptionTypes` . After the 2026 rollout, those accounts increasingly default to**AES-only** on patched DCs, so blind`/rc4` Kerberoast assumptions fail more often. However,**explicitly RC4-enabled service accounts remain excellent offline-crack targets** .<sup>[\[1\]](#references)</sup>
- **PAC validation enforcement matters for forged tickets** – 2024 PAC-signature hardening means that**golden/diamond/sapphire/extraSID-style abuses** need more realistic PAC data and the correct signing context. Unpatched domains or domains left in compatibility/audit-style deployments stay softer targets.<sup>[\[2\]](#references)</sup>
- **Certificate-based Kerberos changed twice** :
  - **Strong certificate binding** (KB5014754 timeline) makes sloppy certificate-to-account mappings less reliable in fully enforced environments.
  - **CVE-2025-26647** added another hardening layer around`altSecurityIdentities` mappings that use a certificate’s Subject Key Identifier. Patch level, enforcement or audit state, and explicit mapping configuration therefore matter when evaluating pass-the-certificate and related certificate-based paths.<sup>[\[5\]](#references)</sup><sup>[\[6\]](#references)</sup> For PKINIT, the KDC also validates the certificate path and checks that the issuer is trusted through the NTAuth store.<sup>[\[8\]](#references)</sup>
- **Cross-domain / cross-forest delegation abuse is still very alive** – Windows supports modern cross-realm**S4U2Self/S4U2Proxy** flows, so writable delegation attributes in another domain are still valuable. The blocker is usually tooling fidelity and trust/policy details, not protocol support.
- **Recursive multi-domain RBCD matters operationally** – in 3+ domain forests,**S4U2Self/S4U2Proxy** can recurse through trust referrals, and**SPN-less** abuse may require a final**`S4U2Self+U2U`** hop plus RC4-dependent ticket handling. See[Resource-Based Constrained Delegation](resource-based-constrained-delegation.html) .<sup>[\[4\]](#references)</sup>
- **Windows Server 2025 introduced delegated Managed Service Accounts (dMSAs)** and their migration logic. If you see delegated rights over OUs or service-account objects in a 2025 domain, check the dedicated[BadSuccessor page](acl-persistence-abuse/BadSuccessor.html) instead of treating it like “just another gMSA”.<sup>[\[7\]](#references)</sup>

## Fast operator checks in modern domains

Before choosing a Kerberos attack path, quickly answer four questions:

1. **Which accounts are still RC4-friendly?**
2. **Which users do not require pre-auth?**
3. **Which objects expose delegation abuse?**
4. **Which parts of the domain are new enough to enforce recent hardening?**

```
# 1) Service accounts explicitly pinned to RC4 / legacy etypes
Get-ADObject -LDAPFilter '(|(msDS-SupportedEncryptionTypes=4)(msDS-SupportedEncryptionTypes=12))' \
  -Properties samAccountName,servicePrincipalName,msDS-SupportedEncryptionTypes
# 2) Service accounts with no explicit etype config
#    (these increasingly inherit AES-only defaults on patched 2026 DCs)
Get-ADObject -LDAPFilter '(&(servicePrincipalName=*)(!(msDS-SupportedEncryptionTypes=*)))' \
  -Properties samAccountName,servicePrincipalName
# 3) AS-REP roastable users
Get-ADUser -LDAPFilter '(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=4194304))' \
  -Properties userAccountControl
# 4) Delegation hot spots
Get-ADComputer -LDAPFilter '(msDS-AllowedToActOnBehalfOfOtherIdentity=*)' \
  -Properties msDS-AllowedToActOnBehalfOfOtherIdentity
Get-ADObject -LDAPFilter '(|(userAccountControl:1.2.840.113556.1.4.803:=524288)(userAccountControl:1.2.840.113556.1.4.803:=16777216))' \
  -Properties samAccountName,servicePrincipalName,userAccountControl
# 5) DC-side RC4 hardening / compatibility clues
Get-WinEvent -LogName System | Where-Object {
  $_.ProviderName -eq 'Microsoft-Windows-Kerberos-Key-Distribution-Center' -and $_.Id -in 201..209
}
```
Practical interpretation:

- If **interesting SPN accounts are explicitly RC4-capable** , Kerberoasting stays cheap and fast.
- If most service accounts have **no explicit etype configuration** , expect**AES-only** behavior on updated 2026 DCs and plan for slower offline cracking or a different path.
- If **RBCD / KCD / unconstrained delegation** is present, S4U often beats brute-force.
- If **certificate auth** is in play, remember that a failed PKINIT path does**not** always mean the cert is useless; in many environments the same cert still works for**Schannel/LDAPS** abuse (see[AD Certificates / PKINIT abuse](ad-certificates.html) ).

## Common Kerberos errors that change the attack plan

- **`KDC_ERR_ETYPE_NOTSUPP`** → The target account / DC will not use the encryption type you asked for. Stop retrying with RC4 only; supply**AES keys** or request**AES** roast material instead.
- **`KRB_AP_ERR_MODIFIED`** → You likely have the**wrong service key** , the**wrong SPN** , or a forged ticket that does not match the service account actually decrypting it.
- **`KRB_AP_ERR_SKEW`** → Your time is off. Sync to the DC before debugging anything else.
- **`KDC_ERR_BADOPTION`** during S4U / delegation flows → frequently means**sensitive/not-delegable users** , the wrong delegation model, or that you are trying to do**classic KCD** where only**RBCD** would accept a non-forwardable S4U2Self ticket.

## References
