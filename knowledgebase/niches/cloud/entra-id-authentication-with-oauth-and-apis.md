---
title: "Entra ID - Authentication with OAuth and API's"
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/architecture/entra-id-authentication-with-oauth-and-apis
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

Microsoft Entra ID uses OAuth (2.0) for authentication. An application (Oauth client - web app) can sign in to the Authorization server, get bearer tokens to access Resource Server (Microsoft Graph and other APIs).&#x20;

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FiPHxGiFZvzOF2b8Uv34C%2Fimage.png?alt=media&amp;token=a2964792-78dd-4de6-9233-e043a245b3b5" alt=""><figcaption></figcaption></figure>

This flow is better described in the following diagram:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FGqDNhQsyQl4TsSZD8MTR%2Fimage.png?alt=media&amp;token=c15d40aa-894f-45c6-b402-00407835a2b0" alt=""><figcaption></figcaption></figure>

## Bearer token

A very important factor is the Bearer token. This is also a access token.  These are JSON Web tokens. a bearer token, as the name suggests, grants the bearer access to a protected resource. There are three types of tokens used in OIDC:

1. Access tokens: The client presents this token to the resource server to access resources. It can be used only for a specific combination of user, client, and resource and cannot be revoked until expiry - that is 1 hour by default.
2. ID tokens: The client receives this token from the authorization server. It contains basic information about the user. It is bound to a specific combination of user and client.
3. Refresh tokens: Provided to the client with access token. Used to get new access and ID tokens. It is bound to a specific combination of user and client and can be revoked. Default expiry is 90 days for inactive refresh tokens and no expiry for active tokens.

When using Access Tokens to access resources there are no logs, if you use a refresh token there will be logs.

### Conditional Access and tokens

Conditional access is only in place when authenticating to Entra ID. This means that when using a access token, you will **not** be effected by conditional access.

## User identity & workload identity

User identities represent human users who access resources within or via the Microsoft Entra ID environment. These identities are typically tied to individual people. Workload identities represent applications or services (e.g., virtual machines, containers, or serverless functions) rather than human users. These identities allow workloads to securely access Azure resources or other external services.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FxJgOIkJiX5sJu5DjPMlE%2Fimage.png?alt=media&amp;token=b2a22f49-d734-471a-bd2d-c052dc4767b0" alt=""><figcaption></figcaption></figure>

To protect workload identities (enterprise applications) with conditional access, you will need a premium subscriptions e.g. 15 dollars a month per application.

In general, to be opsec, try to avoid user identities and instead use workload identities

## Continuous Access Evaluation (CAE)

Exists to invalidate tokens before their expiry time (default 1 hour). It is a defense mechanism by Microsoft to protect against attacks.

CAE steps in when a access token is used outside a trusted location. For example, if a conditional access policy is defined to restrict access to the ip 12.33.44.55, but a access token is used there, CAE steps in and invalidated the token. Country-based locations are **not** supported.

It is invalidated AFTER the first use, so it is still possible to use the access token once
