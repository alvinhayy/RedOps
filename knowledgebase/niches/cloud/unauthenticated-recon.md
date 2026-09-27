---
title: Unauthenticated Recon
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/service-discovery-recon-enumeration-and-initial-access-attacks/unauthenticated-recon
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

With just a e-mail address or domain we can get the following information:

### Get if Azure tenant is in use, tenant name and Federation

```
https://login.microsoftonline.com/getuserrealm.srf?login=%5bUSERNAME@DOMAIN%5d&xml=1
```

### Get tenant ID

```
https://login.microsoftonline.com/[DOMAIN]/.well-known/openid-configuration
```

### Validate Email ID by sending requests

```
https://login.microsoftonline.com/common/GetCredentialType
```

## AADInternals

It is a PS module that you can use for multiple attacks against AzureAD

```powershell
Import-Module AADInternals.psd1 -Verbose
```

### Recon as outsider

```powershell
Invoke-AADIntReconAsOutsider -DomainName pp.onmicrosoft.com
Tenant brand:       Defense Corporation
Tenant name:        pp
Tenant id:          2d50cb29-5f7b-48a4-87ce-fkk49d321
DesktopSSO enabled: False

Name  : pp.onmicrosoft.com
DNS   : True
MX    : True
SPF   : True
DMARC : False
Type  : Managed
STS   :
```

## Check if an email ID belongs to a tenant using o365creeper

```powershell
C:\Python27\python.exe C:\AzAD\Tools\o365creeper\o365creeper.py -f C:\AzAD\Tools\emails.txt
test@pp.onmicrosoft.com - VALID
pp.onmicrosoft.com - INVALID
```

## Check if an email ID belongs to a tenant using omnispray

```
python.exe omnispray.py --type enum -uf ../users.txt --module o365_enum_office
```

## Azure Services Discovery

Azure services are available at specific domains and subdomains. We can enumerate services by finding subdomains.

Example: <https://ppbackup.blob.core.windows.net/>

### MicroBurst

MicroBurst is a useful tool for security assessment for Azure. It uses Az, AzureAD, AzurRM ans MSOL tools and additional REST API calls.

```powershell
Import-Module MicroBurst.psm1
```

Enumerate Subdomains:

```powershell
Invoke-EnumerateAzureSubDomains -Base pp -Verbose
VERBOSE: Found pp.onmicrosoft.com
VERBOSE: Found pp.onmicrosoft.com
VERBOSE: Found pp.onmicrosoft.com
VERBOSE: Found pp.mail.protection.outlook.com
VERBOSE: Found pp.mail.protection.outlook.com
VERBOSE: Found pp.mail.protection.outlook.com
```

## Find subdomains with AzSubEnum

```python
python3 azsubenum.py -b megabigtech --thread 10
```
