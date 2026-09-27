---
title: Subdomain Enumeration
source_url: https://notes.incendium.rocks/pentesting-notes/web/subdomain-enumeration
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---
We can find subdomains of websites using various techniques.

## OSINT - SSL/TLS certificates

<https://crt.sh/>

<https://transparencyreport.google.com/https/certificates>

### OSINT - Search Engines

Search engines contain trillions of links to more than a billion websites, which can be an excellent resource for finding new subdomains.

**-site:[www.tryhackme.com](http://www.tryhackme.com)  site:\*.tryhackme.com**

### OSINT - Sublist3r

```bash
./sublist3r.py -d acmeitsupport.thm
```

## DNS bruteforce

* DNSrecon

```bash
dnsrecon -t brt -d acmeitsupport.thm
```

## Virtual hosts

Some subdomains aren't always hosted in publically accessible DNS results, such as development versions of a web application or administration portals. Instead, the DNS record could be kept on a private DNS server or recorded on the developer's machines.

Find size:

```bash
ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/namelist.txt -H "Host: FUZZ.acmeitsupport.thm" -u <http://10.10.73.103>
```

Exclude size:

```bash
ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/namelist.txt -H "Host: FUZZ.acmeitsupport.thm" -u <http://10.10.73.103> -fs {size}
```
