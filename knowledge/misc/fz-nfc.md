---
title: "FZ - NFC"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/todo/radio-hacking/flipper-zero/fz-nfc.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Intro

For info about RFID and NFC check the following page:

## Supported NFC cards

Caution

Apart from NFC cards Flipper Zero supports **other type of High-frequency cards** such as several **Mifare** Classic and Ultralight and **NTAG**.

The capability list below describes the firmware documented by the original article and should not be treated as the current exhaustive support matrix. Flipper firmware has added protocols and changed NFC behavior over time; check the current official documentation for the installed firmware.[\[1\]](#references)[\[2\]](#references)

- **Bank cards (EMV)** — only read UID, SAK, and ATQA without saving.
- **Unknown cards** — read the UID, SAK, and ATQA and emulate a UID.

For **NFC card types B, F, and V**, the documented firmware could read a UID without saving it.

### NFC cards type A

#### Bank card (EMV)

The documented firmware could read a UID, SAK, ATQA, and available application data from a bank card **without saving it**.

For these bank cards, the firmware displayed data without saving or emulating the card.

#### Unknown cards

When Flipper Zero is **unable to determine NFC card’s type**, then only an **UID, SAK, and ATQA** can be **read and saved**.

For an unknown NFC card, this mode can emulate only its UID.

### NFC cards types B, F, and V

In the firmware documented by the original article, NFC card types B, F, and V could only have an identifier read and displayed without saving it.[\[1\]](#references)

## Actions

For an intro about NFC [**read this page**](../pentesting-rfid.html#high-frequency-rfid-tags-13.56-mhz).

### Read

Flipper Zero can read NFC cards but does not implement every higher-level protocol built on ISO 14443. It may therefore recover the low-level UID, SAK, and ATQA while leaving the application protocol unknown. For primitive access systems that authorize only by UID, the tool can read, manually enter, and emulate that identifier; cryptographically authenticated systems require more than a copied UID.[\[1\]](#references)

#### Reading the UID VS Reading the Data Inside

In Flipper, reading 13.56 MHz tags can be divided into two parts:[\[1\]](#references)

- **Low-level read** — reads only the UID, SAK, and ATQA. Flipper tries to guess the high-level protocol based on this data read from the card. You can’t be 100% certain with this, as it is just an assumption based on certain factors.
- **High-level read** — reads the data from the card’s memory using a specific high-level protocol. That would be reading the data on a Mifare Ultralight, reading the sectors from a Mifare Classic, or reading the card’s attributes from PayPass/Apple Pay.

### Read Specific

In case Flipper Zero isn’t capable of finding the type of card from the low level data, in `Extra Actions` you can select `Read Specific Card Type` and **manually** **indicate the type of card you would like to read**.

#### EMV Bank Cards (PayPass, payWave, Apple Pay, Google Pay)

Older Flipper firmware and compatible EMV cards could expose more than the UID, potentially including the PAN, expiration date, cardholder name, or transaction log when those records were made available by the card. Availability varies by card, application, and firmware. The magnetic-stripe CVV printed on the card is not exposed this way, and reading these records does not clone the cryptographic transaction capability needed to make a contactless payment.[\[1\]](#references)

## References
