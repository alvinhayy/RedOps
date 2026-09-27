---
title: ROADTools
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/authenticated-enumeration/roadtools
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
ROADTools is a tool for enumerating Entra ID environments. It uses different version of API's that provides more information (AADGraph 1.61-internal). Enumeration using RoadRecon includes three steps:

* Authentication
* Data Gathering
* Data Exploration

### Authenticate

We can activate a Python virtual environment to use ROADTools

```powershell
PS C:\Windows\system32> cd C:\AzAD\Tools\ROADTools\
PS C:\AzAD\Tools\ROADTools> .\venv\Scripts\activate
(venv) PS C:\AzAD\Tools\ROADTools> .\roadrecon\^C
(venv) PS C:\AzAD\Tools\ROADTools> roadrecon auth -u test@pp.onmicrosoft.com -p Password123!
Tokens were written to .roadtools_auth
```

Once authentication is done we can gather data

### Gather data

```powershell
roadrecon gather
```

This takes a while (depends if you have a big environment).

### Visualize data

We can use roadrecon to analyze the gathered information through a GUI.&#x20;

```
roadrecon gui
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F5tsLEDd3cHK5kKmYUxRy%2Fimage.png?alt=media&amp;token=096036d3-1375-4c24-bbe3-fe243e9187a1" alt=""><figcaption></figcaption></figure>

### Get conditional access policies

```
roadrecon plugin policies
```

This will write all conditional acccess information to a .html file
