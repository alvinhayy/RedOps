---
title: "Windows privilege escalation: a full walk-through"
source_url: https://medium.com/@bannamalak156/windows-privilege-escalation-a-full-walk-through-faa3427ad031
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: windows
---

getting a foothold in a windows machine is only half the battle as a cybersecurity engineer i always focus on the next big step which is privilege escalation this lab covers the core techniques used to climb the ladder from a normal user to nt authority system through these 18 tasks we explored how insecure services weak registry permissions and even gui apps can be a gateway to full control we also tested advanced token impersonation attacks and learned how to use automated scripts to find these flaws faster than doing it manually this report is a step by step documentation of my journey through the lab showing exactly how each exploit works and how to fix these common misconfigurations in the real world

## Task 1 : Deploy the Vulnerable Windows VM

## Task 2 : Generate a Reverse Shell Executable

first we need a way to get inside the machine so we use msfvenom to create our reverse shell file . the command generates a file called reverse.exe that will connect back to our kali ip on port 53.

to get this file onto the windows target we start a python http server on our kali . we see the request in the logs when the windows machine downloads it . finally we start a netcat listener and run the exe to get our first user shell.

## Task 3 : Service Exploits — Insecure Service Permissions

in this task we start looking for ways to become admin. we check a service called daclsvc using the sc qc command . the output shows it runs with localsystem privileges which is exactly what we want.

to see if we can mess with it we use accesschk.exe to check our user permissions . we find out that our user has service_change_config which means we can tell this service to run anything we want.

## Task 4 : Service Exploits — Unquoted Service Path

now that we know we can change the config we use sc config to change the binpath . we point the path to our reverse.exe shell that we uploaded earlier.

after the change is a success we just need to start the service using net start daclsvc . the service tries to start and executes our shell giving us a new connection on kali as system.

## Task 5 : Service Exploits — Weak Registry Permissions

this task focuses on the registry instead of the service config directly. we look at the regsvc service and try to trigger it . even though the service gives an error it still executes our payload in the background.

we check our listener and find a new connection. when we type whoami it confirms we are now nt authority system. this happens because we had permission to overwrite the registry key that tells the service which file to run.

## Task 6 : Service Exploits — Insecure Service Executables

here we search for services that have weak file permissions on their actual exe files . we find a service called filepermave. the goal here is to replace the original service file with our own malicious one.

once we replace it or point to our shell we use net start fileperwave to run it . the system runs our file thinking it is the normal service . we get the connection back and verify with whoami that we successfully escalated our privileges again.

## Task 7 : Registry — AutoRuns

first we need to log into the windows machine using rdp with the admin credentials we found to start our investigation

once we are in we set up a netcat listener on our kali machine on port 53 and wait for the connection

the exploit works by replacing a file that runs automatically when someone logs in so we trigger the login to get the shell

after we get the connection we check whoami to see our current user and we find that we are now logged in as admin

## Task 8 : Registry — AlwaysInstallElevated

in this task we check if the system allows installing any msi file with system privileges so we check the first registry key in hklm

the output shows the value is 0x1 which means it is enabled then we must check the same key in hkcu to confirm the vulnerability

since both keys are enabled we can now create a malicious msi file using msfvenom on our kali machine

the command finishes and we save the payload as setup.msi ready to be sent to the windows machine

now we start a python http server on our kali to host the msi file so the target can download it

on the windows machine we use the certutil command to download the setup.msi file into the privesc folder

the python logs show that the windows machine successfully requested and downloaded the file

we prepare our listener on kali again and then we run the msi file quietly using the msiexec command

the exploit works perfectly and we receive a new shell connection on our kali terminal

finally we type whoami and the result confirms we have achieved the highest privilege as nt authority system

## Task 9 : Passwords — Registry

we start task 9 by searching the registry for any passwords that might be stored in plain text . first we check the winlogon registry key because sometimes admins set up auto logon which saves the password in the registry . we find that the default user is admin and autoadminlogon is set.

after that we try to search for passwords in other places like vnc and putty sessions but the registry keys were not there . so we decide to search for xml files on the whole disk because they often have sensitive info like passwords from installation or sysprep.

