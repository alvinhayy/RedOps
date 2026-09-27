---
title: "ServiceNow"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/servicenow.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Quick notes

Useful paths during recon:

- `/login.do`
- `/api/now/sp/widget/<widget_id>`
- `/api/now/table/<table_name>`
- `/stats.do`

The important ServiceNow mistake is often **not a single CVE**, but **public or weak ACLs** reached through a widget or API. Test **widgets** and the **Table REST API** as distinct request paths, while remembering that both ultimately depend on the effective roles plus applicable table, field, and endpoint controls.[\[1\]](#references)[\[3\]](#references)[\[5\]](#references)

## Bootstrap an unauthenticated session

ServiceNow commonly issues a usable **anonymous session** before authentication. Request `/login.do`, keep the cookies (for example `JSESSIONID`), and extract the `g_ck` value used as `X-UserToken`. Reuse that anonymous session for every probe.[\[1\]](#references)

If `/login.do` immediately redirects to SSO/IdP, anonymous bootstrapping may fail, but still inspect the redirect flow (`oauth_redirect.do`) in Burp because some deployments still leak a usable cookie/token pair there.

## Treat Service Portal widgets as backend APIs

A public widget is also a **JSON API**. Service Portal widgets can contain both client-side and server-side logic, so call the exposed endpoint directly instead of assessing only the portal UI.[\[6\]](#references)

```
POST /api/now/sp/widget/WIDGET_ID HTTP/1.1
Host: target.service-now.com
X-UserToken: <public_g_ck>
Cookie: JSESSIONID=<public_session>
Content-Type: application/json
{"payload":{"start":0,"end":1}}
```
Interesting built-in widgets to probe:

- `ticket-attachments`
- `kb-article-page`
- `kb-search`
- `kb-category-list`
- `sc-category`
- `widget-simple-list`

Don’t stop at defaults. Mature instances often contain **custom widgets** with organization-specific ACL assumptions, so enumerate installed widget IDs and test them with the same anonymous session.

## Abuse `widget-simple-list` as a table oracle

`widget-simple-list` as a table oracle
If `widget-simple-list` is public, it can become a **generic table-query primitive**. The attacker supplies a table (`t`) and optionally a display field (`f`), while the widget queries backend records with the permissions of the anonymous session.[\[1\]](#references)[\[3\]](#references)

```
POST /api/now/sp/widget/widget-simple-list?t=incident&f=number HTTP/1.1
Host: target.service-now.com
X-UserToken: <public_g_ck>
Cookie: JSESSIONID=<public_session>
Content-Type: application/json
```
Use curated and environment-specific table/field pairs such as:

- `sys_user.email`
- `incident.number`
- `kb_knowledge.short_description`
- `cmn_department.name`
- `oauth_entity.name`

If `display_value` is `null` but the widget still reports a positive count, treat it as a signal that the **table is reachable** and the chosen field is the wrong one or field-level ACLs differ.

## Test the Table REST API separately

Widget server scripts and the Table REST API are different access paths and can produce different outcomes. A target may block one widget but still expose rows through `/api/now/table/*`; ServiceNow documents that the Table API caller must have sufficient roles for the requested data.[\[5\]](#references)

```
curl -s 'https://target.service-now.com/api/now/table/sys_user?sysparm_limit=1' \
  -H 'X-UserToken: <public_g_ck>' \
  -H 'Cookie: JSESSIONID=<public_session>'
```
Prioritize high-value tables such as `sys_user`, `incident`, `kb_knowledge`, `sc_cat_item`, `cmn_department`, `cmdb_ci`, and `oauth_entity`.

## Count-only responses are blind inference oracles

If ServiceNow refuses to return rows but still reveals **how many records matched** attacker-controlled filters, you have a **count oracle**, not a clean denial. Vary `filterText`, prefixes, or boolean predicates and compare counts to infer protected data incrementally.[\[4\]](#references)

Treat this as **blind data inference**, not direct row disclosure. Report the oracle separately from full record exposure.

## `snowpick`

`snowpick`
[`snowpick`](https://github.com/BishopFox/snowpick) automates the anonymous-session bootstrap, widget discovery, `widget-simple-list` table enumeration, and optional Table REST API probing.[\[1\]](#references)[\[2\]](#references)

```
go install github.com/BishopFox/snowpick@latest
snowpick -target target.service-now.com
snowpick -target target.service-now.com -table-api
snowpick -target target.service-now.com -discover -discover-limit 200
snowpick -targets hosts.txt -concurrency 5 -proxy http://127.0.0.1:8080 -rate 200ms
```
Useful behaviors:

- Distinguishes **`exposed`** rows from**`count_oracle`** findings
- Preserves **bounded evidence** (`record_count` , small samples, reproducible request details)
- Flags public `/stats.do` access
- Supports JSON output for triage and replay

## Detection / validation notes

From a defender or purple-team perspective, review logs for:[\[1\]](#references)

- Anonymous requests to `/api/now/sp/widget/*`
- Anonymous requests to `/api/now/table/*`
- Systematic variation of `t` ,`f` , table names, field names, or`filterText`
- Public access to `/stats.do`

When validating impact, prefer **bounded evidence**: keep the total count, a minimal sample, and a reproducible request instead of bulk-exporting every accessible row.

## References
