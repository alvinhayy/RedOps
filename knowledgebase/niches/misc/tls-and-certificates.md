---
title: "TLS & Certificates"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/crypto/tls-and-certificates/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

# TLS and Certificates

## X.509 Parsing

OpenSSL can print a certificate’s decoded fields, while `asn1parse` shows the underlying ASN.1 structure.[\[1\]](#references)[\[2\]](#references)

```
openssl x509 -in cert.pem -noout -text
openssl asn1parse -in cert.pem
```
Review at least:

- the subject, issuer, and Subject Alternative Name (SAN);
- key usage and extended key usage;
- basic constraints and path-length constraints;
- the `notBefore` and`notAfter` validity times;
- the public-key parameters and signature algorithm.

Legacy signatures such as MD5- or SHA-1-based certificate signatures are particularly important findings, although the exact acceptance and impact depend on the validator and trust context.[\[3\]](#references)

RFC 5280 defines the Internet X.509 profile and the processing rules for extensions such as SAN, key usage, name constraints, and basic constraints.[\[3\]](#references)

## Encodings and Containers

- **PEM-style textual encoding:** Base64 data between`BEGIN` and`END` boundaries.
- **DER:** the binary Distinguished Encoding Rules representation.
- **PKCS#7/CMS (`.p7b`):** commonly carries certificates and a certificate chain, but not private keys.
- **PKCS#12 (`.p12` or `.pfx`):** can carry private keys, certificates, and supporting certificates.

RFC 7468 specifies the textual encodings used for PKIX, PKCS, and CMS structures; OpenSSL’s `pkcs12` command creates and parses PKCS#12 files.[\[4\]](#references)[\[5\]](#references)

```
openssl x509 -in cert.cer -outform PEM -out cert.pem
openssl x509 -in cert.pem -outform DER -out cert.der
openssl pkcs12 -in file.pfx -out out.pem
```
Treat `out.pem` as sensitive: unless options such as `-nokeys` are used, the output may contain private-key material.[\[5\]](#references)

## Security Review Checklist

Apply the certificate-processing requirements in RFC 5280 when reviewing a validator or trust decision.[\[3\]](#references)

- Verify the complete chain to an explicitly trusted anchor; do not trust user-supplied roots implicitly.
- Confirm the hostname or service identity against SAN values.<sup>[\[8\]](#references)</sup>
- Enforce basic constraints, name constraints, key usage, and extended key usage.
- Reject expired or not-yet-valid certificates and disallowed key or signature algorithms.
- Bind client-certificate identities to the correct application account and authorization context.

## Certificate Transparency Logs

Certificate Transparency provides publicly auditable logs of issued certificates.<sup>[\[6\]](#references)</sup> Search a domain with crt.sh during authorized asset discovery.[\[7\]](#references)

## References
