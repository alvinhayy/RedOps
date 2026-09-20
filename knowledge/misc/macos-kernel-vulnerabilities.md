---
title: "macOS Kernel Vulnerabilities"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/mac-os-architecture/macos-kernel-vulnerabilities.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Attack surfaces that still matter

- **Mach/MIG handlers** in system daemons and kernel-facing services: malformed descriptors, out-of-line (OOL) data, and stateful multi-message flows.
- **IOKit user clients** : selector-specific parsing, entitlement-gated methods, and wrapper libraries/daemons that hide the real call graph.
- **XNU data-only primitives** : races around credentials, SMR-protected pointers, read-only zones, and other places where corruption changes policy without first winning RIP/PC control.
- **Third-party / auxiliary kernel code** : legacy kexts are rarer, but enterprise fleets, reduced-security Apple Silicon systems, and vendor`.fs` / helper bundles still create high-value kernel-adjacent paths.

## [Pwning OTA](https://jhftss.github.io/The-Nightmare-of-Apple-OTA-Update/)

In [**this report**](https://jhftss.github.io/The-Nightmare-of-Apple-OTA-Update/) several OTA/update-chain bugs are combined to reach kernel compromise by abusing the software update pipeline and rootless-related capabilities.[\[3\]](#references)

[**PoC**](https://github.com/jhftss/POC/tree/main/CVE-2022-46722).

## 2024: In-the-wild kernel protection bypass chain (CVE-2024-23225 & CVE-2024-23296)

Apple’s [**March 2024 macOS security releases**](https://support.apple.com/en-us/120895) fixed two issues that were **actively exploited**:[\[6\]](#references)

- **CVE-2024-23225 – Kernel** : a memory-corruption bug where an attacker with arbitrary kernel read/write could bypass kernel memory protections.
- **CVE-2024-23296 – RTKit** : a second memory-corruption bug with the same public impact statement.

Public root-cause details are still scarce, but the pair is a good reminder that modern Apple exploit chains often need **more than “just” kernel R/W**: post-exploitation work against memory protections, coprocessor-adjacent code, or secondary trust boundaries is frequently where the real chain gets stabilized.

Quick patch triage:

```
sw_vers
uname -v
softwareupdate --history | tail -n 20
```
## 2025: SMR + read-only credential race (CVE-2025-24118)

Joseph Ravichandran’s [**TRAVERTINE write-up**](https://jprx.io/cve-2025-24118/) is a very good modern XNU case study because it is **not** a classic buffer overflow:[\[1\]](#references)

- `proc_ro.p_ucred` is an**SMR-protected pointer** stored in a**read-only**`proc_ro` object.
- Writers must update that pointer **atomically** .
- `kauth_cred_proc_update()` used`zalloc_ro_mut(...)` to mutate`p_ucred` ; on x86_64 that path eventually hits`memcpy` /`rep movsb` , so a concurrent reader can observe a**torn pointer** .
- The bug turns into a **data-only privilege escalation** : if the corrupted credential pointer resolves to a different valid credential object, the current thread can inherit more privileged state without first winning an obvious control-flow hijack.

Minimal trigger pattern:

```
// writer thread: force frequent credential swaps
while (1) {
    setgid(real_gid);
    setgid(saved_or_effective_gid);
}
// reader thread: repeatedly dereference current credentials
while (1) {
    (void)getgid();
}
```
Useful audit heuristic: whenever a kernel path mixes **SMR readers**, **read-only zone mutation**, and **credential or task metadata**, verify that updates use the atomic `zalloc_ro_mut_*` variants rather than copy-based helpers.

## 2024-2025: SIP bypass that re-opens kernel loading paths (CVE-2024-44243)

Microsoft showed that `storagekitd` could be abused to **bypass SIP** and then make third-party kernel code relevant again on machines that would otherwise look “post-kext”. The key idea is:[\[2\]](#references)

1. Drop or overwrite a malicious `.fs` bundle under`/Library/Filesystems` .
2. Trigger `storagekitd` via Disk Utility or`diskutil` .
3. Let the specially entitled daemon spawn bundle executables **without properly dropping privileges / validating the path** .
4. Use the resulting SIP bypass to alter protected file-system state and, in Microsoft’s demonstration, override the kernel extension exclusion list.

For kernel researchers, the important lesson is that **kernel attack surface can be reintroduced from userland management daemons**, even when direct third-party kext loading is heavily restricted.

Useful triage:

```
ls -la /Library/Filesystems
find /Library/Filesystems -maxdepth 3 -type f \( -name 'mount_*' -o -name 'fsck_*' -o -name 'newfs_*' \) 2>/dev/null
log stream --style syslog --predicate 'process == "storagekitd" || process == "diskarbitrationd"'
kmutil showloaded --collection aux
```
## Fuzzing & research workflow

If you are actively hunting this class of bugs, the recent public work is pointing in the same direction:

- [**KextFuzz**](https://www.usenix.org/conference/usenixsecurity23/presentation/yin) is still one of the best references for Apple-Silicon-era kernel research. It uses**static binary rewriting** to recover coverage, disables**entitlement-gated** paths during testing, and infers interface structure from userspace wrappers.<sup>[\[4\]](#references)</sup>
- Project Zero’s [**Simple macOS kernel extension fuzzing in userspace with IDA and TinyInst**](https://projectzero.google/2024/11/simple-macos-kernel-extension-fuzzing.html) shows a very practical workflow for**rebasing a kext / fileset into userspace** so parser-heavy code can be fuzzed at much higher speed before reproducing on-device.<sup>[\[5\]](#references)</sup>
- For Mach-heavy targets, build harnesses around **real message layouts and multi-call state machines** , not just single selector blobs. Recent CoreAudio/Mach research from Project Zero and conference talks such as**Fuzzing at Mach Speed** show why stateful message sequences keep paying off.

Quick local commands you will actually use a lot:

```
# Loaded auxiliary / 3rd party kernel code
kmutil showloaded --collection aux
# Fileset entries in the boot kernel collection
kmutil inspect -B /System/Library/KernelCollections/BootKernelExtensions.kc --show-fileset-entries
# Diffable version info before matching a KDK / symbols pack
sw_vers
uname -a
```
## Quick Enumeration Cheatsheet

```
uname -a                          # Kernel build
sw_vers                           # ProductVersion / BuildVersion
kmutil showloaded                 # List loaded kernel extensions
kmutil showloaded --collection aux  # Auxiliary / 3rd party collections
kextstat 2>/dev/null | grep -v com.apple
csrutil status                    # Check SIP state
spctl --status                    # Confirm Gatekeeper state
```
## References
