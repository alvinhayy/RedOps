---
title: "Wifi Pcap Analysis"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/basic-forensic-methodology/pcap-inspection/wifi-pcap-analysis.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: wireless
---

## Check BSSIDs

With a Wi-Fi capture open in Wireshark, select *Wireless → WLAN Traffic* to summarize the wireless networks observed in the capture; each row represents one wireless network.[\[1\]](#references)

### Brute Force

For WPA/WPA2-PSK captures, `aircrack-ng` requires a usable four-way EAPOL handshake and tests candidate passphrases with a dictionary. Use `-w` to provide the wordlist and `-b` to target the access point’s BSSID:[\[2\]](#references)

```
aircrack-ng -w pwds-file.txt -b <BSSID> file.pcap
```
If a candidate matches, Aircrack-ng recovers the pre-shared key; the matching password and SSID can then be configured in Wireshark’s 802.11 decryption settings when the capture and security mode support it.[\[2\]](#references)[\[5\]](#references)

## Data in Beacons / Side Channel

If you suspect that **data is being leaked in beacon-side-channel traffic**, start with a display filter such as `wlan contains "NAMEofNETWORK"` or `wlan.ssid == "NAMEofNETWORK"`, then inspect matching frames for suspicious strings. The first form is a broad byte search; the second matches the SSID field.[\[3\]](#references)[\[4\]](#references)

## Find Unknown MAC Addresses in a Wi-Fi Network

Wireshark exposes `wlan.ta` as the transmitter address and `wlan.addr` as a hardware/MAC address; display filters can combine these fields with logical operators:[\[3\]](#references)[\[4\]](#references)

- `((wlan.ta == e8:de:27:16:70:c9) && !(wlan.fc == 0x8000)) && !(wlan.fc.type_subtype == 0x0005) && !(wlan.fc.type_subtype ==0x0004) && !(wlan.addr==ff:ff:ff:ff:ff:ff) && wlan.fc.type==2`

If you already know **MAC addresses, remove them from the output** by adding checks like `&& !(wlan.addr == 5c:51:88:31:a0:3b)`.

Once you have detected **unknown MAC** addresses communicating inside the network, use a filter such as `wlan.addr == <MAC address> && (ftp || http || ssh || telnet)` to narrow its traffic. The FTP, HTTP, SSH, and Telnet filters are useful only when Wireshark can dissect the corresponding decrypted payload.[\[3\]](#references)[\[5\]](#references)

## Decrypt Traffic

To add an 802.11 decryption key in Wireshark, open *Edit → Preferences → Protocols → IEEE 802.11* and click *Edit* next to *Decryption Keys*.[\[5\]](#references)

For WPA/WPA2, Wireshark normally needs the EAPOL four-way handshake and the matching password/SSID; supplying the transient key can avoid the handshake requirement. WPA3 per-connection decryption requires the connection’s PMK.[\[5\]](#references)

## References
