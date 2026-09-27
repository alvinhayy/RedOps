---
title: "SMB port (139,445)"
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/smb
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---
## SMB | Port (139,445)

***

### Hacktricks

[139,445 - Pentesting SMB](https://book.hacktricks.xyz/network-services-pentesting/pentesting-smb)

### IPC$ share

From book ***Network Security Assessment 3rd edition***

With an anonymous null session you can access the IPC$ share and interact with services exposed via named pipes. The enum4linux utility within Kali Linux is particularly useful; with it, you can obtain the following:

* Operating system information
* Details of the parent domain
* A list of local users and groups
* Details of available SMB shares
* The effective system security policy

### Exploit SMB

To look for possible exploits to the SMB version it important to know which version is being used. If this information does not appear in other used tools, you can:

Use the **MSF** auxiliary module \_**auxiliary/scanner/smb/smb\_version**

\_Or\*\* this script\*\*:

```bash
#!/bin/sh
#Author: rewardone
#Description:
# Requires root or enough permissions to use tcpdump
# Will listen for the first 7 packets of a null login
# and grab the SMB Version
#Notes:
# Will sometimes not capture or will print multiple
# lines. May need to run a second time for success.
if [ -z $1 ]; then echo "Usage: ./smbver.sh RHOST {RPORT}" && exit; else rhost=$1; fi
if [ ! -z $2 ]; then rport=$2; else rport=139; fi
tcpdump -s0 -n -i tap0 src $rhost and port $rport -A -c 7 2>/dev/null | grep -i "samba\|s.a.m" | tr -d '.' | grep -oP 'UnixSamba.*[0-9a-z]' | tr -d '\n' & echo -n "$rhost: " &
echo "exit" | smbclient -L $rhost 1>/dev/null 2>/dev/null
echo "" && sleep .1
```

### Enum4Linux

[https://www.kali.org/tools/enum4linux/#:\~:text=Enum4linux is a tool for,%2C rpclient%2C net and nmblookup](https://www.kali.org/tools/enum4linux/#:~:text=Enum4linux%20is%20a%20tool%20for,%2C%20rpclient%2C%20net%20and%20nmblookup).

```bash
enum4linux -a [-u "<username>" -p "<passwd>"] <IP>
```

### SMBclient

**List shares:**

```bash
smbclient -L //10.10.10.134 -N
```

**Connect to share (anonymous)**

```bash
smbclient //10.10.10.134/Backups -N
```

### SMB client with kerberos

We can use impacket-smbclient to authenticate using kerberos. May come in handy when NTLM authentication is disabled

```bash
impacket-smbclient -k scrm.local/ksimpson:ksimpson@DC1.scrm.local
```
