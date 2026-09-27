---
title: "AD information in printers"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/active-directory-methodology/ad-information-in-printers.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: ad
---

# Information in Printers

## Printer Configuration

- **Location** : The LDAP server list is usually found in the web interface (e.g.*Network ➜ LDAP Setting ➜ Setting Up LDAP* ).
- **Behavior** : Many embedded web servers allow LDAP server modifications**without re-entering credentials** (usability feature → security risk).
- **Exploit** : Redirect the LDAP server address to an attacker-controlled host and use the*Test Connection* /*Address Book Sync* button to force the printer to bind to you.

## Capturing Credentials

### Method 1 – Netcat Listener

```
sudo nc -k -v -l -p 389     # LDAPS → 636 (or 3269)
```
Small/old MFPs may send a simple *simple-bind* in clear-text that netcat can capture. Modern devices usually perform an anonymous query first and then attempt the bind, so results vary.[\[1\]](#references)

### Method 2 – Full Rogue LDAP server (recommended)

Because many devices will issue an anonymous search *before* authenticating, standing up a real LDAP daemon yields much more reliable results:[\[1\]](#references)

```
# Debian/Ubuntu example
sudo apt install slapd ldap-utils
sudo dpkg-reconfigure slapd   # set any base-DN – it will not be validated
# run slapd in foreground / debug 2
slapd -d 2 -h "ldap:///"      # only LDAP, no LDAPS
```
When the printer performs its lookup you will see the clear-text credentials in the debug output.

💡  You can also use `impacket/examples/ldapd.py` (Python rogue LDAP) or `Responder -w -r -f` to harvest NTLMv2 hashes over LDAP/SMB.

## Recent Pass-Back Vulnerabilities (2024-2025)

Pass-back is *not* a theoretical issue – vendors keep publishing advisories in 2024/2025 that exactly describe this attack class.

### Xerox VersaLink – CVE-2024-12510 & CVE-2024-12511

Firmware ≤ 57.69.91 of Xerox VersaLink C70xx MFPs allowed an authenticated admin (or anyone when default creds remain) to:

- **CVE-2024-12510 – LDAP pass-back** : change the LDAP server address and trigger a lookup, causing the device to leak the configured Windows credentials to the attacker-controlled host.
- **CVE-2024-12511 – SMB/FTP pass-back** : identical issue via*scan-to-folder* destinations, leaking NetNTLMv2 or FTP clear-text creds.<sup>[\[2\]](#references)</sup>

A simple listener such as:

```
sudo nc -k -v -l -p 389     # capture LDAP bind
```
or a rogue SMB server (`impacket-smbserver`) is enough to harvest the credentials.

### Canon imageRUNNER / imageCLASS – Advisory 20 May 2025

Canon confirmed a **SMTP/LDAP pass-back** weakness in dozens of Laser & MFP product lines. An attacker with admin access can modify the server configuration and retrieve the stored credentials for LDAP **or** SMTP (many orgs use a privileged account to allow scan-to-mail).[\[3\]](#references)

The vendor guidance explicitly recommends:

1. Updating to patched firmware as soon as available.
2. Using strong, unique admin passwords.
3. Avoiding privileged AD accounts for printer integration.

## Automated Enumeration / Exploitation Tools

| Tool | Purpose | Example |
|---|---|---|
| **PRET** (Printer Exploitation Toolkit) | PostScript/PJL/PCL abuse, file-system access, default-creds check, *SNMP discovery* | `python pret.py 192.168.1.50 pjl` |
| **Praeda** | Harvest configuration (including address books & LDAP creds) via HTTP/HTTPS | `perl praeda.pl -t 192.168.1.50` |
| **Responder / ntlmrelayx** | Capture & relay NetNTLM hashes from SMB/FTP pass-back | `responder -I eth0 -wrf` |
| **impacket-ldapd.py** | Lightweight rogue LDAP service to receive clear-text binds | `python ldapd.py -debug` |

## Hardening & Detection

1. **Patch / firmware-update** MFPs promptly (check vendor PSIRT bulletins).
2. **Least-Privilege Service Accounts** – never use Domain Admin for LDAP/SMB/SMTP; restrict to*read-only* OU scopes.
3. **Restrict Management Access** – place printer web/IPP/SNMP interfaces in a management VLAN or behind an ACL/VPN.
4. **Disable Unused Protocols** – FTP, Telnet, raw-9100, older SSL ciphers.
5. **Enable Audit Logging** – some devices can syslog LDAP/SMTP failures; correlate unexpected binds.
6. **Monitor for Clear-Text LDAP binds** on unusual sources (printers should normally talk only to DCs).
7. **SNMPv3 or disable SNMP** – community`public` often leaks device & LDAP config.

## References