the search finds an unattend.xml file in the panther directory so we use the type command to read its content . inside the file we see an autologon section with a username called admin and a password value that looks like base64.

now we take that encoded string to our kali machine and use the base64 command to decode it . the command reveals that the clear text password is password123.

## Task 10 : Passwords — Saved Creds

in task 10 we look at another way to find passwords by checking the windows credential manager . we run the cmdkey /list command to see if there are any credentials saved for our machine . we find that there is a stored credential for the admin user which is perfect for us.

since the credentials are saved we can use them to run any file as admin without knowing the actual password by using the runas command with the savecred flag . we tell windows to start our reverse.exe file as the admin user.

we go back to our kali machine where we have a netcat listener waiting on port 53 . a new connection arrives from the target windows machine . finally we run whoami and it shows that we are now logged in as the admin user.

## Task 11 : Passwords — Security Account Manager (SAM)

first we log in to the machine as an admin using the winexe tool because we need high privileges to access the system files.

then we map a network drive from our kali machine to the windows target using the net use command so we can transfer the files we find easily.

we go to the windows repair folder and copy the sam file which contains the local user hashes directly to our z drive.

we also copy the system file from the same repair folder because we need it to decrypt the sam file later on our kali machine.

after getting the files we use the pwdump script from the creddump7 suite on our kali to extract the actual hashes from the sam and system files.

the tool finishes the work and shows us the ntlm hashes for the administrator and other accounts like guest and defaultaccount.

## Task 12 : Passwords — Passing the Hash

in this task we use the administrator hash we just found to log in without needing the plain text password by using a pass the hash attack.

we run the impacket tool with the hash and it gives us a semi-interactive shell that confirms we successfully logged in as the admin user.

## Task 13 : Scheduled Tasks

we start checking for any scripts that run automatically and we find a file called cleanup.ps1 that is supposed to run as system every minute.

we use the accesschk tool to see if we can modify this script and the results show that our user has full write permissions on the file.

next we use a powershell command to download our reverse shell payload from our kali server and save it in the privesc folder.

we use the echo command to add a line to the cleanup.ps1 script that tells it to run our reverse.exe shell every time the task triggers.

we wait for the scheduled task to run and then we get a connection back on our netcat listener which gives us full system access.

## Task 14 : Insecure GUI Apps

we notice that a gui application like paint is running with administrator privileges so we try to find a way to escape from it.

we go to the file menu and click open to bring up the windows file explorer dialog which allows us to browse the system.

in the file name box we type the path to cmd.exe and press enter to trick the system into launching a command prompt with admin rights.

## Task 15 : Startup Apps

in this task we check if we have permissions to write to the startup folder. we use the accesschk tool and the output shows that builtin users have read and write access to the startup directory.

now we run a vbs script that is designed to create a malicious shortcut of our reverse shell in that folder.

after setting the shortcut we simulate an admin login by using rdp to connect to the machine. as soon as the admin logs in the startup shortcut triggers and connects back to our kali listener on port 4444.

we check our identity and it confirms that we successfully gained access as the admin user.

## Task 16 : Token Impersonation — Rogue Potato

this task is about exploiting tokens but first we need to get a shell as a service account. we use psexec64 to execute our reverse shell with the permissions of nt authority\local service.

## Task 17 : Token Impersonation — PrintSpoofer

now that we are a service account we can use the printspoofer exploit to become system. we run the printspoofer command and point it to our reverse shell file.

the tool successfully finds the seimpersonateprivilege and starts the process for us.

## Task 18 : Privilege Escalation Scripts

in this task we explore four different tools that help us find vulnerabilities automatically instead of searching manually

we have winpeasany seatbelt powerup and sharpup all located in the privesc directory on the windows machine

first we run winpeas which is the most famous one because it covers almost everything from services to registry keys

then we try seatbelt which is more about gathering system information and security settings rather than just finding direct exploits

we also use powerup which is a powershell script that is great for finding weak service permissions and registry issues

finally we test sharpup which is a c# version of powerup that is very fast but it doesn’t have as many checks as winpeas

after testing all of them we find that the answer is ***no*** because each tool has a different focus and they don’t all identify every single technique we used in the previous tasks
