---
title: "Bcp.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Bcp/
fetched_at: 2026-09-20T17:14:25Z
license: unspecified
category: windows
---

Microsoft SQL Server Bulk Copy Program utility for importing and exporting data between SQL Server instances and data files.

## Paths
- C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\bcp.exe
- C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\130\Tools\Binn\bcp.exe
- C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\110\Tools\Binn\bcp.exe
- C:\Program Files (x86)\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\bcp.exe
- C:\Program Files (x86)\Microsoft SQL Server\Client SDK\ODBC\130\Tools\Binn\bcp.exe
- C:\Program Files (x86)\Microsoft SQL Server\Client SDK\ODBC\110\Tools\Binn\bcp.exe
- C:\Program Files (x86)\Microsoft SQL Server\120\Tools\Binn\bcp.exe

## Resources
- [https://docs.microsoft.com/en-us/sql/tools/bcp-utility](https://docs.microsoft.com/en-us/sql/tools/bcp-utility)
- [https://asec.ahnlab.com/en/61000/](https://asec.ahnlab.com/en/61000/)
- [https://asec.ahnlab.com/en/78944/](https://asec.ahnlab.com/en/78944/)
- [https://www.huntress.com/blog/attacking-mssql-servers](https://www.huntress.com/blog/attacking-mssql-servers)
- [https://www.huntress.com/blog/attacking-mssql-servers-pt-ii](https://www.huntress.com/blog/attacking-mssql-servers-pt-ii)
- [https://news.sophos.com/en-us/2024/08/07/sophos-mdr-hunt-tracks-mimic-ransomware-campaign-against-organizations-in-india/](https://news.sophos.com/en-us/2024/08/07/sophos-mdr-hunt-tracks-mimic-ransomware-campaign-against-organizations-in-india/)
- [https://research.nccgroup.com/2018/03/10/apt15-is-alive-and-strong-an-analysis-of-royalcli-and-royaldns/](https://research.nccgroup.com/2018/03/10/apt15-is-alive-and-strong-an-analysis-of-royalcli-and-royaldns/)

## Acknowledgements
- Mahir Ali Khan ([@mahiralikhan07](https://twitter.com/@mahiralikhan07))

## Detections
- IOC: Process creation of bcp.exe with queryout or Out parameter
- IOC: bcp.exe writing executable files to temp or users directories
- IOC: Network connections from bcp.exe to SQL Server followed by file creation
- IOC: Event ID 4688 - Process creation for bcp.exe
- IOC: Event ID 4663 - File system access by bcp.exe
- Sigma: [https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_bcp_export_data.yml](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_bcp_export_data.yml)

## Download

1. Export binary payload stored in SQL Server database to file system.

```
bcp "SELECT payload_data FROM database.dbo.payloads WHERE id=1" queryout "C:\Windows\Temp\payload.exe" -S localhost -T -c
```

   - Use case: Extract malicious executable from database storage to local file system for execution.

   - Privileges required: User

   - Operating systems: Windows

   - ATT&CK® technique: T1105
