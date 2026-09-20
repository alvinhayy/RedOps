---
title: "Android APK Checklist"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/android-checklist.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile
---

### [Learn Android fundamentals](android-app-pentesting/index.html#2-android-application-fundamentals)

### [Static Analysis](android-app-pentesting/index.html#static-analysis)

-  Check for [obfuscation](android-checklist.html#some-obfuscation-deobfuscation-information) , root/emulator detection, and anti-tampering checks.[Read this for more information](android-app-pentesting/index.html#other-checks) .
- Sensitive applications (like bank apps) should check if the mobile is rooted and should actuate in consequence.
-  Search for [interesting strings](android-app-pentesting/index.html#looking-for-interesting-info) (passwords, URLs, API, encryption, backdoors, tokens, Bluetooth uuids…).
  -  Special attention to [firebase](android-app-pentesting/index.html#firebase) APIs.
-  Special attention to
-  [Read the manifest:](android-app-pentesting/index.html#basic-understanding-of-the-application-manifest-xml)  - Check if the application is in debug mode and try to “exploit” it
  - Check if the APK allows backups
  -  Exported Activities
    -  Unity Runtime: exported UnityPlayerActivity/UnityPlayerGameActivity with a `unity` CLI extras bridge. Test`-xrsdk-pre-init-library <abs-path>` for pre-init`dlopen()` RCE. See[Intent Injection → Unity Runtime](android-app-pentesting/intent-injection.html) .<sup>[\[1\]](#references)</sup>
  -  Unity Runtime: exported UnityPlayerActivity/UnityPlayerGameActivity with a
  - Content Providers
  - Exposed services
  - Broadcast Receivers
  - URL Schemes
-  Is the application [saving data insecurely, internally or externally](android-app-pentesting/index.html#insecure-data-storage) ?
-  Is any [password hard-coded or saved on disk](android-app-pentesting/index.html#poorkeymanagementprocesses) ? Is the app[using insecure cryptographic algorithms](android-app-pentesting/index.html#useofinsecureandordeprecatedalgorithms) ?
- Are all native libraries compiled as PIE where the platform requires it?
-  Use [static Android analyzers](android-app-pentesting/index.html#automatic-analysis) to complement manual review.
-  `android:exported`**mandatory on Android 12+** – misconfigured exported components can lead to external intent invocation.
-  Review **Network Security Config** (`networkSecurityConfig` XML) for`cleartextTrafficPermitted="true"` or domain-specific overrides.
-  Look for calls to **Play Integrity / SafetyNet / DeviceCheck** – determine whether custom attestation can be hooked/bypassed.
-  Inspect **App Links / Deep Links** (`android:autoVerify` ) for intent-redirection or open-redirect issues.
-  Identify usage of **WebView.addJavascriptInterface** or`loadData*()` that may lead to RCE / XSS inside the app.
-  Analyse cross-platform bundles (Flutter `libapp.so` , React-Native JS bundles, Capacitor/Ionic assets). Dedicated tooling:
  - `flutter-packer` ,`fluttersign` ,`rn-differ`
-  Scan third-party native libraries for known CVEs (e.g., **libwebp CVE-2023-4863** ,**libpng** , etc.).
-  Evaluate **SEMgrep Mobile rules** ,**Pithus** and the latest**MobSF ≥ 3.9** AI-assisted scan results for additional findings.
-  Check OEM ROM add-ons (OxygenOS/ColorOS/MIUI/OneUI) for extra **exported ContentProviders** that bypass permissions; try`content query --uri content://com.android.providers.telephony/ServiceNumberProvider` without`READ_SMS` (e.g., OnePlus CVE-2025-10184).<sup>[\[2\]](#references)</sup>

### [Dynamic Analysis](android-app-pentesting/index.html#dynamic-analysis)

-  Prepare the environment ([online](android-app-pentesting/index.html#online-dynamic-analysis) ,[local VM or physical](android-app-pentesting/index.html#local-dynamic-analysis) )
-  Is there any [unintended data leakage](android-app-pentesting/index.html#unintended-data-leakage) (logging, copy/paste, crash logs)?
-  [Confidential information being saved in SQLite dbs](android-app-pentesting/index.html#sqlite-dbs) ?
-  [Exploitable exposed Activities](android-app-pentesting/index.html#exploiting-exported-activities-authorisation-bypass) ?
-  [Exploitable Content Providers](android-app-pentesting/index.html#exploiting-content-providers-accessing-and-manipulating-sensitive-information) ?
-  [Exploitable exposed Services](android-app-pentesting/index.html#exploiting-services) ?
-  [Exploitable Broadcast Receivers](android-app-pentesting/index.html#exploiting-broadcast-receivers) ?
-  Is the application [transmitting information in clear text/using weak algorithms](android-app-pentesting/index.html#insufficient-transport-layer-protection) ? is a MitM possible?
-  [Inspect HTTP/HTTPS traffic](android-app-pentesting/index.html#inspecting-http-traffic)  - This one is really important, because if you can capture the HTTP traffic you can search for common Web vulnerabilities (Hacktricks has a lot of information about Web vulns).
-  Check for possible [Android Client Side Injections](android-app-pentesting/index.html#android-client-side-injections-and-others) (probably some static code analysis will help here)
-  [Frida](android-app-pentesting/index.html#frida) : Just Frida, use it to obtain interesting dynamic data from the application (maybe some passwords…)
-  Test for **Tapjacking / Animation-driven attacks (TapTrap 2025)** even on Android 15+ (no overlay permission required).<sup>[\[3\]](#references)</sup><sup>[\[4\]](#references)</sup>
-  Attempt **overlay / SYSTEM_ALERT_WINDOW clickjacking** and**Accessibility Service abuse** for privilege escalation.
-  Check if `adb backup` /`bmgr backupnow` can still dump app data (apps that forgot to disable`allowBackup` ).
-  Probe for **Binder-level LPEs** (e.g.,**CVE-2023-20963, CVE-2023-20928** ); use kernel fuzzers or PoCs if permitted.
-  If Play Integrity / SafetyNet is enforced, try runtime hooks (`Frida Gadget` ,`MagiskIntegrityFix` ,`Integrity-faker` ) or network-level replay. Recent Play Integrity Fix forks (≥17.x) embed`playcurl` —focus on ZygiskNext + PIF + ZygiskAssistant/TrickyStore combinations to regain DEVICE/STRONG verdicts.
-  Instrument with modern tooling:
  - **Objection > 2.0** ,**Frida 17+ (Android 16 support, ART offset fixes)** ,**NowSecure-Tracer (2024)**
  - Dynamic system-wide tracing with `perfetto` /`simpleperf` .
-  For OEM telephony/provider bugs (e.g., OxygenOS CVE-2025-10184), attempt **permission-less SMS read/send** via the`content` CLI or in-app`ContentResolver` ; test blind SQLi in`update()` to exfiltrate rows.<sup>[\[2\]](#references)</sup>

### Some obfuscation/Deobfuscation information

## References
