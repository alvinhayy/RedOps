---
title: Azure Blob Storage
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/service-discovery-recon-enumeration-and-initial-access-attacks/azure-blob-storage
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

Blob storage is used to store unstructured data (like filed, videos, audio, etc). There are three types of resources in blob storage:

1. Storage account - Unique namespace across Azure (can be accessed over HTTP and HTTPS)
2. Container in the storage account (may be multiple in a storage account) also known as the 'Folders' in the storage account
3. Blob in a container - Stores data. Three types of blobs - Block, append and page blobs.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FBhWEkE74o4H1VcEGigvi%2Fblob1.png?alt=media&amp;token=5d1f9f73-04ae-4333-860a-ce645349c7fc" alt=""><figcaption></figcaption></figure>

### Storage account endpoints

A storage account has globally unique endpoints. It is very useful in enumeration too by guessing the storage account names:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F3A7IYNpVl4lWb90IYOUg%2Fimage.png?alt=media&amp;token=17ba50b4-50ab-45c3-afc6-41ffed98d541" alt=""><figcaption></figcaption></figure>

### Storage Account Access

Storage Accounts support RBAC. For example the 'Storage Blob Data Reader' role allows a identity to read the data inside the storage account. Other than that, storage accounts support `Access keys`.

Access keys are not rotated by default

### Anonymous access

By default, anonymous access is not allowed for storage accounts. However, if enabled, this allows read access to blobs or even containers to the public. We can enumerate these using Microbust:

```powershell
Invoke-EnumerateAzureBlobs -Base x
Found Storage Account -  xcodebackup.blob.core.windows.net
Found Storage Account -  xcommon.blob.core.windows.net
```

If you have found a container that allows you to list blobs (files), you can list those files using:

```
https://xcommon.blob.core.windows.net/backup?restype=container&comp=list
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FEXYrGTOz5kJn3x6Jct44%2Fimage.png?alt=media&amp;token=ee2564f0-1ab4-4ef4-817a-3fbc8d8286bb" alt=""><figcaption></figcaption></figure>

It contains a blob called "blob\_client.py", to access the file we can go to

```
https://xcommon.blob.core.windows.net/backup/blob_client.py
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FjoLK1a0Z0VmIaH9IDCah%2Fimage.png?alt=media&amp;token=18d2db96-4373-4496-9b35-96c61ded8ad9" alt=""><figcaption></figcaption></figure>

Check for interesting secrets that allow access to other storage accounts

If it contains a `SAS`url, we can use Azure Storage Explorer to connect to that container:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FZYeoyJy3klt8RL6jJk76%2Fimage.png?alt=media&amp;token=1f591722-6b87-4da2-958e-cf917f9640fd" alt=""><figcaption></figcaption></figure>

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FBZyDTS8cNikgwfJ5xGnP%2Fimage.png?alt=media&amp;token=f8604ab3-e5cd-4a6d-ac0d-0ea8bf6cdceb" alt=""><figcaption></figcaption></figure>

### Storage Container

Get containers context

```powershell
Get-AzStorageContainer -Context (New-AzStorageContext -StorageAccountName defcorpcodebackup)
```

### Versioning

Maybe there are deleted files that we can recover. We can check for versioning using curl:

```sh
curl -H "x-ms-version: 2019-12-12" 'https://XXXX.blob.core.windows.net/RESOURCE?restype=container&comp=list&include=versions' | xmllint --format - | less
```

Note that we include the `x-ms-version`as header because else this is not supported by Azure. If there are any hits download the file using curl:

```sh
curl -H "x-ms-version: 2019-12-12" 'https://XXXX.blob.core.windows.net/RESOURCE/myzip.zip?versionId=2024-03-29T20:55:40.8265593Z'  -o myzip.zip
```
