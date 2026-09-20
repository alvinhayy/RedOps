---
title: "Common Binary Exploitation Protections & Bypasses"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/binary-exploitation/common-binary-protections-and-bypasses/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: reversing
---

## Enable core dumps

A core dump records selected parts of a process’s memory and execution state when the process terminates abnormally. It is useful for reproducing a crash and inspecting registers, mappings, and the call stack, but it can also contain secrets from process memory.[\[1\]](#references)

### Enable core-dump generation

The shell’s soft `RLIMIT_CORE` value controls the largest core file its child processes may create. Set it to `unlimited` for the current shell and commands started from it:[\[1\]](#references)[\[2\]](#references)

```
ulimit -c unlimited
```
For PAM-managed login sessions, a corresponding `/etc/security/limits.conf` entry is:

```
* soft core unlimited
```
This setting does not necessarily apply to services started by `systemd`; service limits and the kernel’s `core_pattern` can redirect or suppress dumps. Check `ulimit -c`, `/proc/sys/kernel/core_pattern`, and the applicable service configuration before assuming that a file named `core` will appear.[\[1\]](#references)

### Analyze a core dump with GDB

Pass both the exact executable and its core dump to GDB:[\[3\]](#references)

```
gdb /path/to/executable /path/to/core_file
```
Useful first commands include `info registers`, `info proc mappings`, `bt`, and `x/i $pc`. Use the same executable and shared-library versions that produced the dump so addresses and symbols resolve correctly.

## References
