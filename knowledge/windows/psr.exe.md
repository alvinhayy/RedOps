---
title: "Psr.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Psr/
fetched_at: 2026-09-20T17:11:07Z
license: unspecified
category: windows
---

Windows Problem Steps Recorder, used to record screen and clicks.

## Paths
- c:\windows\system32\psr.exe
- c:\windows\syswow64\psr.exe

## Resources
- [https://social.technet.microsoft.com/wiki/contents/articles/51722.windows-problem-steps-recorder-psr-quick-and-easy-documenting-of-your-steps-and-procedures.aspx](https://social.technet.microsoft.com/wiki/contents/articles/51722.windows-problem-steps-recorder-psr-quick-and-easy-documenting-of-your-steps-and-procedures.aspx)

## Acknowledgements
- Leon Rodenko ([@L3m0nada](https://twitter.com/@L3m0nada))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_psr_capture_screenshots.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_psr_capture_screenshots.yml)
- IOC: psr.exe spawned
- IOC: suspicious activity when running with "/gui 0" flag

## Reconnaissance

1. Record a user screen without creating a GUI. You should use “psr.exe /stop” to stop recording and create output file.

```
psr.exe /start /output {PATH_ABSOLUTE:.zip} /sc 1 /gui 0
```

   - Use case: Can be used to take screenshots of the user environment

   - Privileges required: User

   - Operating systems: since Windows 7 (client) / Windows 2008 R2

   - ATT&CK® technique: T1113
