---
title: "Privilege Escalation"
source_url: https://htb.linuxsec.org/active-directory/privilege-escalation
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: ad
---

Windows Privilege Escalation Checks

Privilege escalation checks on Windows involve examining various aspects of the system and its configuration to identify potential vulnerabilities or misconfigurations that could be exploited to elevate privileges.

### Labs

### Tools and Checklists

Here are some common tools and checks used for privilege escalation on Windows systems:

### WinPEAS

Windows Privilege Escalation Awesome Scripts

### Unattended Windows Installations

When installing Windows on a large number of hosts, administrators may use Windows Deployment Services, which allows for a single operating system image to be deployed to several hosts through the network. These kinds of installations are referred to as unattended installations as they don't require user interaction. Such installations require the use of an administrator account to perform the initial setup, which might end up being stored in the machine in the following locations:

- C:\Unattend.xml
- C:\Windows\Panther\Unattend.xml
- C:\Windows\Panther\Unattend\Unattend.xml
- C:\Windows\system32\sysprep.inf
- C:\Windows\system32\sysprep\sysprep.xml

### UACME

UAC Bypass

### PowerUp

PowerUp.ps1 is a program that enables a user to perform quick checks against a Windows machine for any privilege escalation opportunities. It is not a comprehensive check against all known privilege escalation techniques, but it is often a good place to start when you are attempting to escalate local privileges.

### PrivescCheck

This script aims to identify Local Privilege Escalation (LPE) vulnerabilities that are usually due to Windows configuration issues, or bad practices. It can also gather useful information for some exploitation and post-exploitation tasks.

Last updated
