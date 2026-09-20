---
title: "XSRFProbe v3 — CSRF/XSRF auditing workflow"
source: 0xinfection.xyz
source_url: https://0xinfection.xyz/posts/xsrfprobe-v3.0-a-ground-up-rewrite/
fetched_at: 2026-09-21T00:00:00Z
license: unspecified
category: web
---

# XSRFProbe v3 — CSRF/XSRF auditing workflow

XSRFProbe v3 is a Python toolkit for authorized cross-site request forgery (CSRF/XSRF) assessment. It combines bounded crawling and form/endpoint discovery with a self-calibrating response-difference engine, structured JSON reporting, and optional proof-of-concept generation. Treat it as an assessment aid: it is not a substitute for reviewing application state changes and business impact.

## Safe assessment workflow

1. Obtain written scope, use a disposable test account, and run only against a local or staging target. The tool submits forms and can trigger state changes such as password updates or deletion actions.
2. Crawl only the in-scope origin and review discovered forms/endpoints before enabling active checks. Keep request rate and crawl depth bounded.
3. Establish a baseline with several valid submissions using fresh sessions/tokens. Send a forged-token probe and a plain `GET`/non-state-changing request to confirm that the endpoint produces a distinguishable response.
4. Run a check only when the baseline demonstrates a reliable behavioral difference. Preserve request/response evidence and stop if a check appears to alter data unexpectedly.
5. Export the JSON report and reproduce findings manually with the least-impacting request. Generate a PoC only for a disposable test endpoint.

## Check families

- **Token presence and binding:** missing token, login CSRF, method-switch/omitted-token variants, cross-session token replay, non-session cookie tokens, naive double-submit, empty tokens, and custom-header enforcement.
- **HTTP method/content-type confusion:** `_method=POST`, `X-HTTP-Method-Override`, and alternate content types.
- **Origin and Referer validation:** `Origin: null`, spoofed subdomains, omitted Origin/Referer, and narrowly scoped validation bypass probes.
- **Cookie policy:** SameSite behavior and browser-based SameSite bypass conditions.
- **Token quality:** structure, entropy, predictability, and reuse observations.

Findings should record the check identifier, severity, endpoint, preconditions, baseline/forged response comparison, and remediation. A positive result is meaningful only when the request is state-changing and the server fails to bind it to the user’s intentional action.

## Defensive guidance

Prefer framework-supported synchronizer tokens or correctly bound double-submit tokens, validate Origin/Referer where appropriate, use `SameSite=Lax`/`Strict` as defense-in-depth, require safe methods for reads, and avoid state changes on cross-site requests. Login and sensitive account-management flows need the same CSRF protections as ordinary forms.

## Safety boundary

This material is for authorized testing only. Do not run active checks against production, third-party, or shared-tenant systems; do not use the crawler or PoC generator to create load or perform destructive actions. Store reports without real credentials, session cookies, or personal data.

## References

- [XSRFProbe v3 — A Ground-Up Rewrite](https://0xinfection.xyz/posts/xsrfprobe-v3.0-a-ground-up-rewrite/)
