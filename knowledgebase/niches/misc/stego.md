---
title: "Stego"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/stego/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Entry Point

Approach steganography as a forensics problem: identify the real container, enumerate high-signal locations (metadata, appended data, embedded files), and only then apply content-level extraction techniques.

### Workflow & triage

A structured workflow that prioritizes container identification, metadata/string inspection, carving, and format-specific branching.

### Images

Where most CTF stego lives: LSB/bit-planes (PNG/BMP), chunk/file-format weirdness, JPEG tooling, and multi-frame GIF tricks.

### Audio

Spectrogram messages, sample LSB embedding, and telephone keypad tones (DTMF) are recurring patterns.

### Text

If text renders normally but behaves unexpectedly, consider Unicode homoglyphs, zero-width characters, or whitespace-based encoding.

### Documents

PDFs and Office files are containers first; attacks usually revolve around embedded files/streams, object/relationship graphs, and ZIP extraction.

### Malware and delivery-style steganography

Payload delivery can use valid-looking files, such as GIF or PNG images, that carry marker-delimited text payloads rather than hiding data in pixels.

## References
