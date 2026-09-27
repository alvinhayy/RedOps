---
title: "DDS/RTPS Security and Service Impersonation"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/pentesting-network/dds-rtps-security.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: network
---

## DDS/RTPS attack surface

The **Data Distribution Service (DDS)** is a data-centric publish/subscribe middleware frequently used by robotics, industrial, automotive, and real-time systems. Its DDSI-RTPS discovery plane announces domain participants and their reader/writer endpoints. Cyclone DDS exposes these records through the `DCPSParticipant`, `DCPSPublication`, and `DCPSSubscription` built-in topics, including endpoint topic names, type names, and QoS metadata.[\[3\]](#references)[\[5\]](#references)

When DDS Security is not enabled, network reachability to a domain may be enough to:[\[3\]](#references)[\[7\]](#references)

- enumerate participants, writers, readers, topic names, and type names;
- subscribe to telemetry or state streams;
- create a writer for a discovered topic and impersonate an internal publisher;
- invoke RPC-like services implemented as request/response topic pairs.

DDS Security adds participant authentication, topic/domain access control, cryptographic protection, and security-event logging; normal DTLS, VPN, or application-session encryption outside DDS does not supply those DDS-level authorization decisions.[\[3\]](#references)[\[7\]](#references)

### Discovery reconnaissance with Cyclone DDS

In the Unitree G1 case study, Domain 0 discovery was visible over RTPS multicast at `239.255.0.1:7400`. Treat that endpoint as a useful default-deployment indicator rather than a universal constant: domain IDs, transports, multicast policy, interface selection, and static peers can differ.[\[3\]](#references)

Install the Python binding, select the interface that reaches the target, and inspect the built-in topics. Explicit peers help where multicast is filtered, but they do not replace correct interface and locator selection.[\[3\]](#references)[\[5\]](#references)

```
python3 -m venv dds-venv
dds-venv/bin/pip install cyclonedds
export CYCLONEDDS_URI=file://$PWD/cyclonedds.xml
dds-venv/bin/python dds_dump.py
```
## Minimal Cyclone DDS endpoint enumerator

```
#!/usr/bin/env python3
import time
from cyclonedds.domain import DomainParticipant
from cyclonedds.builtin import (
    BuiltinDataReader,
    BuiltinTopicDcpsParticipant,
    BuiltinTopicDcpsPublication,
    BuiltinTopicDcpsSubscription,
)
dp = DomainParticipant(0)
time.sleep(10)
participants = BuiltinDataReader(
    dp, BuiltinTopicDcpsParticipant
).take(256)
writers = BuiltinDataReader(
    dp, BuiltinTopicDcpsPublication
).take(2048)
readers = BuiltinDataReader(
    dp, BuiltinTopicDcpsSubscription
).take(2048)
for p in participants:
    print("PARTICIPANT", p.key)
for e in sorted(writers, key=lambda x: x.topic_name):
    print("WRITER", e.topic_name, e.type_name, e.qos)
for e in sorted(readers, key=lambda x: x.topic_name):
    print("READER", e.topic_name, e.type_name, e.qos)
```
Example interface/peer pinning for Cyclone DDS:[\[3\]](#references)

```
<CycloneDDS>
  <Domain id="0">
    <General>
      <Interfaces>
        <NetworkInterface name="eth1"/>
      </Interfaces>
      <AllowMulticast>true</AllowMulticast>
    </General>
    <Discovery>
      <Peers>
        <Peer address="192.0.2.10"/>
      </Peers>
    </Discovery>
  </Domain>
</CycloneDDS>
```
If discovery works but a writer reports **zero matched subscriptions**, inspect the advertised unicast locators in RTPS traffic. Multi-homed hosts may announce the wrong source interface even though multicast discovery succeeds. Reproduce from a single-homed Linux host, pin the interface, and verify the target sees the writer before debugging payload serialization.[\[3\]](#references)[\[4\]](#references)

## Reconstructing types and impersonating services

Discovery usually reveals a **type name**, not the complete application schema. Recover the exact structure from shipped IDL, generated Python/C++ classes, firmware, mobile applications, debug symbols, or captured samples. Preserve member order, integer widths, bounded strings/sequences, keys, extensibility annotations, and XCDR version. Then compile the recovered IDL with `idlc`; Cyclone DDS generates the descriptors and serialization support needed for wire-compatible samples.[\[3\]](#references)[\[6\]](#references)

```
idlc request.idl
cc exploit.c request.c -lddsc -o dds_client
```
Common application-level RPC conventions use separate topics such as `rt/api/<service>/request` and `rt/api/<service>/response`. A request header may carry a correlation ID, lease/policy fields, and an `api_id` or opcode selecting the handler, while another member contains JSON as a string. Once the type is correct, a malicious participant can publish directly to the request topic; service code may treat it identically to a message from a trusted internal process.[\[3\]](#references)[\[4\]](#references)

A practical sequence is:[\[3\]](#references)[\[4\]](#references)

1. Read publication/subscription built-in topics and map request writers to service readers.
2. Recover the precise request and response types.
3. Match the target reader’s reliability, durability, partition, and data-representation QoS.
4. First send a harmless enumeration/status `api_id` .
5. Correlate the response using the request identity field.
6. Only in an authorized test, exercise state-changing operations and monitor physical safety effects.

### WebRTC or API bridges into DDS

Treat any WebRTC, WebSocket, HTTP, or BLE component that translates attacker-supplied data into native DDS samples as a **privileged middleware gateway**. If a client controls the destination topic or operation and the bridge lacks a strict allowlist, one valid signaling credential can expose every service reachable by the bridge. DTLS protects the WebRTC data channel in transit, but it does not authorize DDS topics or service functions.[\[3\]](#references)[\[4\]](#references)

Audit bridge messages for fields such as `topic`, `type`, `api_id`, `service`, and stringified `parameter` objects. Test whether the bridge accepts ordinary telemetry topics, arbitrary `rt/api/` request topics, malformed type/topic combinations, and operations not used by the official client. Also compare the bridge path with **direct DDS publication**: an application-layer credential is irrelevant if the internal DDS domain accepts unauthenticated participants.[\[3\]](#references)[\[4\]](#references)

## Compound pivots exposed by DDS service access

The UniBLEed research illustrates why service impersonation should be tested as part of a complete trust chain rather than as an isolated message-injection issue.[\[3\]](#references)[\[4\]](#references)

- **Shared device keys across transports:** reusing one long-lived symmetric key for BLE provisioning and WebRTC turns a leak in release logs, WebView arguments, diagnostic events, or a bootstrap handler into access to every protocol sharing the key. If a cloud endpoint unwraps a device credential, verify account-to-device ownership before decryption; otherwise it becomes a cross-tenant decryption oracle.<sup>[\[3\]](#references)[\[4\]](#references)</sup>
- **Runtime-unpacked Android clients:** when a packer replaces the shipped DEX with stubs and defines decrypted classes only at runtime, use a rooted test emulator,`frida-server` , and`frida-dexdump` , then decompile the recovered DEX files with JADX. Search the result for protocol opcodes, signing routines, raw keys, release logging, WebView bridges, and cloud ownership parameters.<sup>[\[2\]](#references)[\[3\]](#references)</sup>
- **Deterministic firmware “encryption”:** encryption is reversible when the package carries the KDF seed in plaintext and the distributed updater contains the KDF constants. Reproduce the KDF and cipher variant, decrypt nested packages recursively, and recompute any unkeyed checksum. Unitree UPK research, for example, recovers a TEA key from a four-byte seed stored at offset`0x1c` plus constants embedded in OTA binaries.<sup>[\[1\]](#references)[\[3\]](#references)</sup>
- **Traversal write into a privileged consumer:** if a DDS handler appends an extension to an attacker-controlled identifier but does not canonicalize and enforce base-directory containment,`../` components can place content in another service’s watched or executable directory. A second root service that snapshots filenames with`os.listdir()` and later passes an allowed file to`sh` turns arbitrary file write into command execution even when the filename ends in`.md` .<sup>[\[3\]](#references)[\[4\]](#references)</sup>
- **File read as a PIE bypass:** a privileged path-read primitive can disclose`/proc/<pid>/maps` . Parse the executable mapping base and add statically recovered offsets for PLT entries,`.bss` objects, flags, and callback structures to make a position-dependent memory-corruption exploit repeatable.<sup>[\[3\]](#references)[\[4\]](#references)</sup>
- **Unquoted-heredoc configuration injection:** values expanded into an unquoted shell heredoc can contain newlines that terminate the intended value and add attacker-selected configuration directives. Length-dependent “manual configuration” fallbacks deserve special attention because they may bypass a safer normal code path and can force a target onto attacker-controlled networking.<sup>[\[3\]](#references)[\[4\]](#references)</sup>
- **`.bss` overflow into event-loop cleanup state:** when a global fixed-size input buffer precedes termination flags and cleanup objects, an oversized write can set the exit flag and forge a callback/argument pair. After using the PIE leak to target`system@PLT` , event-loop shutdown invokes the command. If later cleanup frees forged static data and aborts, background the payload so it survives the daemon crash.<sup>[\[3\]](#references)[\[4\]](#references)</sup>

## Hardening and detection

Apply controls at both the DDS layer and every external bridge:[\[5\]](#references)[\[7\]](#references)

- enable DDS Security mutual authentication and cryptographic protection;
- write governance/permissions rules per domain and topic, separating publish from subscribe rights;
- deny discovery and user-data traffic across untrusted interfaces and network segments;
- configure bridges with a fixed topic/type allowlist and operation-level authorization rather than accepting a client-selected topic;
- inventory expected participant GUIDs, topic/type pairs, and QoS, then alert on new participants, unexpected writers, or duplicate writers for safety-critical topics;
- use distinct, rotatable credentials per transport and bind cloud key operations to the authenticated device owner.

## References
