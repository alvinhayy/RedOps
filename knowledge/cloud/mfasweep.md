---
title: MFASweep
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/authenticated-enumeration/mfasweep
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

MFASweep is a PowerShell script that attempts to log in to various Microsoft services using a provided set of credentials and will attempt to identify if MFA is enabled. Depending on how conditional access policies and other multi-factor authentication settings are configured some protocols may end up being left single factor. It also has an additional check for ADFS configurations and can attempt to log in to the on-prem ADFS server if detected.

```powershell
invoke-mfasweep -username {{user_email}} -password {{user_password}} -Recon -IncludeADFS
```

Example output:

```
---------------- ADFS Authentication ----------------
[*] Getting ADFS URL...
[*] ADFS does not appear to be in use. Authentication appears to be managed by Microsoft.
[*] Authenticating to On-Prem ADFS Portal at:
######### SINGLE FACTOR ACCESS RESULTS #########
Microsoft Graph API                  | YES
Microsoft Service Management API     | YES
M365 w/ Windows UA                   | NO
M365 w/ Linux UA                     | NO
M365 w/ MacOS UA                     | NO
M365 w/ Android UA                   | NO
M365 w/ iPhone UA                    | NO
M365 w/ Windows Phone UA             | NO
Exchange Web Services (BASIC Auth)   | NO
Active Sync (BASIC Auth)             | NO
ADFS                                 | NO
```

Microsoft 365 applications such as Outlook, Teams and SharePoint rely on the Graph API, and this could allow us to enumerate and exfiltrate user generated content that might be useful to our engagement objectives.
