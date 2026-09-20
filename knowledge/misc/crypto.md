---
title: "Crypto"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/crypto/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## How to use this section

Start by identifying the primitive and its parameters. Then determine what the attacker controls or observes, such as an oracle, a leaked value, or nonce reuse, before selecting an attack.

### CTF workflow

### Symmetric cryptography

### Hashes, MACs, and KDFs

### Public-key cryptography

### TLS and certificates

### Cryptography in malware

### Miscellaneous

## Quick setup

Create an isolated Python environment and install commonly used packages. PyCryptodome’s documentation recommends installing `pycryptodome` with `pip`; SageMath provides separate installation guidance for each supported platform.[\[1\]](#references)[\[2\]](#references)

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pycryptodome gmpy2 sympy pwntools
```
SageMath is often useful for algebraic, lattice, RSA, and elliptic-curve calculations.[\[2\]](#references)

## References
