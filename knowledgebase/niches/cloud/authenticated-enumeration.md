---
title: Authenticated Enumeration
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/authenticated-enumeration
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

## Microsoft Graph Module

### Connect to MS Graph

Login pop-up

```powershell
Connect-MgGraph
```

Use token

<pre class="language-powershell"><code class="lang-powershell"><strong>$Token = eyJ0
</strong><strong>Connect-MgGraph -AccessToken ($Token | ConvertTo-SecureString -AsPlainText -Force)
</strong></code></pre>

### Get a Token

```powershell
$passwd = ConvertTo-SecureString "Password123!" -AsPlainText -Force
$creds =  New-Object System.management.automation.pscredential ("test@pp.onmicrosoft.com", $passwd)
Connect-AzAccount -Credential $creds
$Token = (Get-AzAccessToken -ResourceTypeName MSGraph).token
$token
```

Simple script to automate process

```powershell
# Prompt for Email
$email = Read-Host "Enter your email address"

# Prompt for Password (input is hidden)
$password = Read-Host "Enter your password" -AsSecureString

# Create a PSCredential object
$creds = New-Object System.Management.Automation.PSCredential ($email, $password)

# Connect to Azure Account
Connect-AzAccount -Credential $creds

# Get the Access Token for MSGraph
$Token = (Get-AzAccessToken -ResourceTypeName MSGraph).Token

# Output the token (optional)
Write-Host "Access Token for Mg-Graph:" $Token
```

### Users

Enumerate all users

```powershell
Get-MgUser -All
```

Enumerate specific user

```powershell
Get-MgUser -UserId test@pp.onmicrosoft.com
```

Search for users who contain the word "admin" in their Display name:

```powershell
Get-MgUser -Search '"DisplayName:admin"' -ConsistencyLevel eventual
```

All users who are synced from on-prem:

```powershell
Get-MgUser -All | ?{$_.OnPremisesSecurityIdentifier -ne $null}
```

Objects owned by a specific user:

```powershell
Get-MgUserOwnedObject -UserId test@pp.onmicrosoft.com | fl *
```

If a normal user owns a object with a sensitive role such as "Global Administrator', the normal user is indirectly a GA as well!

### Groups

Get goups and roles where specified user is a member of

```powershell
PS C:\Windows\system32> $RoleId = (Get-MgDirectoryRole -Filter "DisplayName eq 'Global Administrator'").Id
(Get-MgDirectoryRoleMember -DirectoryRoleId $RoleId).AdditionalProperties
Key                          Value
---                          -----
@odata.type                  #microsoft.graph.group
creationOptions              {}
groupTypes                   {}
proxyAddresses               {}
resourceBehaviorOptions      {}
resourceProvisioningOptions  {}
onPremisesProvisioningErrors {}
serviceProvisioningErrors    {}
@odata.type                  #microsoft.graph.group
creationOptions              {}
groupTypes                   {}
proxyAddresses               {}
resourceBehaviorOptions      {}
resourceProvisioningOptions  {}
onPremisesProvisioningErrors {}
serviceProvisioningErrors    {}
```

Get Members of a group:

```powershell
Get-AzADGroupMember -GroupDisplayName 'Name' | select DisplayName
```

### Roles

Get all available role templates

```
Get-MgDirectoryRoleTemplate
```

Get users who have a specific role such as Global Administrator:

```powershell
$RoleId = (Get-MgDirectoryRole -Filter "DisplayName eq 'Global Administrator'").Id
(Get-MgDirectoryRoleMember -DirectoryRoleId $RoleId).AdditionalProperties
```

User assigned roles:

```powershell
$userEmail = "yuki.tanaka@megabigtech.com"
$user = Get-MgUser -Filter "userPrincipalName eq '$userEmail'"

$directoryRoles = Get-MgDirectoryRole

$userRoleNames = @()

foreach ($role in $directoryRoles) {
    $members = Get-MgDirectoryRoleMember -DirectoryRoleId $role.Id
    if ($members.Id -contains $user.Id) {
        $userRoleNames += $role.DisplayName
    }
}

$userRoleNames
```

### Devices

List owners of all the devices

```powershell
(Get-MgUserOwnedDevice -userId pp@pp.onmicrosoft.com).AdditionalProperties
```

List devices registered by a user

```powershell
(Get-MgUserRegisteredDevice -userId pp@pp.onmicrosoft.com).AdditionalProperties
```

List devices managed using Intune

```powershell
Get-MgDevice -All| ?{$_.IsCompliant -eq "True"} | fl *
```

### Applications (Registered Applications)

Get all applications objects registered with the current tenant

```powershell
Get-MgApplication -All
```

The `Get-MgApplication` will show all the applications details including password but password value is not shown. List all the apps with an application password&#x20;

```powershell
Get-MgApplication -All| ?{$_.PasswordCredentials -ne $null}
```

### Service Principals (Enterprise Applications)

Get All Service Principals:

```powershell
Get-MgServicePrincipal -all
```

Via Graph token:

```powershell
$RequestParams = @{Method = 'GET'; Uri = $URI; Headers = @{'Authorization' = "Bearer $graphtoken"}}; (Invoke-RestMethod @RequestParams).value
```

### Administrative Unit

Get the administrative units:

```powershell
Get-MgDirectoryAdministrativeUnit
```

Get the scoped role member:

```powershell
Get-MgDirectoryAdministrativeUnitScopedRoleMember
```

Get Role ID

```powershell
(Get-MgDirectoryAdministrativeUnitScopedRoleMember -AdministrativeunitId <ID>).RoleMemberInfo
```

