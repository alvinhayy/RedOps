---
title: "Conhost.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Conhost/
fetched_at: 2026-09-20T17:09:43Z
license: unspecified
category: windows
---

Console Window host

## Paths
- c:\windows\system32\conhost.exe

## Resources
- [https://www.hexacorn.com/blog/2020/05/25/how-to-con-your-host/](https://www.hexacorn.com/blog/2020/05/25/how-to-con-your-host/)
- [https://twitter.com/Wietze/status/1511397781159751680](https://twitter.com/Wietze/status/1511397781159751680)
- [https://twitter.com/embee_research/status/1559410767564181504](https://twitter.com/embee_research/status/1559410767564181504)
- [https://twitter.com/ankit_anubhav/status/1561683123816972288](https://twitter.com/ankit_anubhav/status/1561683123816972288)

## Acknowledgements
- Adam ([@hexacorn](https://twitter.com/@hexacorn))
- Wietze ([@wietze](https://twitter.com/@wietze))

## Detections
- IOC: conhost.exe spawning unexpected processes
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_conhost_susp_child_process.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_conhost_susp_child_process.yml)

## Execute

1. Execute a command line with conhost.exe as parent process

```
conhost.exe {CMD}
```

   - Use case: Use conhost.exe as a proxy binary to evade defensive counter-measures

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD

2. Execute a command line with conhost.exe as parent process

```
conhost.exe --headless {CMD}
```

   - Use case: Specify –headless parameter to hide child process window (if applicable)

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD
