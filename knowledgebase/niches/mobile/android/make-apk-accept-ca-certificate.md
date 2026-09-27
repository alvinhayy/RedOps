---
title: "Make APK Accept CA Certificate"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/android-app-pentesting/make-apk-accept-ca-certificate.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile/android
---

# Make an APK Trust a User CA Certificate

## Automatic

[`apk-mitm`](https://github.com/shroudedcode/apk-mitm) automates APK patching for HTTPS inspection and includes patches for several common certificate-pinning implementations.[\[2\]](#references)

## Manual

Decompile the APK:

```
apktool d app.apk
```
In `AndroidManifest.xml`, add the following attribute to the `<application>` element if it is not already set:[\[1\]](#references)

`android:networkSecurityConfig="@xml/network_security_config"`

Before adding:

After adding:

Create or update `res/xml/network_security_config.xml` with the following content. The `system` source keeps the preinstalled trust anchors, while `user` adds user-installed CAs:[\[1\]](#references)

```
<network-security-config>
    <base-config>
        <trust-anchors>
            <!-- Trust preinstalled CAs -->
            <certificates src="system" />
            <!-- Additionally trust user-added CAs -->
            <certificates src="user" />
        </trust-anchors>
    </base-config>
</network-security-config>
```
Rebuild the APK:

```
apktool b app -o patched.apk
```
Repackaging invalidates the original signature, so sign the rebuilt APK before installing it. [See the APK signing section](smali-changes.html#sign-the-new-apk).

## References

- [1] [Android Developers - Network Security Configuration](https://developer.android.com/privacy-and-security/security-config)
- [2] [apk-mitm - Prepare Android APK files for HTTPS inspection](https://github.com/shroudedcode/apk-mitm)
