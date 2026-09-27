---
title: Architecture
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/azure/architecture
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
Azure architecture is organized hierarchically to provide structured management and control over resources and services. The main building blocks include **Management Groups**, **Subscriptions**, **Resource Groups**, and **Resources**. These components help in organizing, managing, and controlling access to resources across an Azure environment.&#x20;

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fl5lRaTnYprMyfz5As3qb%2Fimage.png?alt=media&amp;token=c405f733-6f69-4de5-ada9-56d496ea31e6" alt=""><figcaption></figcaption></figure>

## **Management Groups**

* **Definition**: Management Groups provide a level of organization above subscriptions. They are used to manage access, policies, and compliance across multiple Azure subscriptions.
* **Purpose**: They help in managing resources at scale across various subscriptions within an organization. You can group subscriptions by departments, regions, or any other logic, and apply policies and access controls at the management group level.
* **Hierarchy**: Management Groups can be nested, allowing for a tree-like structure. A root management group is created by default and can have child management groups.
* **Privileges Inheritance**: When policies or access controls (such as role-based access control or RBAC) are applied to a management group, those permissions are inherited by all subscriptions within that management group. This simplifies large-scale management, ensuring consistent policies across all underlying resources.

## **Subscriptions**

* **Definition**: A subscription is a billing and access boundary in Azure. It contains a collection of resources and services that are linked to a specific account.
* **Purpose**: Subscriptions allow organizations to divide their cloud environment for billing, security, and administrative reasons. Each subscription can have its own set of resources and access controls.
* **Hierarchy**: Subscriptions are contained within management groups. You can have multiple subscriptions under a single management group, and a subscription can only belong to one management group at a time.
* **Privileges Inheritance**: Access control and policies applied at the management group level propagate down to subscriptions. However, any access controls applied directly to a subscription override the inherited ones, allowing for more specific or restrictive control at the subscription level.

## **Resource Groups**

* **Definition**: A Resource Group is a container that holds related resources for an Azure solution. It includes virtual machines, databases, networking resources, and more, which are managed together.
* **Purpose**: Resource Groups allow for organizing resources by lifecycle, permissions, and geographical location. Resources within a resource group share the same lifecycle, meaning they can be deployed, updated, and deleted together.
* **Hierarchy**: Resource groups are contained within subscriptions. Each subscription can have multiple resource groups, and each resource group can hold multiple resources.
* **Privileges Inheritance**: Role-based access control (RBAC) permissions applied to a resource group are inherited by all resources within that group. However, permissions can also be defined at the individual resource level, allowing for finer control over specific resources.

## **Resources**

* **Definition**: Resources are the individual services and components that you deploy in Azure, such as virtual machines, storage accounts, databases, or networking components.
* **Purpose**: Resources are the actual workloads or services that are managed and run within the Azure cloud. Each resource has its own properties and configurations, and they exist within a resource group.
* **Hierarchy**: Resources reside within resource groups, which in turn reside within subscriptions. Resources are the lowest level in the Azure management hierarchy.
* **Privileges Inheritance**: Resources can inherit RBAC permissions from their parent resource group, but they can also have unique, granular permissions applied directly to them. For example, a specific virtual machine can have its own access control distinct from the resource group it's part of.

## How Privileges Are Inherited

Azure uses **Role-Based Access Control (RBAC)** to manage access and permissions. Here's how privileges are inherited across the hierarchy:

1. **Management Groups**: Any access control or policy applied at the management group level is inherited by all subscriptions within that management group. This provides centralized access management for an entire organization.
2. **Subscriptions**: Access controls and policies set at the subscription level override inherited permissions from the management group. Subscriptions are the main boundary for billing, and you can apply more granular controls at this level.
3. **Resource Groups**: Permissions at the resource group level are inherited by all resources within that group. However, individual resources can have specific permissions set, which can override or augment the inherited permissions.
4. **Resources**: Resources inherit permissions from their resource group, but access can be customized per resource. For example, you could have a user who has access to a resource group but does not have permission to manage certain resources within that group (like a specific virtual machine or database).

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2F8hHITE87l4dkyFplzZQL%2Frbac-overview.png?alt=media&amp;token=a0c908ea-8c0f-4798-bb77-396d8d166fc5" alt=""><figcaption></figcaption></figure>

#### Example of Privileges Inheritance:

* A user is given the **Owner** role at the **Management Group** level. This user will inherit full access to all subscriptions under this management group.
* Within a **Subscription**, the same user has the **Contributor** role. This means they can manage resources but not assign roles or manage access within that subscription.
* Within a **Resource Group**, the user may have the **Reader** role, meaning they can view resources but not modify them.
* For a **Resource**, they may have specific access based on the permissions set for that resource (for example, the **Contributor** role for a virtual machine but no access to a database).

#### Summary of Inheritance:

* **Management Groups**: Global access policies applied here propagate to all subscriptions.
* **Subscriptions**: Inherit access from management groups but can have specific access controls.
* **Resource Groups**: Inherit access from subscriptions but can have specific access controls.
* **Resources**: Inherit access from resource groups but can have specific, granular permissions.

This hierarchical structure allows for flexible and scalable management of Azure environments, ensuring that policies and access controls can be applied at different levels depending on organizational needs.
