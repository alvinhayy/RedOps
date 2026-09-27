---
title: Android APK
source_url: https://notes.incendium.rocks/pentesting-notes/reversing/android-apk
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: reversing
---

## apktool

A tool for reverse engineering 3rd party, closed, binary Android apps. It can decode resources to nearly original form and rebuild them after making some modifications; it makes possible to debug smali code step by step. Also it makes working with an app easier because of project-like file structure and automation of some repetitive tasks like building apk.

```
apktool d Directory\ file.apk
```
