---
title: "Wlrmdr.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Wlrmdr/
fetched_at: 2026-09-20T17:12:01Z
license: unspecified
category: windows
---

Windows Logon Reminder executable

## Paths
- c:\windows\system32\wlrmdr.exe

## Resources
- [https://twitter.com/0gtweet/status/1493963591745220608](https://twitter.com/0gtweet/status/1493963591745220608)
- [https://twitter.com/Oddvarmoe/status/927437787242090496](https://twitter.com/Oddvarmoe/status/927437787242090496)
- [https://twitter.com/falsneg/status/1461625526640992260](https://twitter.com/falsneg/status/1461625526640992260)
- [https://docs.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-notifyicondataw](https://docs.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-notifyicondataw)

## Acknowledgements
- Grzegorz Tworek ([@0gtweet](https://twitter.com/@0gtweet))
- Oddvar Moe ([@Oddvarmoe](https://twitter.com/@Oddvarmoe))
- Freddy ([@falsneg](https://twitter.com/@falsneg))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_wlrmdr.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_lolbin_wlrmdr.yml)
- IOC: wlrmdr.exe spawning any new processes

## Execute

1. Execute executable with wlrmdr.exe as parent process

```
wlrmdr.exe -s 3600 -f 0 -t _ -m _ -a 11 -u {PATH:.exe}
```

   - Use case: Use wlrmdr as a proxy binary to evade defensive countermeasures

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1202

   - Tags: Execute: EXE
