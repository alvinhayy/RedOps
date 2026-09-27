---
title: IDOR (Insecure Direct Object Reference)
source_url: https://notes.incendium.rocks/pentesting-notes/web/idor-insecure-direct-object-reference
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---

Insecure Direct Object Reference

IDOR stands for Insecure Direct Object Reference and is a type of access control vulnerability.

This type of vulnerability can occur when a web server receives user-supplied input to retrieve objects (files, data, documents), too much trust has been placed on the input data, and it is not validated on the server-side to confirm the requested object belongs to the user requesting it.

## Example:

**service.thm/profile?user\_id=1305**

If you would be able to change the id to 1000 for example, and see another user's information, than this would be an IDOR vulnerability.

## IDOR trough encoded IDs

When passing data from page to page either by post data, query strings, or cookies, web developers will often first take the raw data and encode it.

```bash
echo 'base_64_string' | base64 -d
```

## IDOR trough hased IDs

Hashed IDs are a little bit more complicated to deal with than encoded ones, but they may follow a predictable pattern, such as being the hashed version of the integer value.

<https://crackstation.net/> <https://www.dcode.fr/md5-hash>

## IDOR Unpredictable IDs

If the Id cannot be detected using the above methods, an excellent method of IDOR detection is to create two accounts and swap the Id numbers between them. If you can view the other users' content using their Id number while still being logged in with a different account (or not logged in at all), you've found a valid IDOR vulnerability.
