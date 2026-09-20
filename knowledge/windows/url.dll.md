---
title: "Url.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Url/
fetched_at: 2026-09-20T17:16:26Z
license: unspecified
category: windows
---

Internet Shortcut Shell Extension DLL.

## Paths
- c:\windows\system32\url.dll
- c:\windows\syswow64\url.dll

## Resources
- [https://bohops.com/2018/03/17/abusing-exported-functions-and-exposed-dcom-interfaces-for-pass-thru-command-execution-and-lateral-movement/](https://bohops.com/2018/03/17/abusing-exported-functions-and-exposed-dcom-interfaces-for-pass-thru-command-execution-and-lateral-movement/)
- [https://twitter.com/DissectMalware/status/995348436353470465](https://twitter.com/DissectMalware/status/995348436353470465)
- [https://twitter.com/bohops/status/974043815655956481](https://twitter.com/bohops/status/974043815655956481)
- [https://twitter.com/yeyint_mth/status/997355558070927360](https://twitter.com/yeyint_mth/status/997355558070927360)
- [https://twitter.com/Hexacorn/status/974063407321223168](https://twitter.com/Hexacorn/status/974063407321223168)
- [https://windows10dll.nirsoft.net/url_dll.html](https://windows10dll.nirsoft.net/url_dll.html)

## Acknowledgements
- Adam (OpenURL) ([@hexacorn](https://twitter.com/@hexacorn))
- Jimmy (OpenURL) ([@bohops](https://twitter.com/@bohops))
- Malwrologist (FileProtocolHandler - HTA) ([@DissectMalware](https://twitter.com/@DissectMalware))
- r0lan (Obfuscation) ([@r0lan](https://twitter.com/@r0lan))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)

## Execute

1. Launch a HTML application payload by calling OpenURL.

```
rundll32.exe url.dll,OpenURL {PATH_ABSOLUTE:.hta}
```

   - Use case: Invoke an HTML Application via mshta.exe (Default Handler).

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: HTA

2. Launch an executable payload via proxy through a .url (information) file by calling OpenURL.

```
rundll32.exe url.dll,OpenURL {PATH_ABSOLUTE:.url}
```

   - Use case: Load an executable payload by calling a .url file.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: URL

3. Launch an executable by calling OpenURL.

```
rundll32.exe url.dll,OpenURL file://^C^:^/^W^i^n^d^o^w^s^/^s^y^s^t^e^m^3^2^/^c^a^l^c^.^e^x^e
```

   - Use case: Load an executable payload by specifying the file protocol handler (obfuscated).

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: EXE

4. Launch an executable by calling FileProtocolHandler.

```
rundll32.exe url.dll,FileProtocolHandler {PATH_ABSOLUTE:.exe}
```

   - Use case: Launch an executable.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: EXE

5. Launch an executable by calling FileProtocolHandler.

```
rundll32.exe url.dll,FileProtocolHandler file://^C^:^/^W^i^n^d^o^w^s^/^s^y^s^t^e^m^3^2^/^c^a^l^c^.^e^x^e
```

   - Use case: Load an executable payload by specifying the file protocol handler (obfuscated).

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: EXE

6. Launch a HTML application payload by calling FileProtocolHandler.

```
rundll32.exe url.dll,FileProtocolHandler file:///C:/test/test.hta
```

   - Use case: Invoke an HTML Application via mshta.exe (Default Handler).

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: HTA
