---
title: "iButton"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/todo/radio-hacking/ibutton.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Intro

iButton is a generic name for an electronic identification key packed in a **coin-shaped metal container**. It is also called **Dallas Touch** Memory or contact memory. Even though it is often wrongly referred to as a “magnetic” key, there is **nothing magnetic** in it. In fact, a full-fledged **microchip** operating on a digital protocol is hidden inside.[\[1\]](#references)

### What is iButton?

The name iButton describes the durable coin-shaped package and contact arrangement. Holders include plastic fobs, rings, and pendants.

When both contacts meet the reader, the device receives power and exchanges data. If the recessed contact geometry prevents the outer ground contacts from meeting, tilting the key against the reader wall can restore contact.[\[1\]](#references)

### **1-Wire protocol**

**1-Wire protocol**

Dallas/Maxim keys use the 1-Wire protocol: one data contact carries bidirectional traffic and may also provide parasitic power, while the metal can is the return contact. The controller initiates transactions and the device responds.[\[2\]](#references)

When the key (Slave) contacts the intercom (Master), the chip inside the key turns on, powered by the intercom, and the key is initialized. Following that the intercom requests the key ID. Next, we will look up this process in more detail.

Flipper can act as the controller while reading a key and as the emulated device while presenting a stored identifier to a reader.[\[1\]](#references)

### Dallas, Cyfral & Metakom keys

For information about how these keys works check the page [https://blog.flipperzero.one/taming-ibutton/](https://blog.flipperzero.one/taming-ibutton/)[\[1\]](#references)

### Attacks

iButtons can be attacked with Flipper Zero:

## References
