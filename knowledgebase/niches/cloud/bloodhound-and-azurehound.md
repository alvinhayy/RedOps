---
title: "BloodHound & AzureHound"
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/authenticated-enumeration/bloodhound-and-azurehound
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

BloodHound's AzureHound (<https://github.com/SpecterOps/AzureHound>) supports Azure and Entra ID too to map attack paths. It uses AzureAD and Az PowerShell modules for gathering the data through it collectors.

Because READ access to objects is required to even know it's existence, AzureHound is not as interesting as BloodHound

### Get Data

<pre class="language-powershell" data-line-numbers><code class="lang-powershell">$passwd = ConvertTo-SecureString "Password@1234" -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential("test@pp.onmicrosoft.com", $passwd)
<strong>Import-Module AzureAD
</strong><strong>Connect-AzAccount -Credential $creds
</strong>Connect-AzureAD -Credential $creds
. C:\AzAD\Tools\AzureHound\AzureHound.ps1
Invoke-AzureHound -Verbose
</code></pre>

The gathered data can be uploaded to the BloodHound application.

Or from bash:

```bash
./azurehound -u "Jose.Rodriguez@tenant.com" -p "password123!" list --tenant "tenant.com" -o output.json
```

### Visualize data with BloodHound community edition

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FznBVqDeuA2bsJ837fNjy%2Fimage.png?alt=media&amp;token=e893a9ce-0ff0-4951-8bd1-8b288e5506a7" alt=""><figcaption></figcaption></figure>

### Custom AzureHound queries
