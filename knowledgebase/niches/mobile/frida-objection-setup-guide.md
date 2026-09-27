---
title: "The Frida & Objection Setup Guide: Solving Version Hell on Android & iOS (Timeless Guide)"
source_url: https://infosecwriteups.com/the-frida-objection-setup-guide-solving-version-hell-on-android-ios-timeless-guide-f55eb98459a0
fetched_at: 2026-09-20T01:59:59Z
license: unspecified
category: mobile
---

## Stop Wasting Hours on Frida Version Mismatches — Here’s the Only Guide You’ll Ever Need

*If you’ve ever spent hours debugging “ObjC is not defined” errors or wrestling with Frida version incompatibilities, you’re not alone. Even AI assistants get confused by the maze of Frida versions, tools, and dependencies. This guide teaches you* *how to find compatible versions* *rather than just giving you numbers that will become outdated.*

🎁 **Note:** This article is available without a Medium subscription. ➤ Access it here.

## Table of Contents

1. **Quick Troubleshooting Checklist**
2. **About This Guide**
3. **Understanding Version Compatibility Issues**
4. **The Smart Setup: How to Choose Compatible Versions**
5. **Android Setup: Two Methods**
6. **iOS Setup**
7. **Conclusion**

## TL;DR — Quick Fix

*Just want it to work?* *Run this on your computer:*

`pip install frida==16.7.19 frida-tools objection`
*Then follow the Android or iOS setup below with version* *16.7.19*

## Quick Troubleshooting Checklist

Before you start, verify:

- **Device is rooted** (Android) or**jailbroken** (iOS)
- **Debugging enabled** (Android) or**SSH access** (iOS)
- **Python 3.6+** installed on your computer
- You know your **device architecture** (arm64, x86, etc.)

## About This Guide

*This guide teaches methodology over memorization.*

While we use specific version numbers as examples (like 16.7.19), these will change over time. What won’t change is:

- **How to find compatible versions**
- **How to troubleshoot issues**

**Current Example:** As of writing, Frida 16.7.19 works well with Objection. By the time you read this, newer versions may have resolved previous issues. Use our methodology to find what works now.

## Understanding Version Compatibility Issues

## Why Version Issues Keep Happening

- **Frida 16 to 17:** Changes that affected Objection (as of writing)
- **Future versions:** Will likely have their own breaking changes

*This is normal!* *Frida evolves rapidly, and dependent tools need time to catch up.*

