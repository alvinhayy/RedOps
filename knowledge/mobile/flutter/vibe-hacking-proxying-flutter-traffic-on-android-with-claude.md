---
title: "Vibe Hacking: Proxying Flutter Traffic on Android with Claude - Randy Westergren"
source_url: https://randywestergren.com/vibe-hacking-proxying-flutter-traffic-on-android-with-claude/
fetched_at: 2026-09-20T02:00:09Z
license: unspecified
category: mobile/flutter
---

I’m a regular Cronometer user and as usual, I was interested in exploring the API driving the app – authentication, request patterns, the typical curiosity that drives my posts. When my go-to Android MiTM approach failed, my curiosity only increased and I brought in Claude Opus 4.5 to help troubleshoot. What followed was an interesting collaboration in reverse engineering Flutter’s network stack – and it worked well enough that I wanted to capture both the technical outcome and what AI-assisted mobile security research can actually look like.

## The Challenge

I usually start with a rooted Android emulator running Frida with a mitmproxy system cert installed. Frida scripts help address the common issues in the way of capturing traffic, for example certificate pinning or device root detection. When I started up Cronometer with an unpinning script, mitmproxy logs were mostly empty despite obvious app activity. The app seemed to function fine, unaffected by my attempts to capture its traffic.

I started an OpenCode session with Opus 4.5 and described the situation. It started initial analysis by decompiling the APK and reviewing the source – it quickly found that Cronometer was built with Flutter and pointed me to some helpful background reading. Flutter, I realized, posed some unique challenges to my approach:

1. Flutter doesn’t use the Android TrustManager – It ships with its own SSL/TLS implementation via BoringSSL (Google’s fork of OpenSSL)
2. Flutter isn’t proxy-aware – Even if you set the system proxy, Flutter’s Dart runtime will happily bypass it and connect directly
3. The certificate pinning is baked into `libflutter.so` – There’s no Java/Kotlin layer to hook with traditional Frida scripts

Prior work + the emulator help solve some of these problems:

- reFlutter patches the Flutter engine at compile time (requires rebuilding the APK)
- NVISO’s disable-flutter-tls.js bypasses SSL pinning via Frida (but doesn’t address proxy routing)
- The Android emulator can force a proxy at the hardware-level, but remains a problem on physical devices – more on this later

## Instrumenting with Frida

### Emulator

Now with a better understanding of the challenges, I provided Claude with access to the rooted emulator via both `adb` and Frida and instructed it to begin hooking the app to capture API traffic. I preferred Frida instrumentation over the reFlutter approach, so I gave NVISO’s disable-flutter-tls.js a try. This unfortunately failed to hook any of the target functions in the libflutter library – the root cause was iterated on by Opus 4.5, summarized below: 

```
## x86_64 Emulator with ARM64 App (Fails ❌)
1. No Native x86_64 Library: Cronometer's XAPK only ships config.arm64_v8a.apk - no x86/x86_64 native libraries
2. ARM Binary Translation: Android uses libndk_translation.so (5.3MB) to translate ARM64 instructions to x86_64 at runtime
3. Invisible to Frida: The ARM64 libflutter.so is embedded in the APK and executed through the translation layer - it never appears as a loaded module
      Process.findModuleByName("libflutter.so") → null
```
As you can see above, Frida’s `Process.findModuleByName("libflutter.so")` returns null, so there’s nothing to scan for SSL bypass patterns in the script. Without the SSL bypass, the app rejects mitmproxy’s certificate during the TLS handshake.

Since I didn’t have the hardware to run an ARM64 emulator, I switched to a physical device.

### Physical Device

Moving over to a rooted Pixel 6, let’s start with detecting `libflutter.so` – Claude crafted a quick script:

```
$ frida -U -n "Cronometer"
     ____
    / _  |   Frida 17.5.2 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at https://frida.re/docs/home/
   . . . .
   . . . .   Connected to Pixel 6 Pro (id=1C121FDEE008KR)

[Pixel 6 Pro::Cronometer ]->
[Pixel 6 Pro::Cronometer ]-> var modules = Process.enumerateModules();
for (var i = 0; i < modules.length; i++) {
    if (modules[i].name === "libflutter.so") {
        console.log("[+] libflutter.so detected!");
        console.log("    Base: " + modules[i].base);
        console.log("    Size: " + modules[i].size);
        console.log("    Path: " + modules[i].path);
    }
}

[+] libflutter.so detected!
    Base: 0x702c105000
    Size: 11313152
    Path: /data/app/~~BhuO8FToqjKy_-agNfm1eg==/com.cronometer.android.gold-Sn9E8JQ_dkZzhPAw6gugUA==/split_config.arm64_v8a.apk!/lib/arm64-v8a/libflutter.so
```
With `libflutter.so` now being detected, let’s try the disable-flutter-tls-verification script:

