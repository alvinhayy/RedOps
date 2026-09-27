---
title: "Network Privacy and Anonymous Connectivity"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/privacy/network-privacy-and-anonymous-connectivity.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

# Network Privacy & Anonymous Connectivity

## What each observer can usually see

| Path | Local network / ISP | Intermediary | Destination | Main limitation | Relative speed |
|---|---|---|---|---|---|
| Direct HTTPS | Source, destination metadata, timing/volume | Hosting/CDN sees connection | Source IP, browser/app data | No source-IP privacy | Fastest |
| Commercial VPN | Source connected to VPN; not usual destination metadata | VPN sees source and destination metadata | VPN egress IP | One provider becomes a correlation point | Usually fast |
| Self-hosted VPN/VPS | Source connected to VPS | Host/account/payment/control-plane logs | VPS egress IP | Easy to attribute to the rented server/account | Usually fast |
| Tor Browser | Source connected to Tor/bridge; timing/volume | Relays each see a limited portion | Tor exit, browser data | Slower; account/endpoint/correlation risks | Moderate/slow |
| Tails/Whonix | Similar Tor path, with stronger routing boundaries | Same Tor limitations | Tor exit/application data | Operational mistakes and host/hardware remain | Moderate/slow |
| Public guest Wi-Fi + HTTPS | Venue sees local device/timing and destinations | Venue ISP sees metadata | Guest public IP | Physical/captive-portal/device correlation | Fast/variable |
| Cellular hotspot | Carrier sees subscriber/device/location and destinations | VPN/Tor if used | Carrier, VPN, or Tor egress IP | Mobile subscription and location are durable identifiers | Fast/variable |
| Mixnet | Access sees mixnet use; timing/volume | Multiple mixing nodes | Gateway/egress | Emerging ecosystem; latency and bandwidth cost | Slowest |

