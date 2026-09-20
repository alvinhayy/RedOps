---
title: Application Proxy
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/lateral-movement/application-proxy
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
Application Proxies allow access to on-prem web applications after sign-in to Entra ID. They have the following components:

* Endpoint; external URL that the users browse to access the on-prem application. External users must authenticate to AAD
* Application proxy service. This service runs in the cloud and passes the token provided by Entra ID to the on-prem connector
* Application Proxy Connector - Agent that runs on the on-prem infra and acts as a communication agent between the cloud proxy service and on-prem app.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FBgrSTFuXPzfWHLT7dewl%2Fazureappproxxy_hu0e2704d3d39a37a92e2cc48ef40136a9_94161_660x0_resize_box_3.png?alt=media&amp;token=84edc085-64e6-4425-a5a9-75aec6b68336" alt=""><figcaption></figcaption></figure>

### Enumerate Application Proxies

```powershell
. .\Get-MgApplicationProxyApplication.ps1
[+] Access token retrieved successfully.
Retrieving applications from Microsoft Graph...
[+] Successfully retrieved applications.

Application Proxy used by application: 'Finance Management System'
External URL: https://fms-defcorphq.msappproxy.net/
Internal URL: http://deffin-appproxy/
External Authentication Type: aadPreAuthentication
```

Script:

{% code title="Get-MgApplicationProxyApplication.ps1" lineNumbers="true" %}

```powershell
# This script is a part of Attacking and Defending Azure - Beginner's Edition course by Altered Security
# https://www.alteredsecurity.com/azureadlab

$token = (Get-AzAccessToken -ResourceUrl "https://graph.microsoft.com/").Token

if (-not $token) {
    Write-Host "[+] Failed to retrieve access token." -ForegroundColor Red
    exit
} else {
    Write-Host "[+] Access token retrieved successfully." -ForegroundColor Green
}

$applicationsUrl = "https://graph.microsoft.com/beta/applications"

Write-Host "Retrieving applications from Microsoft Graph..." -ForegroundColor Cyan
$applications = Invoke-RestMethod -Uri $applicationsUrl -Headers @{ Authorization = "Bearer $token" }

if (-not $applications) {
	Write-Host "[-] No applications found or failed to retrieve applications." -ForegroundColor Red
    exit
} else {
    Write-Host "[+] Successfully retrieved applications." -ForegroundColor Green
}

foreach ($application in $applications.value) {
    $objectId = $application.id
    $displayName = $application.displayName

    try {
        $proxyUrl = "$applicationsUrl/$objectId/onPremisesPublishing"

        $proxyDetail = Invoke-RestMethod -Uri $proxyUrl -Method Get -Headers @{ Authorization = "Bearer $token" }

        if ($proxyDetail) {
			Write-Host ""
            Write-Host "Application Proxy used by application: '$displayName'" -ForegroundColor White
            Write-Host "External URL: $($proxyDetail.externalUrl)" -ForegroundColor White
            Write-Host "Internal URL: $($proxyDetail.internalUrl)" -ForegroundColor White
            Write-Host "External Authentication Type: $($proxyDetail.externalAuthenticationType)" -ForegroundColor White
        } else {
        }
    } catch {
    }
}
```

{% endcode %}

### Vulnerabilities

Most applications behind a proxy are most-likely old or important applications. Web vulnerabilities do not magically go away, so if there is such a vulnerability in the web-app, it may be exploited.
