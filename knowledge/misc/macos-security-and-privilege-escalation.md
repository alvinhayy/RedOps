---
title: "macOS Security & Privilege Escalation"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Basic macOS

If you are not familiar with macOS, start with the basics and the incident-response, malware-analysis, and command references listed below.[\[1\]](#references)[\[2\]](#references)[\[3\]](#references)[\[4\]](#references)

- Special macOS **files & permissions:**

[macOS Files, Folders, Binaries & Memory](macos-files-folders-and-binaries/index.html)

- Common macOS **users**

[macOS Users & External Accounts](macos-users.html)

- **AppleFS**

- The **architecture** of the**kernel**

[macOS Kernel & System Extensions](mac-os-architecture/index.html)

- Common macOS **network services and protocols**

[macOS Network Services & Protocols](macos-protocols.html)

- **Opensource** macOS:[https://opensource.apple.com/](https://opensource.apple.com/)  - To download a `tar.gz` change a URL such as[https://opensource.apple.com/**source**/dyld/](https://opensource.apple.com/source/dyld/) to[https://opensource.apple.com/**tarballs**/dyld/**dyld-852.2.tar.gz**](https://opensource.apple.com/tarballs/dyld/dyld-852.2.tar.gz)
- To download a

### macOS MDM

In corporate environments, macOS systems are often managed with mobile device management (MDM). From an attacker’s perspective, it is therefore useful to understand how MDM works:

### macOS - Inspecting, Debugging And Fuzzing

[macOS Apps - Inspecting, debugging and Fuzzing](macos-apps-inspecting-debugging-and-fuzzing/index.html)

## macOS Security Protections

## Attack Surface

### File Permissions

If a **process running as root writes** a file that can be controlled by a user, the user could abuse this to **escalate privileges**.

This could occur in the following situations:

- File used was already created by a user (owned by the user)
- File used is writable by the user because of a group
- File used is inside a directory owned by the user (the user could create the file)
- File used is inside a directory owned by root but user has write access over it because of a group (the user could create the file)

Being able to **create a file** that is going to be **used by root**, allows a user to **take advantage of its content** or even create **symlinks/hardlinks** to point it to another place.

For this kind of vulnerabilities don’t forget to **check vulnerable `.pkg` installers**:

### File Extension & URL scheme app handlers

Unexpected applications registered for file extensions or URL schemes may expose useful attack surfaces or handler-hijacking opportunities.

[macOS File Extension & URL scheme app handlers](macos-file-extension-apps.html)

## macOS TCC / SIP Privilege Escalation

In macOS **applications and binaries can have permissions** to access folders or settings that make them more privileged than others.

Therefore, an attacker that wants to successfully compromise a macOS machine will need to **escalate its TCC privileges** (or even **bypass SIP**, depending on his needs).

These privileges are usually granted through code-signing **entitlements** or through user-approved access recorded in the **TCC databases**. Some privileges may also be inherited from a parent process, depending on the protection and execution chain.[\[5\]](#references)

Follow these links for ways to [**escalate TCC privileges**](macos-security-protections/macos-tcc/index.html#tcc-privesc-and-bypasses), [**bypass TCC**](macos-security-protections/macos-tcc/macos-tcc-bypasses/index.html), and understand how [**SIP has been bypassed**](macos-security-protections/macos-sip.html#sip-bypasses) in the past.

## macOS Traditional Privilege Escalation

From a red-team perspective, escalation to root is another important objective. The following page covers common approaches:

## macOS Compliance

## References
