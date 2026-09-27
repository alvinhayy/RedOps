---
title: "Wsreset.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Wsreset/
fetched_at: 2026-09-20T17:12:06Z
license: unspecified
category: windows
---

Used to reset Windows Store settings according to its manifest file

## Paths
- C:\Windows\System32\wsreset.exe

## Resources
- [https://www.activecyber.us/activelabs/windows-uac-bypass](https://www.activecyber.us/activelabs/windows-uac-bypass)
- [https://twitter.com/ihack4falafel/status/1106644790114947073](https://twitter.com/ihack4falafel/status/1106644790114947073)
- [https://github.com/hfiref0x/UACME/blob/master/README.md](https://github.com/hfiref0x/UACME/blob/master/README.md)

## Acknowledgements
- Hashim Jawad ([@ihack4falafel](https://twitter.com/@ihack4falafel))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_uac_bypass_wsreset_integrity_level.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_uac_bypass_wsreset_integrity_level.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_uac_bypass_wsreset.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_uac_bypass_wsreset.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/registry/registry_event/registry_event_bypass_via_wsreset.yml#](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/registry/registry_event/registry_event_bypass_via_wsreset.yml#)
- Splunk: [https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/wsreset_uac_bypass.yml](https://github.com/splunk/security_content/blob/18f63553a9dc1a34122fa123deae2b2f9b9ea391/detections/endpoint/wsreset_uac_bypass.yml)
- IOC: wsreset.exe launching child process other than mmc.exe
- IOC: Creation or modification of the registry value HKCU\Software\Classes\AppX82a6gwre4fdg3bt635tn5ctqjf8msdd2\Shell\open\command
- IOC: Microsoft Defender Antivirus as Behavior:Win32/UACBypassExp.T!gen

## UAC bypass

1. During startup, wsreset.exe checks the registry value HKCU\Software\Classes\AppX82a6gwre4fdg3bt635tn5ctqjf8msdd2\Shell\open\command for the command to run. Binary will be executed as a high-integrity process without a UAC prompt being displayed to the user.

```
wsreset.exe
```

   - Use case: Execute a binary or script as a high-integrity process without a UAC prompt.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1548.002
