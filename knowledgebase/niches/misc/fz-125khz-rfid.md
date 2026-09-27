---
title: "FZ - 125kHz RFID"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/todo/radio-hacking/flipper-zero/fz-125khz-rfid.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Intro

For background on how 125 kHz tags work, see:

The [low-frequency RFID introduction](../pentesting-rfid.html#low-frequency-rfid-tags-125khz) explains the common tag families and their data formats.

## Actions

### Read

Use **Read** to capture the tag data. After a successful read, Flipper Zero can emulate the saved tag.[\[1\]](#references)

Warning

Some intercom readers attempt to detect writable duplicate tags by issuing a write command before reading. A Flipper Zero emulation does not expose writable tag memory in the same way.[\[1\]](#references)

### Add manually

You can manually enter tag data in Flipper Zero, save it, and then emulate it.[\[1\]](#references)

#### IDs on cards

Sometimes a card has all or part of its ID printed on its exterior.

- **EM Marin**

For example, the pictured EM-Marin card exposes the last three of its five ID bytes. If the tag cannot be read, the two missing bytes may be brute-forced.

- **HID**

Similarly, the pictured HID card prints only two of the three ID bytes.

### Emulate/Write

After reading a tag or entering its ID manually, Flipper Zero can emulate the saved credential. For supported writable tags, it can also write the saved data to a compatible card.[\[1\]](#references)

## References
