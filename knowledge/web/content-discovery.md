---
title: Content Discovery
source_url: https://notes.incendium.rocks/pentesting-notes/web/content-discovery
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---

Discovering content on the website is a important step in the reconnaissance phase of web pentesting.

***

**Table of contents:**

***

## Robots.txt

The robots.txt file is a document that tells search engines which pages they are and aren't allowed to show on their search engine results or ban specific search engines from crawling the website altogether.

```
http(s)://site.com/robots.txt
```

## Favicon

<https://wiki.owasp.org/index.php/OWASP_favicon_database>

Command:

```bash
curl <https://static-labs.tryhackme.cloud/sites/favicon/images/favicon.ico> | md5sum
```

## Sitemap.xml

Unlike the robots.txt file, which restricts what search engine crawlers can look at, the sitemap.xml file gives a list of every file the website owner wishes to be listed on a search engine.

```
http(s)://site.com/sitemap.xml
```

## **HTTP Headers**

When we make requests to the web server, the server returns various HTTP headers. These headers can sometimes contain useful information such as the webserver software and possibly the programming/scripting language in use.

Command:

```bash
curl <http://10.10.252.141> -v
```

## **Wappalyzer extension**

Find out the technology stack of any website. Create lists of websites that use certain technologies, with company and contact details. Use our tools for lead generation, market analysis and competitor research.

## Wayback machine

Search cached websites and webpages using the wayback machine.

## **S3 Buckets**

S3 Buckets are a storage service provided by Amazon AWS, allowing people to save files and even static website content in the cloud accessible over HTTP and HTTPS. The owner of the files can set access permissions to either make files public, private and even writable. Sometimes these access permissions are incorrectly set and inadvertently allow access to files that shouldn't be available to the public.

```
http(s)://{name}.s3.amazonaws.com
```

## Automated tools

### ffuf

```bash
ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt -u <http://10.10.252.141/FUZZ>
```

### dirb

```bash
dirb <http://10.10.252.141/> /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt
```

### gobuster

```
gobuster dir --url http://10.10.252.141/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt
```

#### finding files:

```bash
gobuster dir -u 10.10.10.191/ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt
```

#### Find API endpoints using all HTML responses

```jsx
ffuf -w ~/Tools/SecLists/Discovery/Web-Content/big.txt -u <http://prd.m.rendering-api.interface.htb/api/FUZZ> -mc all -fs 50 -X POST
```
