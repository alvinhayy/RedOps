---
title: "Sftp.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Sftp/
fetched_at: 2026-09-20T17:11:39Z
license: unspecified
category: windows
---

sftp.exe is a Windows command-line utility that uses the Secure File Transfer Protocol (SFTP) to securely transfer files between a local machine and a remote server.

## Paths
- C:\Windows\System32\OpenSSH\sftp.exe

## Resources
- [https://news.sophos.com/en-us/2025/05/09/lumma-stealer-coming-and-going/](https://news.sophos.com/en-us/2025/05/09/lumma-stealer-coming-and-going/)

## Acknowledgements
- Swachchhanda Shrawan Poudel ([@_swachchhanda_](https://twitter.com/@_swachchhanda_))
- Nir Chako (Pentera) ([@C_h4ck_0](https://twitter.com/@C_h4ck_0))

## Detections
- IOC: sftp.exe executions with ProxyCommand on the command line
- IOC: sftp.exe spawning ssh.exe with ProxyCommand on the command line
- Sigma: [https://github.com/SigmaHQ/sigma/pull/5414/files](https://github.com/SigmaHQ/sigma/pull/5414/files)

## Execute

1. Spawns ssh.exe which in turn spawns the specified command line. See also this project’s entry for ssh.exe.

```
sftp -o ProxyCommand="{CMD}" .
```

   - Use case: Proxy execution of specified command, can be used as a defensive evasion.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD

2. Spawns ssh.exe which in turn spawns the specified command line. See also this project’s entry for ssh.exe.

```
sftp -D "{CMD}"
```

   - Use case: Proxy execution of specified command, can be used as a defensive evasion.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD
