---
title: "RBAC & ABAC roles"
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/architecture/rbac-and-abac-roles
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

Azure RBAC Roles or simply Azure roles, provides access management for Azure resources using the authorization system of ARM. There are over more than 120 built-in roles and we can define custom roles too.

However, there are five fundamental roles:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FTtbgx0IuESxmhAv5AQql%2Fimage.png?alt=media&amp;token=af871488-09bd-4e90-91eb-95c1dd075a5e" alt=""><figcaption></figcaption></figure>

### RBAC Assignment

Something to remember:

Principal HAS role ON scope

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FOdVRL4Qmqcwr8YoYHgvD%2Fimage.png?alt=media&amp;token=6a4f70b0-c36d-4008-b86d-ef62ba20ef63" alt=""><figcaption></figcaption></figure>

### ABAC

ABAC builds on RBAC and provides fine-grained access control based on attributes of a resource, security principal and environment. These are implemented using role assignment condition.

* Only used by storage accounts
* Low level functionality

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F4ASGgwA8L8khnPhvm3pU%2Fimage.png?alt=media&amp;token=8a47d0ce-e344-4c41-a1ff-a6f7b07fdefb" alt=""><figcaption></figcaption></figure>

If these are all RBAC/ABAC managed, who manages them? Well this is where Entra ID roles come in.
