---
title: "Flutter SSL Bypass: How to Intercept HTTPS Traffic When All Other Frida Scripts Fail"
source_url: https://m4kr0.vercel.app/posts/flutter-ssl-bypass-how-to-intercept-https-traffic-when-all-other-frida-scripts-fail/
fetched_at: 2026-09-20T02:00:10Z
license: CC BY-NC-SA 4.0
category: mobile/flutter
---
Author: Adham A. Makroum (m4kr0) - Published 2025-05-17 - License: CC BY-NC-SA 4.0
Categories: Mobile Pentest / Android-Pentest / Flutter / Frida / ssl-pinning

> Note: images referenced in the original article are omitted in this capture.

In this article, the author walks through intercepting HTTPS traffic from a Flutter-based APK during a pentesting engagement, after two days of trying Frida scripts that did not work.

The target APK was developed using Flutter. Flutter apps are written in Dart, and Dart does not use the system CA store. That means traditional certificate pinning bypass techniques often don't work.

Capturing the app's HTTPS traffic with Burp Suite initially failed - no requests came through.

Scripts tried without success:

- NVISO Flutter TLS bypass
- Frida FlutterProxy
- reflutter

## Manual traffic redirect attempt

Burp Suite was configured to listen on all interfaces (port 8083), then iptables rules redirected all traffic to Burp:

```
iptables -t nat -A OUTPUT -p tcp -j DNAT --to-destination Burp_IP:Burp_Port
```

TLS verification blocked the traffic. Notably, the same scripts worked for a colleague - so the author tested them against demo Flutter apps (they worked), confirming the issue was environment-specific:

- The colleague ran the AVD on macOS (ARM-based emulator)
- The author ran the AVD on a PC (x86_64 architecture)

The architecture difference led to different memory layouts and offsets in the binary: the scripts matched memory patterns on ARM but not on x86_64.

## Deep dive into libflutter.so

`libflutter.so` was extracted using apktool (choosing x86_64 to match the emulator architecture), then opened in Ghidra (File -> Import -> select libflutter.so -> analyze).

Flutter uses BoringSSL for SSL. BoringSSL is open source. From various resources, `ssl_x509.cc` is responsible for SSL certificates; inside it, the function `ssl_crypto_x509_session_verify_cert_chain` handles certificate-chain verification during the SSL handshake.

This function:

- Takes 3 arguments
- Returns a boolean (true = success, false = failed)

To find it in `libflutter.so`:

- In Ghidra: Search -> For Strings
- Look for `ssl_client` (appears in the same source file around line 230), double-click the result and explore its XREFs
- There are 2 XREFs (possibly more) - check all of them
- The correct candidate is the function that takes 3 arguments and returns a boolean (in the author's case, the second one)

## Calculating the offset

After locating the function, the Ghidra address was e.g. `02184644`. Subtract the base load address (usually `100000`) to get the module-relative offset used by Frida:

```
02184644 - 100000 = 2084644
```

This is the address used in the Frida script.

## Frida script

A simple script to hook and patch the return value of `ssl_crypto_x509_session_verify_cert_chain`:

- Script: https://github.com/m4kr0x/flutter_ssl_bypass/
- Replace the offset with your own

Tested on an AVD with Android 11 on x86_64.

After running the script, Burp Suite intercepted all HTTPS traffic from the app - the SSL pinning was completely bypassed.

## Related

- [Play Integrity API: How It Works & How to Bypass It](https://m4kr0.vercel.app/posts/play-integrity-api-how-it-works--how-to-bypass-it/)
