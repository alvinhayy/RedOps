---
title: "Shdocvw.dll"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Libraries/Shdocvw/
fetched_at: 2026-09-20T17:16:21Z
license: unspecified
category: windows
---

Shell Doc Object and Control Library.

## Paths
- c:\windows\system32\shdocvw.dll
- c:\windows\syswow64\shdocvw.dll

## Resources
- [http://www.hexacorn.com/blog/2018/03/15/running-programs-via-proxy-jumping-on-a-edr-bypass-trampoline-part-5/](http://www.hexacorn.com/blog/2018/03/15/running-programs-via-proxy-jumping-on-a-edr-bypass-trampoline-part-5/)
- [https://bohops.com/2018/03/17/abusing-exported-functions-and-exposed-dcom-interfaces-for-pass-thru-command-execution-and-lateral-movement/](https://bohops.com/2018/03/17/abusing-exported-functions-and-exposed-dcom-interfaces-for-pass-thru-command-execution-and-lateral-movement/)
- [https://twitter.com/bohops/status/997690405092290561](https://twitter.com/bohops/status/997690405092290561)
- [https://windows10dll.nirsoft.net/shdocvw_dll.html](https://windows10dll.nirsoft.net/shdocvw_dll.html)

## Acknowledgements
- Adam ([@hexacorn](https://twitter.com/@hexacorn))
- Jimmy ([@bohops](https://twitter.com/@bohops))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml](https://github.com/SigmaHQ/sigma/blob/62d4fd26b05f4d81973e7c8e80d7c1a0c6a29d0e/rules/windows/process_creation/proc_creation_win_rundll32_susp_activity.yml)

## Execute

1. Launch an executable payload via proxy through a URL (information) file by calling OpenURL.

```
rundll32.exe shdocvw.dll,OpenURL {PATH_ABSOLUTE:.url}
```

   - Use case: Load an executable payload by calling a .url file with or without quotes. The .url file extension can be renamed.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.011

   - Tags: Execute: URL
