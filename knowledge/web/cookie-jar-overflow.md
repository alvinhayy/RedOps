---
title: "Cookie Jar Overflow"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/hacking-with-cookies/cookie-jar-overflow.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

```
const attrs = "Path=/";
let prev = -1;
for (let i = 0; i < 400; i++) {
  document.cookie = `junk${i}=${"A".repeat(32)}; ${attrs}`;
  const visible = document.cookie ? document.cookie.split(/; */).length : 0;
  if (visible === prev) break;
  prev = visible;
}
```
## Overwriting `HttpOnly` Cookies

`HttpOnly` Cookies
This technique can still be used to **evict an `HttpOnly` cookie and then recreate it without `HttpOnly`**, but only if you can **match the original scope** (`name`, `Path`, and host/`Domain` behavior):[\[1\]](#references)

```
const targetScope = "Path=/app; Secure";
for (let i = 0; i < 250; i++) {
  document.cookie = `junk${i}=${crypto.randomUUID()}; ${targetScope}`;
}
document.cookie = `session=attacker-controlled; ${targetScope}`;
```
If the original cookie was set for a different `Path` or with a wider `Domain`, you may only create a sibling cookie and the server will receive both. At that point, ordering rules and server parsing decide which one wins, so check [cookie tossing](cookie-tossing.html) as well.

Caution

This attack does **not** let JavaScript modify `HttpOnly` in place. The practical primitive is: **evict first, then create a new non-`HttpOnly` cookie with the same scope**.

## Reliability Notes

- **Eviction is not always “oldest cookie first”** . In Chromium the garbage collector is LRU-like and tends to preserve more valuable cookies longer, especially`Secure` and higher-priority cookies. A recently used session cookie is usually harder to evict than a stale low-priority one.<sup>[\[2\]](#references)</sup>
- **Profile the real cookie first** . Before overflowing, capture the original`Set-Cookie` in Burp/DevTools and note`Path` ,`Domain` ,`Priority` , prefixes, and whether the cookie is`Partitioned` .
- **Prefer first-party execution** . Modern browsers increasingly isolate or block third-party cookies. If the cookie is partitioned (`Partitioned` / CHIPS, or browser-enforced third-party partitioning), overflowing the jar of`cdn.example` while embedded in`siteA.com` will not evict the cookie that the same origin uses as a top-level site or while embedded in`siteB.com` .<sup>[\[3\]](#references)</sup>
- **Prefixed cookies reduce the impact** .`__Host-` constrains scope, while browsers that enforce the newer`__Http-` and`__Host-Http-` prefixes require the cookie to be set through`Set-Cookie` with`Secure` and`HttpOnly` . JavaScript may still be able to evict one of these cookies, but it cannot recreate a conforming same-named replacement through`document.cookie` .<sup>[\[4\]](#references)</sup>

## References

- [1] [Overwriting HttpOnly cookies from JavaScript using cookie jar overflow](https://www.sjoerdlangkemper.nl/2020/05/27/overwriting-httponly-cookies-from-javascript-using-cookie-jar-overflow/)
- [2] [Chromium eviction notes](https://blog.yoav.ws/posts/how_chromium_cookies_get_evicted/)
- [3] [CHIPS / partitioned cookies](https://privacysandbox.google.com/cookies/chips)
- [4] [HTTP State Management Mechanism (draft RFC 6265bis)](https://httpwg.org/http-extensions/draft-ietf-httpbis-rfc6265bis.html)
