---
title: "Android Physical Attacks"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/android-app-pentesting/android-physical-attacks.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile/android
---

## BFU / AFU, FBE, and physical extraction attacks

For **mobile app pentests** and **seizure/forensics threat modeling**, it is useful to separate the device into 2 states:[\[1\]](#references)

- **BFU (Before First Unlock)** : after boot and before the user unlocks once.**Credential Encrypted (CE)** data is still cryptographically protected.
- **AFU (After First Unlock)** : the user already unlocked the device after boot.**CE keys are already resident in memory** , so the lockscreen becomes mostly a**UI barrier** unless the device reboots.

### Android credential path that matters during physical attacks

Modern Android credential protection is not just the lockscreen UI:[\[2\]](#references)

- **Gatekeeper** verifies PIN/password/pattern and rate-limits guesses.<sup>[\[3\]](#references)</sup>
- **Keymaster / KeyMint** releases**authentication-bound keys** only after a valid Gatekeeper token.<sup>[\[5\]](#references)</sup>
- **Synthetic Password** protects the CE keys used by`fscrypt` .<sup>[\[1\]](#references)</sup>
- **StrongBox / Weaver** (when present) moves part of the secret material and throttling into a separate hardened chip.<sup>[\[4\]](#references)</sup>

The important implication is that **TEE compromise and lockscreen bypass are not always the same thing**. On FBE devices, attackers often still need the credential-derived material used to decrypt the **Synthetic Password**.[\[1\]](#references)

Useful artifact locations during rooted/physical analysis:[\[1\]](#references)

- scrypt parameters + salt used by Synthetic Password live under **`/data/system_de/<user_id>/spblob`**
- background task snapshots often live under **`/data/system_ce/0/snapshots`**

### BFU attack pattern on devices without a Secure Element

On devices **without** a real Secure Element / StrongBox-backed Weaver path, the reusable pattern is:[\[1\]](#references)

1. Gain **pre-OS code execution** via**Boot ROM** bug or vendor mode such as**MediaTek Download Mode** /**Qualcomm EDL** .
2. Patch the early boot chain so later stages no longer verify signatures.
3. Load a modified **Trusted OS / TEE** and patch**Gatekeeper** to accept arbitrary credentials.
4. Abuse **Keymaster** to recover intermediate key material.
5. Extract the encrypted **Synthetic Password** and brute-force the credential**offline** .

That offline step converts the problem from device-side rate limiting into attacker-side compute:[\[1\]](#references)

```
for candidate in candidates:
    stretched = scrypt(candidate, salt, params_from_spblob)
    applicationId = derive_application_id(stretched, other_material)
    plaintext = aes_gcm_decrypt(encrypted_synthetic_password, applicationId)
    if gcm_tag_valid(plaintext):
        return candidate
```
If you need the early-boot details for MediaTek devices, review:

[Android Mediatek Secure Boot Bl2 Ext Bypass El3](../../hardware-physical-access/firmware-analysis/android-mediatek-secure-boot-bl2_ext-bypass-el3.html)

Also note that **public tooling such as [MTKClient](https://github.com/bkerler/mtkclient)** makes several MediaTek Boot ROM / download-mode workflows practical on affected chipsets.[\[6\]](#references)

### Biometric TA AuthToken forgery: root-to-CE bypass without patching Gatekeeper

A second reusable pattern is to **abuse biometric Trusted Applications (fingerprint / face TAs) that share the same AuthToken HMAC trust domain as Gatekeeper and Keymaster / KeyMint**. On Android, a successful authenticator returns a signed **`hw_auth_token_t`** proving who authenticated, by which method, and when. If a biometric TA can be tricked into **signing attacker-controlled data** or **leaking the shared per-boot HMAC key**, Android root can be upgraded into **PIN recovery** and sometimes **BFU CE decryption**.[\[7\]](#references)

Relevant AuthToken properties:[\[7\]](#references)

- `hw_auth_token_t` is a fixed**69-byte** structure with fields such as`challenge` ,`user_sid` ,`authenticator_id` ,`authenticator_type` ,`timestamp` , and a trailing**32-byte HMAC-SHA256** computed with a**per-boot shared secret** .
- `authenticator_type = 1` is the important value for**Gatekeeper / PIN** tokens.
- Keymaster / KeyMint validates the HMAC, freshness, SID binding, and expected authenticator type before releasing authentication-bound key operations.

Common exploitation patterns seen in vendor biometric TAs:[\[7\]](#references)

1. **Signing oracle (`GET_AUTH_OBJ`-style bugs)** : a TA command accepts an arbitrary 69-byte buffer and simply HMAC-signs it, without checking that a fingerprint/face match actually happened.
2. **Biometric result oracle + verifier confusion** : a TA emits a valid**type-2** biometric token without a real match, and Keymaster incorrectly accepts it for operations that should require**type-1** Gatekeeper authentication.
3. **Error-path secret leakage** : HMAC verification failures print or return the shared**32-byte per-boot AuthToken HMAC key** via TrustZone logs, shared memory, or even`dmesg` -reachable secure logs.
4. **TA memory disclosure / corruption** : out-of-bounds reads or arbitrary-read primitives leak plaintext per-boot HMAC keys from heap / stack / BSS after defeating weak TA ASLR.

Once the attacker can mint a valid **type-1** token (or a verifier incorrectly accepts **type-2**), the remaining CE attack looks very similar to the early-boot TEE-patching chain, but **without** modifying Gatekeeper itself:[\[7\]](#references)

1. Obtain **Android root / kernel EL1 R/W** .
2. Invoke the biometric TA directly with **`libTEEC`** or an equivalent TEE client.
3. Forge or request a signed **Gatekeeper-typed AuthToken** .
4. Pass that token to **Keymaster / KeyMint** to decrypt the first-stage**Synthetic Password** blob.
5. Brute-force the real PIN **offline** using the AES-GCM tag as a correctness oracle.

Minimal attacker view:[\[7\]](#references)

```
at = forge_gatekeeper_authtoken()                  # type = 1, HMAC valid
spblob = read('/data/system_de/<uid>/spblob/...')
intermediate = keymaster_decrypt(at, spblob)
for pin in range(1_000_000):
    key = derive_synthetic_pw(intermediate, pin)
    if aes_gcm_decrypt(intermediate, key):
        return pin
```
Operational notes:[\[7\]](#references)

- **BFU impact** usually requires a forged**type-1 / Gatekeeper** token that Keymaster accepts before first unlock.
- **AFU-only** cases can still exist if the device incorrectly accepts biometric**type-2** tokens after first unlock.
- Multiple dormant fingerprint TAs in one firmware image increase attack surface because **each TA may hold the same per-boot AuthToken HMAC material** .
- **StrongBox / Weaver-backed** designs reduce the usefulness of this chain because recovering the Keymaster-gated intermediate is not always enough to obtain an offline brute-force oracle.

### StrongBox / Weaver changes the brute-force model

If the device uses **Weaver** backed by a separate Secure Element / StrongBox, compromising Android or even the TEE is usually **not enough** to obtain an offline brute-force primitive:[\[1\]](#references)

- the Weaver secret should remain inside the separate chip
- throttling is enforced by hardware outside the main SoC
- guesses often remain **online only** , sometimes with exponential backoff

This is why **short PINs** are still weak, but a **long alphanumeric password** becomes much more resistant on properly implemented StrongBox devices.[\[1\]](#references)

### AFU USB exploitation: lockscreen is not the boundary anymore

In **AFU** state, many forensic chains no longer attack the password. They attack the **USB-reachable kernel attack surface** exposed while the device is locked:[\[1\]](#references)

- **HID**
- **USB Audio / ALSA**
- **UVC**
- **MTP / MSC**

A malicious peripheral emulator can present crafted descriptors/reports to reachable drivers, trigger memory corruption or information leaks, gain kernel code execution, and then read **already-decrypted CE storage**. At that point, the lockscreen is just UI and the attacker can pivot to **full filesystem extraction**, app databases, cached tokens, previews, and any application secrets that remain in memory.[\[1\]](#references)

### iOS parallel: USB policy bugs reopen AFU attack surface

The same idea appears on iOS:

- **checkm8** is the classic**Boot ROM** example for older A5-A11 devices.<sup>[\[1\]](#references)</sup>
- Newer iPhone physical attacks tend to focus on **AFU USB access** and**USB Restricted Mode** bypasses.<sup>[\[1\]](#references)</sup>
- **CVE-2025-24200** is a good example of a**policy-enforcement bug** where a privileged path could re-enable USB data on a locked device.<sup>[\[8\]](#references)</sup>

For defenders and app testers, the important lesson is simple: **if the target device is AFU, assume filesystem-level compromise can expose app data unless the app adds its own cryptographic boundary**.

## References
