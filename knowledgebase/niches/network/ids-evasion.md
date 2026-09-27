---
title: "IDS and IPS Evasion"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/pentesting-network/ids-evasion.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: network
---

# IDS/IPS Evasion Techniques

## **TTL Manipulation**

**TTL Manipulation**

Send some packets with a TTL enough to arrive to the IDS/IPS but not enough to arrive to the final system. And then, send another packets with the same sequences as the other ones so the IPS/IDS will think that they are repetitions and won’t check them, but indeed they are carrying the malicious content.[\[3\]](#references)

**Nmap option:** `--ttl <value>`.[\[4\]](#references)

## Avoiding signatures

Add random data to packets so fixed IPS/IDS signatures are less likely to match.[\[4\]](#references)

**Nmap option:** `--data-length 25`.[\[4\]](#references)

## **Fragmented Packets**

**Fragmented Packets**

Just fragment the packets and send them. If the IDS/IPS doesn’t have the ability to reassemble them, they will arrive to the final host.[\[4\]](#references)

**Nmap option:** `-f`.[\[4\]](#references)

## **Invalid** ***checksum***

**Invalid**

**checksum**
Some firewalls and IDSs may not verify checksums. An attacker can send a packet that will be **interpreted by the sensor but rejected by the final host**.[\[4\]](#references)

Example:

Send a packet with the RST flag and an invalid checksum, so then, the IPS/IDS may think that this packet is going to close the connection, but the final host will discard the packet as the checksum is invalid.[\[4\]](#references)

## **Uncommon IP and TCP options**

**Uncommon IP and TCP options**

A sensor might disregard packets with certain flags and options set within IP and TCP headers, whereas the destination host accepts the packet upon receipt.[\[3\]](#references)

## **Overlapping**

**Overlapping**

It is possible that when you fragment a packet, some kind of overlapping exists between packets (maybe first 8 bytes of packet 2 overlaps with last 8 bytes of packet 1, and 8 last bytes of packet 2 overlaps with first 8 bytes of packet 3). Then, if the IDS/IPS reassembles them in a different way than the final host, a different packet will be interpreted.

Or maybe, 2 packets with the same offset comes and the host has to decide which one it takes.[\[3\]](#references)

- **BSD** : It has preference for packets with smaller*offset* . For packets with same offset, it will choose the first one.
- **Linux** : Like BSD, but it prefers the last packet with the same offset.
- **First** (Windows): First value that comes, value that stays.
- **Last** (cisco): Last value that comes, value that stays.

These names are useful historical approximations, **not reliable fingerprints for current targets**. Modern measurements show that reassembly changes across OS versions and can depend on the exact overlap relation, protocol, number of chunks and whether overlaps are sent separately or in the same sequence.[\[5\]](#references)

## **TCP Stream Overlap / Reassembly Mismatch**

**TCP Stream Overlap / Reassembly Mismatch**

Like IP fragments, **overlapping TCP segments** can be reassembled differently by the IDS/IPS and by the destination host. If the sensor and the host disagree on **which bytes win** in the overlap, you can place benign bytes where the IDS/IPS looks and malicious bytes where the host finally reassembles them.[\[3\]](#references)

- Send a benign segment first and a **malicious overlapping segment** later (or invert the order) depending on the target OS reassembly policy.
- Use **tiny overlaps** to keep the stream valid for the host while maximizing ambiguity for the sensor.<sup>[\[3\]](#references)</sup>

## **Multi-overlap Reassembly Differentials**

**Multi-overlap Reassembly Differentials**

Testing only two overlapping fragments/segments can miss the interesting path. Research published in 2025 found that policies inferred from **pairs** were usually inconsistent with the behavior observed for **three overlapping chunks**. It also identified reassembly errors in OS, embedded-stack and NIDS implementations, including cases affecting payload reconstruction, connection termination and what a NIDS records.[\[5\]](#references)

For an authorized lab, validate a candidate differential end to end rather than assuming that a `first`, `last`, `bsd` or `linux` label describes the target. A useful workflow derived from that research is:[\[5\]](#references)

1. Pin the endpoint OS/kernel and the exact NIDS version and policy.
2. Generate **IPv4, IPv6 and TCP** overlap families: same-offset duplicates, partial overlaps, holes and three-way overlaps; vary arrival order and test overlaps both individually and together.
3. Capture before and after any middlebox. Compare the endpoint response/reassembled application data with the NIDS alert, extracted payload and logs.
4. Treat the sequence as evasion only when the endpoint consumes the malicious byte stream while the sensor reconstructs benign bytes, ignores the sequence or stops inspection. A sensor-only difference is insertion/noise, not evasion.
5. Repeat after OS, NIC-offload, firewall or NIDS upgrades because any of them can change the effective reassembly path.

[PYROLYSE](https://github.com/ANSSI-FR/pyrolyse) automates exhaustive overlap-case generation, stack/NIDS testing, policy extraction and analysis for up to three overlapping chunks. Its repository includes reproducible command recipes under `ws/` for traffic generation, replay, detection and policy comparison.[\[6\]](#references)

```
git clone --recurse-submodules https://github.com/ANSSI-FR/pyrolyse
export PYROLYSE_PATH="$PWD/pyrolyse"
cd "$PYROLYSE_PATH/rust_code/reassembly_test_pipeline"
cargo build
# Select the protocol/target workflow from $PYROLYSE_PATH/ws/
```
A short defensive validation is to alert on conflicting overlap bytes, drop IPv6 overlaps, normalize ambiguous traffic before inspection, and continuously retest the configured NIDS policy against the actual protected stack.[\[5\]](#references)

## **IPv6 Extension Headers & Fragment Tricks**

**IPv6 Extension Headers & Fragment Tricks**

IPv6 allows **arbitrary header chains**, and the upper-layer (TCP/UDP/ICMPv6) header appears **after** all extension headers. If a device doesn’t parse the full chain, it can be bypassed by inserting extension headers or by fragmenting so the upper-layer header is not visible where the device expects it.<sup>[\[2\]](#references)</sup> RFC 7112 **requires the entire IPv6 header chain to be present in the first fragment**; devices that accept non-compliant tiny fragments can be evaded by pushing the L4 header into later fragments.[\[1\]](#references)

Practical patterns:

- **Long extension-header chains** to push the upper-layer header deeper in the packet.
- **Small first fragments** that contain only IPv6 + Fragment + options, leaving the L4 header for later fragments.
- Combining **extension headers + fragmentation** to hide the real upper-layer protocol from devices that only inspect the first fragment.

## Tools

- [https://github.com/vecna/sniffjoke](https://github.com/vecna/sniffjoke)
- [https://github.com/secdev/scapy](https://github.com/secdev/scapy)
- [https://github.com/ANSSI-FR/pyrolyse](https://github.com/ANSSI-FR/pyrolyse)<sup>[\[6\]](#references)</sup>

## References
