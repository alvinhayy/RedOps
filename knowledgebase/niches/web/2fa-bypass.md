---
title: "2FA/MFA/OTP Bypass"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/2fa-bypass.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## **Enhanced Two-Factor Authentication Bypass Techniques**

### **Direct Endpoint Access**

**Direct Endpoint Access**

See [Proxmox VE](../network-services-pentesting/pentesting-web/proxmox-ve.html#tfa-state-confusion-to-a-full-api-ticket) for a product-specific example of client-selected TFA state.

Try the post-login endpoint directly and verify that the server—not only the UI—requires completion of the MFA state. If an application incorrectly trusts navigation metadata, also test the correctly spelled HTTP **`Referer` header**; a secure implementation must not use it as proof of MFA.[\[2\]](#references)[\[5\]](#references)

### **Token Reuse**

**Token Reuse**

Reutilizing previously used tokens for authentication within an account can be effective.[\[2\]](#references)

### **Utilization of Unused Tokens**

**Utilization of Unused Tokens**

Test whether an unused token generated for your own test account is incorrectly accepted for another authorized test account. This checks that OTPs are bound to the correct account, session, purpose, and transaction.[\[2\]](#references)[\[5\]](#references)

### **Exposure of Token**

**Exposure of Token**

Investigate whether the token is disclosed in a response from the web application.[\[2\]](#references)

### **Verification Link Exploitation**

**Verification Link Exploitation**

Using the **email verification link sent upon account creation** can allow profile access without 2FA, as highlighted in a detailed [post](https://srahulceh.medium.com/behind-the-scenes-of-a-security-bug-the-perils-of-2fa-cookie-generation-496d9519771b).[\[3\]](#references)

### **Session Manipulation**

**Session Manipulation**

Initiate sessions for two authorized test accounts, complete MFA in one, and verify that its completion state cannot be transplanted into the other session. The backend must bind the MFA result to the same account and pre-authentication session.[\[5\]](#references)

### **Password Reset Mechanism**

**Password Reset Mechanism**

Investigating the password reset function, which logs a user into the application post-reset, for its potential to allow multiple resets using the same link is crucial. Logging in with the newly reset credentials might bypass 2FA.[\[2\]](#references)

### **OAuth Platform Compromise**

**OAuth Platform Compromise**

Check whether a federated **OAuth/OIDC** login path enforces an assurance level equivalent to the application’s password-plus-MFA path. Control of the upstream identity account may bypass the application’s local MFA only when the relying party accepts that weaker federated session.[\[5\]](#references)

### **Brute Force Attacks**

**Brute Force Attacks**

#### **Rate Limit Absence**

**Rate Limit Absence**

The lack of a limit on the number of code attempts allows for brute force attacks, though potential silent rate limiting should be considered.[\[1\]](#references)[\[2\]](#references)

Note that even if a rate limit is in place you should try to see if the response is different when the valid OTP is sent. In [**this post**](https://mokhansec.medium.com/the-2-200-ato-most-bug-hunters-overlooked-by-closing-intruder-too-soon-505f21d56732), the bug hunter discovered that even if a rate limit is triggered after 20 unsuccessful attempts by responding with 401, if the valid one was sent a 200 response was received.[\[4\]](#references)

#### **Slow Brute Force**

**Slow Brute Force**

A slow brute force attack is viable where flow rate limits exist without an overarching rate limit.[\[1\]](#references)

#### **Code Resend Limit Reset**

**Code Resend Limit Reset**

Resending the code resets the rate limit, facilitating continued brute force attempts.[\[1\]](#references)

#### **Client-Side Rate Limit Circumvention**

**Client-Side Rate Limit Circumvention**

If throttling exists only in JavaScript, replay the request directly and verify whether the server independently enforces per-account, per-session, and broader abuse limits.[\[1\]](#references)[\[5\]](#references)

#### **Internal Actions Lack Rate Limit**

**Internal Actions Lack Rate Limit**

Rate limits may protect login attempts but not internal account actions.[\[1\]](#references)

#### **SMS Code Resend Costs**

**SMS Code Resend Costs**

Excessive resending of codes via SMS incurs costs to the company, though it does not bypass 2FA.

#### **Infinite OTP Regeneration**

**Infinite OTP Regeneration**

Endless OTP generation with simple codes allows brute force by retrying a small set of codes.[\[1\]](#references)

### **Race Condition Exploitation**

**Race Condition Exploitation**

Send the same OTP or recovery code concurrently and verify that validation and consumption are atomic. A race exists if more than one request can redeem a single-use value.[\[5\]](#references)

### **CSRF/Clickjacking Vulnerabilities**

**CSRF/Clickjacking Vulnerabilities**

Exploring CSRF or Clickjacking vulnerabilities to disable 2FA is a viable strategy.[\[1\]](#references)[\[2\]](#references)

### **“Remember Me” Feature Exploits**

**“Remember Me” Feature Exploits**

#### **Predictable Cookie Values**

**Predictable Cookie Values**

Guessing the “remember me” cookie value can bypass restrictions.[\[1\]](#references)

#### **IP Address Impersonation**

**IP Address Impersonation**

Impersonating the victim’s IP address through the **X-Forwarded-For** header can bypass restrictions.[\[1\]](#references)

### **Utilizing Older Versions**

**Utilizing Older Versions**

#### **Subdomains**

**Subdomains**

Test whether subdomains expose older applications or authentication paths that lack the current MFA requirement.[\[1\]](#references)

#### **API Endpoints**

**API Endpoints**

Older API versions, indicated by /v*/ directory paths, may be vulnerable to 2FA bypass methods.[\[1\]](#references)

### **Handling of Previous Sessions**

**Handling of Previous Sessions**

Terminating existing sessions upon 2FA activation secures accounts against unauthorized access from compromised sessions.[\[1\]](#references)

### **Access Control Flaws with Backup Codes**

**Access Control Flaws with Backup Codes**

Immediate generation and potential unauthorized retrieval of backup codes upon 2FA activation, especially with CORS misconfigurations/XSS vulnerabilities, poses a risk.[\[1\]](#references)[\[2\]](#references)

### **Information Disclosure on 2FA Page**

**Information Disclosure on 2FA Page**

Sensitive information disclosure (e.g., phone number) on the 2FA verification page is a concern.[\[1\]](#references)

### **Password Reset Disabling 2FA**

**Password Reset Disabling 2FA**

A process demonstrating a potential bypass method involves account creation, 2FA activation, password reset, and subsequent login without the 2FA requirement.[\[2\]](#references)

### **Decoy Requests**

**Decoy Requests**

Utilizing decoy requests to obfuscate brute force attempts or mislead rate limiting mechanisms adds another layer to bypass strategies. Crafting such requests requires a nuanced understanding of the application’s security measures and rate limiting behaviours.

### OTP Construction errors

If the OTP is derived only from predictable or client-supplied data, a user may be able to reproduce it. Verify that codes are generated from a cryptographically secure secret, are short-lived, single-use, and bound to the correct account and action.[\[5\]](#references)

## References
