---
title: "Firmware Integrity"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/hardware-physical-access/firmware-analysis/firmware-integrity.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Unauthenticated transport bridges to privileged update protocols

A common embedded design mistake is exposing the **same internal command protocol over several transports** but enforcing authentication on only one of them. For example, USB may require challenge-response while BLE simply forwards unauthenticated **GATT writes** into the same privileged firmware-update handler.[\[1\]](#references)

Typical offensive workflow:

1. Enumerate the BLE GATT database and identify writable characteristics used by the official mobile app.
2. Sniff app traffic and look for **magic bytes / opcodes** that match the wired protocol.
3. Replay privileged commands over BLE **without pairing** and verify whether sensitive operations still work.
4. If firmware upgrade, config write, debug, or factory-test opcodes are reachable, treat BLE as a **radio-reachable admin port** .

Quick checks:

```
# Enumerate services/characteristics
ble.enum <MAC>
# Replay a sniffed command
ble.write <MAC> <UUID> <HEX_DATA>
# gatttool equivalent
# gatttool -b <MAC> --char-write-req -a <HANDLE> -n <HEX_DATA>
```
Things to verify while reversing:

- Does BLE require **pairing/bonding** or just a plain connection?
- Are all transports routed to the same internal dispatcher table?
- Are privileged opcodes filtered differently on USB / BLE / UART / Wi-Fi?
- Can the mobile app trigger firmware update, recovery, or diagnostic handlers remotely?

## Checksum-only firmware containers are still attacker-controlled firmware

A firmware container protected only by an **unkeyed checksum** (CRC32, SHA-256, MD5, etc.) provides corruption detection, **not authenticity**. If the attacker can reach the update routine, they can patch the image, recompute the checksum, and flash arbitrary code.[\[1\]](#references)

Red flags during RE:

- Update code validates only a trailing checksum blob such as `CHK2` ,`CRC` , or`SHA256` .
- No signature verification or secure-boot root of trust is present.
- No device-bound MAC / HMAC / authenticated encryption is used.
- Recovery mode accepts the same unauthenticated image format.

Practical validation flow:

1. Extract the firmware container and identify bootloader, main firmware, and integrity metadata.
2. Modify a harmless string or banner in the image.
3. Recompute the checksum exactly as the updater expects.
4. Reflash the image through the normal update path.
5. Confirm the change on boot to prove arbitrary firmware replacement.

If this works over a remotely reachable transport such as BLE/Wi-Fi, the bug is effectively **unauthenticated OTA firmware replacement**.

## Turning a trusted USB peripheral into BadUSB via firmware reflashing

When the target device is already trusted by the host over USB, malicious firmware may not need to implement a full new USB stack. A much easier pivot is often to **reuse existing HID support**.[\[1\]](#references)

Useful pattern:

1. Check whether the device already enumerates as a **HID Consumer Control** / media / vendor HID interface.
2. Locate the existing **HID report descriptor** in firmware.
3. Append or replace descriptor entries so the device also advertises **keyboard** capability.
4. Reuse existing firmware routines that already send HID reports instead of writing a new transport implementation.
5. Inject key press + key release reports to type commands on the host.

This turns firmware compromise into **host compromise** because the PC will trust the reflashed peripheral as a legitimate keyboard.

### Minimal assessment checklist

- Does `dmesg` , Device Manager, or USB descriptors show an existing HID interface?
- Is there spare room near the report descriptor or a relocatable descriptor table?
- Can existing media-control send routines be reused for keyboard reports?
- Does the host auto-accept the new keyboard interface after reflashing?

## Reliable payload execution inside RTOS firmware

Instead of inserting fragile trampolines into random code paths, look for **existing RTOS tasks** that are unused or low-impact in normal operation.[\[1\]](#references)

Why this is useful:

- The scheduler starts your payload naturally during boot.
- You avoid corrupting critical control flow.
- Delayed payloads are less likely to trigger watchdog resets than when run inside a latency-sensitive USB/network handler.

Good targets are diagnostic, factory-test, telemetry, or coprocessor service tasks that appear dormant in normal usage.

## Fast exploit iteration: repurpose benign protocol handlers

Once firmware patching is possible, a compact way to accelerate RE is to overwrite a harmless command handler (for example an **echo/debug opcode**) with custom **memory read / write / execute** primitives. This avoids full reflashing for every experiment and is especially useful when the device supports the modified handler over a fast wired transport.[\[1\]](#references)

Use this to:

- Verify scatter-loaded memory maps
- Inspect heap/task state live
- Test small payloads before burning them into flash
- Recover function pointers, strings, and descriptor tables safely

## References

- [1] [Pwnd Blaster: Hacking your PC using your speaker without ever touching it](https://blog.nns.ee/2026/06/03/katana-badusb/)
- [2] [firmware-mod-kit](https://github.com/rampageX/firmware-mod-kit)
- [3] [Firmware Analysis Toolkit](https://github.com/attify/firmware-analysis-toolkit)
- [4] [Metasploit - How to use `msfvenom`](https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-msfvenom.html)
