---
title: "Ruby Json Pollution"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/deserialization/ruby-_json-pollution.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

# Ruby on Rails `_json` pollution

`_json` pollution

## Basic information

When a Rails endpoint receives a JSON body whose root value is not a hash, such as an array, the parsed value is exposed under the synthetic `_json` parameter. Depending on the parser and Rails version, an attacker-supplied `_json` member in an object can create an unexpected parameter shape or collide with application logic that also trusts `_json`.[\[1\]](#references)

This becomes a security issue when validation or authorization checks one parameter representation but a later operation consumes the polluted `_json` value. The following object illustrates attacker-controlled values placed under that reserved-looking key:[\[1\]](#references)

```
{
  "id": 123,
  "_json": [456, 789]
}
```
## References