```
frida -U -n "Cronometer" -l disable-flutter-tls.js
     ____
    / _  |   Frida 17.5.2 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at https://frida.re/docs/home/
   . . . .
   . . . .   Connected to Pixel 6 Pro (id=1C121FDEE008KR)
Attaching...
[+] Pattern version: May 19 2025
[+] Arch: arm64
[+] Platform:  linux
[ ] Locating Flutter library 1/5
[+] Flutter library located
[+] ssl_verify_peer_cert found at offset: 0x706aac
[+] ssl_verify_peer_cert has been patched
[Pixel 6 Pro::Cronometer ]->
```
As you can see, the patch was successful. While this successfully bypassed the pinning, it meant I had at least one remaining problem: forcing the proxy routing. The (new) goal: intercept traffic from an unmodified APK on a physical ARM64 device, without rebuilding or patching it, using runtime instrumentation.

### Proxy Injection

This is where things get more interesting and the power of AI assistance started to shine. The iteration here was rapid and sometimes laborious, so I’ll try to summarize what ultimately lead to successful traffic interception.

The first step in forcing routing through mitmproxy was to understand how the network stack was working. Claude made a copy of the disable-flutter-tls-verification script and added socket connection monitoring by hooking the raw socket `connect()`. It worked well, but initially only displayed IP address destinations –  I challenged Claude to also hook the DNS resolution process.

```
$ frida -U -f com.cronometer.android.gold -l flutter-intercept.js
     ____
    / _  |   Frida 17.5.2 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at https://frida.re/docs/home/
   . . . .
   . . . .   Connected to Pixel 6 Pro (id=1C121FDEE008KR)
Spawning `com.cronometer.android.gold`...
============================================================
[*] Flutter TLS Bypass + Socket Observer + DNS Tracking
[*] Arch: arm64
============================================================
[+] Hooking getaddrinfo() at 0x7441cb04e0
[+] Hooking connect() at 0x7441c83580
[*] Initialization complete. Waiting for connections...
Spawned `com.cronometer.android.gold`. Resuming main thread!
[DNS] mobile.cronometer.com -> 3.151.103.34
[DNS] mobile.cronometer.com -> 3.19.109.145
[CONNECT] mobile.cronometer.com (3.151.103.34):443
[CONNECT] mobile.cronometer.com (3.19.109.145):443
[+] Flutter library found: libflutter.so
[+] ssl_verify_peer_cert found at: 0x706aac
[+] ssl_verify_peer_cert has been patched
Now we're empirically detecting the DNS resolution and correlating it with the connections:
[DNS] mobile.cronometer.com -> 3.151.103.34
[DNS] mobile.cronometer.com -> 3.19.109.145
[CONNECT] mobile.cronometer.com (3.151.103.34):443
[CONNECT] mobile.cronometer.com (3.19.109.145):443
The script now:
1. Hooks getaddrinfo() with the correct struct offset (32 for ai_addr on Android arm64)
2. Captures hostname -> IP mappings dynamically
3. Shows the resolved hostname when connections are made
4. No static fallback needed - it's all detected empirically
```
Impressive! Next, let’s intercept  `mobile.cronometer.com` within `connect()` and redirect it to my mitmproxy. A few more iterations on the script later:

