---
title: SSRF
source_url: https://notes.incendium.rocks/pentesting-notes/web/ssrf
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---
SSRF stands for Server-Side Request Forgery. It's a vulnerability that allows a malicious user to cause the webserver to make an additional or edited HTTP request to the resource of the attacker's choosing.

A successful SSRF attack can result in any of the following:

* Access to unauthorised areas.
* Access to customer/organisational data.
* Ability to Scale to internal networks.
* Reveal authentication tokens/credentials.

**Table of contents:**

***

### **Types of SSRF**

There are two types of SSRF vulnerability; the first is a regular SSRF where data is returned to the attacker's screen. The second is a Blind SSRF vulnerability where an SSRF occurs, but no information is returned to the attacker's screen.

In this example, the attacker can control the server's subdomain to which the request is made. Take note of the payload ending in **\&x=**  being used to stop the remaining path from being appended to the end of the attacker's URL and instead turns it into a parameter (?x=) on the query string.

```bash
https://website.thm/item/2?server=server.website.thm/flag?id=9&x=
```

Server Requesting: **<https://server.website.thm/flag?id=9\\&x=.website.thm/api/item?id=2>**

***

### Finding an SSRF

Potential SSRF vulnerabilities can be spotted in web applications in many different ways. Here is an example of four common places to look:

**When a full URL is used in a parameter in the address bar:**

**A hidden field in a form:**

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/237696fc8e405d25d4fc7bbcc67919f0.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/237696fc8e405d25d4fc7bbcc67919f0.png)

**A partial URL such as just the hostname:**

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/f3c387849e91a4f15a7b59ff7324be75.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/f3c387849e91a4f15a7b59ff7324be75.png)

**Or perhaps only the path of the URL:**

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/3fd583950617f7a3713a107fcb4cfa49.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/3fd583950617f7a3713a107fcb4cfa49.png)

If working with a blind SSRF where no output is reflected back to you, you'll need to use an external HTTP logging tool to monitor requests such as requestbin.com, your own HTTP server or Burp Suite's Collaborator client.

[requestbin.com](http://requestbin.com/)

***

### Bypass SSRF defenses

More security-savvy developers aware of the risks of SSRF vulnerabilities may implement checks in their applications to make sure the requested resource meets specific rules. There are usually two approaches to this, either a deny list or an allow list.

**Deny List**

Attackers can bypass a Deny List by using alternative localhost references such as 0, 0.0.0.0, 0000, 127.1, 127.*.*.\*, 2130706433, 017700000001 or subdomains that have a DNS record which resolves to the IP Address 127.0.0.1 such as 127.0.0.1.nip.io.

**Allow List**

An allow list is where all requests get denied unless they appear on a list or match a particular pattern, such as a rule that an URL used in a parameter must begin with **<https://website.thm>.** An attacker could quickly circumvent this rule by creating a subdomain on an attacker's domain name, such as <https://website.thm.attackers-domain.thm>. The application logic would now allow this input and let an attacker control the internal HTTP request.

### Practical

image style can confirm this in the above DIV element as per the screenshot below:

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/bd9ee9ac0b7592b5343cbc8dd9b57189.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/bd9ee9ac0b7592b5343cbc8dd9b57189.png)

If you choose one of the avatars and then click the **Update Avatar** button, you'll see the form change and, above it, display your currently selected avatar. Viewing the page source will show your current avatar is displayed using the data URI scheme, and the image content is base64 encoded as per the screenshot below.

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/fff0ea113602635dcf5d1e8d0b1d8bca.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/fff0ea113602635dcf5d1e8d0b1d8bca.png)

Now let's try making the request again but changing the avatar value to **private** in hopes that the server will access the resource and get past the IP address block. To do this, firstly, right-click on one of the radio buttons on the avatar form and select **Inspect**:

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/2ef87608418e47625bedad9d0361ed08.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/2ef87608418e47625bedad9d0361ed08.png)

**And then edit the value of the radio button to private:**

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/a1712298679cc642d792d935b14effe5.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/a1712298679cc642d792d935b14effe5.png)

And then click the **Update Avatar** button. Unfortunately, it looks like the web application has a deny list in place and has blocked access to the /private endpoint.

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/a59460cc19eaf5776ee8a882e25b2d64.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/a59460cc19eaf5776ee8a882e25b2d64.png)

As you can see from the error message, the path cannot start with /private but don't worry, we've still got a trick up our sleeve to bypass this rule. We can use a directory traversal trick to reach our desired endpoint. Try setting the avatar value to **x/../private**

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/84b88d9c6fa6a29450520625bb42870d.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/84b88d9c6fa6a29450520625bb42870d.png)

You'll see we have now bypassed the rule, and the user updated the avatar. This trick works because when the web server receives the request for **x/../private**, it knows that the **../** string means to move up a directory that now translates the request to just **/private**.

## SSRF via host header

The HTTP Host header is a mandatory request header as of HTTP/1.1. It specifies the domain name that the client wants to access. For example, when a user visits `https://incendium.rocks/web-security`, their browser will compose a request containing a Host header as follows:

`GET /web-security HTTP/1.1 Host: incendium.rocks.net`

In some cases, such as when the request has been forwarded by an intermediary system, the Host value may be altered before it reaches the intended back-end component. We will discuss this scenario in more detail below.

### Exploit examples

Simple:

```http
GET /example HTTP/1.1
Host: bad-stuff-here
```

Line wrapping:

```http
GET /example HTTP/1.1
    Host: bad-stuff-here
Host: vulnerable-website.com
```

Absolute URL

```http
GET https://vulnerable-website.com/ HTTP/1.1
Host: bad-stuff-here
```

## SSRF via Referer header

```http
GET /product?productId=1 HTTP/2
Host: vulnerable-webste.com
Referer: http://sa6dc7pljx3tcldy06a8lcp7jyppdg15.oastify.com
```
