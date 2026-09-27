---
title: Objection - Android (pwny.cc)
source_url: https://www.pwny.cc/so/android/objection
fetched_at: 2026-09-20T02:00:03Z
license: unspecified
category: mobile/android
---
# objection

Objection is a runtime mobile exploration toolkit, powered by Frida, built to help you assess the security posture of your mobile applications, without needing a jailbreak.

## Installation

`pip3 install objection`
## Connection

Make a **regular ADB conection** and **start** the **frida** server in the device (and check that frida is working in both the client and the server).

If you are using a **rooted device** it is needed to select the application that you want to test inside the ***--gadget*** option. in this case:

`objection --gadget com.sensepost.ipewpew explore`
## Commands

### Patch apk

Before you can use any of the objection commands on an Android application, the application's APK itself needs to be patched and code signed to load the frida-gadget.so on start (**or setup frida-server**).

`objection patchapk -s testAPK.apk`
### Objection Basics

```
! (executes operating system commands using pythons subprocess module)
env (enumerate interesting directories that relate to the application)
reconnect (attempts to reconnect to the Frida Gadget specified with --gadget on startup)
frida (print frida information)
jobs list (list the currently running jobs)
jobs kill <job_uuid> (kills a running job identified by its UUID)
plugin load <local_path> (loads an objection plugin into the current session)
```
### File Operations

### Device actions

### App Analysis

### Hooking

### Keystore

### Intents

### Memory

### SQLite

## References

Last updated
