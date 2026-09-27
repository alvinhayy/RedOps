---
title: "iOS App Extensions"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/ios-pentesting/ios-app-extensions.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile/ios
---

### **Security Considerations**

**Security Considerations**

Key security aspects include:[\[1\]](#references)

- Extensions and their containing apps communicate via inter-process communication, not directly.
- A legacy **Today widget** can request that the system open its containing app through its extension context; do not generalize this behavior to every extension point.
- Shared data access is allowed within a private container, but direct access is restricted.
- Certain APIs, including HealthKit, are off-limits to app extensions, which also cannot start long-running tasks, access the camera, or microphone, except for iMessage extensions.

### Static Analysis

#### **Identifying App Extensions**

**Identifying App Extensions**

To find app extensions in source code, search for `NSExtensionPointIdentifier` in Xcode or inspect the app bundle for `.appex` files indicating extensions. Without source code, use grep or SSH to locate these identifiers within the app bundle.[\[1\]](#references)[\[2\]](#references)

#### **Supported Data Types**

**Supported Data Types**

Check the `Info.plist` file of an extension for `NSExtensionActivationRule` to identify supported data types. This setup ensures only compatible data types trigger the extension in host apps.[\[1\]](#references)[\[2\]](#references)

#### **Data Sharing**

**Data Sharing**

Data sharing between a containing app and its extension normally uses an App Group container. Shared preferences can use `UserDefaults(suiteName:)` (`NSUserDefaults` in Objective-C), while files and databases use the group container URL. Background `URLSession` transfers initiated by an extension also require a shared container configured on the session.[\[1\]](#references)[\[2\]](#references)

#### **Restricting Extensions**

**Restricting Extensions**

Apps can restrict certain extension types, particularly custom keyboards, ensuring sensitive data handling aligns with security protocols.[\[1\]](#references)[\[2\]](#references)

### Dynamic Analysis

Dynamic analysis involves:[\[1\]](#references)[\[2\]](#references)

- **Inspecting Shared Items** : Hook into`NSExtensionContext - inputItems` to see shared data types and origins.
- **Identifying Extensions** : Discover which extensions process your data by observing internal mechanisms, like`NSXPCConnection` .

Tools like `frida-trace` can aid in understanding the underlying processes, especially for those interested in the technical details of inter-process communication.

## References

- [1] [MASTG-KNOW-0082: App Extensions - OWASP MASTG](https://mas.owasp.org/MASTG-KNOW-0082/)
- [2] [MASTG-TEST-0072: Testing App Extensions - OWASP MASTG](https://mas.owasp.org/MASTG/tests/ios/MASVS-PLATFORM/MASTG-TEST-0072/)
- [3] [Apple — App Extension Programming Guide: Today widgets](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/Today.html)
