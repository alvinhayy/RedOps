---
title: "4786 - Cisco Smart Install"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/4786-cisco-smart-install.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Basic information

Cisco Smart Install is a legacy zero-touch deployment feature in which a director provides configuration files and software images to client switches. Communication between the director and clients uses TCP port **4786**.[\[1\]](#references)

**Default port:** 4786

```
PORT      STATE  SERVICE
4786/tcp  open   smart-install
```
## CVE-2018-0171

CVE-2018-0171 is a critical Smart Install client vulnerability in affected Cisco IOS and IOS XE releases. An unauthenticated attacker can send a crafted message to TCP/4786 and trigger a buffer overflow, potentially causing a reload, arbitrary code execution, or a watchdog crash. Only vulnerable devices with Smart Install client functionality enabled are affected.[\[2\]](#references)

Cisco provides fixed releases. Where Smart Install is not needed, disable it with `no vstack`; where it must remain enabled, restrict TCP/4786 so that only the director can reach clients.[\[2\]](#references)[\[3\]](#references)

## Smart Install Exploitation Tool

The [Smart Install Exploitation Tool (SIET)](https://github.com/frostbits-security/SIET) can test Smart Install exposure and retrieve a configuration from a vulnerable lab switch. Configuration files commonly contain sensitive topology and authentication data, so store and handle retrieved files as credentials.[\[4\]](#references)

In the following authorized lab example, `-g` requests the configuration and `-i` supplies the target address:[\[4\]](#references)

The original SIET walkthrough tested a physical Cisco Catalyst 2960. Virtual lab images do not necessarily implement Smart Install, so confirm that the chosen image exposes TCP/4786 before treating a failed virtual test as evidence that the technique does not work.[\[4\]](#references)

```
~/opt/tools/SIET$ sudo python2 siet.py -g -i 10.10.100.10
```
SIET stores the retrieved configuration under its `tftp/` directory.

## References

- [1] [Cisco Smart Install Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/smart_install/configuration/guide/smart_install.pdf)
- [2] [Cisco advisory - CVE-2018-0171 Smart Install remote code execution](https://www.cisco.com/c/en/us/support/docs/csa/cisco-sa-20180328-smi2.html)
- [3] [Cisco - Action required to secure Smart Install](https://www.cisco.com/c/en/us/support/docs/csa/cisco-sa-20180409-smi.html)
- [4] [SIET - Smart Install Exploitation Tool](https://github.com/frostbits-security/SIET)
