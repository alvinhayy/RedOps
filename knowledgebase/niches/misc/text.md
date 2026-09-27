---
title: "Text Stego"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/stego/text/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

# Text Steganography

## Practical path

If plain text behaves unexpectedly, preserve the original evidence, inspect its codepoints, and normalize only a copy.

### Technique

Text steganography frequently relies on characters that render identically or invisibly:

- Homoglyphs: different Unicode codepoints that look alike (for example, Latin `a` and Cyrillic`а` )<sup>[\[1\]](#references)</sup>
- Zero-width characters: joiners, non-joiners, and zero-width spaces<sup>[\[2\]](#references)</sup>
- Whitespace encodings: spaces versus tabs, trailing-space patterns, and deliberate line-length patterns<sup>[\[3\]](#references)[\[4\]](#references)</sup>

Additional high-signal cases:

- Bidirectional controls, which can visually reorder text<sup>[\[1\]](#references)</sup>
- Variation selectors and combining characters, which can carry hidden state while leaving the visible text nearly unchanged<sup>[\[1\]](#references)</sup>

### Decode helpers

### Inspect codepoints

```
python3 - <<'PY'
import sys
s=sys.stdin.read()
for i,ch in enumerate(s):
  if ord(ch) > 127 or ch.isspace():
    print(i, hex(ord(ch)), repr(ch))
PY
```
## CSS `unicode-range` channels

`unicode-range` channels
`@font-face` rules can be abused to encode bytes in `unicode-range: U+..` entries. Extract the codepoints, concatenate the hexadecimal values, and decode them:[\[3\]](#references)

```
grep -o "U+[0-9A-Fa-f]\+" styles.css | tr -d 'U+\n' | xxd -r -p
```
If ranges contain multiple values per declaration, split on commas first and normalize (`tr ',+' '\n'`). Python can parse and emit the bytes when the formatting is inconsistent.[\[3\]](#references)

## References

- [1] [Unicode Technical Report #36: Unicode Security Considerations](https://www.unicode.org/reports/tr36/)
- [2] [Irongeek: Unicode Steganography with Zero-Width Characters and Homoglyphs](https://www.irongeek.com/i.php?page=security/unicode-steganography-homoglyph-encoder)
- [3] [0xdf: Flagvent 2025 (Medium) — Santa’s Wishlist](https://0xdf.gitlab.io/flagvent2025/medium)
- [4] [Debian manual: `stegsnow` whitespace steganography](https://manpages.debian.org/trixie/stegsnow/stegsnow.1.en.html)
