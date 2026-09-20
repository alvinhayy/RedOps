---
title: "iOS UIActivity Sharing"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/ios-pentesting/ios-uiactivity-sharing.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile/ios
---

## UIActivity Sharing Simplified

Since iOS 6, applications can present a system activity view to share text, URLs, images, and other items with services such as AirDrop or compatible app extensions.[\[2\]](#references)

Apple’s `UIActivity.ActivityType` documentation enumerates built-in activity identifiers. Developers can set `excludedActivityTypes`, but the security review must also inspect the actual items and any custom activities.[\[3\]](#references)

## **How to Share Data**

**How to Share Data**

Attention should be directed towards:[\[1\]](#references)

- The nature of the data being shared.
- The inclusion of custom activities.
- The exclusion of certain activity types.

Sharing is facilitated through the instantiation of a `UIActivityViewController`, to which the items intended for sharing are passed. This is achieved by calling:

```
$ rabin2 -zq Telegram\ X.app/Telegram\ X | grep -i activityItems
0x1000df034 45 44 initWithActivityItems:applicationActivities:
```
Review the items and custom activities passed to `UIActivityViewController`, along with any configured `excludedActivityTypes`.

## **How to Receive Data**

**How to Receive Data**

The following aspects are crucial when receiving data:[\[1\]](#references)

- The declaration of **custom document types** .
- The specification of **document types the app can open** .
- The verification of the **integrity of the received data** .

Without source, inspect `Info.plist` for `UTExportedTypeDeclarations`, `UTImportedTypeDeclarations`, and `CFBundleDocumentTypes`. These legacy UTI keys still appear in deployed apps; newer source commonly uses the Uniform Type Identifiers framework and `UTType` APIs.[\[4\]](#references)

Exported declarations define types owned by the app, imported declarations describe types owned elsewhere, and document types associate those identifiers with the app’s open/import behavior.[\[4\]](#references)

## Dynamic Testing Approach

To test **sending activities**, one could:[\[1\]](#references)

- Hook into the `init(activityItems:applicationActivities:)` method to capture the items and activities being shared.
- Identify excluded activities by intercepting the `excludedActivityTypes` property.

For **receiving items**, it involves:[\[1\]](#references)

- Sharing a file with the app from another source (e.g., AirDrop, email) that prompts the “Open with…” dialogue.
- Hooking `application:openURL:options:` among other methods identified during static analysis to observe the app’s response.
- Employing malformed files or fuzzing techniques to evaluate the app’s robustness.

## References

- [1] [OWASP MASTG — Testing App Extensions](https://mas.owasp.org/MASTG/tests/ios/MASVS-PLATFORM/MASTG-TEST-0072/)
- [2] [Apple — `UIActivityViewController`](https://developer.apple.com/documentation/uikit/uiactivityviewcontroller)
- [3] [Apple — `UIActivity.ActivityType`](https://developer.apple.com/documentation/uikit/uiactivity/activitytype)
- [4] [Apple — Defining file and data types for your app](https://developer.apple.com/documentation/uniformtypeidentifiers/defining-file-and-data-types-for-your-app)
