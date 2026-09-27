---
title: "Clone a Website"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/phishing-methodology/clone-a-website.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: redteam
---

# Cloning a Website

## wget

The following command uses Wget’s mirroring, page-requisite, link-conversion, and extension-adjustment modes, then serves the downloaded files from the current directory with Python’s `http.server` module on port 8000.[\[1\]](#references)[\[2\]](#references)

```
wget --mirror --page-requisites --convert-links --adjust-extension <URL>
cd <URL>
python3 -m http.server 8000
```
## goclone

The goclone repository describes the utility as downloading a website to a local directory while preserving its relative link structure, and documents the `goclone <url>` invocation.[\[3\]](#references)

```
#https://github.com/imthaghost/goclone
goclone <url>
```
## Social Engineering Toolit

The Social-Engineer Toolkit (SET) repository identifies SET as an open-source penetration-testing framework for authorized social-engineering assessments.[\[4\]](#references)

```
#https://github.com/trustedsec/social-engineer-toolkit
```
## References

- [1] [GNU Wget Manual](https://www.gnu.org/software/wget/manual/wget.html)
- [2] [Python `http.server` documentation](https://docs.python.org/3/library/http.server.html)
- [3] [goclone repository](https://github.com/imthaghost/goclone)
- [4] [Social-Engineer Toolkit repository](https://github.com/trustedsec/social-engineer-toolkit)
