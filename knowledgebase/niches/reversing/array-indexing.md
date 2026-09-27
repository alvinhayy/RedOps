---
title: "Array Indexing"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/binary-exploitation/array-indexing.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: reversing
---

## Basic Information

Array-indexing vulnerabilities occur when a program fails to validate an index before using it to read or write an array. An out-of-bounds access may disclose memory, corrupt adjacent objects, or alter control data. The exploitation strategy depends on the array layout, the attacker’s control over the index and value, and the binary’s mitigations.[\[5\]](#references)

## Read-dependent constrained OOB writes

An unchecked integer used to index a pointer table can produce more than a simple OOB read when the surrounding logic reads the slot and conditionally updates it. Audit patterns equivalent to the following, including indexes parsed from database rows, configuration objects, or plugin input.[\[6\]](#references)

```
entry = table[node][index];
if (entry == NULL) {
    table[node][index] = current;
} else {
    while (entry->next != NULL)
        entry = entry->next;
    entry->next = current;
}
```
The initial access selects `B + index * sizeof(pointer)`. A negative index reaches memory before `B`, while an index at or above the element count reaches memory after the array. The value read determines which constrained corruption primitive follows:[\[6\]](#references)

- **Zero slot:** the code writes the live`current` object pointer to the same attacker-selected relative slot. The destination is partially controlled, but the written value is not.
- **Nonzero slot:** unrelated memory is type-confused as an object. The loop follows fixed-offset`next` pointers until a NULL field is found and then writes`current` there. Useful exploitation requires a readable pointer chain; otherwise the process crashes during traversal.

A very large index is useful for confirming the missing check because it normally reaches unmapped memory, but this demonstrates only a crash. Turning the primitive into a security-sensitive write usually requires a reachable mapped offset, a zero slot or predictable pointer chain, an address disclosure when ASLR is enabled, heap-layout control, and a target that is useful when replaced with the constrained object pointer.[\[6\]](#references)

### Native-extension example: PostGIS `address_standardizer`

`address_standardizer`
PostGIS `address_standardizer` illustrated this pattern in native code running inside the PostgreSQL backend. A caller could select a rules table whose rule strings end in attacker-controlled `Type` and `Weight` integers; the path `standardize_address()` → `load_rules()` → `parse_rule()` → `rules_add_rule()` → `classify_link()` validated token symbols but previously allowed `Type` to reach a five-entry `KW *` table without a `0..4` bounds check. On a 64-bit build the selected address was therefore `B + Type * 8`, so `Type = -1` selected the qword immediately before the 40-byte row and `Type = 5` selected the first qword after it.[\[6\]](#references)

The following authenticated crash probe uses a caller-owned rules table and a distant index. Run denial-of-service probes only in an isolated test instance because the affected backend can terminate.[\[6\]](#references)

```
CREATE TEMP TABLE poc_rules_oob (
    id serial PRIMARY KEY,
    rule text NOT NULL
);
INSERT INTO poc_rules_oob(rule)
VALUES ('29 -1 1 -1 2147483647 1');
SELECT standardize_address(
    'us_lex', 'us_gaz', 'poc_rules_oob',
    '123 Main St', 'Springfield'
);
```
This primitive does not return the OOB value to SQL and does not by itself provide an arbitrary-value write or defeat ASLR. The reported full chain paired it with a separate address disclosure and targeted backend-local cached authorization state; this is an example of converting a relative, pointer-valued write into privilege escalation by corrupting process-local security state rather than persistently modifying database catalogs.[\[6\]](#references)

## Examples

- **SwampCTF 2019 - dreamheaps:** Two arrays store allocation addresses and sizes. Their indexes overlap, so an out-of-bounds operation can turn a size entry into an attacker-chosen pointer. The exploit redirects a write to`free@GOT` , replaces it with`system` , and frees a buffer containing`/bin/sh` .<sup>[\[1\]](#references)</sup>
- **CSAW 2018 - doubletrouble:** A 64-bit binary with an executable stack sorts attacker-supplied doubles before returning. The exploit converts shellcode bytes and control-flow addresses into sortable floating-point values, arranges them so the sort does not move the canary, and places a suitable`ret` address in the overwritten return slot. The largest sorted value is a pointer into the leaked stack, so the final return reaches the shellcode.<sup>[\[2\]](#references)</sup>
- **SECCON CTF 2019 - sum:** This 64-bit binary has no RELRO or PIE, but it does have a stack canary and NX. An off-by-one stack-array index corrupts a pointer used as the destination for a calculated sum, producing a constrained write-what-where primitive. The exploit overwrites`exit@GOT` with a`pop rdi; ret` gadget and places`main` on the stack so the process loops instead of exiting. A following ROP stage passes`puts@GOT` to`puts` to disclose libc, returns to`main` again, and finally executes a ret2libc call to`system` .<sup>[\[3\]](#references)</sup>
- **TUCTF - guestbook:** This 32-bit PIE binary has NX but no RELRO or stack canary. A negative/out-of-range index leaks libc and heap pointers from the stack. A separate buffer overflow then uses those disclosures to build a ret2libc call to`system("/bin/sh")` while satisfying an application check that requires the heap address.<sup>[\[4\]](#references)</sup>

## References
