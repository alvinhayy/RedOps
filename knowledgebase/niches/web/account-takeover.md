---
title: "Account Takeover"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/account-takeover.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## **Authorization Issue**

**Authorization Issue**

The email of an account should be attempted to be changed, and the confirmation process **must be examined**. If found to be **weak**, the email should be changed to that of the intended victim and then confirmed.[\[2\]](#references)

## **Unicode Normalization Issue**

**Unicode Normalization Issue**

1. The account of the intended victim `victim@gmail.com`
2. An account should be created using Unicode
 for example:`vićtim@gmail.com`<sup>[\[2\]](#references)</sup>

As explained in [**this talk**](https://www.youtube.com/watch?v=CiIyaZ3x49c), the previous attack could also be done abusing third party identity providers:[\[10\]](#references)

- Create an account in the third party identity with similar email to the victim using some unicode character (`vićtim@company.com` ).
  - The third party provider shouldn’t verify the email
  - If the identity provider verifies the email, maybe you can attack the domain part like: `victim@ćompany.com` and register that domain and hope that the identity provider generates the ascii version of the domain while the victim platform normalize the domain name.
- Login via this identity provider in the victim platform who should normalize the unicode character and allow you to access the victim account.

### Unicode/email parser disagreement

Normalization bugs don’t only happen in the UI. Also compare how the **DB collation**, the **SMTP server**, and any **OAuth/OIDC provider** interpret the same mailbox:

1. The application looks up the attacker-controlled email using a **permissive collation** and matches the victim row.
2. The reset token, magic link, or federated identity is later bound to the **raw attacker-controlled Unicode address** instead of the canonical email stored in the DB.
3. The attacker receives the artifact or is logged in as the victim.

Practical checks:

- Intercept forgot-password, email-change, and invite flows and replace the victim email with a **confusable / Unicode** variant you control.
- If social login is supported, repeat the same idea with the **email returned by the IdP** during the callback.
- If the backend sends the email **taken from user input** instead of the**canonical address stored in the database** , the flow is usually exploitable.

For further details, refer to the document on Unicode Normalization:

## **Reusing Reset Token**

**Reusing Reset Token**

Should the target system allow the **reset link** (or an equivalent **magic link**) to be **reused**, efforts should be made to **find more reset links** using tools such as `gau`, `wayback`, or `scan.io`.<sup>[\[2\]](#references)</sup> Also verify whether the artifact still works **after an email change** or when redeemed from a **second browser/device**.

## **Pre Account Takeover**

**Pre Account Takeover**

1. The victim’s email should be used to sign up on the platform, and a password should be set (an attempt to confirm it should be made, although lacking access to the victim’s emails might render this impossible).
2. One should wait until the victim signs up using OAuth and confirms the account.
3. It is hoped that the regular signup will be confirmed, allowing access to the victim’s account.<sup>[\[2\]](#references)</sup>

## **CORS Misconfiguration to Account Takeover**

**CORS Misconfiguration to Account Takeover**

If the page contains **CORS misconfigurations** you might be able to **steal sensitive information** from the user to **takeover his account** or make him change auth information for the same purpose:[\[2\]](#references)

[CORS - Misconfigurations & Bypass](cors-bypass.html)

## **CSRF to Account Takeover**

**CSRF to Account Takeover**

If the page is vulnerable to CSRF, you may be able to make the **user modify their password, email, or authentication settings** and then access the account:[\[2\]](#references)

[CSRF (Cross Site Request Forgery)](csrf-cross-site-request-forgery.html)

## **XSS to Account Takeover**

**XSS to Account Takeover**

If you find XSS in an application, you may be able to steal cookies, local-storage data, or page content that enables account takeover:[\[2\]](#references)

- Attribute-only reflected payloads on login pages can hook `document.onkeypress` , exfiltrate keystrokes through`new Image().src` , and steal credentials without submitting the form. See[Attribute-only login XSS behind WAFs](xss-cross-site-scripting/README.html#attribute-only-login-xss-behind-wafs) for a practical workflow.<sup>[\[1\]](#references)</sup>

## **Same Origin + Cookies**

**Same Origin + Cookies**

If you find a limited XSS or a subdomain take over, you could play with the cookies (fixating them for example) to try to compromise the victim account:[\[2\]](#references)

## **Predictable SSO / bearer cookies and staged login replay**

Some cross-application SSO stacks treat a client-visible cookie as a **bearer secret** and use it directly as the **server-side cache key** for the authenticated identity. If the value is generated from **low-entropy data** such as `System.currentTimeMillis()`, a sequential ID, or an encoded timestamp with no MAC/signature, the attacker only needs to predict the victim’s login window and replay candidate values.[\[8\]](#references)

Quick triage:

- Inspect post-login cookies for **13-digit timestamps** ,**sequential values** , or trivially encoded IDs.
- Review **product-specific overrides** : the shared framework may use a safe UUID generator while one SSO subclass replaces it with a predictable value.
- If the SSO resolver only runs for tickets claiming to come from **another integrated application** , try a**mismatched app tag / source-product cookie** to force the cross-product branch.

Typical exploitation pattern:

1. Send a request to a protected endpoint with the candidate ticket and the alternate-app tag.
2. If the ticket resolves, the first request may only **stage the victim identity in a new server-side session** and return an auto-submitting login form.
3. Replay the returned form or its equivalent auth endpoint (`/j_security_check` , SAML/OIDC bridge, custom login handler, etc.) because this**second step often establishes the authenticated principal** .
4. Confirm the takeover with a follow-up protected request (`200` ) versus the normal login redirect (`302` ).

```
GET /protected.do HTTP/1.1
Host: target.tld
Cookie: CUSTOM_SSO_TICKET=<candidate>; CUSTOM_SSO_APP_TAG_NAME=<other-product>
```
Important constraints:

- The correct ticket may only work from the **victim’s source IP** , shared NAT, internal foothold, or a path through a**trusted proxy** . Check whether proxy-trust settings let`X-Forwarded-For` override the recorded client IP.
- A **rolling throttle** on path + real source IP can make even a 1-second millisecond window (~1,000 candidates) slow to enumerate. Reuse the ideas in[Rate Limit Bypass](rate-limit-bypass.html) , but remember that distributing guesses across random IPs will fail if only the victim’s IP can produce a hit.
- Replacing predictable tokens with UUIDs stops unauthenticated guessing, but a separately stolen live cookie may still replay if the token remains a **pure bearer credential** . For generic cookie abuse patterns see[Cookies Hacking](hacking-with-cookies/README.html) .

Safe detection tip: send an **impossible historical token** plus the **mismatched app tag** to a protected path and look for **branch-specific cleanup `Set-Cookie` headers** (forced cookie deletion / logout). That proves the cross-application SSO replay path is reachable without resolving a real victim session, but it does **not** prove the generator is still predictable.[\[9\]](#references)

## **Attacking Password Reset Mechanism**

**Attacking Password Reset Mechanism**

[Reset/Forgotten Password Bypass](reset-password.html)

## **Magic Links / Passwordless Login**

**Magic Links / Passwordless Login**

Passwordless email-login flows deserve the same scrutiny as reset-password flows:[\[6\]](#references)

- If the unauthenticated endpoint that creates the magic link accepts attacker-controlled `redirect_url` ,`next` ,`return_to` , or`callback` parameters, request a link for the victim and make the post-login redirect land on an attacker origin first.
- If the confirmation endpoint puts the token or session in the URL, fragment, or a browser-readable response, the attacker-controlled landing page can steal it and then bounce the victim back to the real application.
- On mobile, test **custom schemes** ,**Branch/app.link-style deep links** , and**unverified App / Universal Links** . A malicious app can register the same handler and intercept the login token.
- Verify the link is **single-use** and**browser/app-bound** : open it from two browsers, two profiles, webmail vs native mail, and browser vs native app.
- If the same endpoint silently creates users, combine this with **pre-account takeover** and**email verification bypass** tests.

```
POST /api/auth/magic-link HTTP/1.1
Host: target.tld
Content-Type: application/json
{"email":"victim@target.tld","redirect_url":"https://attacker.tld/callback"}
```
## Security-question resets that trust client-supplied usernames

If an “update security questions” flow takes a `username` parameter even though the caller is already authenticated, you can overwrite any account’s recovery data (including admins) because the backend typically runs `UPDATE ... WHERE user_name = ?` with your untrusted value. The pattern is:[\[4\]](#references)

1. Log in with a throwaway user and capture the session cookie.
2. Submit the victim username plus new answers via the reset form.
3. Immediately authenticate through the security-question login endpoint using the answers you just injected to inherit the victim’s privileges.

```
POST /reset.php HTTP/1.1
Host: file.era.htb
Cookie: PHPSESSID=<low-priv>
Content-Type: application/x-www-form-urlencoded
username=admin_ef01cab31aa&new_answer1=A&new_answer2=B&new_answer3=C
```
Anything gated by the victim’s `$_SESSION` context (admin dashboards, dangerous stream-wrapper features, etc.) is now exposed without touching the real answers.

Enumerated usernames can then be targeted via the overwrite technique above or reused against ancillary services (FTP/SSH password spraying).[\[4\]](#references)

## OAuth to Account takeover

## **QR / Cross-Device Login Flows**

**QR / Cross-Device Login Flows**

Desktop QR login, TV/device-code login, wallet login, and “approve on your phone” flows are now common ATO surfaces. Treat `qrId`, `device_code`, approval handles, and polling session identifiers like password-reset tokens.[\[7\]](#references)

Common weaknesses to test:

- **Unbound browser session** : approving the flow authenticates a different browser than the one that created it.
- **Reusable QR / device codes** : the same code authenticates multiple browsers (“double login”).
- **Predictable or attacker-controlled identifiers** : short, sequential, or client-generated`qrId` /`device_code` values can be brute-forced or replaced.
- **Weak approval context** : the mobile app doesn’t show enough origin, device, or action details, making consent phishing and session swapping realistic.

Practical workflow:

1. Start the flow in the attacker browser and capture the polling/status endpoint.
2. Reuse the same `qrId` /`device_code` from a second browser or after the first login completes.
3. Swap browser/session identifiers between two accounts and check whether approval follows the **code** instead of the original session.
4. Try parallel polling/races and brute-forcing short QR identifiers.
5. If the platform supports wallet or passkey-based cross-device login, verify whether the handoff is rejected when the QR/device code is stale, already redeemed, or replayed from the wrong context.

From the defender side, current guidance is to require **short-lived one-time codes**, add **request-binding / extra confirmation data**, and where possible **prove device proximity**.[\[7\]](#references)

## Host Header Injection

1. The Host header is modified following a password reset request initiation.
2. The `X-Forwarded-For` proxy header is altered to`attacker.com` .
3. The Host, Referrer, and Origin headers are simultaneously changed to `attacker.com` .
4. After initiating a password reset and then opting to resend the mail, all three of the aforementioned methods are employed.<sup>[\[2\]](#references)</sup>

## Response Manipulation

If the client reduces an authentication decision to a simple Boolean, test changing `false` to `true` as well as the status/body variants below. A secure server must enforce the decision independently of the client response.[\[2\]](#references)

1. **Code Manipulation** : The status code is altered to`200 OK` .
2. **Code and Body Manipulation** :
  - The status code is changed to `200 OK` .
  - The response body is modified to `{"success":true}` or an empty object`{}` .
3. The status code is changed to

These manipulation techniques are effective in scenarios where JSON is utilized for data transmission and receipt.[\[2\]](#references)

## Change email of current session

One disclosed workflow behaved as follows:[\[3\]](#references)

- The attacker requests an email change to an address they control.
- The attacker receives the email-change confirmation link.
- The attacker sends that link to the victim and convinces them to open it.
- The victim’s authenticated session confirms the attacker’s chosen email.
- The attacker resets the password and takes over the account.

### Bypass email verification for Account Takeover

- The attacker logs in as `attacker@test.com` and verifies that email during signup.
- Attacker changes verified email to victim@test.com (no secondary verification on email change)
- Now the website allows victim@test.com to login and we have bypassed email verification of victim user.

### Old Cookies

In one disclosed case, it was possible to log in, save the authenticated cookies, log out, and then log in again. Although the second login generated different cookies, the earlier cookies became valid again.[\[11\]](#references)

### Trusted device cookies + batch API leakage

*Long-lived device identifiers that gate recovery can be stolen when a batch API lets you copy unreadable subresponses into writable sinks.*[\[5\]](#references)

- Identify a **trusted-device cookie** (`SameSite=None` , long-lived) used to relax recovery checks.
- Find a **first-party endpoint** that returns that device ID in JSON (e.g., an OAuth`code` exchange returning`machine_id` ) but is not readable cross-origin.
- Use a **batch/chained API** that allows referencing earlier subresponses (`{result=name:$.path}` ) and writing them to an attacker-visible sink (page post, upload-by-URL, etc.). Example with Facebook Graph API:

```
POST https://graph.facebook.com/
batch=[
  {"method":"post","omit_response_on_success":0,"relative_url":"/oauth/access_token?client_id=APP_ID%26redirect_uri=REDIRECT_URI","body":"code=SINGLE_USE_CODE","name":"leaker"},
  {"method":"post","relative_url":"PAGE_ID/posts","body":"message={result=leaker:$.machine_id}"}
]
access_token=PAGE_ACCESS_TOKEN&method=post
```
- Load the batch URL in a hidden `<iframe>` so the victim sends the trusted-device cookie; the JSON-path reference copies`machine_id` into the attacker-controlled post even though the OAuth response is unreadable to the page.
- Replay: set the stolen device cookie in a new session. Recovery now treats the browser as trusted, often exposing weaker “no email/phone” flows (e.g., automated document upload) to add an attacker email without the password or 2FA.

## References
