---
title: Conditional Access
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/service-discovery-recon-enumeration-and-initial-access-attacks/conditional-access
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

Conditional Access policies at their simplest are if-then statements; **if** a user wants to access a resource, **then** they must complete an action. For example: If a user wants to access an application or service like Microsoft 365, then they must perform multifactor authentication to gain access.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FbVh8KNpP9JeYVnwSiDiR%2Fconditional-access-signal-decision-enforcement.png?alt=media&amp;token=b70bb244-dfd6-4a65-9ed8-6796a4fcd935" alt=""><figcaption></figcaption></figure>

## Findings flaws

Conditional access management can be very hard. Now that Microsoft is enforcing MFA since 2025, a lot of exceptions are being made in conditional access. This allows attackers to match/bypass a policy and still get access. Also, some conditional access policies like OS or location can be matched by just modifying the user-agent header or changing to a "safe" country by VPN.

A big problem is that someone from the outside never knows **why** the authentication fails (which condition they don't meet).

### Access tokens

When you get an access token, you are not authenticating anymore. So this always bypasses conditional access. However, [CAE ](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation)could still be an problem.

### Device platforms

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FNWzVNOnqRKTYpz1MPzyA%2Fimage.png?alt=media&amp;token=ae827913-6bb0-4b88-b6df-4cfbd7b49808" alt=""><figcaption></figcaption></figure>

Check by modifying the `user-agent` header if you can login.

### Location

Location can be GEO-based and IP-based. <https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-assignment-network>. A lot of times, the company WAN address(es) is included as a safe location. So if you manage to compromise a system within that internal network, or a application with for example a `managed identity`, try to authenticate through that system/application.

### Get conditional access policies

```
roadrecon plugin policies
```

This will write all conditional acccess information to a .html file
