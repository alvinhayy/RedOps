---
title: "Msdeploy.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Msdeploy/
fetched_at: 2026-09-20T17:15:03Z
license: unspecified
category: windows
---

Microsoft tool used to deploy Web Applications.

## Paths
- C:\Program Files\IIS\Microsoft Web Deploy V2\msdeploy.exe
- C:\Program Files (x86)\IIS\Microsoft Web Deploy V2\msdeploy.exe
- C:\Program Files\IIS\Microsoft Web Deploy V3\msdeploy.exe
- C:\Program Files (x86)\IIS\Microsoft Web Deploy V3\msdeploy.exe
- C:\Program Files\IIS\Microsoft Web Deploy V4\msdeploy.exe
- C:\Program Files (x86)\IIS\Microsoft Web Deploy V4\msdeploy.exe
- C:\Program Files\IIS\Microsoft Web Deploy V5\msdeploy.exe
- C:\Program Files (x86)\IIS\Microsoft Web Deploy V5\msdeploy.exe

## Resources
- [https://twitter.com/pabraeken/status/995837734379032576](https://twitter.com/pabraeken/status/995837734379032576)
- [https://twitter.com/pabraeken/status/999090532839313408](https://twitter.com/pabraeken/status/999090532839313408)

## Acknowledgements
- Pierre-Alexandre Braeken ([@pabraeken](https://twitter.com/@pabraeken))
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_msdeploy.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_msdeploy.yml)

## Execute

1. Launch .bat file via msdeploy.exe.

```
msdeploy.exe -verb:sync -source:RunCommand -dest:runCommand="{PATH_ABSOLUTE:.bat}"
```

   - Use case: Local execution of batch file using msdeploy.exe.

   - Privileges required: User

   - Operating systems: Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11, Windows Server

   - ATT&CK® technique: T1218

   - Tags: Execute: CMD

2. Launch .bat file via msdeploy.exe.

```
msdeploy.exe -verb:sync -source:RunCommand -dest:runCommand="{PATH_ABSOLUTE:.bat}"
```

   - Use case: Local execution of batch file using msdeploy.exe.

   - Privileges required: User

   - Operating systems: Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11, Windows Server

   - ATT&CK® technique: T1218

   - Tags: Execute: CMD

3. Copy file from source to destination.

```
msdeploy.exe -verb:sync -source:filePath={PATH_ABSOLUTE:.source.ext} -dest:filePath={PATH_ABSOLUTE:.dest.ext}
```

   - Use case: Copy file.

   - Privileges required: User

   - Operating systems: Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11, Windows Server

   - ATT&CK® technique: T1105
