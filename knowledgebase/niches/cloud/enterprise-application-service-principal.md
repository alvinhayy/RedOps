---
title: Enterprise Application / Service Principal
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/privilege-escalation/enterprise-application-service-principal
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

When we create/register a new application with a secret, redirect uri ETC. It's called a "application" but when a user **consents** to this application, a new "enterprise application" is created automatically with the same name as the application. This is called a **service principal**.

A service principal is the part can can be used, role assignment, permissions, etc.

Also, conditional access can be implemented on enterprise applications/service principals. Since you will need a extra subscription to protect these workload identities, it is very likely that MFA is enforced on these. This is why we are interested in obtaining access to a enterprise application.

### Authenticating with a App secret

When we know a app's secret from the application registration, we can authenticate as the SPN using:

```powershell
$password = ConvertTo-SecureString 'APP-SECRET' -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential('APP-ID', $password)

Connect-AzAccount -ServicePrincipal -Credential $creds -Tenant TENANT-ID
```
