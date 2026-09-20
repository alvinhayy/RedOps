---
title: "Stack Canaries"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/binary-exploitation/common-binary-protections-and-bypasses/stack-canaries/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: reversing
---

## StackGuard and StackShield

**StackGuard** introduced compiler-inserted canaries between vulnerable local data and control data. Its historical *terminator canary* used bytes such as NUL, newline, EOF, and carriage return (often shown as `0x000aff0d`), while later variants used random or XOR canaries. Terminator bytes obstruct string-copy functions, but length-based operations such as `recv()`, `memcpy()`, `read()`, and `bcopy()` can still copy them. The check detects a changed canary when the function returns; it does not by itself prevent corruption of data placed before the canary. In the historical layouts analyzed by Core Security, the saved frame pointer (`EBP`) was before the protected return address and could therefore remain a separate corruption target.[\[5\]](#references)[\[9\]](#references)

**StackShield** stores return addresses in a separate Global Return Stack. Its default mode restores the separately saved value, while other modes can compare return addresses or apply range checks. This protects direct saved-return-address overwrites, but not arbitrary local-variable, function-argument, frame-pointer, or other code-pointer corruption. Return-to-libc, ROP, and ret2ret remain useful code-reuse techniques after another primitive supplies control flow, but simply overwriting a return address protected by the Global Return Stack is not by itself a bypass.[\[9\]](#references)

## Stack-Smashing Protector (`-fstack-protector`)

`-fstack-protector`)
Modern compiler stack protection places a guard between selected local objects and saved control data, verifies it in the function epilogue, and calls `__stack_chk_fail` on mismatch. ProPolice also proposed variable reordering and copying vulnerable pointer arguments. Older/default implementations could omit arrays below an eight-byte threshold and, depending on how the compiler represented them, buffers embedded in structures. Exact selection remains compiler- and option-dependent: GCC’s `-fstack-protector`, `-strong`, `-all`, and `-explicit` intentionally cover different sets of functions, so the historical limitation is useful when auditing old binaries but is not a universal current rule.[\[6\]](#references)[\[9\]](#references)

On common Linux/glibc builds, the process initializes a randomized guard and accesses it through thread-local storage. Older glibc code used kernel `AT_RANDOM` data when available, could fall back to `/dev/urandom`, and finally constructed a terminator-style value (commonly rendered as `0xff0a0000` on 32-bit little-endian systems) if randomness was unavailable. Current glibc takes kernel-provided random bytes and clears the byte encountered first by a typical string overflow.[\[8\]](#references)<sup>[\[10\]](#references)</sup> Frequently encountered i386 and x86-64 layouts use `gs:0x14` and `fs:0x28`, respectively, but these offsets are ABI/runtime implementation details rather than portable guarantees. A `fork()` child inherits the current address space and guard value; separately forked request workers can therefore provide repeated guesses against one canary. Threads normally start with the process’s guard value even though the access location is thread-local.[\[1\]](#references)

The compiler injects a prologue that copies the guard into the frame and an epilogue that verifies the copy before using the saved return state.

When a crash is isolated to a forked request worker and the parent keeps spawning workers with the same guard, an attacker may be able to brute-force it byte by byte. A successful `execve()` replaces the process image and causes the new runtime to initialize a new guard. `vfork()` is not a canary defense: the child temporarily shares the parent’s address space and must call `_exit()` or an `exec` function without modifying other memory.[\[7\]](#references)

### Lengths

In typical Linux/glibc `x86_64` binaries, the guard is an **8-byte** value. In memory, its least-significant byte is NUL and the remaining seven bytes carry the unpredictable portion.

In typical Linux/glibc `i386` binaries, it is a **4-byte** value with a least-significant NUL and three unpredictable bytes.[\[1\]](#references)

Caution

The least-significant NUL byte is encountered first by a contiguous overflow from a lower-addressed local buffer on these little-endian layouts, frustrating string-copy primitives. Do not assume this byte layout on every OS, architecture, or runtime.

## Bypasses

**Leaking the canary** and then overwriting it (e.g. buffer overflow) with its own value.[\[1\]](#references)

- If the **canary is forked in child processes** it might be possible to**brute-force** it one byte at a time:

[BF Forked & Threaded Stack Canaries](bf-forked-stack-canaries.html)

- If there is some interesting **leak or arbitrary read vulnerability** in the binary it might be possible to leak it:

- **Overwriting stack stored pointers**

The stack vulnerable to a stack overflow might **contain addresses to strings or functions that can be overwritten** in order to exploit the vulnerability without needing to reach the stack canary. Check:

- **Modifying both master and thread canary**

A sufficiently large overflow from a thread stack may reach the thread-local guard stored in the adjacent TLS mapping. If the exploit overwrites both the frame copy and the TLS guard with the same value, the epilogue comparison still succeeds. The Robot Factory writeup demonstrates this **master-canary forging** path.[\[2\]](#references)

The CODE BLUE presentation explains the relevant layout: runtimes commonly create both thread stacks and TLS-related mappings with `mmap`, which can place the guard within reach of an overflow on a specific build.[\[4\]](#references)

- **Modify the GOT entry of `__stack_chk_fail`**

If the binary has Partial RELRO, then you can use an arbitrary write to modify the **GOT entry of `__stack_chk_fail`** to be a dummy function that does not block the program if the canary gets modified.

The Scrambler writeup demonstrates this attack.[\[3\]](#references)

## References