**The Current Issue:** Frida 17.x breaks Objection with the dreaded `ReferenceError: 'ObjC' is not defined` error (Issue #740).

https://github.com/sensepost/objection/issues/740

```
✅ SAFE: Frida 16.x.x + Compatible Tools
❌ BROKEN: Frida 17.x + Objection (ObjC errors)
```
## The Smart Setup: How to Choose Compatible Versions

On your computer terminal:

`pip install frida==16.7.19 frida-tools objection`
This automatically installs:

- ✅ **Frida 16.7.19**
- ✅ **Compatible frida-tools**
- ✅ **Compatible objection**

*Why this works:* *Pip’s dependency resolver ensures all tools are version-matched.*

**Important Note:** Currently, I am using Frida 16.7.19, but the compatibility issues mentioned here may be resolved in the future. Always verify the current status!

The key here is to use the single command:

`pip install frida==<version> frida-tools objection`
to automatically ensure compatibility, even as new versions are released.

**To remove all three packages at once**, just run:

`pip uninstall frida frida-tools objection`
## Android Setup: Two Methods

## Prerequisites

- **Rooted Android device**
- **ADB installed** and device connected
- **Python with pip** installed on your computer
- **Frida client already installed** (see “The Smart Setup” section above)

## Method 1: Using Frida Launcher (Easiest)

**1. Install Frida Launcher APK**

- Download from: `github.com/thecybersandeep/Frida-Launcher`
- Install the APK on your device

**2. Select Version 16.7.19**

- Open Frida Launcher
- Select version 16.7.19
- Download and start

**3. Test Your Setup**

Replace `owasp.mstg.uncrackable1` with your app's actual package name, then run:

`frida -U -f owasp.mstg.uncrackable1`
## Method 2: Manual Installation (More Control)

**1. Determine Your Device Architecture**

```
# Check your Android architecture
adb shell getprop ro.product.cpu.abi
```
**Architecture Mapping:**

- `arm64-v8a` → use`frida-server-16.7.19-android-arm64.xz`
- `armeabi-v7a` → use`frida-server-16.7.19-android-arm.xz`
- `x86_64` → use`frida-server-16.7.19-android-x86_64.xz`
- `x86` → use`frida-server-16.7.19-android-x86.xz`

**2. Download the Correct Binary**

## Get Sandeep Wawdane’s stories in your inbox

Join Medium for free to get updates from this writer.

Download and prepare the Frida server for Android:

```
wget https://github.com/frida/frida/releases/download/16.7.19/frida-server-16.7.19-android-arm64.xz
xz -dc frida-server-16.7.19-android-arm64.xz > frida-server && chmod +x frida-server
```
**3. Push to Device**

`adb push frida-server /data/local/tmp/`
**4. Set Permissions & Run**

```
adb shell chmod 777 /data/local/tmp/frida-server
adb shell su -c "/data/local/tmp/frida-server &"
```
*Success Check:* *Run* *Objection* *-*

## iOS Setup

## Prerequisites

- **Jailbroken iOS device**
- **SSH access** to your device
- **Python with pip** installed on your computer
- Your device’s **IP address** (find in Settings, then Wi-Fi, then (i) icon)

## Choosing the Right Version

*Principle:* *Use the same Frida version on both client (your computer) and server (iOS device) for maximum compatibility.*

**How to Decide Which Version:**

- Check what version your tools support (especially Objection)
- Verify the version works with your iOS version in Frida’s release notes
- Use the same version as your Android setup for consistency

## Method 1: Cydia/Sileo (Easiest but Version-Limited)

*Warning:* *As of writing, this method installs Frida 17.x which may have compatibility issues with tools like Objection. Check current status before using.*

**1. Add Frida Repository**

- Open Cydia or Sileo
- Go to Sources, then Edit, then Add
- Enter: `https://build.frida.re`

**2. Install Frida**

- Search for “Frida”
- Install the package
- Respring when prompted

**When to Use This Method:**

- You want the absolute latest Frida version
- You’re not using Objection or tools with compatibility issues

## Method 2: Manual Installation (More Control)

*Use this when:* *You need a specific version or are experiencing compatibility issues with Method 1.*

When you need precise control over Frida’s version — or encounter compatibility issues with the pip approach — installing manually is your best bet. This method walks you through selecting the correct release, deploying it to your device, and verifying that everything’s working smoothly.

**1. Choose the Right Version**

Match your Frida client:

`frida --version`
**2. Download the .deb Package**

Visit Frida’s GitHub releases page to find your target version, then download the appropriate ARM64 package for iOS:

```
# Example for v16.7.19:
curl -LO https://github.com/frida/frida/releases/download/16.7.19/frida_16.7.19_iphoneos-arm64.deb
```
**3. Transfer to Your Device**

Push the .deb file to your device’s temporary folder:

`scp frida_16.7.19_iphoneos-arm64.deb root@<DEVICE_IP>:/tmp/`
**4. Remove Any Previous Installation**

Clean out the old Frida package before installing the new one:

```
ssh root@<DEVICE_IP> "dpkg -r frida"
ssh root@<DEVICE_IP> "dpkg -P re.frida.server"
```
**5. Install Your Chosen Version**

Install the freshly copied .deb:

`ssh root@<DEVICE_IP> "dpkg -i /tmp/frida_16.7.19_iphoneos-arm64.deb"`
**6. Verify where the binary lives**

`ssh root@<DEVICE_IP> "dpkg -L re.frida.server | grep frida-server"`
*Pro Tip:* *Modern jailbreaks often use* */var/jb/usr/sbin/* *instead of the traditional* */usr/sbin/**. Always verify the actual path!*

**7. Start Frida with its full path**

`ssh root@<DEVICE_IP> "nohup /var/jb/usr/sbin/frida-server &"`
*If you see “Already have a frida-server listening on that port”, you’re good to go!*

On your host, confirm you can launch apps via objection:

## Common Issues & Quick Fixes

*Version Mismatch Error?* *Make sure client and server versions match exactly:* *frida --version* *should match your server version*

*“Address already in use”?* *Kill existing frida-server: Android:* *adb shell "pkill frida-server"* *iOS:* *ssh root@<IP> "pkill frida-server"*

*“ObjC is not defined”?* *You’re using Frida 17.x with Objection. Downgrade to 16.x*

## Conclusion

*You now have a working Frida and Objection setup that avoids all the common pitfalls. No more version hell, no more ObjC errors, no more wasted hours.*

## Found This Helpful?

Share it with your team — they’ll thank you for saving them hours of debugging. Have questions or found a new issue? Drop a comment below with your Frida version and error message.
