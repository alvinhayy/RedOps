---
title: "macOS Apple Scripts"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-security-protections/macos-tcc/macos-tcc-bypasses/macos-apple-scripts.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Apple Scripts

AppleScript is an automation language that can send Apple Events to scriptable applications. With the relevant grants, malware can inject JavaScript into a scriptable browser tab or use System Events/Accessibility to click a permission dialog. Apple Events and Accessibility are distinct TCC services and generally require their respective user approvals.[\[3\]](#references)

```
tell window 1 of process "SecurityAgent"
     click button "Always Allow" of group 1
end tell
```
The `abbeycode/AppleScripts` repository contains automation examples.[\[7\]](#references)

Find more info about malware using applescripts [**here**](https://www.sentinelone.com/blog/how-offensive-actors-use-applescript-for-attacking-macos/).[\[3\]](#references)

### Automation / TCC quirks

Apple Events approvals are **directional**: the prompt is for a **source process -> target process** pair. Once the user clicks **Allow**, future requests from the same source to the same target are allowed until the entry is reset. During testing, granting `Terminal -> Finder` or `Terminal -> System Events` once is enough to reuse the permission later without another popup.[\[1\]](#references)

```
# Remove previously granted Automation permissions from Terminal
tccutil reset AppleEvents com.apple.Terminal
```
This is especially relevant when the **target** is **Finder**, because Finder always has **Full Disk Access** even if it doesn’t appear in the FDA UI. Therefore, any host that already has Automation over Finder can be used as an AppleScript/JXA proxy to access TCC-protected files.<sup>[\[1\]](#references)</sup> The generic Finder and System Events payloads are already documented in [the main TCC page](../README.html) and in [the Apple Events page](../macos-apple-events.html).

### Modern offensive tradecraft

`/usr/bin/osascript` is only the most visible entry point. AppleScript and JXA can also execute from **Mach-O binaries** via **`NSAppleScript`** / **`OSAScript`**, which is useful both for evasion and for living inside a host that already has interesting TCC grants.[\[2\]](#references)

```
osascript -l JavaScript <<'EOF'
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.doShellScript("id > /tmp/jxa_id");
EOF
```
If you build a custom helper that sends Apple Events directly, giving it a **real app identity** makes testing and operations much more reliable. In practice this means embedding an `Info.plist` with `CFBundleIdentifier` and `NSAppleEventsUsageDescription`, signing the binary, and granting the `com.apple.security.automation.apple-events` entitlement. Otherwise the Apple Events prompt is frequently attributed to the **parent host** (for example `Terminal`) or the `NSAppleScript` execution just fails with confusing `-1750` / `errOSASystemError` errors.[\[2\]](#references)

AppleScripts can be saved in compiled form and ordinarily decompiled with `osadecompile`.

However, these scripts can also be **exported as “Read only”** (via the “Export…” option):

```
file mal.scpt
mal.scpt: AppleScript compiled
```
In that case `osadecompile` refuses to recover normal source, but the bytecode and Apple Event terminology can still be analyzed.

SentinelOne’s run-only research describes how to recover structure despite that restriction. `applescript-disassembler` and `aevt_decompile` help inspect the compiled script and Apple Event data.[\[4\]](#references)[\[5\]](#references)[\[6\]](#references)

## References
