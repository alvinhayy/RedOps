---
title: "hop-by-hop headers"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/abusing-hop-by-hop-headers.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

### Abusing Hop-by-Hop Headers

Security problems arise when front-end and back-end components disagree about which fields were removed or which component was responsible for a control. For example, `Connection: X-Forwarded-For` can cause one proxy to strip an authentication-relevant field before the request reaches a later component.[\[1\]](#references)

### Testing for Hop-by-Hop Header Handling

The handling of hop-by-hop headers can be tested by observing changes in server responses when specific headers are marked as hop-by-hop. Tools and scripts can automate this process, identifying how proxies manage these headers and potentially uncovering misconfigurations or proxy behaviors.

Abusing hop-by-hop headers can lead to various security implications. Below are a couple of examples demonstrating how these headers can be manipulated for potential attacks:

### Bypassing Security Controls with `X-Forwarded-For`

`X-Forwarded-For`
An attacker can nominate `X-Forwarded-For` as hop-by-hop to make a compliant intermediary remove it. The exploit is not that the proxy forwards a spoofed value; it is that a downstream component may fail open when the trusted provenance field is unexpectedly absent.

**Attack Scenario:**

1. The attacker sends an HTTP request to a web application behind a proxy, including a fake IP address in the `X-Forwarded-For` header.
2. The attacker also includes the `Connection: close, X-Forwarded-For` header, prompting the proxy to treat`X-Forwarded-For` as hop-by-hop.
3. The misconfigured proxy forwards the request to the web application without the spoofed `X-Forwarded-For` header.
4. The web application, not seeing the original `X-Forwarded-For` header, might consider the request as coming directly from a trusted proxy, potentially allowing unauthorized access.

### Cache Poisoning via Hop-by-Hop Header Injection

If a nominated field changes an origin response but is omitted from the cache key, a cache may store the attacker-influenced response and serve it to other users. Whether `Cookie` can be nominated, removed, and cached this way depends on the exact intermediary chain and cache policy; confirm each hop instead of assuming the scenario works generically.[\[1\]](#references)

**Attack Scenario:**

1. An attacker sends a request to a web application with a hop-by-hop header that should not be cached (e.g., `Connection: close, Cookie` ).
2. The poorly configured cache server does not remove the hop-by-hop header and caches the response specific to the attacker’s session.
3. Future users requesting the same resource receive the cached response, which was tailored for the attacker, potentially leading to session hijacking or exposure of sensitive information.

## References
