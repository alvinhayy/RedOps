---
title: "WWW2Exec - __malloc_hook & __free_hook"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/binary-exploitation/arbitrary-write-2-exec/aw2exec-__malloc_hook.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: reversing
---

## **Malloc Hook**

**Malloc Hook**

As you can [Official GNU site](https://www.gnu.org/software/libc/manual/html_node/Hooks-for-Malloc.html), the variable **`__malloc_hook`** is a pointer pointing to the **address of a function that will be called** whenever `malloc()` is called **stored in the data section of the libc library**. Therefore, if this address is overwritten with a **One Gadget** for example and `malloc` is called, the **One Gadget will be called**.[\[1\]](#references)

To call malloc it’s possible to wait for the program to call it or by **calling `printf("%10000$c")`** which allocates too bytes many making `libc` calling malloc to allocate them in the heap.[\[2\]](#references)

More info about One Gadget in:

Warning

Note that hooks are **disabled for GLIBC >= 2.34**. There are other techniques that can be used on modern GLIBC versions. See: [https://github.com/nobodyisnobody/docs/blob/main/code.execution.on.last.libc/README.md](https://github.com/nobodyisnobody/docs/blob/main/code.execution.on.last.libc/README.md).[\[3\]](#references)

## Free Hook

This was abused in one of the example from the page abusing a fast bin attack after having abused an unsorted bin attack:

It’s posisble to find the address of `__free_hook` if the binary has symbols with the following command:

```
gef➤  p &__free_hook
```
[In the post](https://guyinatuxedo.github.io/41-house_of_force/bkp16_cookbook/index.html) you can find a step by step guide on how to locate the address of the free hook without symbols.<sup>[\[4\]](#references)</sup> As summary, in the free function:

```
gef➤  x/20i free
0xf75dedc0
Learn & practice GCP Hacking:
Learn & practice Az Hacking:
Browse the
```
: push   ebx
0xf75dedc1 : call   0xf768f625
0xf75dedc6 : add    ebx,0x14323a
0xf75dedcc :  sub    esp,0x8
0xf75dedcf :  mov    eax,DWORD PTR [ebx-0x98]
0xf75dedd5 :  mov    ecx,DWORD PTR [esp+0x10]
**0xf75dedd9 :  mov    eax,DWORD PTR [eax]--- BREAK HERE
0xf75deddb**
