---
title: "Evil Twin EAP-TLS"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/pentesting-wifi/evil-twin-eap-tls.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: wireless
---

## Unauthenticated EAP identity leakage / username enumeration

EAP drives an identity exchange *before* TLS starts. If the client uses the real domain username as its outer identity, anyone in RF range can harvest it without authenticating.[\[1\]](#references)

**Passive harvest workflow**

```
# 1) Park on the right channel/BSSID
airodump-ng -i $IFACE -c $CHAN --bssid $BSSID
# 2) Decode EAP frames and extract identities
# Trigger a client connection (e.g., your phone) to see the leak
tshark -i "$IFACE" -Y eap -V | grep "Identity: *[a-z]\|*[A-Z]\|*[0-9]"
```
Impact: fast, no-auth username collection → fuels password spraying, phishing, account correlation. Worse when usernames match email addresses.[\[1\]](#references)

### Managed-profile quick check (outer identity hygiene)

Managed Android Enterprise deployments still need an explicit **outer identity** / privacy value for certificate-based Wi-Fi profiles. If MDM leaves that field blank (or sets it to the real UPN), the device will keep exposing a correlatable username in the first `EAP-Response/Identity` before TLS.<sup>[\[10\]](#references)</sup> During assessments, `anonymous` or `anonymous@realm` is what you want to observe over the air.[\[3\]](#references)

```
# Capture only EAP identity responses during reconnects
tshark -i "$IFACE" -Y 'eap.code == 2 && eap.type == 1' \
  -T fields -e frame.time -e wlan.sa -e eap.identity
```
If managed devices still emit mail-style identities while the org claims “EAP-TLS hides usernames”, the privacy knob was never enforced in the onboarding profile.

## TLS 1.3 privacy vs downgrade games

TLS 1.3 encrypts client certificates and most handshake metadata, so a supplicant that actually negotiates TLS 1.3 does not expose its certificate or inner identity to a passive Evil Twin; the outer EAP-Response/Identity remains visible unless the profile uses an anonymous NAI. Many enterprise stacks still allow TLS 1.2 for compatibility; RFC 9190 warns that a rogue AP can offer only TLS 1.2 static-RSA suites to force a fallback and re-expose the outer identity (or even the client cert) in cleartext EAP-TLS.[\[5\]](#references)

**Offensive playbook (downgrade to leak ID):**

- Compile hostapd-wpe with only TLS 1.2 static RSA ciphers enabled and TLS 1.3 disabled in `openssl_ciphersuite` /`ssl_ctx_flags` .
- Advertise the corporate SSID; when the victim initiates TLS 1.3, respond with a TLS alert and restart the handshake so the peer retries with TLS 1.2, revealing its real identity before cert validation succeeds.
- Pair this with `force_authorized=1` in hostapd-wpe so the 4-way handshake completes even if client-auth fails, giving you DHCP/DNS-level traffic to phish or portal.

**Defensive toggle (what to look for during an assessment):**

- hostapd/wpa_supplicant 2.10 added EAP-TLS server *and* peer support for TLS 1.3 but ships it**disabled by default** ; enabling it on clients with`phase1="tls_disable_tlsv1_3=0"` does not by itself remove the downgrade window—clients should also reject the TLS 1.2 static-RSA fallback described in RFC 9190.<sup>[\[5\]](#references)[\[6\]](#references)</sup>

### TLS 1.3 realities in 2024–2025

- FreeRADIUS 3.0.23+ supports EAP-TLS 1.3; its maintainer notes that EAP-TLS, EAP-TTLS, and EAP-PEAP share the TLS configuration, so interoperability should be tested rather than assumed. Any `tls_max_version = "1.2"` compatibility pin should be reviewed for downgrade exposure.<sup>[\[5\]](#references)[\[7\]](#references)</sup>
- Windows 11 uses EAP-TLS 1.3 by default from version 22H2, but session resumption is not supported; Microsoft also notes NPS and older third-party RADIUS interoperability issues that may require TLS 1.3 to be disabled.<sup>[\[9\]](#references)</sup>
- RSA key exchange for TLS 1.2 is being deprecated by the IETF; OpenSSL security level 3 rejects cipher suites without forward secrecy, while lower levels still impose restrictions, so static-RSA downgrade labs should use a deliberately tested legacy/permissive stack (for example, OpenSSL 1.1.1 with `@SECLEVEL=0` ).<sup>[\[11\]](#references)[\[12\]](#references)[\[13\]](#references)</sup>

**Practical version steering during an engagement**

- **Force TLS 1.2 on the rogue** (to leak identities):```
# hostapd-wpe.conf
ssl_ctx_flags=0
openssl_ciphers=RSA+AES:@SECLEVEL=0   # lower the policy; test with a legacy OpenSSL build
disable_tlsv1_3=1
```
- **Probe client TLS intolerance** : run two rogues – one advertising TLS 1.3-only (`disable_tlsv1=1` ,`disable_tlsv1_1=1` ,`disable_tlsv1_2=1` ) and one TLS 1.2-only. Clients that only join the 1.2 BSS are downgradeable.
- **Watch for fallback in captures** : filter in Wireshark for`tls.handshake.version==0x0303` after an initial`ClientHello` with`supported_versions` containing 0x0304; victims that retry 0x0303 are leaking their outer ID again.

## [Evil Twin via broken server validation (“mTLS?”)](#evil-twin-via-broken-server-validation-mtls)

Rogue APs broadcasting the corporate SSID can present any certificate. If the client:

- **doesn’t validate** the server cert, or
- **prompts the user** and allows override of untrusted CAs/self-signed certs,
then EAP-TLS stops being mutual. A modified**hostapd/hostapd-wpe** that skips client-cert validation (e.g.,`SSL_set_verify(..., 0)` ) is enough to stand up the Evil Twin.<sup>[\[2\]](#references)</sup>

### [Rogue infra quick note](#rogue-infra-quick-note)

For baseline testing on current Kali, the packaged `hostapd-wpe` is usually enough:

```
apt update
apt install hostapd-wpe
hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf
```
Only rebuild/patch when you specifically need to:

- disable client-cert validation for EAP-TLS MitM (`SSL_set_verify(..., 0)` -style patch), or
- build a TLS 1.2 static-RSA-only downgrade lab with an older/OpenSSL-1.1.1 userspace and `@SECLEVEL=0` .

That second case is increasingly lab-only: modern OpenSSL 3.x defaults make static-RSA downgrade setups fragile, so keeping a dedicated container/VM for the rogue RADIUS stack is usually easier than modifying your daily driver.

### [Windows supplicant misconfig pitfalls (GUI/GPO)](#windows-supplicant-misconfig-pitfalls-guigpo)

Key knobs from the Windows EAP-TLS profile:[\[4\]](#references)

- **Verify the server’s identity by validating the certificate**  - Checked → chain must be trusted; unchecked → any self-signed cert is accepted.
- **Connect to these servers**  - Empty → any cert from a trusted CA is accepted; set CN/SAN list to pin expected RADIUS names.
- **Don’t prompt user to authorise new servers or trusted certification authorities**  - Checked → users cannot click through; unchecked → user can trust an untrusted CA/cert and join the rogue AP.

Observed outcomes:[\[1\]](#references)

- **Strict validation + no prompts** → rogue cert rejected; Windows logs an event and TLS fails (good detection signal).
- **Validation + user prompt** → user acceptance = successful Evil Twin association.
- **No validation** → silent Evil Twin association with any cert.

### [Silent Evil Twin with a trusted cert (no prompt required)](#silent-evil-twin-with-a-trusted-cert-no-prompt-required)

User-clickthrough is only one path. If the supplicant trusts a CA that the attacker can abuse (for example, by stealing the real NPS certificate or obtaining another **Server Authentication** cert from the same private PKI), the rogue can often become **promptless** instead of merely “click-through”.

Practical implications on Windows profiles:

- **Empty `Connect to these servers`** = any server certificate chaining to a trusted CA is acceptable.
- **Windows 11 prefers SAN DNS matching over CN** when the certificate contains a SAN DNS entry, so stale CN-only pinning can behave differently than expected.<sup>[\[9\]](#references)</sup>
- **Wildcard / broad name patterns** increase the blast radius if the org trusts an internal CA capable of issuing arbitrary RADIUS-like names.

This is where Wi-Fi Evil Twin work starts to overlap with [AD Certificates](../../windows-hardening/active-directory-methodology/ad-certificates/README.html): once you can mint or steal a trusted server-auth cert, you are no longer betting on bad UX or user clicks.

**Quick triage on a Windows endpoint**

```
# Export the WLAN profile and inspect the server-validation block
netsh wlan export profile name="CorpWiFi" folder=.
Select-String -Path .\Wi-Fi-*.xml -Pattern 'ServerNames|TrustedRootCAHash|DisablePrompt'
```
Red flags:

- empty `ServerNames`
- more trusted roots than the deployment really needs
- `DisablePrompt` absent/false on unmanaged endpoints
- wildcard/regex-like server-name patterns broader than the real NPS farm

## [References](#references)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
