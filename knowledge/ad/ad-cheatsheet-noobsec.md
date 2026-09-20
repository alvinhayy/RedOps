---
title: "Active Directory (AD) Cheatsheet"
source_url: https://www.noobsec.net/ad-cheatsheet/
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: ad
---

This post assumes that opsec is not required and you can be as noisy as may be required to perform the enumeration and lateral movement. This post is meant for pentesters as well as defenders for the same reason - understand the AD environment better.

This cheatsheet would help some certifications like [CRTP](https://www.pentesteracademy.com/activedirectorylab), [OSCP](https://www.offensive-security.com/pwk-oscp/), [PNPT](https://certifications.tcm-sec.com/pnpt/), and such.

Note: Only a subset of flags and switches, which are most commonly used, are shared. Best documentation is the code itself.

This is a living document. Last updated: 19 / June / 2022

## Enumeration

Initial and lateral movement enumeration

### Get the Dog Out - SharpHound + BloodHound

Let’s have the dog sniff things out because automated enumeration is cool

The tools used are - [BloodHound](https://github.com/BloodHoundAD/BloodHound/releases/), [SharpHound.exe](https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors) or [SharpHound.ps1]

Leverage secure LDAP

Getting all the data

It’s best to pull session info separately

Gathering data in a loop (default 2hrs), makes sense for sessions as they change

Run in a different context

Specify domain

Next step would be to take this data and then feed it to BloodHound GUI to finally have some fun :)

### Getting Hands Dirty - PowerView

Let’s have some fun ourselves with manual enumeration.

We will use PowerView and some net commands to perform enumeration manually.

Assuming that latest PowerView script (master and dev are the same) has been loaded in memory.

#### Domain Enumeration

Get basic information of the domain

Get domain SID

Get domain policies

Get domain Kerberos policy

Get list of DCs

Get DC IP

#### Forest Enumeration

Get current forest

Get a list of domains

#### User Enumeration

Get a list of users

Get a count of users

Get a list of users with some specific properties

Get a list of users with their logon counts, bad password attempts where attempts are greater than 0

Finding users with SPN

Finding users who are AllowedToDelegateTo

Finding users who can be delegated

#### Computer Enumeration

Get a list of computers

Get a list of computers with Unconstrained delegation

Finding users who are AllowedToDelegateTo

#### Group Enumeration

Get a list of groups in a domain

Get a list of groups in a domain

Get group membership

#### ACL Enumeration

Get resolved ACEs, optionally for a specific user/group and domain

Get interesting resolved ACLs

Get interesting resolved ACLs owned by specific object (ex. noobsec)

#### Session Enumeration

Finding sessions on a computer

Get who is logged on locally where

#### User Hunting

Get list of machines where current user has local admin access

Find machines where members of specific groups have sessions. Default: Domain Admins

Find machines where current user has local admin access AND specific group sessions are present

## Lateral Movement

### Kerberoasting

To see existing tickets

Remove all tickets

#### PowerView

Request a kerberos service ticket for specified SPN.

By default output in Hashcat format

#### Manually

By doing it manually, ticket is generated, it requires to be extracted to crack the hash

Dump the tickets out

Now, crack ’em
