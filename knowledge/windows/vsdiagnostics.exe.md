---
title: "VSDiagnostics.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/VSDiagnostics/
fetched_at: 2026-09-20T17:15:35Z
license: unspecified
category: windows
---

Command-line tool used for performing diagnostics.

## Paths
- C:\Program Files\Microsoft Visual Studio\2022\Community\Team Tools\DiagnosticsHub\Collector\VSDiagnostics.exe

## Resources
- [https://twitter.com/0xBoku/status/1679200664013135872](https://twitter.com/0xBoku/status/1679200664013135872)

## Acknowledgements
- Bobby Cooke ([@0xBoku](https://twitter.com/@0xBoku))

## Detections
- Sigma: [https://github.com/tsale/Sigma_rules/blob/d5b4a09418edfeeb3a2d654f556d5bca82003cd7/LOL_BINs/VSDiagnostics_LoLBin.yml](https://github.com/tsale/Sigma_rules/blob/d5b4a09418edfeeb3a2d654f556d5bca82003cd7/LOL_BINs/VSDiagnostics_LoLBin.yml)

## Execute

1. Starts a collection session with sessionID 1 and calls kernelbase.CreateProcessW to launch specified executable.

```
VSDiagnostics.exe start 1 /launch:{PATH:.exe}
```

   - Use case: Proxy execution of binary

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE

2. Starts a collection session with sessionID 2 and calls kernelbase.CreateProcessW to launch specified executable. Arguments specified in launchArgs are passed to CreateProcessW.

```
VSDiagnostics.exe start 2 /launch:{PATH:.exe} /launchArgs:"{CMD:args}"
```

   - Use case: Proxy execution of binary with arguments

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: CMD