````
The proxy redirection is now working. We can see:
```
[REDIRECT] mobile.cronometer.com (3.19.109.145):443 -> 192.168.50.150:8080
[REDIRECT] PENDING (non-blocking)
```
The script is successfully:
1. Detecting DNS lookups - mobile.cronometer.com -> 3.19.109.145
2. Intercepting connections - catching the connect() call
3. Rewriting the destination - redirecting from the original IP:443 to your proxy at 192.168.50.150:8080
4. Bypassing TLS verification - so the proxy can intercept HTTPS
You should now see the traffic from mobile.cronometer.com in your mitmproxy. Note that for the proxy to work correctly with HTTPS, mitmproxy needs to be configured in transparent mode or the app needs to send HTTP CONNECT requests (which Flutter won't do automatically).
Since we're redirecting port 443 traffic to 8080, make sure your mitmproxy is set up to handle this - you may need to run it in transparent proxy mode or configure it to accept raw TLS connections on port 8080.
````
While the redirection was active, the proxy remained empty. A quick look at the mitmproxy logs revealed why:

*Client TLS handshake failed. The client disconnected during the handshake. If this happens consistently for mobile.cronometer.com, this may indicate that the client does not trust the proxy’s certificate.*

This was exactly what Claude warned about in point #4 above. Since I was redirecting traffic at the syscall level, the app was initiating a raw TLS handshake directly with the proxy port. However, mitmproxy (running in regular mode) was expecting a standard `HTTP CONNECT` request to identify the destination. Receiving a TLS Client Hello where it expected an HTTP verb caused the handshake to fail immediately.

Rather than enabling transparent mode in mitmproxy (the easy way out), I challenged Claude to manually inject the `HTTP CONNECT` verb. This turned out to be the most complex part of the exercise – Claude had to iterate through several versions to ensure the logic handled the socket handshake correctly and that the SSL pinning patches were applied before the redirection logic engaged.

The final result worked perfectly – again, very impressive. It would have taken me hours of manual trial-and-error to get right.

```
# ... snipped for brevity
[+] ssl_verify_peer_cert found at: 0x706aac
[+] ssl_verify_peer_cert has been PATCHED - TLS bypass active!
[CONNECT] 192.168.50.150:8080 (IPv4-mapped)
[DNS] mobile.cronometer.com -> 3.151.103.34
[REDIRECT] mobile.cronometer.com (3.151.103.34):443 -> 192.168.50.150:8080
[PROXY] Waiting for non-blocking connect to complete...
[PROXY] Connection ready, sending CONNECT
[PROXY] Sending: CONNECT mobile.cronometer.com:443
[PROXY] Sent 79 bytes
[PROXY] SUCCESS: HTTP/1.1 200 Connection established
```
Finally seeing those nutritious API calls.

Note this solution wasn’t required – transparent mode would have probably solved this immediately, but the goal here was part exploration into the LLM’s capabilities.

### Bonus – Dynamic Proxy Detection

The script worked well, though it hard-coded the proxy config in variables at the top. Let’s ask Claude to detect the Android system proxy dynamically and use it for the redirection.

```
console.log("[*] Detecting system proxy settings...");
// ============ PROXY DETECTION ============
function detectSystemProxy() {
    Java.perform(function() {
        try {
            var Settings = Java.use("android.provider.Settings$Global");
            var ActivityThread = Java.use("android.app.ActivityThread");
            var app = ActivityThread.currentApplication();
            if (!app) {
                console.log("[!] App context not ready yet, retrying in 100ms...");
                setTimeout(detectSystemProxy, 100);
                return;
            }
            var context = app.getApplicationContext();
            if (!context) {
                console.log("[!] App context not ready yet, retrying in 100ms...");
                setTimeout(detectSystemProxy, 100);
                return;
            }
            var contentResolver = context.getContentResolver();
            var proxy = Settings.getString(contentResolver, "http_proxy");
            if (proxy && proxy.indexOf(":") !== -1) {
                var parts = proxy.split(":");
                PROXY_HOST = parts[0];
                PROXY_PORT = parseInt(parts[1]);
                console.log("[+] Detected system proxy: " + PROXY_HOST + ":" + PROXY_PORT);
                proxyDetected = true;
            } else {
                console.log("[!] ERROR: No system proxy configured!");
                console.log("[!] Set proxy via: Settings > Wi-Fi > [network] > Proxy");
                proxyDetectionFailed = true;
            }
        } catch (e) {
            console.log("[!] App context not ready yet, retrying in 100ms... (" + e + ")");
            setTimeout(detectSystemProxy, 100);
        }
    });
}
// Start proxy detection immediately
detectSystemProxy();
```
As you can see, the solution is very readable – the full implementation within the connect hook is much more complex. You can find it here.

## Conclusion

It’s clear that AI-assisted debugging dramatically accelerated the reverse engineering process. Overall, the code Opus 4.5 generated was well written, and this type of problem was a perfect fit for its iterative approach – especially since the criteria for success were clear (“are we capturing traffic?”). The proxy injection and HTTP CONNECT tunnel were particularly clever solutions.

*Share this:*
