---
title: "SQLToolsPS.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Sqltoolsps/
fetched_at: 2026-09-20T17:15:26Z
license: unspecified
category: windows
---

Tool included with Microsoft SQL that loads SQL Server cmdlts. A replacement for sqlps.exe. Successor to sqlps.exe in SQL Server 2016+.

## Paths
- C:\Program files (x86)\Microsoft SQL Server\130\Tools\Binn\sqlps.exe

## Resources
- [https://twitter.com/pabraeken/status/993298228840992768](https://twitter.com/pabraeken/status/993298228840992768)
- [https://docs.microsoft.com/en-us/sql/powershell/sql-server-powershell?view=sql-server-2017](https://docs.microsoft.com/en-us/sql/powershell/sql-server-powershell?view=sql-server-2017)

## Acknowledgements
- Pierre-Alexandre Braeken ([@pabraeken](https://twitter.com/@pabraeken))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_mssql_sqltoolsps_susp_execution.yml](https://github.com/SigmaHQ/sigma/blob/683b63f8184b93c9564c4310d10c571cbe367e1e/rules/windows/process_creation/proc_creation_win_mssql_sqltoolsps_susp_execution.yml)
- Splunk: [https://github.com/splunk/security_content/blob/aa9f7e0d13a61626c69367290ed1b7b71d1281fd/docs/_posts/2021-10-05-suspicious_copy_on_system32.md](https://github.com/splunk/security_content/blob/aa9f7e0d13a61626c69367290ed1b7b71d1281fd/docs/_posts/2021-10-05-suspicious_copy_on_system32.md)

## Execute

1. Run a SQL Server PowerShell mini-console without Module and ScriptBlock Logging.

```
SQLToolsPS.exe -noprofile -command Start-Process {PATH:.exe}
```

   - Use case: Execute PowerShell command.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1218

   - Tags: Execute: PowerShell
