---
title: "WAF Landscape — Detection, Fingerprinting & Evasion (Curated)"
source: 0xInfection/Awesome-WAF
source_url: https://github.com/0xInfection/Awesome-WAF
fetched_at: 2026-09-20T19:15:00Z
license: apache-2.0
category: web
---

# WAF Landscape — Detection, Fingerprinting & Evasion (Curated)

Curated index of [0xInfection/Awesome-WAF](https://github.com/0xInfection/Awesome-WAF) (Apache-2.0, community-maintained), reorganized for WAF benchmark and evasion-research use. The upstream catalog documents 140 WAF products with manual fingerprints, evasion technique categories, per-vendor known bypasses, and tooling. This document condenses the structure and the benchmark-relevant signals; consult the upstream README for full per-WAF fingerprint details.

## How WAFs Work

- Rule-based separation of normal vs malicious requests; some products add a learning mode that derives rules from observed user behaviour.
- **Operation models:**
  - *Negative (blacklist)* — pre-set signatures block clearly malicious requests (e.g. a rule blocking `<script>…</script>` inputs stops basic XSS). Common choice for public-facing apps.
  - *Positive (whitelist)* — only traffic matching explicit criteria passes (e.g. GET from certain IPs). Effective against large-scale attacks but blocks legitimate traffic; best for internal apps with a limited user group.
  - *Mixed/hybrid* — blacklist for the public surface, whitelist for sensitive areas such as admin panels.

## Detection & Fingerprinting

### Where to look

- Common HTTP ports first (`80`, `443`, `8000`, `8080`, `8888`), but a WAF can sit on any HTTP port — enumerate HTTP services before hunting.
- WAF-set cookies (Citrix NetScaler, Yunsuo), extra headers (Anquanbao, AWS WAF), header jumbling (NetScaler, BIG-IP), `Server` header values (Approach, WTS-WAF), blockpage content (DotDefender, Armor, SiteLock), and unusual status codes on malicious requests (WebKnight, 360).

### Provocation techniques (active detection)

1. Baseline GET from a browser; record response headers/cookies.
2. Repeat via curl without a user-agent; diff response content and headers.
3. Banner-grab random open ports.
4. Inject common detectable payloads (e.g. `" or 1 = 1 --`) into login pages.
5. Inject noisy payloads (`<script>alert()</script>`) into search/contact forms.
6. Append `../../../etc/passwd` to a random parameter.
7. Append catchy keywords such as `' OR SLEEP(5) OR '` to a random parameter.
8. Request with outdated protocols (HTTP/0.9).
9. Watch the `Server` header vary across interactions.
10. Drop-action technique — raw crafted FIN/RST packet and observe the response (HPing3, Scapy).
11. Side-channel: examine timing behaviour of request/response.

### Fingerprint catalog (140 WAFs)

Upstream table lists per-WAF detectability and methodology. Covered products include: 360, aeSecure, Airlock, Alert Logic, Aliyundun, Anquanbao, Anyu, Approach, Armor Defense, ArvanCloud, ASPA, ASP.NET Generic, Astra, AWS ELB, Baidu Yunjiasu, Barikode, Barracuda, Bekchy, BinarySec, BitNinja, BIG-IP ASM, BlockDos, Bluedon IST, BulletProof Security Pro, CDN NS Application Gateway, Chaitin Safeline, ChinaCache, Cisco ACE XML Gateway, Cloudbric, Cloudflare, CloudfloorDNS, CloudFront, Comodo cWatch, CrawlProtect, Deny-All, Distil, DoSArrest, DotDefender, DynamicWeb, e3Learning, Eisoo Cloud, Expression Engine, F5 ASM, FortiWeb, GoDaddy, GreyWizard, Huawei Cloud, HyperGuard, IBM DataPower, Imperva Incapsula, Imunify360, IndusGuard, Instart DX, ISA Server, Janusec, Jiasule, KeyCDN, KnownSec, LiteSpeed, Malcare, MissionControl, ModSecurity, ModSecurity CRS, NAXSI, Nemesida, Netcontinuum, NetScaler AppFirewall, NevisProxy, NewDefend, Nexusguard, NinjaFirewall, NSFocus, NullDDoS, onMessage Shield, OpenResty Lua WAF, Palo Alto, PentaWAF, pkSecurityModule, Positive Technologies, PowerCDN, Profense, Puhui, Qiniu CDN, Radware AppWall, Reblaze, Request Validation Mode, RSFirewall, Sabre, Safe3, SafeDog, SecKing, SecuPress, Secure Entry, SecureIIS, SecureSphere, SEnginx, ServerDefender VP, Shadow Daemon, ShieldSecurity, SiteGround, SiteLock TrueShield, SonicWall, Sophos UTM, SquareSpace, SquidProxy IDS, StackPath, Stingray, Sucuri CloudProxy, Synology Cloud, Tencent Cloud, Teros, TrafficShield, TransIP, UCloud UEWaf, URLMaster, URLScan, USP Secure Entry, Varnish CacheWall, Viettel, VirusDie, WallArm, WatchGuard IPS, WebARX, WebKnight, WebLand, WebRay, WebSEAL, WebTotem, West263CDN, Wordfence, WTS-WAF, XLabs Security, Xuanwudun, Yunaq Chuangyu, Yundun, Yunsuo, YxLink, ZenEdge, ZScaler.

Representative signal families (full detail upstream):

- **Unique status codes** — e.g. 360 replies `493` on unusual requests; Airlock commonly `406`; WebKnight `999`.
- **Blockpage markers** — strings/URLs embedded in the block response (e.g. `wzws-waf-cgi/` dir for 360, `wangshan.360.cn`).
- **Unique response headers** — `X-Powered-By-360WZB`, `WZWS-Ray` (360); vendor cookies such as Netscaler's `ns_af` / Citrix patterns.
- **Server header values** — `qianxin-waf`, Approach, WTS-WAF, etc.

## Evasion technique categories

1. **Fuzzing/bruteforcing** — run payload wordlists (SecLists/Fuzzing, FuzzDB) against the endpoint, randomize user agents, raise latency on blocks. ⚠ *Load-generating; historically uses IP-rotation advice — explicitly out of scope for lab-mode benchmarks.*
2. **Regex reversing** — infer the WAF's signature regexes from blocked/allowed probes, then craft payloads avoiding blacklisted keywords. Most efficient method; purely analytical.
3. **Blacklisting detection/bypass** — progressive keyword-filter probing. Classic escalation (SQLi): filter `and|or|union` → bypass `1 || (select user from users where user_id = 1) = 'admin'`; add `where` → `limit 1`; add `limit` → `group by … having …`. Each round infers the new rule and rewrites the payload.
4. **Obfuscation** — encoding/whitespace/case/comment tricks on payloads (upstream catalogues dozens of variants per vulnerability class).
5. **HTTP Parameter Pollution (HPP)** — duplicate parameters so the WAF and backend parse differently.
6. **HTTP Parameter Fragmentation (HPF)** — split the payload across multiple parameters that the app later concatenates.
7. **Browser bugs** — parser differentials in how browsers vs WAFs tokenize markup.
8. **Atypical equivalent syntax** — semantically equivalent but syntactically unusual constructions.
9. **SSL/TLS cipher abuse** — negotiate ciphers the WAF cannot inspect (tool: abuse-ssl-bypass-waf).
10. **WAF response-limit abuse** — oversized responses exceeding WAF inspection buffers. ⚠ *Load-generating.*
11. **DNS history** — find the origin behind the WAF via historical DNS records (bypass-firewalls-by-DNS-history).
12. **Whitelist strings** — embed strings that whitelist-oriented rules let through.
13. **Request header spoofing** — headers that make requests appear internal (Burp Bypass-WAF plugin, enumXFF).
14. **Google dorks** — locate cached/origin content reachable without traversing the WAF.

## Known per-WAF bypasses (upstream catalogue)

Upstream lists concrete bypass payloads for: Airlock Ergon, AWS WAF, Barracuda, Cerber (WordPress), Citrix NetScaler, Cloudflare, Cloudbric, Comodo, DotDefender, FortiWeb, F5 ASM/BIG-IP/FirePass, ModSecurity, Imperva, Kona SiteDefender, Profense, QuickDefense, Sucuri, StackPath, URLScan, WebARX, WebKnight, Wordfence, Apache generic, IIS generic. Examples of documented classes: Airlock overlong UTF-8 sequence SQLi (`%C0%80'+union+select+…`), AWS WAF SQLi via statement termination (`"; select * from TARGET_TABLE --`), XSS via `popovertarget`/`onbeforetoggle` event handlers, HTML5 event-handler abuse on Cloudflare/ModSecurity, and null-byte/comment-based SQLi on older ModSecurity rules. ⚠ *Concrete payloads are for authorized lab use against the local/private allowlist.*

## Tools

### Fingerprinting
- [wafw00f](https://github.com/enablesecurity/wafw00f) — passive-plus-probe WAF fingerprinting, largest fingerprint DB.
- [identYwaf](https://github.com/stamparm/identywaf) — blind WAF detection using accumulated fingerprint cache.

### Testing / benchmarking
- [GoTestWAF](https://github.com/wallarm/gotestwaf) — tests WAF detection logic and bypasses; produces scoring reports.
- [Lightbulb Framework](https://github.com/lightbulb-framework/lightbulb-framework) — Python WAF testing suite.
- [WAFBench](https://github.com/microsoft/wafbench) — Microsoft WAF performance testing suite.
- [FTW (Framework for Testing WAFs)](https://github.com/coreruleset/ftw) — OWASP CRS team's rigorous rule-testing framework.
- [WAFtester](https://github.com/waftester/waftester) — fingerprints 197+ vendors, benchmarks rule coverage (F1/MCC scoring), automates bypass discovery; CI output (SARIF/SonarQube/GitLab SAST).
- Imperva WAF Testing Framework — vendor tooling.

### Evasion ⚠
- [WAFNinja](https://github.com/khalilbijjou/wafninja) — fuzzes and suggests bypasses. ⚠ *Active fuzzing — bounded samples/delay required.*
- [WAFTester (Raz0r)](https://github.com/Raz0r/waftester) — payload obfuscation.
- [libinjection-fuzzer](https://github.com/migolovanov/libinjection-fuzzer) — finds libinjection bypasses. ⚠ *Fuzzer — bounded samples/delay required.*
- [bypass-firewalls-by-DNS-history](https://github.com/vincentcox/bypass-firewalls-by-DNS-history) — origin discovery via DNS history (passive).
- [abuse-ssl-bypass-waf](https://github.com/LandGrey/abuse-ssl-bypass-waf) — SSL/TLS cipher evasion.
- [SQLMap tamper scripts](https://github.com/sqlmapproject/sqlmap) — payload obfuscation chain.
- [Bypass WAF Burp plugin](https://portswigger.net/bappstore/ae2611da3bbc4687953a1f4ba6a4e04c) — internal-network header spoofing.
- [enumXFF](https://github.com/infosec-au/enumXFF) — X-Forwarded-* header enumeration for 403 bypass.
- [waf-bypass (Nemesida)](https://github.com/nemesida-waf/waf-bypass) — FP/FN analysis with predefined/custom payload sets. ⚠ *Active scanning — bounded samples/delay required.*
- [nowafpls](https://github.com/assetnote/nowafpls) — junk-data insertion to exceed WAF buffers. ⚠ *Load-generating amplifier — explicit amplifier declaration + local/lab targets only.*
- [impersonate-proxy](https://github.com/ytkoka/impersonate-proxy) — MITM proxy spoofing TLS (JA3/JA4)/HTTP2/header fingerprints for bot-detection testing.

### Management
- [AWS Firewall Factory](https://github.com/globaldatanet/aws-firewall-factory) — centralized AWS WAF deploy/stage via FMS.

## Consumption guardrails (for the waf benchmark module)

Every benchmark or evasion exercise built on this catalogue must:

1. **Bound the workload** — explicit sample caps and inter-request delay; no unbounded fuzzing loops.
2. **Declare amplifiers explicitly** — junk-data, response-limit, and bruteforce techniques are amplifiers; they require an explicit amplifier flag before use.
3. **Target allowlist** — local, private, or lab-mode targets only; no third-party/production endpoints.
4. **No DoS, no IP rotation, no cross-site activity** — these are out of scope regardless of tool capabilities (several upstream tool descriptions mention proxychains/IP rotation; that guidance is intentionally not reproduced as practice here).

_Upstream: 0xInfection/Awesome-WAF (Apache-2.0), compiled by Pinaki (0xInfection) and community contributors._
