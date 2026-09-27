---
title: "vstest.console.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/vstest.console/
fetched_at: 2026-09-20T17:16:02Z
license: unspecified
category: windows
---

VSTest.Console.exe is the command-line tool to run tests

## Paths
- C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\TestWindow\vstest.console.exe
- C:\Program Files (x86)\Microsoft Visual Studio\2022\TestAgent\Common7\IDE\CommonExtensions\Microsoft\TestWindow\vstest.console.exe

## Resources
- [https://learn.microsoft.com/en-us/visualstudio/test/vstest-console-options?view=vs-2022](https://learn.microsoft.com/en-us/visualstudio/test/vstest-console-options?view=vs-2022)

## Acknowledgements
- Onat Uzunyayla
- Ayberk Halac

## Detections
- IOC: vstest.console.exe spawning unexpected processes

## AWL bypass

1. VSTest functionality may allow an adversary to executes their malware by wrapping it as a test method then build it to a .exe or .dll file to be later run by vstest.console.exe. This may both allow AWL bypass or defense bypass in general

```
vstest.console.exe {PATH:.dll}
```

   - Use case: Proxy Execution and AWL bypass, Adversaries may run malicious code embedded inside the test methods of crafted dll/exe

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: DLL
