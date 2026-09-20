---
title: Azure Services - Application Endpoint
source_url: https://github.com/swisskyrepo/InternalAllTheThings/blob/203bb0c0b290bf7c9158c32d43523b8d66f292c1/docs/cloud/azure/azure-services-application-endpoint.md
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
## Enumerate

* Enumerate possible endpoints for applications starting/ending with PREFIX

    ```powershell
    PS C:\Tools> Get-AzureADServicePrincipal -All $true -Filter "startswith(displayName,'PREFIX')" | % {$_.ReplyUrls}
    PS C:\Tools> Get-AzureADApplication -All $true -Filter "endswith(displayName,'PREFIX')" | Select-Object ReplyUrls,WwwHomePage,HomePage
    ```

## Access

```ps1
https://myapps.microsoft.com/signin/<App ID>?tenantId=<TenantID>
```

## References

* [Training - Attacking and Defending Azure Lab - Altered Security](https://www.alteredsecurity.com/azureadlab)
