---
title: "DHCPv6"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/pentesting-network/dhcpv6.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: network
---

### DHCPv6 vs. DHCPv4 Message Types Comparison

The following table compares DHCPv6 message types with their DHCPv4 counterparts.[\[4\]](#references)

| DHCPv6 Message Type | DHCPv4 Message Type |
|---|---|
| Solicit (1) | DHCPDISCOVER |
| Advertise (2) | DHCPOFFER |
| Request (3), Renew (5), Rebind (6) | DHCPREQUEST |
| Reply (7) | DHCPACK / DHCPNAK |
| Release (8) | DHCPRELEASE |
| Information-Request (11) | DHCPINFORM |
| Decline (9) | DHCPDECLINE |
| Confirm (4) | none |
| Reconfigure (10) | DHCPFORCERENEW |
| Relay-Forw (12), Relay-Reply (13) | none |

The message roles are summarized below.[\[5\]](#references)

1. **Solicit (1)** : Clients use it to discover DHCPv6 servers.
2. **Advertise (2)** : Servers use it to announce availability in response to Solicit.
3. **Request (3)** : A client requests configuration, addresses, or delegated prefixes from a selected server.
4. **Confirm (4)** : A client checks whether its assigned addresses still fit the current link.
5. **Renew (5)** : A client asks the original server to extend leases or update configuration.
6. **Rebind (6)** : A client asks any available server to extend leases after Renew receives no response.
7. **Reply (7)** : A server answers configuration exchanges and acknowledges Release or Decline.
8. **Release (8)** : A client relinquishes one or more assigned leases.
9. **Decline (9)** : A client reports that an assigned address is already in use.
10. **Reconfigure (10)** : A server asks a client to start a transaction for updated configuration.
11. **Information-Request (11)** : A client requests configuration without requesting leases.
12. **Relay-Forw (12)** : A relay forwards client or relay messages toward servers.
13. **Relay-Reply (13)** : A server returns a client reply to a relay agent.

## Quick Protocol Notes (Offensive)

- DHCPv6 clients listen on UDP port `546` ; servers and relay agents listen on UDP port`547` .<sup>[\[5\]](#references)</sup>
- Clients use **All_DHCP_Relay_Agents_and_Servers** (`ff02::1:2` ) on-link; relay agents can use site-scoped**All_DHCP_Servers** (`ff05::1:3` ).<sup>[\[5\]](#references)</sup>
- `OPTION_CLIENTID` and`OPTION_SERVERID` carry client and server**DUIDs** , which can help correlate a host across address changes.<sup>[\[5\]](#references)</sup>
- Clients request non-temporary addresses with `IA_NA` and delegated prefixes with`IA_PD` .<sup>[\[5\]](#references)</sup>

### Quick Recon

Capture DHCPv6 traffic with `tcpdump`:

```
# Basic DHCPv6 traffic capture
sudo tcpdump -vvv -i <IFACE> 'udp port 546 or udp port 547'
# THC-IPv6: dump available servers and their setup
sudo atk6-dump_dhcp6 <IFACE>
```
The THC-IPv6 information tool dumps available servers and their setup.[\[3\]](#references)

### Rogue DHCPv6 Server (Address/DNS Hijack)

The THC-IPv6 toolkit includes a fake DHCPv6 server that can configure an address and DNS server.[\[3\]](#references)

```
# THC-IPv6: rogue DHCPv6 server advertising address + DNS
sudo atk6-fake_dhcps6 <IFACE> <PREFIX>/<LEN> <DNSv6>
```
This is a generic on-link rogue DHCPv6 server. A related DHCPv6 DNS-takeover workflow uses IPv6-capable `ntlmrelayx` for WPAD and credential relaying; see [Pentesting IPv6](pentesting-ipv6.html).[\[6\]](#references)

### Pool Exhaustion / DHCPv6 Starvation

The THC-IPv6 toolkit also provides a DHCP client flooder intended to deplete a DHCPv6 server’s address pool.[\[3\]](#references)

```
# THC-IPv6: exhaust the server's address pool
sudo atk6-flood_dhcpc6 <IFACE>
```
### Reconfigure Message Caveat

Clients are unwilling to accept **Reconfigure** messages by default; they signal willingness with `OPTION_RECONF_ACCEPT`, and valid messages must also pass the protocol’s other checks.<sup>[\[5\]](#references)</sup> Unsolicited Reconfigure attempts are therefore unreliable unless the target’s behavior is confirmed.

## References
