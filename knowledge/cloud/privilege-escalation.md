---
title: Privilege Escalation
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/privilege-escalation
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
Some good questions to ask after gaining a foothold with a compromised user are:<br>

* Is the user part of any group? If so, does this group has any role assigned to it?
* Does the user have any Azure Entra ID roles assigned to them?
* Which objects has this user created?
* Is this user the owner of any service principal?
