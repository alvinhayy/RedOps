---
title: "FZ - iButton"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/todo/radio-hacking/flipper-zero/fz-ibutton.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Introduction

For background on iButton technology, see:

## Design

In the following image, the **blue** area shows how to place a physical iButton against the Flipper Zero’s contacts for reading. The **green** area shows which contacts should touch a reader during emulation.[\[1\]](#references)

## Actions

### Read

In Read mode, the Flipper Zero waits for a key to touch its contacts, detects the protocol, and displays the protocol above the key ID. The built-in application supports Dallas, Cyfral, and Metakom access-control keys.[\[2\]](#references)

### Add manually

You can manually enter key data for the Dallas, Cyfral, and Metakom protocols.[\[2\]](#references)

### Emulate

You can emulate a saved key, whether it was read from a physical key or entered manually.[\[2\]](#references)

If the built-in contacts cannot reach the reader, connect the data and ground contacts through the GPIO pins.[\[2\]](#references)

## References
