---
title: Bypass Root Detection — Flutter Jailbreak Detection
source_url: https://medium.com/@rayhanhanaputra/bypass-root-detection-flutter-jailbreak-detection-65f1dbb9cbf3
fetched_at: 2026-09-20T02:00:13Z
license: unspecified
category: mobile/flutter
---
During a recent mobile pentest, I encountered a mobile banking app created with Flutter that had multiple layers of protection. It included root detection, making dynamic analysis challenging. It was such a pain in the ass.

Flutter applications are increasingly using community plugins for added security. One such plugin is `flutter_jailbreak_detection`, which wraps platform-specific libraries to detect rooted or jailbroken devices.

So, for those of you who are currently pentesting a flutter application, here’s how you can bypass the root detection mechanism.

## Bypass Root Detection

This Flutter plugin uses:

- **RootBeer** on Android
- **IOSSecuritySuite** on iOS

This means most of the detection logic happens at the native level. To bypass it, we’ll either hook into those libraries or modify the binary directly.

## iOS

To bypass root detection in iOS apps using this plugin:

1. Clone the following Frida script: https://github.com/CyberCX-STA/flutter-jailbreak-root-detection-bypass.git
2. Run the target Flutter app on a jailbroken device.
3. Attach Frida to the running app: `frida -U -f <com.package.example> -l jailbreak_bypass.js`
4. The script will intercept checks from `IOSSecuritySuite` and return 0 for checking isJailbroken.

This method does not require binary modification and is effective for most apps using the plugin. You can also use environment-hiding tools like **Dopamine’s built-in jailbreak hiding** to bypass root detection without using Frida; these tools hide jailbreak indicators like Cydia, SSH, and tweak injection from targeted apps, making them believe the device is not jailbroken.

## Android

### Option 1:

If the Flutter app is using `flutter_jailbreak_detection` version **1.0.0** (haven’t tested it yet with the latest version), you can use this Frida script: https://github.com/lpilorz/flutter-app/blob/master/frida-flutter-jailbreak-detection-bypass.js

But… if the app has been obfuscated or includes more advanced security techniques — such as anti-Frida hooks, runtime checks, or native-level detection — you will likely need a more advanced or manual bypass approach.

### Option 2:

I initially attempted to bypass the root detection by writing a custom Frida script. I tried tampering with the plugin’s `checkRoot` function by hooking into individual checks—such as blocking commands from being executed (e.g., `which su`) and intercepting file existence checks for the `su` binary or dangerous packages.

However, the newer versions of the plugin integrate more tightly with native code, which makes dynamic hooking less reliable. Some apps also implement anti-Frida techniques, making script injection more difficult.

When Frida becomes ineffective or unstable, manual patching becomes the most dependable method.

**Steps:**

1. Install the application
2. Navigate to the app directory. You can check the directory by simply running `pm path <com.example.packages>`

3. Identify the directory of the target app. Now, navigate to that directory and check for the `libtoolChecker.so` file.

4. Pull the file to your local machine using the following command: `adb pull /data/app/<random-string-package-name>/lib/arm64/libtoolChecker.so`

5. Open the file in Ghidra or any other decompiler. Decompile the `checkForRoot` function and try to analyze it

From the given piece of code, you can see that it returns `1` if the root binary exists.

6. Patch the instruction to always return `0`, regardless of whether it detects root or not

7. Now patch the file by going to **File > Export Program**. Keep the format as **Original File**

8. Push the modified `.so` binary back to: `/data/app/<random-string-package-name>/lib/arm64/libtoolChecker.so`

By simply modifying the `.so` binary, we can bypass the root detection mechanism. This binary patching technique isn’t limited to bypassing root detection — it can also be used to neutralize other native-level security checks, such as **Frida detection**, **anti-debugging**, or **emulator detection**, provided these checks are implemented inside the native `.so` libraries. By reversing and modifying the corresponding functions, you can force them to return false results or disable them entirely, thus effectively bypassing the security logic.

**Note:** This won’t always work, as some applications implement additional detection methods inside the APK itself. You will need to manually bypass those checks using your own-crafted “magic” scripts.

Anyway, happy hacking, everyone!
