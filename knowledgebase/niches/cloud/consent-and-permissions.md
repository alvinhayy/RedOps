---
title: Consent and Permissions
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/architecture/consent-and-permissions
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

Applications can ask users for permissions to access their data. For example, for basic sign-in. If allowed, a normal user can grant consent only for "**Low Impact**" permissions. In all other cases, admin consent is required.

<div align="left"><figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FL8sHp5h76tGwrJ0ZeNob%2Fimage.png?alt=media&amp;token=890f1127-5097-4356-8eed-b0b1cb0ded5a" alt="" width="188"><figcaption></figcaption></figure></div>

### Admin consent

The following roles can consent medium- high level impact (whole tenant) permissions:

* Global administrator
* Application administrator
* Cloud application administrator
* Custom role including "permission to grant permission to applications"

### User consent

By default, all users in the tenant can consent to any app to access the organization's data:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F3m6aOqpEalkEjQBJ37EH%2Fimage.png?alt=media&amp;token=63a76abb-e9ff-44f1-bda3-9615d8f255ed" alt=""><figcaption></figcaption></figure>

One very interesting permission is `User.ReadBasic.All` That allows the app to read display name, first and second name, email, open extension and photo for all the users.

This is also a recommendation to tenants that have the default option set: Only consent from verified publishers or do not allow users to consent at all

### Application Registration and Enterprise application

When we create/register a new application with a secret, redirect uri ETC. It's called a "application" but when a user **consents** to this application, a new "enterprise application" is created automatically with the same name as the application. This is called a **service principal**.

A service principal is the part can can be used, role assignment, permissions, etc.

Also, conditional access can be implemented on enterprise applications/service principals.
