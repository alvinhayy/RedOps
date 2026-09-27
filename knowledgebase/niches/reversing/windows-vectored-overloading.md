---
title: "Windows Vectored Overloading"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/binary-exploitation/windows-vectored-overloading.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: reversing
---

# Vectored Overloading PE Injection

## Technique overview

Vectored Overloading is a **Windows PE injection primitive** that combines classic Module Overloading with **Vectored Exception Handlers (VEHs)** and **hardware breakpoints**. Instead of patching `LoadLibrary` or writing its own loader, the adversary:[\[1\]](#references)[\[4\]](#references)

1. Creates a `SEC_IMAGE` section backed by a legitimate DLL (e.g.,`wmp.dll` ).
2. Overwrites the mapped view with a fully relocated malicious PE but keeps the section object pointing to the benign image on disk.
3. Registers a VEH and programs debug registers so every call to `NtOpenSection` ,`NtMapViewOfSection` , and optionally`NtClose` raises a user-mode breakpoint.
4. Calls `LoadLibrary("amsi.dll")` (or any other benign target). When the Windows loader invokes those syscalls, the VEH**skips the kernel transition** and returns the handles and base addresses of the prepared malicious image.

Because the loader still believes it mapped the requested DLL, tooling that only looks at section backing files sees `wmp.dll` even though memory now contains the attacker’s payload. Meanwhile, imports/TLS callbacks are still resolved by the genuine loader, significantly reducing the amount of custom PE-parsing logic the adversary must maintain.[\[1\]](#references)

## Stage 1 – Build the disguised section

1. **Create and map a section for the decoy DLL**```
NtCreateSection(&DecoySection, SECTION_ALL_ACCESS, NULL,
                0, PAGE_READWRITE, SEC_IMAGE, L"\??\C:\\Windows\\System32\\wmp.dll");
NtMapViewOfSection(DecoySection, GetCurrentProcess(), &DecoyView, 0, 0,
                   NULL, &DecoySize, ViewShare, 0, PAGE_READWRITE);
```
2. **Copy the malicious PE into that view** section by section, honouring`SizeOfRawData` /`VirtualSize` and updating protections afterwards (`PAGE_EXECUTE_READ` ,`PAGE_READWRITE` , etc.).
3. **Apply relocations and resolve imports** exactly as a reflective loader would. Because the view is already mapped as`SEC_IMAGE` , section alignments and guard pages match what the Windows loader expects later.
4. **Normalize the PE header** :
  - If the payload is an EXE, set `IMAGE_FILE_HEADER.Characteristics |= IMAGE_FILE_DLL` and zero the entry point to keep`LdrpCallTlsInitializers` from jumping into EXE-specific stubs.
  - DLL payloads can keep their headers unchanged.
5. If the payload is an EXE, set

At this point the process owns a RWX-capable view whose backing object is still `wmp.dll`, yet the bytes in memory are attacker-controlled.[\[1\]](#references)

## [Stage 2 – Hijack the loader with VEHs](#stage-2--hijack-the-loader-with-vehs)

1. **Register a VEH and arm hardware breakpoints** : program`Dr0` (or another debug register) with the address of`ntdll!NtOpenSection` and set`DR7` so every execution raises`STATUS_SINGLE_STEP` . Repeat later for`NtMapViewOfSection` and optionally`NtClose` .
2. **Trigger DLL loading** with`LoadLibrary("amsi.dll")` .`LdrLoadDll` will eventually call`NtOpenSection` to obtain the real section handle.
3. **VEH hook for `NtOpenSection`** :
  - Locate the stack slot for the `[out] PHANDLE SectionHandle` argument.
  - Write the previously created `DecoySection` handle into that slot.
  - Advance `RIP` /`EIP` to the`ret` instruction so the kernel is never called.
  - Re-arm the hardware breakpoint to watch `NtMapViewOfSection` next.
4. Locate the stack slot for the
5. **VEH hook for `NtMapViewOfSection`** :
  - Overwrite the `[out] PVOID *BaseAddress` (and size/protection outputs) with the address of the already mapped malicious view.
  - Skip the syscall body just like before.
6. Overwrite the
7. **(Optional) VEH hook for `NtClose`** verifies that the fake section handle is cleaned up, preventing resource leaks and providing a final sanity check.

Because the syscalls are never executed, kernel callbacks (ETWti, minifilter, etc.) do not observe the suspicious `NtOpenSection`/`NtMapViewOfSection` events, drastically lowering telemetry. From the loader’s point of view everything succeeded and `amsi.dll` is in memory, so it proceeds with import/TLS resolution against the attacker’s bytes.[\[1\]](#references)

### [PoC implementation notes (2025)](#poc-implementation-notes-2025)

The public PoC shows a few practical details that are easy to miss when re-implementing the technique:[\[2\]](#references)

- **HWBPs are per-thread** . The PoC sets`CONTEXT_DEBUG_REGISTERS` on the**current thread** before calling`LoadLibrary` , so the VEH must run on the same thread that triggers the loader.
- **Syscall emulation** : the VEH sets`RAX = 0` and advances`RIP` to the`ret` inside the`ntdll` stub (it scans for`0xC3` ) so the kernel transition never happens, then resumes with`NtContinue` .
- **Output parameters** : for`NtMapViewOfSection` , the VEH overwrites the returned`BaseAddress` ,`ViewSize` , and`Win32Protect` outputs so the loader believes the mapping succeeded and continues with imports/TLS using the attacker’s view.

Minimal HWBP setup used by the PoC (x64):[\[2\]](#references)

```
CONTEXT ctx = {0};
ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
GetThreadContext(GetCurrentThread(), &ctx);
ctx.Dr0 = (DWORD64)NtOpenSection;
ctx.Dr7 = 1;
SetThreadContext(GetCurrentThread(), &ctx);
AddVectoredExceptionHandler(1, VehHandler);
```
### [Stealth variation](#stealth-variation)

Recent VEH research highlights that handlers can be registered by **manually manipulating the VEH list** instead of calling `AddVectoredExceptionHandler`, which reduces reliance on user-mode APIs that may be monitored or hooked. This is not required for Vectored Overloading but can be combined with it to reduce observable API activity.[\[3\]](#references)

## [Stage 3 – Execute the payload](#stage-3--execute-the-payload)

- **EXE payload** : The injector simply jumps to the original entry point once relocations are done. When the loader thinks it would call`DllMain` , the custom code instead executes the EXE-style entry.
- **DLL payload / Node.js addon** : Resolve and call the intended export (Kidkadi exposes a named function to JavaScript). Because the module is already registered with`LdrpModuleBaseAddressIndex` , subsequent lookups see it as the benign DLL.

When combined with a Node.js native addon (`.node` file), all of the Windows-internals heavy lifting stays outside the JavaScript layer, helping the threat actor ship the same loader with many different obfuscated Node wrappers.[\[1\]](#references)

## [References](#references)

- [1] [Check Point Research – GachiLoader: Defeating Node.js Malware with API Tracing](https://research.checkpoint.com/2025/gachiloader-node-js-malware-with-api-tracing/)
- [2] [VectoredOverloading – PoC implementation](https://github.com/CheckPointSW/VectoredOverloading)
- [3] [IBM X-Force – You just got vectored: Using VEH for defense evasion and process injection](https://www.ibm.com/think/x-force/using-veh-for-defense-evasion-process-injection)
- [4] [Module Overloading proof of concept](https://github.com/hasherezade/module_overloading)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
