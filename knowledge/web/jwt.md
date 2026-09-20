---
title: JWT
source_url: https://notes.incendium.rocks/pentesting-notes/web/jwt
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---
## JWT authentication bypass via jwk header injection

The JSON Web Signature (JWS) specification describes an optional `jwk` header parameter, which servers can use to embed their public key directly within the token itself in JWK format.

```json
{
    "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
    "typ": "JWT",
    "alg": "RS256",
    "jwk": {
        "kty": "RSA",
        "e": "AQAB",
        "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
        "n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9m"
    }
}
```

A potential attack is to create your own key pair and use that to sign the token. The value specified in the "kid" should match. To make these attacks easy, you can install the JWT editor extension in Burp. Example:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FfU3P6p3qI1ag0V4IOwb4%2Fimage.png?alt=media&amp;token=a3aa65eb-8019-4cfa-97c9-e686ccc62979" alt=""><figcaption></figcaption></figure>

Then, in repeater go to the JSON Web Token tab and then to the attack button to embed the JWK.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FRWaDjhLi1wx25hO6NnMV%2Fimage.png?alt=media&amp;token=fbfff141-a77f-4750-8507-61783d99f639" alt=""><figcaption></figcaption></figure>

Next, click sign and select the token.

## Injecting self-signed JWTs via the jku parameter

Instead of embedding public keys directly using the `jwk` header parameter, some servers let you use the `jku` (JWK Set URL) header parameter to reference a JWK Set containing the key. When verifying the signature, the server fetches the relevant key from this URL.

First, using the burp extension "JWT Editor" we generate a new RSA key pair and copy the JWK. Now we should paste it in a file on a webserver which you control. For example /jwks.json:

```json
{
    "keys": [
        {
            "kty": "RSA",
            "e": "AQAB",
            "kid": "75d0ef47-af89-47a9-9061-7c02a610d5ab",
            "n": "o-yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw-fhvsWQ"
        },
        {
            "kty": "RSA",
            "e": "AQAB",
            "kid": "d8fDFo-fS9-faS14a9-ASf99sa-7c1Ad5abA",
            "n": "fc3f-yy1wpYmffgXBxhAUJzHql79gNNQ_cb33HocCuJolwDqmk6GPM4Y_qTVX67WhsN3JvaFYw-dfg6DH-asAScw"
        }
    ]
}
```

Next, in the JWT token we specify a new header "jku" with the URL to our evil server specified:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FzIInASlIQX5WQnFfdnE9%2Fimage.png?alt=media&amp;token=3474cdcb-9fd8-4322-9741-dee3851496ea" alt=""><figcaption></figcaption></figure>

Finally, we sign the JWT using the RSA key that we generated in the first step. Note: the value in "kid" should match!

## JWT authentication bypass via kid header path traversal

Verification keys are often stored as a JWK Set. In this case, the server may simply look for the JWK with the same `kid` as the token. However, the JWS specification doesn't define a concrete structure for this ID - it's just an arbitrary string of the developer's choosing. For example, they might use the `kid` parameter to point to a particular entry in a database, or even the name of a file.

If this parameter is also vulnerable to [directory traversal](https://portswigger.net/web-security/file-path-traversal), an attacker could potentially force the server to use an arbitrary file from its filesystem as the verification key.

A method to exploit this vulnerability is to generate a symmetric key with a empty value and point the path of the key  to /dev/null. Then the key matches because both are empty.&#x20;

First using the JWT editor extension in Burp, we generate a new symmetric key with a empty secret:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FiOX9Y6oVpa9Go8RFcyor%2Fimage.png?alt=media&amp;token=64149bea-4f4e-471e-97c0-080a04a72414" alt=""><figcaption></figcaption></figure>

Next, in the JWT header we specify the path to /dev/null:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FbJhMruemiNpS53QQObnK%2Fimage.png?alt=media&amp;token=65734737-7e21-45af-ac64-b555bb3f7800" alt=""><figcaption></figcaption></figure>

We sign the token using the empty symmetric key and that should make it valid.
