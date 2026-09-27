---
title: ARM Deployment History
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/privilege-escalation/arm-deployment-history
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

When a identity has the permissions `Microsoft.Resources/deployments/read` and `Microsoft.Resources/subscriptions/resourceGroups/read`, it can read the deployment history.

### Deployment history

Each resource group maintains a deployment history for up to 800 deployments. They are a a rich resource of information. It can contain sensitive information like passwords "String" type.&#x20;

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FW0OWb2LoWY4ievZvUgz4%2Fimage.png?alt=media&amp;token=9ab014d4-26d8-4410-951a-c512106be60b" alt=""><figcaption></figcaption></figure>

There are no logs for reading these templates

### Common scenario

A inline command that is being executed:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FXNA8QA2EgY6OBXJ5na1B%2Fimage.png?alt=media&amp;token=bb7e2066-c78a-4155-b339-6e7beaf09ac3" alt=""><figcaption></figcaption></figure>
