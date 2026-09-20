---
title: Storage Accounts (database)
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/authenticated-enumeration/storage-accounts-database
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
### List databases

```
az storage account list --query "[].name" -o tsv
```

### Get tables

```
az storage table list --account-name <db-name> --output table --auth-mode login
```

### Get data

```
az storage entity query --table-name <table-name> --account-name <db-name> --output table --auth-mode login
```
