---
title: "Basic Forensic Methodology"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/basic-forensic-methodology/index.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: methodology
---

## Creating and Mounting an Image

## Malware Analysis

This **isn’t necessary the first step to perform once you have the image**. But you can use this malware analysis techniques independently if you have a file, a file-system image, memory image, pcap… so it’s good to **keep these actions in mind**:

## Inspecting an Image

if you are given a **forensic image** of a device you can start **analyzing the partitions, file-system** used and **recovering** potentially **interesting files** (even deleted ones). Learn how in:

[Partitions/File Systems/Carving](partitions-file-systems-carving/index.html)

Depending on the used OSs and even platform different interesting artifacts should be searched:

## Deep inspection of specific file-types and Software

If you have very **suspicious** **file**, then **depending on the file-type and software** that created it several **tricks** may be useful.

Read the following page to learn some interesting tricks:

[Specific Software/File-Type Tricks](specific-software-file-type-tricks/index.html)

I want to do a special mention to the page:

## Memory Dump Inspection

## Pcap Inspection

## **Anti-Forensic Techniques**

**Anti-Forensic Techniques**

Keep in mind the possible use of anti-forensic techniques:

## Threat Hunting

## References
