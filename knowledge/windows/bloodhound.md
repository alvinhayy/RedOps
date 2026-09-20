---
title: Bloodhound
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/tools/bloodhound
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fe7y9RDe9I6CsSQzNjCSh%2Fbloodhound.png?alt=media&amp;token=5e6845fb-fc56-4589-b24b-7e4c37bc52a0" alt=""><figcaption></figcaption></figure>

BloodHound uses graph theory to reveal the hidden and often unintended relationships within an Active Directory environment. As of version 4.0, BloodHound now also supports Azure. Attackers can use BloodHound to easily identify highly complex attack paths that would otherwise be impossible to quickly identify. Defenders can use BloodHound to identify and eliminate those same attack paths. Both blue and red teams can use BloodHound to easily gain a deeper understanding of privilege relationships in an Active Directory environment.

<https://bloodhound.readthedocs.io/en/latest/index.html>

***

Download [AzureHound](https://github.com/BloodHoundAD/AzureHound/releases) and/or [SharpHound](https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors) to collect your first data set.

```jsx
C:\> SharpHound.exe or SharpHound.ps1
```

Collecting your first data set with AzureHound:

```jsx
PS C:\> Import-Module Az
PS C:\> Import-Module AzureADPreview
PS C:\> Connect-AzureAD
PS C:\> Connect-AzAccount
PS C:\> . .\AzureHound.ps1
PS C:\> Invoke-AzureHound
```

Invoking SharpHound:

```jsx
SharpHound.ps1
```

Next Invoking bloodhound and actually getting data from the node

```bash
Invoke-Bloodhound -CollectionMethod All -Domain CONTROLLER.local -ZipFileName loot.zip
```

Now we can import the data in BloodHound and see some interesting results, for example the shortest path to domain admin

## Running bloodhound-python:

```python
bloodhound-python -d blackfield.local -u support -p 'password' -ns 10.10.10.192 -c All
```

## Custom queries

* Get more info from bloodhound by using custom queries
