---
title: "Documents"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/stego/documents/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

# Document Steganography

## PDF

### Technique

PDF files can contain objects, streams, JavaScript, and embedded files. During analysis, common tasks include:

- Extracting embedded attachments.
- Expanding object streams to make objects easier to inspect.
- Identifying JavaScript, embedded images, and unusual streams.<sup>[\[1\]](#references)</sup><sup>[\[2\]](#references)</sup>

### Quick checks

```
pdfinfo file.pdf
pdfdetach -list file.pdf
pdfdetach -saveall file.pdf
qpdf --qdf --object-streams=disable file.pdf out.pdf
```
The `--qdf --object-streams=disable` combination produces a more readable representation and removes object streams, which makes manual inspection easier.<sup>[\[2\]](#references)</sup> Then search `out.pdf` for suspicious objects and strings.

## Office OOXML

### Technique

Office Open XML files (`.docx`, `.xlsx`, and `.pptx`) use Open Packaging Conventions: a ZIP-based package made of parts and XML relationship files.[\[3\]](#references)<sup>[\[4\]](#references)</sup> Treat the package as a relationship graph and inspect media, external relationships, and unusual custom parts.

In practice:

- The document is a directory tree of XML and assets.
- The `_rels/` relationship files can point to external resources or hidden parts.
- Embedded data frequently lives in `word/media/` , custom XML parts, or unusual relationships.

### Quick checks

```
7z l file.docx
7z x file.docx -oout
```
Then inspect:

- `word/document.xml`
- `word/_rels/` for external relationships
- embedded media in `word/media/`

## References
