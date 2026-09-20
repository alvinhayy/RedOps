---
title: Azure Services - Application Proxy
source_url: https://github.com/swisskyrepo/InternalAllTheThings/blob/203bb0c0b290bf7c9158c32d43523b8d66f292c1/docs/cloud/azure/azure-services-application-proxy.md
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
## Enumerate

* Enumerate applications that have Proxy

    ```powershell
    PS C:\Tools> Get-AzureADApplication -All $true | %{try{GetAzureADApplicationProxyApplication -ObjectId $_.ObjectID;$_.DisplayName;$_.ObjectID}catch{}}
    PS C:\Tools> Get-AzureADServicePrincipal -All $true | ?{$_.DisplayName -eq "Finance Management System"}

    PS C:\Tools> . C:\Tools\GetApplicationProxyAssignedUsersAndGroups.ps1
    PS C:\Tools> Get-ApplicationProxyAssignedUsersAndGroups -ObjectId <OBJECT-ID>
    ```

## References

* [Training - Attacking and Defending Azure Lab - Altered Security](https://www.alteredsecurity.com/azureadlab)
