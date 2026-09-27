---
title: "Spoofing SSDP and UPnP Devices with EvilSSDP"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/pentesting-network/spoofing-ssdp-and-upnp-devices.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: network
---

## **SSDP & UPnP Overview**

**SSDP & UPnP Overview**

SSDP (Simple Service Discovery Protocol) advertises and discovers network services over UDP port 1900 and can operate without DHCP or DNS configuration. It forms the discovery layer of UPnP, which supports zero-configuration networking for devices such as PCs, printers, gateways, and mobile devices.[\[2\]](#references)

## **UPnP Flow & Structure**

**UPnP Flow & Structure**

The UPnP Device Architecture defines six stages: addressing, discovery, description, control, eventing, and presentation. After obtaining an address through DHCP or Auto-IP, control points use SSDP discovery; they send M-SEARCH requests, while devices advertise services with NOTIFY messages. A control point retrieves XML device and service descriptions, invokes actions with SOAP, subscribes to eventing, and may load a presentation URL.[\[2\]](#references)

## **IGD & Tools Overview**

**IGD & Tools Overview**

UPnP IGD’s WANIPConnection service defines SOAP actions such as `AddPortMapping` for NAT port mappings. The Umap code in `upnp-arsenal` targets deployments with exposed SOAP controls and uses such actions to test mappings; only run it with authorization.[\[3\]](#references)[\[6\]](#references)

Miranda is a command-line UPnP tool for discovering and interacting with devices, while `upnp-arsenal` collects Miranda and other UPnP scripts and tools.[\[4\]](#references)[\[5\]](#references)

## **Evil SSDP Practical Usage**

**Evil SSDP Practical Usage**

Evil SSDP responds to SSDP discovery as a fake UPnP device that can appear in Windows Explorer and serve a configurable phishing page, relying on users’ trust in apparently legitimate network services. Its templates include scanner, Office365, and password-vault examples; form templates can POST credentials, and `-u` can redirect users after capture to preserve the deception.[\[1\]](#references)[\[7\]](#references)

## **Mitigation Strategies**

**Mitigation Strategies**

To combat these threats, recommended measures include:[\[7\]](#references)

- Disabling UPnP on devices when not needed.
- Educating users about phishing and network security.
- Monitoring network traffic for unencrypted sensitive data.

In essence, while UPnP offers convenience and network fluidity, it also opens doors to potential exploitation. Awareness and proactive defense are key to ensuring network integrity.[\[7\]](#references)

## References

- [1] [evil-ssdp](https://github.com/initstring/evil-ssdp)
- [2] [Universal Plug and Play Device Architecture](https://upnp.org/specs/arch/UPnPDA10_20000613.htm)
- [3] [WANIPConnection:1 Service Template](https://upnp.org/specs/gw/UPnP-gw-WANIPConnection-v1-Service.pdf)
- [4] [miranda-upnp](https://github.com/0x90/miranda-upnp)
- [5] [upnp-arsenal](https://github.com/0x90/upnp-arsenal)
- [6] [Umap v0.1beta source](https://raw.githubusercontent.com/0x90/upnp-arsenal/master/umap-bypass.py)
- [7] [Evil SSDP: Spoofing the SSDP and UPnP Devices](https://www.hackingarticles.in/evil-ssdp-spoofing-the-ssdp-and-upnp-devices/)
