---
title: Azure SQL databases
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/authenticated-enumeration/azure-sql-databases
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
Connect to database with credentials

```powershell
$conn = New-Object System.Data.SqlClient.SqlConnection
$password='$reporting$123'
$conn.ConnectionString = "Server=XX.database.windows.net;Database=Finance;User ID=financereports;Password=$password;"
$conn.Open()
```

Check tables

```powershell
$sqlcmd = $conn.CreateCommand()
$sqlcmd.Connection = $conn
$query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';"
$sqlcmd.CommandText = $query
$adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
$data = New-Object System.Data.DataSet
$adp.Fill($data) | Out-Null
$data.Tables
```

Get data

```powershell
$sqlcmd = $conn.CreateCommand()
$sqlcmd.Connection = $conn
$query = "SELECT * FROM Subscribers;"
$sqlcmd.CommandText = $query
$adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
$data = New-Object System.Data.DataSet
$adp.Fill($data) | Out-Null
$data.Tables | ft
```
