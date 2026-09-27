---
title: "dtutil.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Dtutil/
fetched_at: 2026-09-20T17:14:42Z
license: unspecified
category: windows
---

Microsoft command line utility used to manage SQL Server Integration Services packages.

## Paths
- C:\Program Files\Microsoft SQL Server\<version>\DTS\Binn\dtutil.exe
- C:\Program Files (x86)\Microsoft SQL Server\<version>\DTS\Binn\dtutil.exe

## Resources
- [https://learn.microsoft.com/en-us/sql/integration-services/dtutil-utility?view=sql-server-ver16](https://learn.microsoft.com/en-us/sql/integration-services/dtutil-utility?view=sql-server-ver16)

## Acknowledgements
- Avihay Eldad ([@AvihayEldad](https://twitter.com/@AvihayEldad))

## Copy

1. Copy file from source to destination

```
dtutil.exe /FILE {PATH_ABSOLUTE:.source.ext} /COPY FILE;{PATH_ABSOLUTE:.dest.ext}
```

   - Use case: Use to copies the source file to the destination file

   - Privileges required: Administrator

   - Operating systems: Windows

   - ATT&CK® technique: T1105
