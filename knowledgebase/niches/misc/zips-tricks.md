---
title: "ZIPs tricks"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/basic-forensic-methodology/specific-software-file-type-tricks/zips-tricks.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: misc
---

## Anti-reversing tricks in APKs using manipulated ZIP headers

Modern Android malware droppers use malformed ZIP metadata to break static tools (jadx/apktool/unzip) while keeping the APK installable on-device. The most common tricks are:[\[2\]](#references)

- Fake encryption by setting the ZIP General Purpose Bit Flag (GPBF) bit 0
- Abusing large/custom Extra fields to confuse parsers
- File/directory name collisions to hide real artifacts (e.g., a directory named `classes.dex/` next to the real`classes.dex` )

### 1) Fake encryption (GPBF bit 0 set) without real crypto

Symptoms:

-
`jadx-gui` fails with errors like:```
java.util.zip.ZipException: invalid CEN header (encrypted entry)
```
-
`unzip` prompts for a password for core APK files even though a valid APK cannot have encrypted`classes*.dex` ,`resources.arsc` , or`AndroidManifest.xml` :```
unzip sample.apk
[sample.apk] classes3.dex password:
  skipping: classes3.dex                          incorrect password
  skipping: AndroidManifest.xml/res/vhpng-xhdpi/mxirm.png  incorrect password
  skipping: resources.arsc/res/domeo/eqmvo.xml            incorrect password
  skipping: classes2.dex                          incorrect password
```

Detection with zipdetails:

```
zipdetails -v sample.apk | less
```
Look at the General Purpose Bit Flag for local and central headers. A telltale value is bit 0 set (Encryption) even for core entries:

```
Extract Zip Spec      2D '4.5'
General Purpose Flag  0A09
  [Bit 0]   1 'Encryption'
  [Bits 1-2] 1 'Maximum Compression'
  [Bit 3]   1 'Streamed'
  [Bit 11]  1 'Language Encoding'
```
Heuristic: If an APK installs and runs on-device but core entries appear “encrypted” to tools, the GPBF was tampered with.

Fix by clearing GPBF bit 0 in both Local File Headers (LFH) and Central Directory (CD) entries. Minimal byte-patcher:

## Minimal GPBF bit-clear patcher

```
# gpbf_clear.py – clear encryption bit (bit 0) in ZIP local+central headers
import struct, sys
SIG_LFH = b"\x50\x4b\x03\x04"  # Local File Header
SIG_CDH = b"\x50\x4b\x01\x02"  # Central Directory Header
def patch_flags(buf: bytes, sig: bytes, flag_off: int):
    out = bytearray(buf)
    i = 0
    patched = 0
    while True:
        i = out.find(sig, i)
        if i == -1:
            break
        flags, = struct.unpack_from('<H', out, i + flag_off)
        if flags & 1:  # encryption bit set
            struct.pack_into('<H', out, i + flag_off, flags & 0xFFFE)
            patched += 1
        i += 4  # move past signature to continue search
    return bytes(out), patched
if __name__ == '__main__':
    inp, outp = sys.argv[1], sys.argv[2]
    data = open(inp, 'rb').read()
    data, p_lfh = patch_flags(data, SIG_LFH, 6)  # LFH flag at +6
    data, p_cdh = patch_flags(data, SIG_CDH, 8)  # CDH flag at +8
    open(outp, 'wb').write(data)
    print(f'Patched: LFH={p_lfh}, CDH={p_cdh}')
```
Usage:

```
python3 gpbf_clear.py obfuscated.apk normalized.apk
zipdetails -v normalized.apk | grep -A2 "General Purpose Flag"
```
You should now see `General Purpose Flag  0000` on core entries and tools will parse the APK again.

### 2) Large/custom Extra fields to break parsers

Attackers stuff oversized Extra fields and odd IDs into headers to trip decompilers. In the wild you may see custom markers (e.g., strings like `JADXBLOCK`) embedded there.

Inspection:

```
zipdetails -v sample.apk | sed -n '/Extra ID/,+4p' | head -n 50
```
Examples observed: unknown IDs like `0xCAFE` (“Java Executable”) or `0x414A` (“JA:”) carrying large payloads.[\[2\]](#references)

DFIR heuristics:

- Alert when Extra fields are unusually large on core entries (`classes*.dex` ,`AndroidManifest.xml` ,`resources.arsc` ).
- Treat unknown Extra IDs on those entries as suspicious.

Practical mitigation: rebuilding the archive (e.g., re-zipping extracted files) strips malicious Extra fields. If tools refuse to extract due to fake encryption, first clear GPBF bit 0 as above, then repackage:

```
mkdir /tmp/apk
unzip -qq normalized.apk -d /tmp/apk
(cd /tmp/apk && zip -qr ../clean.apk .)
```
### 3) File/Directory name collisions (hiding real artifacts)

A ZIP can contain both a file `X` and a directory `X/`. Some extractors and decompilers get confused and may overlay or hide the real file with a directory entry. This has been observed with entries colliding with core APK names like `classes.dex`.

Triage and safe extraction:

```
# List potential collisions (names that differ only by trailing slash)
zipinfo -1 sample.apk | awk '{n=$0; sub(/\/$/,"",n); print n}' | sort | uniq -d
# Extract while preserving the real files by renaming on conflict
unzip normalized.apk -d outdir
# When prompted:
# replace outdir/classes.dex? [y]es/[n]o/[A]ll/[N]one/[r]ename: r
# new name: unk_classes.dex
```
Programmatic detection post-fix:

```
from zipfile import ZipFile
from collections import defaultdict
with ZipFile('normalized.apk') as z:
    names = z.namelist()
collisions = defaultdict(list)
for n in names:
    base = n[:-1] if n.endswith('/') else n
    collisions[base].append(n)
for base, variants in collisions.items():
    if len(variants) > 1:
        print('COLLISION', base, '->', variants)
```
Blue-team detection ideas:

- Flag APKs whose local headers mark encryption (GPBF bit 0 = 1) yet install/run.
- Flag large/unknown Extra fields on core entries (look for markers like `JADXBLOCK` ).
- Flag path-collisions (`X` and`X/` ) specifically for`AndroidManifest.xml` ,`resources.arsc` ,`classes*.dex` .

## Other malicious ZIP tricks (2024–2026)

### Concatenated central directories (multi-EOCD evasion)

In a 2024 phishing campaign, attackers shipped a single blob that was actually **two ZIP files concatenated**. Each had its own End of Central Directory (EOCD) record and central directory. Different extractors parsed different directories (7-Zip read the first, while WinRAR read the last), letting attackers hide payloads that only some tools showed; scanners that inspect only one directory can miss the other archive.[\[5\]](#references)[\[6\]](#references)

**Triage commands**

```
# Count EOCD signatures
binwalk -R "PK\x05\x06" suspect.zip
# Show EOCD records and their central-directory offsets
zipdetails --scan -v suspect.zip | grep -ni -A2 "end central"
```
If more than one EOCD appears or there are “data after payload” warnings, split the blob and inspect each part:

```
# Recover the second archive from its first local-file-header offset.
binwalk -R "PK\x03\x04" suspect.zip
# Adjust OFF to the second archive's local-header offset from that output.
OFF=123456
dd if=suspect.zip bs=1 skip="$OFF" of=tail.zip
7z l tail.zip   # list hidden content
```
### Quoted-overlap / overlapping-entry bombs (non-recursive)

Quoted-overlap ZIP bombs build a tiny **kernel** (a highly compressed DEFLATE block) and reuse it across overlapping entries. Full-overlap variants point multiple central-directory entries at one local header, while quoted-overlap variants quote local headers inside DEFLATE streams; the published construction achieves more than 28M:1 without nested archives.[\[7\]](#references)

**Quick detection (duplicate LFH offsets)**

```
# detect full-overlap variants by identical relative offsets
import struct, sys
buf=open(sys.argv[1],'rb').read()
off=0; seen=set()
while True:
    i = buf.find(b'PK\x01\x02', off)
    if i<0: break
    rel = struct.unpack_from('<I', buf, i+42)[0]
    if rel in seen:
        print('OVERLAP at offset', rel)
        break
    seen.add(rel); off = i+4
```
**Handling**

- Perform a dry-run walk: `zipdetails -v file.zip | grep -n "Local Header Offset"` and compare referenced local-header offsets and compressed-data ranges; duplicate offsets flag full-overlap variants.<sup>[\[7\]](#references)[\[8\]](#references)</sup>
- Cap accepted total uncompressed size and entry count before extraction with a parser; `zipinfo -t file.zip` reports totals but does not enforce a safety limit.<sup>[\[8\]](#references)</sup>
- When you must extract, do it inside a cgroup/VM with CPU and disk limits (avoid unbounded inflation crashes).<sup>[\[8\]](#references)</sup>

### Local-header vs central-directory parser confusion

Recent differential-parser research showed that ZIP ambiguity is still exploitable in modern toolchains. The main idea is simple: some software trusts the **Local File Header (LFH)** while others trust the **Central Directory (CD)**, so one archive can present different filenames, paths, comments, offsets, or entry sets to different tools.[\[9\]](#references)

Practical offensive uses:

- Make an upload filter, AV pre-scan, or package validator see a benign file in the CD while the extractor honors a different LFH name/path.
- Abuse duplicate names, entries present only in one structure, or ambiguous Unicode path metadata (for example, Info-ZIP Unicode Path Extra Field `0x7075` ) so different parsers reconstruct different trees.
- Combine this with path traversal to turn a “harmless” archive view into a write-primitive during extraction. For the extraction side, see [Archive Extraction Path Traversal](../../../generic-hacking/archive-extraction-path-traversal.html) .

DFIR triage:

```
# compare Central Directory names against the referenced Local File Header names
import struct, sys
b = open(sys.argv[1], 'rb').read()
lfh = {}
i = 0
while (i := b.find(b'PK\x03\x04', i)) != -1:
    n, e = struct.unpack_from('<HH', b, i + 26)
    lfh[i] = b[i + 30:i + 30 + n].decode('utf-8', 'replace')
    i += 4
i = 0
while (i := b.find(b'PK\x01\x02', i)) != -1:
    n = struct.unpack_from('<H', b, i + 28)[0]
    off = struct.unpack_from('<I', b, i + 42)[0]
    cd = b[i + 46:i + 46 + n].decode('utf-8', 'replace')
    if off in lfh and cd != lfh[off]:
        print(f'NAME_MISMATCH off={off} cd={cd!r} lfh={lfh[off]!r}')
    i += 4
```
Complement it with:

```
zipdetails -v suspect.zip | less
zipinfo -v suspect.zip | grep -E "file name|offset|comment"
```
Heuristics:

- For security-sensitive ingestion, reject or isolate archives with mismatched LFH/CD names, duplicate filenames, multiple EOCD records, or trailing bytes after the final EOCD.<sup>[\[9\]](#references)[\[10\]](#references)</sup>
- Treat ZIPs using unusual Unicode-path extra fields or inconsistent comments as suspicious if different tools disagree on the extracted tree.<sup>[\[4\]](#references)[\[9\]](#references)</sup>
- If analysis matters more than preserving the original bytes, repackage the archive with a strict parser after extraction in a sandbox and compare the resulting file list to the original metadata.

This matters beyond package ecosystems: the same ambiguity class can hide payloads from mail gateways, static scanners, and custom ingestion pipelines that “peek” at ZIP contents before a different extractor handles the archive.[\[9\]](#references)

## References
