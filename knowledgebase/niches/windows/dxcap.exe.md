---
title: "Dxcap.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Dxcap/
fetched_at: 2026-09-20T17:14:46Z
license: unspecified
category: windows
---

DirectX diagnostics/debugger included with Visual Studio.

## Paths
- C:\Windows\System32\dxcap.exe
- C:\Windows\SysWOW64\dxcap.exe

## Resources
- [https://twitter.com/harr0ey/status/992008180904419328](https://twitter.com/harr0ey/status/992008180904419328)

## Acknowledgements
- Matt harr0ey ([@harr0ey](https://twitter.com/@harr0ey))
- Vikas Singh ([@vikas891](https://twitter.com/@vikas891))
- Naor Evgi ([@ghosts621](https://twitter.com/@ghosts621))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_susp_dxcap.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_susp_dxcap.yml)
- IOC: dxcap.exe executing from outside of System32/SysWOW64
- IOC: dxcap.exe spawning Xperf.exe
- IOC: Xperf.exe executing from unusual directories (if not running from ADK path)

## Execute

1. Launch specified executable as a subprocess of dxcap.exe. Note that you should have write permissions in the current working directory for the command to succeed; alternatively, add ‘-file c:\path\to\writable\location.ext’ as first argument.

```
Dxcap.exe -c {PATH_ABSOLUTE:.exe}
```

   - Use case: Local execution of a process as a subprocess of dxcap.exe

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1127

   - Tags: Execute: EXE

2. Once executed, dxcap.exe will execute xperf.exe in the same folder. Thus, if dxcap.exe is copied to a folder and an arbitrary executable is renamed to xperf.exe, dxcap.exe will spawn it.

```
dxcap.exe -usage
```

   - Use case: Execute an arbitrary executable via trusted system executable.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1127

   - Tags: Execute: EXERequires: Rename
