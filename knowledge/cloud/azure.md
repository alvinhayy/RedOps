---
title: Azure
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fbnmgv06X1mPiLb4SsgXb%2FMicrosoft_Azure-Logo.wine.png?alt=media&amp;token=4c300722-20e9-4644-943f-40d710728872" alt="" width="375"><figcaption></figcaption></figure>

## Contents

[Architecture](/pentesting-notes/cloud/azure/architecture.md)

[Service Discovery, Recon, Enumeration and Initial Access Attacks](/pentesting-notes/cloud/azure/service-discovery-recon-enumeration-and-initial-access-attacks.md)

[Authenticated Enumeration](/pentesting-notes/cloud/azure/authenticated-enumeration.md)

[Privilege Escalation](/pentesting-notes/cloud/azure/privilege-escalation.md)

[Lateral Movement](/pentesting-notes/cloud/azure/lateral-movement.md)

## Introduction

**Entra ID** is the new name for what was previously known as **Azure Active Directory (Azure AD)**, Microsoft's cloud-based identity and access management service. It is part of the **Microsoft Entra** product family, which focuses on securing and managing access across various digital environments, such as cloud, on-premises, and hybrid setups.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fprra5c7Og2Xl1sSLhs7y%2FEntra_ID_Diagram_new.avif?alt=media&amp;token=ed2e952b-ccc4-4a19-980f-098ff9fe7e95" alt=""><figcaption></figcaption></figure>

Microsoft Entra ID empowers organizations to manage and secure identities so people can access the applications and services they need. Microsoft Entra ID provides an identity solution that integrates broadly, from on-premises legacy apps to thousands of top software-as-a-service (SaaS) applications.

## Azure Kill Chain

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FTmm4VghIPOtbHLMrICbC%2Fimage.png?alt=media&amp;token=d52f0baa-1522-406b-a806-12725b59a2e7" alt=""><figcaption></figcaption></figure>

* **Reconnaissance**\
  Attackers gather information about the Azure environment, such as public-facing applications, IP addresses, Azure AD configuration, and exposed APIs. Tools like Azure CLI, PowerShell, or third-party scanners may be used to probe for vulnerabilities.
* **Initial Access**\
  Attackers gain a foothold in the Azure tenant. This could involve exploiting weak credentials, phishing attacks to steal Azure AD credentials, exploiting exposed APIs, or compromising an application hosted in Azure.
* **Enumeration**\
  Enumeration involves attackers actively probing and listing resources, configurations, and users in the Azure environment to identify potential vulnerabilities or misconfigurations that they can exploit. This is a deeper, more targeted activity than reconnaissance, which is often passive.
* **Privilege Escalation**\
  After gaining access, attackers aim to elevate privileges to obtain broader control over the Azure tenant. They may exploit misconfigured role-based access control (RBAC), manipulate Azure AD permissions, or exploit vulnerabilities in virtual machines or containers.
* **Persistence**\
  Attackers establish mechanisms to maintain long-term access. In Azure, this might involve creating malicious service principals, altering configurations for continuous access, or deploying backdoors in virtual machines or serverless functions.
* **Lateral Movement**\
  Attackers navigate the Azure environment to find and access additional resources. This could involve moving between subscriptions, accessing storage accounts, databases, or other resources linked to Azure services.

## Permissions for white/greybox pentest

To start a white box hardening review of some Entra ID tenants you need to ask for **`Global Reader` role on each tenant**. Moreover, to perform a hardening review of different Azure subscriptions you would need at least the **`Reader`role over all the subscriptions**.

Note that if those roles aren't enough to access all the info you need, you could also ask the client for roles with the permissions you need. Just try to **minimize the amount of not read-only permissions you ask for!**
