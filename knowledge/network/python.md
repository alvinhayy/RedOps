---
title: "Python"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/python.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Python-specific execution probe

When an input appears to be evaluated as a Python expression, a harmless call to `str()` can help confirm that the result is being executed rather than reflected verbatim. Adapt the surrounding quotes to the injection context:[\[1\]](#references)

```
"+str(True)+"  # If True is printed, the expression was evaluated.
```
Do not treat this probe alone as proof that arbitrary statements or operating-system commands can run; the sink may expose only a restricted expression language.

## Related techniques

[SSTI (Server Side Template Injection)](../../pentesting-web/ssti-server-side-template-injection/index.html)

## References
