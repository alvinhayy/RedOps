---
title: "Netsh.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Netsh/
fetched_at: 2026-09-20T17:10:50Z
license: unspecified
category: windows
---

Netsh is a Windows tool used to manipulate network interface settings.

## Paths
- C:\WINDOWS\System32\Netsh.exe
- C:\WINDOWS\SysWOW64\Netsh.exe

## Resources
- [https://freddiebarrsmith.com/trix/trix.html](https://freddiebarrsmith.com/trix/trix.html)
- [https://htmlpreview.github.io/?https://github.com/MatthewDemaske/blogbackup/blob/master/netshell.html](https://htmlpreview.github.io/?https://github.com/MatthewDemaske/blogbackup/blob/master/netshell.html)
- [https://liberty-shell.com/sec/2018/07/28/netshlep/](https://liberty-shell.com/sec/2018/07/28/netshlep/)

## Acknowledgements
- Freddie Barr-Smith
- Riccardo Spolaor
- Mariano Graziano
- Xabier Ugarte-Pedrero

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_netsh_helper_dll_persistence.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_netsh_helper_dll_persistence.yml)
- Splunk: [https://github.com/splunk/security_content/blob/2b87b26bdc2a84b65b1355ffbd5174bdbdb1879c/detections/endpoint/processes_launching_netsh.yml](https://github.com/splunk/security_content/blob/2b87b26bdc2a84b65b1355ffbd5174bdbdb1879c/detections/endpoint/processes_launching_netsh.yml)
- Splunk: [https://github.com/splunk/security_content/blob/08ed88bd88259c03c771c30170d2934ed0a8f878/detections/deprecated/processes_created_by_netsh.yml](https://github.com/splunk/security_content/blob/08ed88bd88259c03c771c30170d2934ed0a8f878/detections/deprecated/processes_created_by_netsh.yml)
- IOC: Netsh initiating a network connection

## Execute

1. Use Netsh in order to execute a .dll file and also gain persistence, every time the netsh command is called

```
netsh.exe add helper {PATH_ABSOLUTE:.dll}
```

   - Use case: Proxy execution of .dll

   - Privileges required: Admin

   - Operating systems: Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1546.007

   - Tags: Execute: DLL
