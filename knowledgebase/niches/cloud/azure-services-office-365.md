---
title: Azure Services - Office 365
source_url: https://github.com/swisskyrepo/InternalAllTheThings/blob/203bb0c0b290bf7c9158c32d43523b8d66f292c1/docs/cloud/azure/azure-services-office-365.md
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
## Microsoft Teams Messages

```ps1
TokenTacticsV2> RefreshTo-MSTeamsToken -domain domain.local
AADInternals> Get-AADIntTeamsMessages -AccessToken $MSTeamsToken.access_token | Format-Table id,content,deletiontime,*type*,DisplayName
```

## Outlook Mails

* Read user mails

    ```ps1
    Get-MgUserMessage -UserId <user-id> | ft
    Get-MgUserMessageContent -OutFile mail.txt -UserId <user-id> -MessageId <message-id>
    ```

## OneDrive Files

```ps1
$userId = "<user-id>"
Import-Module Microsoft.Graph.Files
Get-MgUserDefaultDrive -UserId $userId
Get-MgUserDrive -UserId $UserId  -Debug
Get-MgDrive -top 1
```

## References

* [Pentesting Azure Mindmap - Alexis Danizan](https://github.com/synacktiv/Mindmaps)
* [Training - Attacking and Defending Azure Lab - Altered Security](https://www.alteredsecurity.com/azureadlab)
