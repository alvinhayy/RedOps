---
title: "LDAP port (389, 636, 3268, 3269)"
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/ldap
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---
LDAP, the Lightweight Directory Access Protocol, is a mature, flexible, and well supported standards-based mechanism for interacting with directory servers. It’s often used for authentication and storing information about users, groups, and applications, but an LDAP directory server is a fairly general-purpose data store and can be used in a wide variety of applications.

***

**389, 636, 3268, 3269 - Pentesting LDAP from Hacktricks:**

[389, 636, 3268, 3269 - Pentesting LDAP](https://book.hacktricks.xyz/network-services-pentesting/pentesting-ldap)

## LDAPSearch

```bash
sudo apt-get install ldapsearch
```

<https://devconnected.com/how-to-search-ldap-using-ldapsearch-examples/>

**Search for namingcontext:**

```bash
ldapsearch -h 10.10.11.129 -x -s base namingcontexts
```

search.htb shows up as “DC=search,DC=htb”

**Try to go deeper in ldap with namingcontext:**

```bash
ldapsearch -x -b "dc=devconnected,dc=com" -H ldap://192.168.178.29
```

if the output is like:

```bash
# search result
search: 2
result: 1 Operations error
text: 000004DC: LdapErr: DSID-0C090A5C, comment: In order to perform this opera
 tion a successful bind must be completed on the connection., data 0, v4563
```

Then, LDAP is authenticated.

**Authenticate to LDAP if you have creds, and try again:**

```bash
ldapsearch -h 10.10.11.129 -D 'hope.sharp@search.htb' -w "IsolationIsKey?" -b "DC=search,DC=htb"
```

**Nmap automatic scan:**

```bash
nmap -Pn -n -sV --script=ldap* -p 389 10.10.10.175 -vv
```

## LDAPDomainDump

In an Active Directory domain, a lot of interesting information can be retrieved via LDAP by any authenticated user (or machine). This makes LDAP an interesting protocol for gathering information in the recon phase of a pentest of an internal network. A problem is that data from LDAP often is not available in an easy to read format.

ldapdomaindump is a tool which aims to solve this problem, by collecting and parsing information available via LDAP and outputting it in a human readable HTML format, as well as machine readable json and csv/tsv/greppable files.

**Get tool:**

```bash
git clone https://github.com/dirkjanm/ldapdomaindump
```

**Usage:**

```bash
ldapdomaindump -u search.htb\\hope.sharp -p 'IsolationIsKey?' 10.10.11.129 -o ldap/
```
