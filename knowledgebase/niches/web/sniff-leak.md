---
title: "Sniff Leak"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/xss-cross-site-scripting/sniff-leak.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## Leak Script Content by Interpreting It as UTF-16

If a `text/plain` response lacks the `X-Content-Type-Options: nosniff` header, a browser may accept it as a script. In the cited challenge, an attacker-controlled prefix supplies a UTF-16 byte-order mark and valid JavaScript bytes. The remaining secret is then decoded as valid identifier characters, allowing the script to expose it through a property of `window`.[\[1\]](#references)

## Leak Content by Treating It as an ICO Image

In a related challenge, a crafted prefix makes the response parse as an ICO image and positions one secret byte in the image-width field. Loading successive variants as cross-origin images and reading their `width` reveals the secret one byte at a time.[\[2\]](#references)

## References

- [1] [UIUCTF 2022 Writeup – “modernism” (UTF-16 content-sniffing leak)](https://blog.huli.tw/2022/08/01/en/uiuctf-2022-writeup/#modernism21-solves)
- [2] [UIUCTF 2022 Writeup – “precisionism” (ICO content-sniffing leak)](https://blog.huli.tw/2022/08/01/en/uiuctf-2022-writeup/#precisionism3-solves)
