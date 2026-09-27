---
title: "iOS UIPasteboard"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/ios-pentesting/ios-uipasteboard.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile/ios
---

# iOS Pasteboard

## Privacy-aware attack surface (iOS 16+)

A paste prompt is both a protection and a useful test signal. Copy a unique, non-sensitive canary in a separate app, cold-start the target, and do **not** invoke any paste UI. A prompt at launch, resume, or view presentation indicates that the target attempted a programmatic value read. Repeat the flow while denying and allowing access, and correlate it with hooked selectors and network traffic to determine whether the app gates the read correctly or tries to upload the value. Finally, compare this with an explicit paste through the edit menu or `UIPasteControl`; this separates expected user-driven behavior from automatic clipboard harvesting.[\[3\]](#references)[\[6\]](#references)

Do not confuse **classification** with **content access**. `detectPatterns(for:)` / `detectedPatterns(for:)` can disclose that an item resembles a URL, number, email address, phone number, postal address, tracking number, or other supported pattern without returning its value and without notifying the user. This is still a small metadata oracle worth recording during an assessment. Conversely, `detectValues(for:)` / `detectedValues(for:)` returns matched values and must be treated as a content read. Hook both API families to discover apps that first classify the pasteboard and only read it when a desired pattern matches.[\[4\]](#references)[\[7\]](#references)

For sensitive writes, inspect whether the application supplies both `UIPasteboard.OptionsKey.localOnly` and `expirationDate`. `localOnly` keeps the item out of Handoff/Universal Clipboard, while `expirationDate` asks the system to remove it after a bounded interval. Their absence does not prove exploitability, but it increases the exposure window and number of reachable devices.[\[4\]](#references)

```
import UniformTypeIdentifiers
UIPasteboard.general.setItems(
  [[UTType.utf8PlainText.identifier: token]],
  options: [
    .localOnly: true,
    .expirationDate: Date().addingTimeInterval(60)
  ]
)
```
### Static Analysis

For static analysis, search the source code or binary for:[\[3\]](#references)[\[4\]](#references)

- `generalPasteboard` to identify usage of the**systemwide general pasteboard** .
- Value getters such as `string` ,`strings` ,`URL` ,`URLs` ,`image` ,`images` ,`items` ,`itemProviders` , and`dataForPasteboardType:` . Prioritize reads reachable from application launch, scene activation, or view-loading callbacks.
- Writers such as `setString:` ,`setValue:forPasteboardType:` ,`setItems:options:` , and`setItemProviders:localOnly:expirationDate:` . Trace whether secrets, session material, password-reset links, OTPs, or payment data can reach them.
- `detectPatterns` ,`detectedPatterns` ,`detectValues` , and`detectedValues` to distinguish metadata checks from value extraction.
- `UIPasteControl` and`UIPasteConfiguration` to identify intended user-mediated paste flows.
- `pasteboardWithName:create:` and`pasteboardWithUniqueName` for creating**custom pasteboards** . Verify if persistence is enabled, though this is deprecated.

### Dynamic Analysis

Dynamic analysis involves hooking or tracing specific methods:[\[3\]](#references)

- Monitor `generalPasteboard` for system-wide usage.
- Trace `pasteboardWithName:create:` and`pasteboardWithUniqueName` for custom implementations.
- Observe deprecated `setPersistent:` method calls to check for persistence settings.
- Hook getters and their return values separately from setters and their arguments. This identifies whether the target is a clipboard **source** ,**sink** , or both, without relying only on periodic polling.
- Exercise multiple pasteboard representations in the same item. An app may validate the string representation but consume a URL, rich-text, image, or custom UTI representation through another code path.

Key details to monitor include:

- **Pasteboard names** and**contents** (for instance, checking for strings, URLs, images).
- **Number of items** and**data types** present, leveraging standard and custom data type checks.
- **Expiry and local-only options** by inspecting the`setItems:options:` method.
- **Call timing and stack traces** , especially reads performed on launch, foreground transitions, or before any visible paste action.
- **Outbound requests** immediately after a canary is read, which can demonstrate exfiltration rather than merely local feature detection.

An example of monitoring tool usage is **objection’s pasteboard monitor**, which polls the `generalPasteboard` every 5 seconds for changes and outputs the new data. On iOS 16 and later this is an **active read**, not a transparent observer: injected polling executes in the target process and can itself trigger or alter paste-approval behavior. First capture the application’s own `UIPasteboard` calls with hooks, then use polling in a separate run so that the monitor is not mistaken for application behavior.[\[3\]](#references)[\[6\]](#references)

Here’s a simple JavaScript script example, inspired by the objection’s approach, to read and log changes from the pasteboard every 5 seconds:

```
const UIPasteboard = ObjC.classes.UIPasteboard
const Pasteboard = UIPasteboard.generalPasteboard()
var items = ""
var count = Pasteboard.changeCount().toString()
setInterval(function () {
  const currentCount = Pasteboard.changeCount().toString()
  const currentItems = Pasteboard.items().toString()
  if (currentCount === count) {
    return
  }
  items = currentItems
  count = currentCount
  console.log(
    "[* Pasteboard changed] count: " +
      count +
      " hasStrings: " +
      Pasteboard.hasStrings().toString() +
      " hasURLs: " +
      Pasteboard.hasURLs().toString() +
      " hasImages: " +
      Pasteboard.hasImages().toString()
  )
  console.log(items)
}, 1000 * 5)
```
## References

- [1] [OWASP MASTG - Pasteboard](https://mas.owasp.org/MASTG-KNOW-0083/)
- [2] [OWASP iOS Exercise notes (iGoat-Swift)](https://hackmd.io/@robihamanto/owasp-robi)
- [3] [MASTG-TEST-0073: Testing UIPasteboard](https://mas.owasp.org/MASTG/tests/ios/MASVS-PLATFORM/MASTG-TEST-0073/)
- [4] [Apple - `UIPasteboard`](https://developer.apple.com/documentation/uikit/uipasteboard)
- [5] [Apple - Supporting paste and pasteboard access](https://developer.apple.com/documentation/uikit/uipastecontrol)
- [6] [Apple WWDC22 - What’s new in privacy](https://developer.apple.com/videos/play/wwdc2022/10096/)
- [7] [Apple - Detecting pasteboard patterns](https://developer.apple.com/documentation/uikit/uipasteboard/detectedpatterns%28for%3Ainitemset%3A%29)
