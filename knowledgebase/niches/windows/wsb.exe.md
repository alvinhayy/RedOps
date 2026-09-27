---
title: "wsb.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Wsb/
fetched_at: 2026-09-20T17:15:51Z
license: unspecified
category: windows
---

Windows Sandbox command-line interface. Creates, lists, controls, and executes commands inside Windows Sandbox sessions from the host CLI.

## Paths
- C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\wsb.exe

## Resources
- [https://web.archive.org/web/20250116184008/http://blog.syscall.party/2020/12/02/weaponizing-windows-sandbox.html](https://web.archive.org/web/20250116184008/http://blog.syscall.party/2020/12/02/weaponizing-windows-sandbox.html)
- [https://github.com/LloydLabs/wsb-detect](https://github.com/LloydLabs/wsb-detect)
- [https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-cli](https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-cli)
- [https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-versions](https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-versions)
- [https://github.com/secdev02/SandBoxShenanigans](https://github.com/secdev02/SandBoxShenanigans)

## Acknowledgements
- Konrad 'unrooted' Klawikowski
- Lloyd Davies ([@LloydLabs](https://twitter.com/@LloydLabs))

## Detections
- IOC: wsb.exe command line containing –config with an embedded <LogonCommand> XML element
- IOC: wsb.exe command line invoking the share subcommand with –allow-write
- IOC: wsb.exe command line invoking the exec subcommand with -r System
- IOC: WindowsSandboxServer.exe spawns whenever a Sandbox session starts, regardless of whether anyone connects. Lives under %ProgramFiles%\WindowsApps\MicrosoftWindows.WindowsSandbox_*.
- IOC: WindowsSandboxRemoteSession.exe spawns ONLY when an RDP connection to the Sandbox is established - opening a .wsb file directly auto-connects (so both processes appear), but wsb start alone does NOT spawn it. Its absence while WindowsSandboxServer.exe is alive means no user has connected.
- IOC: (highest-signal for headless abuse) WindowsSandboxServer.exe present WITHOUT WindowsSandboxRemoteSession.exe indicates a Sandbox VM is running with no interactive session. Legitimate usage almost always involves an RDP connection (because users want to use the Sandbox); a server-without-remote-session state is consistent with the wsb exec -r System headless attack primitive.
- IOC: vmwp.exe and vmmemWindowsSandbox spawned alongside wsb.exe activity indicate the Sandbox VM is up (vmwp is the Hyper-V worker hosting the Sandbox VM)
- IOC: Host-side file-creation events on paths corresponding to a mapped folder, attributed to vmwp.exe (Hyper-V worker), with timestamps inside the lifetime of an active Sandbox session - empirically verified on Windows 11 24H2 via Process Monitor; this is how a sandbox-to-host cross-boundary write surfaces from host telemetry
- IOC: Microsoft-Windows-Sandbox-Client-Diagnostics/Admin event log entries for Sandbox lifecycle events correlated with wsb.exe invocations

## Execute

1. Executes the given command in a Windows Sandbox from an inline XML configuration with an embedded <LogonCommand>, leaving no .wsb file on disk. Note: <LogonCommand> only fires once WDAGUtilityAccount actually logs in, which only happens after an RDP session is established via wsb connect, so this pattern opens a visible Sandbox window.

```
wsb start --config "<Configuration><LogonCommand><Command>{CMD}</Command></LogonCommand></Configuration>"
wsb exec -r System --id YOUR_ID
```

   - Use case: Fileless execution of arbitrary commands in an EDR-free environment whose host-side process tree is masked by the Sandbox client binaries.

   - Privileges required: User

   - Operating systems: Windows 11 24H2 and later

   - ATT&CK® technique: T1564.006

   - Tags: Execute: CMD

2. Allows the specified folder to be accessible from within the Windows Sandbox, mounted under C:\users\WDAGUtilityAccount\Desktop with the same folder name as the source folder. This allows, for example, for copying payloads from the host system into the sandbox (seen here), copying payloads from the sandbox back to the host system, or for accessing arbitrary host system files by the sandbox.

```
wsb start --config "<Configuration><MappedFolders><MappedFolder><HostFolder>{PATH_ABSOLUTE:folder}</HostFolder><ReadOnly>false</ReadOnly></MappedFolder></MappedFolders></Configuration>"
wsb exec -r System --id YOUR_ID -c "cmd.exe /c copy C:\users\WDAGUtilityAccount\Desktop\Temp\{PATH} {PATH}"
```

   - Use case: Fileless execution of arbitrary commands in an EDR-free environment, with access to files on the host system, while the host-side process tree is masked by the Sandbox client binaries.

   - Privileges required: User

   - Operating systems: Windows 11 24H2 and later

   - ATT&CK® technique: T1564.006

   - Tags: Execute: CMD

3. Allows the specified folder to be accessible from within the Windows Sandbox, mounted at c:\SOME_FOLDER. This allows, for example, for copying payloads from the host system into the sandbox, copying payloads from the sandbox back to the host system (seen here), or for accessing arbitrary host system files by the sandbox.

```
wsb start
wsb share --id YOUR_ID -f {PATH_ABSOLUTE:folder} -s c:\SOME_FOLDER --allow-write
wsb exec -r System --id YOUR_ID -c "cmd.exe /c copy {PATH_ABSOLUTE} c:\SOME_FOLDER"
```

   - Use case: Fileless execution of arbitrary commands in an EDR-free environment, with access to files on the host system, while the host-side process tree is masked by the Sandbox client binaries.

   - Privileges required: User

   - Operating systems: Windows 11 24H2 and later

   - ATT&CK® technique: T1564.006

   - Tags: Execute: CMD
