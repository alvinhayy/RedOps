---
title: Linux binaries
source_url: https://notes.incendium.rocks/pentesting-notes/reversing/linux-binaries
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: reversing
---

## Strace

In the simplest case strace runs the specified command until it exits. It intercepts and records the system calls which are called by a process and the signals which are received by a process.

**Strace a running process**

```
strace -p [pid]
```

**Strace a program**

```
strace ./program [arguments]
```

**Strace a program and threads**

```
strace -f ./program [arguments]
```

## Ltrace

**ltrace** is a program that simply runs the specified command until it exits. It intercepts and records the dynamic library calls which are called by the executed process and the signals which are received by that process.

```
ltrace ./program
```

## Strings

Classic, but OP. You can run strings on binaries to print all 'strings' in a file:

```
strings ./program
```

## Ghidra

Time to read some code.&#x20;

Ghidra is a software reverse engineering (SRE) framework created and maintained by the [National Security Agency](https://www.nsa.gov) Research Directorate.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FfzTz7XP9IzJ1P7nJmiYq%2F1%209N3SURf2cF4fISICAH7tGA.png?alt=media&amp;token=2765face-dc81-42a4-922e-9b0e3a06fd98" alt=""><figcaption></figcaption></figure>
