---
title: "Cmdkey.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Cmdkey/
fetched_at: 2026-09-20T17:09:35Z
license: unspecified
category: windows
---

creates, lists, and deletes stored user names and passwords or credentials.

## Paths
- C:\Windows\System32\cmdkey.exe
- C:\Windows\SysWOW64\cmdkey.exe

## Resources
- [https://web.archive.org/web/20230202122017/https://www.peew.pw/blog/2017/11/26/exploring-cmdkey-an-edge-case-for-privilege-escalation](https://web.archive.org/web/20230202122017/https://www.peew.pw/blog/2017/11/26/exploring-cmdkey-an-edge-case-for-privilege-escalation)
- [https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/cmdkey](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/cmdkey)

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_cmdkey_recon.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_cmdkey_recon.yml)

## Credentials

1. List cached credentials

```
cmdkey /list
```

   - Use case: Get credential information from host

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1078
