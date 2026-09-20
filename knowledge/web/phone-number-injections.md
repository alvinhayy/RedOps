---
title: "Phone Number Injections"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/phone-number-injections.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## OTP Rate-Limit Bypass

If a rate limiter keys attempts by the exact submitted string but the delivery provider normalizes multiple parameterized values to the same destination, an attacker may rotate suffixes to obtain separate attempt counters for one account. The figure illustrates the concept with changing `ext` values; successful exploitation depends on the application’s and provider’s normalization behavior.[\[2\]](#references)

## References

- [1] [RFC 3966 - The `tel` URI for Telephone Numbers](https://www.rfc-editor.org/rfc/rfc3966.html)
- [2] [NahamCon EU 2022 - RTFR (Read The Bleeping RFC), securinti](https://www.youtube.com/watch?v=4ZsTKvfP1g0)