### Get M365 license

```powershell
Get-MgUserLicenseDetail -UserId "Clara.Miller@megabigtech.com"

Id                                          SkuId                                SkuPartNumber
--                                          -----                                -------------
xxx 3b555118-da6a-4418-894f-7df1e2096870 O365_BUSINESS_ESSENTIALS
```

## Az PowerShell

A module from Microsoft for managing Azure resources.

```powershell
Install-Module Az
```

Connect to Entra ID first:

```powershell
Connect-AzAccount
```

Using credentials from Command Line

```powershell
$creds = Get-Credential
Connect-AzAccount -Credential $creds
```

Or:

```powershell
$passwd = ConvertTo-SecureString "password123!" -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential ("test@pp.onmicrosoft.com", $passwd)
Connect-AzAccount -Credential $creds
```

Or use a token:

```
Connect-AzAccount -AccessToken $token -AccountID <account_id>
```

### General context

Get information about the current context:

```powershell
Get-AzContext
```

List all available contexts

```powershell
Get-AzContext -ListAvailable
```

Enumerate all resources visible to the current user:

```powershell
Get-AzResource
```

Enumerate all Azure RBAC role assignments

```powershell
Get-AzRoleAssignment

Get-AzRoleAssignment | Select-Object DisplayName, RoleDefinitionName
```

### VMs

Get all VMs that our context can READ:

```powershell
Get-AzVM | fl
```

### App Registrations

```powershell
Get-AzWebApp
```

### Storage Accounts

```powershell
Get-AzStorageAccount | fl
```

### Key Vaults

```powershell
Get-AzKeyVault
```

### Automated script

{% code title="enum.ps1" lineNumbers="true" %}

```powershell
# Usage: .\enum.ps1 -u <email> -p <password>
# Or use Access Token: .\enum.ps1 -accesstoken <token>
e
param (
    [string]$u,
    [string]$p,
    [string]$accesstoken,
    [string]$accountid
)

function Authenticate-WithCredentials {
    param (
        [string]$Email,
        [string]$Password
    )

    # Convert password to SecureString
    $SecurePassword = ConvertTo-SecureString $Password -AsPlainText -Force

    # Create a PSCredential object
    $creds = New-Object System.Management.Automation.PSCredential ($Email, $SecurePassword)

    # Connect to Azure Account
    Connect-AzAccount -Credential $creds

    # Get the Access Token for MSGraph
    $Token = (Get-AzAccessToken -ResourceTypeName MSGraph).Token

    return $Token
}

# Function to authenticate using an existing access token
function Authenticate-WithToken {
    param (
        [string]$AccessToken
    )
    if (-not $AccessToken) {
        Write-Host "No access token provided. Exiting..." -ForegroundColor Red
        exit
    }
    Write-Host "Using provided access token." -ForegroundColor Green
    Connect-AzAccount -AccessToken $AccessToken -AccountId $accountid
    $Token = (Get-AzAccessToken -ResourceTypeName MSGraph).Token
    return $Token
}

if ($u -and $p) {
    $Token = Authenticate-WithCredentials -Email $u -Password $p
} elseif ($accesstoken) {
    $Token = Authenticate-WithToken -AccessToken $accesstoken
} else {
    Write-Host "Invalid selection. Provide either -u and -p for credentials or -accesstoken for token authentication. Exiting..." -ForegroundColor Red
    exit
}

# If authenticated, enumerate
if ($Token) {
    Write-Host "[+] Successfully authenticated" -ForegroundColor green

    if ($u -and $p) {
    # copy access token to clipboard
    (Get-AzAccessToken -ResourceTypeName MSGraph).Token | clip
    Write-Host "[+] Copied Access Token for $u to clipboard" -ForegroundColor Green
    }

    Write-Host "[+] Getting authenticated context" -ForegroundColor Green
    Get-AzContext | Format-List *

    Write-Host "[+] Getting Role Assignments" -ForegroundColor Green
    Get-AzRoleAssignment | Select-Object DisplayName, RoleDefinitionName, ObjectId | Format-Table -AutoSize

    Write-Host "[+] Getting Resources" -ForegroundColor Green
    Get-AzResource | Select-Object Name, ResourceGroupName | Format-Table -AutoSize

    Write-Host "[+] Getting Key Vaults" -ForegroundColor Green
    Get-AzKeyVault | Select-Object VaultName, ResourceGroupName | Format-Table -AutoSize

    Write-Host "[+] Getting Virtual Machines" -ForegroundColor Green
    Get-AzVM | Select-Object ResourceGroupName, Name, VmId, LicenseType | Format-Table -AutoSize

    Write-Host "[+] Getting Web Applications" -ForegroundColor Green
    Get-AzWebApp | Select-Object hostnames, defaulthostname, RepositorySiteName | Format-Table -AutoSize

    Write-Host "[+] Getting Storage Accounts" -ForegroundColor Green
    Get-AzStorageAccount

}
```

{% endcode %}

Example output:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FugXLWEjgU3HH4eVCm4iB%2Fimage.png?alt=media&amp;token=0311eb90-6fbf-4505-83e9-36f7f4e82f0c" alt=""><figcaption></figcaption></figure>

## Azure CLI

A set of commands used to create and manage Azure resources. Can be installed on multiple platforms and can be used with multiple clouds.

The default output format is JSON

```
Install using MSI https://learn.microsoft.com/nl-nl/cli/azure/install-azure-cli
```

Login using creds:

```powershell
az login -u test@pp.onmicrosoft.com -p "Password123!"
```

### Get users

```powershell
az ad user list --output table
```
