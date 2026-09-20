---
title: "AddinUtil.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Addinutil/
fetched_at: 2026-09-20T17:09:15Z
license: unspecified
category: windows
---

.NET Tool used for updating cache files for Microsoft Office Add-Ins.

## Paths
- C:\Windows\Microsoft.NET\Framework\v4.0.30319\AddinUtil.exe
- C:\Windows\Microsoft.NET\Framework64\v4.0.30319\AddinUtil.exe
- C:\Windows\Microsoft.NET\Framework\v3.5\AddInUtil.exe
- C:\Windows\Microsoft.NET\Framework64\v3.5\AddInUtil.exe

## Resources
- [https://www.blue-prints.blog/content/blog/posts/lolbin/addinutil-lolbas.html](https://www.blue-prints.blog/content/blog/posts/lolbin/addinutil-lolbas.html)

## Acknowledgements
- Michael McKinley ([@MckinleyMike](https://twitter.com/@MckinleyMike))
- Tony Latteri ([@TheLatteri](https://twitter.com/@TheLatteri))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_addinutil_suspicious_cmdline.yml](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_addinutil_suspicious_cmdline.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_addinutil_uncommon_child_process.yml](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_addinutil_uncommon_child_process.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_addinutil_uncommon_cmdline.yml](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_addinutil_uncommon_cmdline.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_addinutil_uncommon_dir_exec.yml](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_addinutil_uncommon_dir_exec.yml)

## Execute

1. AddinUtil is executed from the directory where the ‘Addins.Store’ payload exists, AddinUtil will execute the ‘Addins.Store’ payload.

```
C:\Windows\Microsoft.NET\Framework\v4.0.30319\AddinUtil.exe -AddinRoot:.
```

   - Use case: Proxy execution of malicious serialized payload

   - Privileges required: User

   - Operating systems: Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1218

   - Tags: Execute: .NetObjects