HTTPS protects content in transit but not all metadata. EFF notes that domain, time, and traffic size can remain visible to intermediaries even when page paths, credentials, and messages are encrypted.[\[1\]](#references)

## VPNs: fast privacy with concentrated trust

A VPN is useful for hiding destination metadata from the access ISP, protecting a first hop on an untrusted network, presenting a stable engagement egress address, or reaching a private network. It does **not** make a user anonymous. The VPN sees the source connection and can observe destination metadata; accounts, cookies, GPS, fingerprints, and payment information remain.[\[1\]](#references)

### Provider evaluation checklist

1. **Ownership and jurisdiction:** identify the legal entity, parent company, operating countries, infrastructure subcontractors, and applicable legal process.
2. **Collected data:** distinguish account/billing, source IP, connection timestamps, bandwidth, crash telemetry, DNS queries, and destination logs. “No browsing logs” does not mean “no data.”
3. **Retention and deletion:** find precise durations and whether backups, fraud systems, and processors follow the same schedule.
4. **Evidence:** prefer public audits with scope, date, findings, and remediation; reproducible/open clients; transparency reports; and documented incidents.
5. **Protocol and client:** maintained WireGuard, OpenVPN, or another reviewed protocol; automatic updates; DNS and IPv6 handling; kill switch; and per-platform leak tests.
6. **Business model:** understand how a free or subsidized service is funded. App-store presence alone is not evidence of trustworthy operation.
7. **Payment fit:** alternative payment can reduce billing disclosure to the VPN but does not erase the source IP observed at every connection.

### Configure and verify a VPN

1. Install the provider/organization’s signed client from its official source.
2. Select **full tunnel** unless a documented route must bypass it. Split tunneling creates correlation and leak paths.
3. Enable fail-closed/always-on behavior and block traffic during reconnect.
4. Send DNS through the tunnel and test both IPv4 and IPv6. Disable a protocol only if it cannot be safely tunneled and the loss of functionality is accepted.
5. Test sleep/wake, network switching, captive-portal login, tunnel crash, and hotspot tethering. NCSC warns that tethered clients may bypass a phone’s VPN on some platforms.<sup>[\[2\]](#references)</sup>
6. Use an organization-controlled test endpoint to record observed IPv4, IPv6, DNS resolver, and connection timing. Do not expose a sensitive engagement to random “leak test” sites.
7. Re-test after client, OS, network, or policy changes.

## Tor Browser: stronger web unlinkability

Tor builds a circuit through multiple relays so no single relay normally knows both source and destination. The destination sees a Tor exit rather than the user’s IP; the local network normally sees a Tor connection.<sup>[\[3\]](#references)</sup> Tor is designed for low-latency TCP applications, so it is slower and cannot guarantee protection against an adversary able to correlate both ends.[\[4\]](#references)

### Safe Tor Browser workflow

1. Download Tor Browser only from the Tor Project or an official mirror and verify the signature when possible.
2. Use **Tor Browser** , not a normal browser pointed at a Tor SOCKS port. Ordinary browsers can leak DNS/WebRTC and identifying state.<sup>[\[5\]](#references)</sup>
3. Keep the default size, fonts, extensions, and privacy settings. Additional add-ons can make the browser more unique.<sup>[\[6\]](#references)</sup>
4. Choose **Safer** or**Safest** security level when the increased breakage is acceptable.
5. Use a bridge when direct Tor is blocked or when ordinary relay IPs would create unacceptable local visibility. Bridges reduce easy recognition; they do not eliminate traffic analysis.<sup>[\[7\]](#references)</sup>
6. Do not log into an identifying account, provide identifying information, or open downloaded active documents in an external networked application.
7. Use a separate session/context for each identity. “New circuit” is not the same as erasing browser/application identity; use **New Identity** or restart the isolated environment as appropriate.
8. Prefer authenticated HTTPS or an authenticated onion service. A Tor exit can observe unencrypted HTTP traffic.

### Tor plus VPN

Combining them is not automatically safer. A VPN before Tor may hide direct Tor relay connections from an ISP while the VPN sees the source; Tor before a VPN gives the VPN a stable view of post-Tor activity and may shrink the anonymity set. Misconfiguration can introduce leaks. Tor Project recommends such combinations only for advanced, explicit threat models.[\[8\]](#references)

## Public and guest Wi-Fi

Modern HTTPS means passive neighbors usually cannot read properly encrypted web content, but guest Wi-Fi is not anonymity. The venue can record association times, device identifiers, captive-portal data, destinations, and DHCP details; cameras, purchases, transport, and physical observation can identify the user. A fake similarly named hotspot can also capture portal credentials or manipulate unencrypted traffic.[\[9\]](#references)

### Lawful guest-network workflow

1. Use only a network offered for guests or one for which the owner has granted explicit permission. Ask staff for the exact SSID and portal procedure.
2. Update the endpoint and travel router before arrival. Disable file/printer sharing, inbound discovery, auto-join, and remembered-network probing.
3. Enable the OS’s private/randomized Wi-Fi address. Current Apple systems can use rotating addresses on open/weak networks; modern Android randomization is commonly persistent per SSID. This reduces one local identifier only.<sup>[\[10\]](#references)</sup><sup>[\[11\]](#references)</sup>
4. Prefer an organization-controlled travel router or low-trust bridge device between a privileged workstation and the guest network. This centralizes firewall/VPN policy but does not hide the router from the venue.<sup>[\[12\]](#references)</sup>
5. Complete a captive portal only through the designated low-trust device/browser. Never enter personal or reused credentials for a supposedly anonymous context. Close the portal browser after connectivity is established.
6. Start a full-tunnel VPN or Tor before sensitive activity and confirm fail-closed behavior.
7. Forget the network after use and review the portal account/data-retention policy.

{% hint style=“danger” %} Cracking a neighbor’s Wi-Fi, bypassing a portal, using leaked guest credentials, cloning another guest’s access, or hiding a Raspberry Pi in a café is unauthorized activity—not a privacy technique. The safe equivalents are a lawful guest network, a client-approved site, or a documented drop node placed and recovered with the property owner’s written consent. {% endhint %}

## Travel routers

A travel router can isolate a workstation from hostile local broadcasts, enforce a firewall, provide a consistent internal SSID, and reconnect a VPN automatically. It is **not** anonymous: the upstream sees its radio identity and traffic timing, and its VPN provider sees the tunnel source.

- Use supported OpenWrt/vendor firmware and remove unused services.
- Administer over Ethernet or a dedicated management SSID with a unique password.
- Disable WAN-side administration, UPnP, WPS, file sharing, and unsolicited inbound traffic.
- Use a randomized/private WAN MAC only where supported and permitted.
- Enforce VPN policy on the router, including DNS and IPv6, and block egress when the tunnel fails.
- Do not assume a phone hotspot tunnels tethered devices through the phone’s VPN; test it.

## Cellular, SIMs and eSIMs

Cellular is convenient but not anonymous. Operators maintain subscriber/device identifiers and location derived from network attachment; an eSIM is still a mobile subscription. Prepaid does not reliably mean unregistered—requirements vary by country and change.[\[13\]](#references)

Operationally:

- Use a separate, supported device to reduce exposure of personal data, not to create a fictional subscriber.
- Do not carry a “separate” device continuously alongside a personal phone if co-location is in the threat model.
- Disable unused cellular, Wi-Fi, Bluetooth, and location access; powering off is a stronger radio boundary than UI toggles.
- Put sensitive traffic inside the approved VPN/Tor path, while recognizing the carrier still knows the subscription/device location and tunnel endpoint.
- Verify current registration and retention rules with the national regulator or local counsel; do not rely on online lists of “anonymous SIM countries.”

## DNS and TLS metadata

- **DoH/DoT/DoQ** encrypt DNS between client and resolver, preventing simple local reading or modification, but the resolver still sees queries and transport identifiers. They move trust; they do not provide anonymity.<sup>[\[14\]](#references)</sup>
- **ODoH** adds a proxy so the resolver need not learn the client IP, assuming proxy and target do not collude. Traffic analysis is explicitly out of scope.<sup>[\[15\]](#references)</sup>
- **TLS Encrypted Client Hello (ECH)** can protect the inner server name in a TLS handshake when client, DNS, and server support it. Destination IP, timing, volume, and the endpoint remain visible.<sup>[\[16\]](#references)</sup>
- With a correctly configured VPN or Tor environment, DNS should follow that environment’s supported route. Adding a separate resolver can create a new observer or fingerprint.

### Encrypted-DNS/ECH verification workflow

1. Decide whether DNS is controlled by the VPN/Tor environment, the OS, or the application. Configure it in **one** intended layer instead of stacking unrelated resolvers.
2. Select a resolver from its published privacy/retention policy and enable strict encrypted mode where the platform supports it. Opportunistic fallback may silently return to plaintext.
3. Query a unique subdomain under an authoritative test zone you control; confirm the authoritative log sees the intended recursive resolver.
4. Capture only the test device’s traffic with authorization. Confirm the access network cannot read plaintext DNS, while recognizing it can see the encrypted resolver/tunnel endpoint.
5. Test a blocked/unreachable encrypted resolver. The pass condition is the chosen fail-closed or documented fallback behavior—not an accidental clear query.
6. For ECH, use a controlled ECH-enabled host and inspect client/server diagnostics to confirm the **inner** ClientHello was accepted. Merely offering an HTTPS record does not prove ECH succeeded.
7. Repeat after network changes, captive portals, browser updates and VPN reconnects. Record which component owns DNS/ECH so later administrators do not create a bypass.

## Mixnets

Mixnets such as Nym or Katzenpost add fixed-size packets, delay, reordering, and cover traffic to resist timing correlation. Those properties cost latency and bandwidth, and independent deployment-scale evidence is limited. Treat current consumer mixnets as **emerging/high-latency options**, not faster or guaranteed replacements for Tor/VPNs.[\[17\]](#references)

### Evaluation workflow

1. Identify a maintained client and the exact supported application; do not force arbitrary browser/system traffic through an undocumented proxy.
2. Read the current threat model for entry, mix nodes, gateway, destination and collusion assumptions.
3. Install from the official signed source in a separate test compartment and use only a benign owned endpoint.
4. Measure delivery latency, message-size limits, reliability, retransmission and what happens when the gateway is unavailable.
5. Inspect local traffic and the owned endpoint to confirm the intended path and source. Check whether replies use the same privacy design.
6. Test shutdown/failure: the application must not silently fall back to direct Internet access.
7. Do not disable cover traffic, reduce delays or choose unusual fixed routes merely for speed; these changes can invalidate the stated anonymity model.
8. Keep it experimental until the specific deployment, independent analysis and operational reliability meet the consequence level.

## Network preflight checklist

- Authorization covers the access network, target, dates, and source infrastructure.
- The endpoint contains no unrelated identities or active sync sessions.
- IPv4, IPv6, DNS, and reconnect behavior match the plan.
- The destination sees only the expected egress.
- Captive portal and hotspot behavior have been tested without sensitive traffic.
- Local sharing/discovery and automatic network joining are disabled.
- The observer table and residual traffic-correlation risk are accepted.
- Provider policy, retention, and emergency contact are current.

For split-knowledge relays, route-enforced workloads, pluggable transports, onion services, I2P, and disposable remote browsers, continue to [Advanced Network Privacy Architectures](advanced-network-privacy-architectures.html).

## References
