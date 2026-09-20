---
title: "Use After Free"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/binary-exploitation/libc-heap/use-after-free/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: reversing
---

# Use-After-Free

## Basic Information

A use-after-free (UAF) occurs when a program continues to use a pointer or reference after the referenced allocation has been freed. The stale reference is often called a *dangling pointer*. If the allocator later reuses that region, the stale pointer may refer to data owned by a different object.[\[1\]](#references)

Accessing freed memory is invalid, but it does not necessarily fail immediately. Depending on the operation and the allocator state, a UAF may cause a crash, disclose memory, corrupt a live object, or enable code execution. Exploitation commonly involves reclaiming the freed region with attacker-influenced data before the program dereferences the stale pointer; overwriting a function pointer or another control-sensitive field can then redirect execution.[\[1\]](#references)

## First-Fit Attack

A first-fit attack uses predictable allocation selection to reclaim a freed chunk with a chosen allocation. In a UAF scenario, heap grooming can place attacker-controlled contents where the dangling pointer will later read or write. In glibc, some same-size free lists—notably tcache bins and fastbins—are last-in, first-out, so a matching allocation may return the most recently freed chunk. Other bins and allocators use different selection rules, so the exact result depends on the glibc version, size class, cache/bin state, and allocation sequence.<sup>[\[2\]](#references)</sup> See the dedicated page for details:

## References
