---
title: "Symmetric Crypto"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/crypto/symmetric/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## What to look for in CTFs

- **Mode misuse** : ECB patterns, CBC malleability, CTR/GCM nonce reuse.
- **Padding oracles** : different errors/timings for bad padding.
- **MAC confusion** : using CBC-MAC with variable-length messages, or MAC-then-encrypt mistakes.
- **XOR everywhere** : stream ciphers and custom constructions often reduce to XOR with a keystream.

## AES modes and misuse

NIST specifies the ECB, CBC, and CTR confidentiality modes in SP 800-38A and GCM authenticated encryption in SP 800-38D.[\[2\]](#references)[\[3\]](#references)

### ECB: Electronic Codebook

ECB leaks patterns: equal plaintext blocks → equal ciphertext blocks. That enables:

- Cut-and-paste / block reordering
- Block deletion (if the format remains valid)

If you can control plaintext and observe ciphertext (or cookies), try making repeated blocks (e.g., many `A`s) and look for repeats.

### CBC: Cipher Block Chaining

- CBC is **malleable** : flipping bits in`C[i-1]` flips predictable bits in`P[i]` , while also garbling`P[i-1]` . Modifying the IV targets the first plaintext block without garbling an earlier plaintext block.
- If the system exposes valid padding vs invalid padding, you may have a **padding oracle** .

### CTR

CTR turns AES into a stream cipher: `C = P XOR keystream`.

If a nonce/IV is reused with the same key:

- `C1 XOR C2 = P1 XOR P2` (classic keystream reuse)
- With known plaintext, you can recover the keystream and decrypt others.

**Nonce/IV reuse exploitation patterns**

-
Recover keystream wherever plaintext is known/guessable: ```
keystream[i..] = ciphertext[i..] XOR known_plaintext[i..]
```
Apply the recovered keystream bytes to decrypt any other ciphertext produced with the same key+IV at the same offsets.
-
Highly structured data (e.g., ASN.1/X.509 certificates, file headers, JSON/CBOR) gives large known-plaintext regions. You can often XOR the ciphertext of the certificate with the predictable certificate body to derive keystream, then decrypt other secrets encrypted under the reused IV. See also [TLS & Certificates](../tls-and-certificates/README.html) for typical certificate layouts.<sup>[\[1\]](#references)</sup>
-
When multiple secrets of the **same serialized format/size** are encrypted under the same key+IV, field alignment leaks even without full known plaintext. Example: PKCS#8 RSA keys of the same modulus size place prime factors at matching offsets (~99.6% alignment for 2048-bit). XORing two ciphertexts under the reused keystream isolates`p ⊕ p'` /`q ⊕ q'` , which can be brute-recovered in seconds.<sup>[\[1\]](#references)</sup>
-
Default IVs in libraries (e.g., constant `000...01` ) are a critical footgun: every encryption repeats the same keystream, turning CTR into a reused one-time pad.<sup>[\[1\]](#references)</sup>

**CTR malleability**

- CTR provides confidentiality only: flipping bits in ciphertext deterministically flips the same bits in plaintext. Without an authentication tag, attackers can tamper data (e.g., tweak keys, flags, or messages) undetected.
- Use AEAD (GCM, GCM-SIV, ChaCha20-Poly1305, etc.) and enforce tag verification to catch bit-flips.

### [GCM](#gcm)

GCM also breaks badly under nonce reuse. If the same key+nonce is used more than once, you typically get:

- Keystream reuse for encryption (like CTR), enabling plaintext recovery when any plaintext is known.
- Loss of integrity guarantees. Depending on what is exposed (multiple message/tag pairs under the same nonce), attackers may be able to forge tags.

Operational guidance:

- Treat “nonce reuse” in AEAD as a critical vulnerability.
- Misuse-resistant AEADs such as AES-GCM-SIV reduce nonce-reuse fallout. Callers should still provide unique nonces as required by the construction’s interface; accidental reuse has bounded consequences compared with ordinary GCM.<sup>[\[3\]](#references)[\[4\]](#references)</sup>
- If you have multiple ciphertexts under the same nonce, start by checking `C1 XOR C2 = P1 XOR P2` style relations.

### [Tools](#tools)

- [CyberChef](https://gchq.github.io/CyberChef/) for quick experiments.<sup>[\[8\]](#references)</sup>
- Python’s [PyCryptodome](https://www.pycryptodome.org/) package for scripting.<sup>[\[9\]](#references)</sup>

## [ECB exploitation patterns](#ecb-exploitation-patterns)

ECB (Electronic Code Book) encrypts each block independently:

- equal plaintext blocks → equal ciphertext blocks
- this leaks structure and enables cut-and-paste style attacks

### [Detection idea: token/cookie pattern](#detection-idea-tokencookie-pattern)

If you login several times and **always get the same cookie**, the ciphertext may be deterministic (ECB or fixed IV).

If you create two users with mostly identical plaintext layouts (e.g., long repeated characters) and see repeated ciphertext blocks at the same offsets, ECB is a prime suspect.

### [Exploitation patterns](#exploitation-patterns)

#### [Removing entire blocks](#removing-entire-blocks)

If the token format is something like `<username>|<password>` and the block boundary aligns, you can sometimes craft a user so the `admin` block appears aligned, then remove preceding blocks to obtain a valid token for `admin`.

#### [Moving blocks](#moving-blocks)

If the backend tolerates padding/extra spaces (`admin` vs `admin`    ), you can:

- Align a block that contains `admin`
- Swap/reuse that ciphertext block into another token

## [Padding Oracle](#padding-oracle)

### [What it is](#what-it-is)

In CBC mode, if the server reveals (directly or indirectly) whether decrypted plaintext has **valid PKCS#7 padding**, you can often:[\[7\]](#references)

- Decrypt ciphertext without the key
- Construct a ciphertext that decrypts to chosen plaintext when you can submit crafted preceding blocks or IVs and the application accepts the resulting validly padded message

The oracle can be:

- A specific error message
- A different HTTP status / response size
- A timing difference

### [Practical exploitation](#practical-exploitation)

PadBuster is the classic tool:

Example:

```
perl ./padBuster.pl http://10.10.10.10/index.php "RVJDQrwUdTRWJUVUeBKkEA==" 16 \
  -encoding 0 -cookies "login=RVJDQrwUdTRWJUVUeBKkEA=="
```
Notes:

- Block size is often `16` for AES.
- `-encoding 0` means Base64.
- Use `-error` if the oracle is a specific string.

### [Why it works](#why-it-works)

CBC decryption computes `P[i] = D(C[i]) XOR C[i-1]`. By modifying bytes in `C[i-1]` and watching whether the padding is valid, you can recover `P[i]` byte-by-byte.

## [Bit-flipping in CBC](#bit-flipping-in-cbc)

Even without a padding oracle, CBC is malleable. If you can modify ciphertext blocks and the application uses the decrypted plaintext as structured data (e.g., `role=user`), you can flip specific bits to change selected plaintext bytes at a chosen position in the next block.

Typical CTF pattern:

- Token = `IV || C1 || C2 || ...`
- You control bytes in `C[i]`
- You target plaintext bytes in `P[i+1]` because`P[i+1] = D(C[i+1]) XOR C[i]`

This is not a break of confidentiality by itself, but it is a common privilege-escalation primitive when integrity is missing.

## [CBC-MAC](#cbc-mac)

CBC-MAC is secure only under specific conditions (notably **fixed-length messages** and correct domain separation). AES-CMAC is a standardized construction that safely handles variable-length inputs.[\[5\]](#references)

### [Classic variable-length forgery pattern](#classic-variable-length-forgery-pattern)

CBC-MAC is usually computed as:

- IV = 0
- `tag = last_block( CBC_encrypt(key, message, IV=0) )`

If you can obtain tags for chosen messages, you can often craft a tag for a concatenation (or related construction) without knowing the key, by exploiting how CBC chains blocks.

This frequently appears in CTF cookies/tokens that MAC username or role with CBC-MAC.

### [Safer alternatives](#safer-alternatives)

- Use HMAC (SHA-256/512)
- Use CMAC (AES-CMAC) correctly
- Include message length / domain separation

## [Stream ciphers: XOR and RC4](#stream-ciphers-xor-and-rc4)

### [The mental model](#the-mental-model)

Most stream cipher situations reduce to:

`ciphertext = plaintext XOR keystream`

So:

- If you know plaintext, you recover keystream.
- If keystream is reused (same key+nonce), `C1 XOR C2 = P1 XOR P2` .

### [XOR-based encryption](#xor-based-encryption)

If you know any plaintext segment at position `i`, you can recover keystream bytes and decrypt other ciphertexts at those positions.

Autosolvers:

### [RC4](#rc4)

RC4 is a legacy stream cipher; encrypt/decrypt are the same XOR operation. Its known biases make it unsuitable for new systems, and TLS explicitly prohibits its cipher suites.[\[6\]](#references)

If you can get RC4 encryption of known plaintext under the same key, you can recover the keystream and decrypt other messages of the same length/offset.

Reference writeup (HTB Kryptos):

[Hack The Box - Kryptos - 0xRick\xe2\x80\x99s Blog](https://0xrick.github.io/hack-the-box/kryptos/)

## [References](#references)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
