---
title: Bypassing Flutter TLS/SSL Verification When reFlutter Fails
source_url: https://petruknisme.medium.com/bypassing-flutter-tls-ssl-verification-when-reflutter-fails-a4c41ff758a3
fetched_at: 2026-09-20T01:53:11Z
license: unspecified
category: mobile/flutter
---
Author: Aan (petruknisme.medium.com) - Apr 29, 2026 - 11 min read

Tags: Flutter, reFlutter, Mobile Pentesting, Frida, Reverse Engineering

> Note: captured from the source page; the tail of the article was truncated at fetch time - see the source URL for the complete Frida script.

During Flutter mobile application assessments, `reFlutter` is often the fastest option for bypassing TLS/SSL verification and redirecting traffic to an interception proxy. However, it does not always work. Unsupported engine hashes, debug Flutter engines, missing `libapp.so`, or newer Flutter versions can prevent the automated workflow from continuing.

This article documents a manual approach for those cases. Instead of relying on precomputed offsets, the exact Flutter engine version used by the target application is identified, the corresponding BoringSSL revision is resolved, and the certificate verification routine is located directly inside `libflutter.so`. The final offset can then be hooked with Frida to force the verification result to success.

This workflow is intended for authorized mobile application security testing only.

## Overview

Flutter embeds BoringSSL inside the Flutter engine. On Android, the relevant code is compiled into `libflutter.so`. When the application validates a TLS certificate chain, the verification flow eventually reaches a BoringSSL routine responsible for validating the certificate chain and returning either success or failure.

The manual workflow is:

- Extract the Flutter shared libraries from the APK.
- Identify the Flutter engine version or engine commit from the snapshot hash.
- Resolve the BoringSSL revision used by that engine.
- Inspect the BoringSSL source to identify the target verification function.
- Locate the compiled function inside libflutter.so using Ghidra.
- Convert the Ghidra function address into a module-relative offset.
- Hook the function with Frida and force the return value to success.

This keeps the process deterministic and avoids guessing offsets from unrelated Flutter builds.

## When manual is required

The manual workflow is useful when `reFlutter` cannot process the APK. One common failure is an unsupported engine engine snapshot hash:

```
❯ reflutter app-release.apk
[*] Processing... Engine SnapshotHash: e80067bfb076e849f6ac3ba5a047eb2e
This engine is currently not supported. Most likely this flutter application uses
the Debug version engine which you need to build manually using Docker at the moment.
More details: https://github.com/Impact-I/reFlutter
```

In this situation, `reFlutter` has already extracted the snapshot hash, but it cannot map it to a supported engine offset. The hash can still be used as the starting point for manual analysis.

Another common failure is a missing Flutter application library:

```
❯ reflutter app.apk
[*] Processing...
Is this really a Flutter app? There was no libapp.so (Android) or App (iOS) found in
the package. Make sure it is arm64-v8a/libapp.so or App.framework/App file in the
package. If flutter library name differs you need to rename it properly before patching.
```

If this error appears, verify that the APK contains the expected Flutter libraries, especially: `lib/arm64-v8a/libapp.so` and `lib/arm64-v8a/libflutter.so`. If the libraries are missing, extract the correct APK build or confirm whether the application uses a different packaging layout.

## Prerequisites

The following tools are used in this workflow:

- apktool or unzip, to extract APK contents.
- reFlutter, to retrieve or compare Flutter engine snapshot hashes.
- Ghidra, to locate the compiled verification routine in `libflutter.so`.
- Frida, to hook the target function at runtime.
- Basic command-line tools such as curl, grep, sed, awk, base64, and unzip.

## 1. Identify the Flutter engine version

If `reFlutter` already printed the engine snapshot hash, that hash can be used directly. Otherwise, compute the snapshot hash from `libapp.so`.

The `get_snapshot_hash.py` script can be taken from the reFlutter repository:

```
https://github.com/Impact-I/reFlutter/blob/main/scripts/get_snapshot_hash.py
```

Important: compute the snapshot hash from `libapp.so`, not `libflutter.so`. Running the script against `libflutter.so` produces an invalid result for this purpose.

Example using the wrong file:

```
❯ python get_snapshot_hash.py app-release/lib/arm64-v8a/libflutter.so
34444444444444444444444444443444
```

Example using the correct file:

```
❯ python get_snapshot_hash.py app-release/lib/arm64-v8a/libapp.so
78da37fed6bf1489361a312568249f3f
```

Next, match the snapshot hash against reFlutter's engine hash table:

```
curl https://raw.githubusercontent.com/Impact-I/reFlutter/refs/heads/main/enginehash.csv | grep 78da37fed6bf1489361a312568249f3f
```

Output:

```
3.41.1,3452d735bd38224ef2db85ca763d862d6326b17f,78da37fed6bf1489361a312568249f3f
```

This means:

- Flutter version: 3.41.1
- Flutter engine commit: 3452d735bd38224ef2db85ca763d862d6326b17f
- Snapshot hash: 78da37fed6bf1489361a312568249f3f

### 1b. Generate engine hash table (optional)

If the snapshot hash is not found in `enginehash.csv`, a fresh table can be generated from the reFlutter scripts:

```
git clone https://github.com/Impact-I/reFlutter
cd reFlutter/scripts
python gen_enginehash.py
```

This process clones Flutter release data and can take time because the Flutter repository is large. You may see matches in `enginehash.csv` or `scripts/enginehash.tmp.csv`. Use the matching line that contains your hash and read the version and engine commit from it.

## 2. Download the exact Flutter source

Download the source archive for the matching Flutter version:

```
wget https://github.com/flutter/flutter/archive/refs/tags/3.41.1.zip
```

The source archive is needed because the Flutter repository contains the `DEPS` file that maps Flutter to the exact dependency revisions used by that release, including BoringSSL.

## 3. Find the BoringSSL revision

Read the `DEPS` file from the Flutter source archive and search for the BoringSSL revision:

```
unzip -p 3.41.1.zip | grep boringssl_rev
```

Output:

```
'dart_boringssl_rev': '9f138d05879fcf61965d1ea9d6c8b2cfc8bc12cb',
'https://boringssl.googlesource.com/boringssl.git' + '@' + Var('dart_boringssl_rev'),
```

The BoringSSL commit used by this Flutter release is:

```
9f138d05879fcf61965d1ea9d6c8b2cfc8bc12cb
```

## 4. Inspect the BoringSSL source

Retrieve the relevant BoringSSL source file from the resolved commit:

```
curl "https://boringssl.googlesource.com/boringssl/+/9f138d05879fcf61965d1ea9d6c8b2cfc8bc12cb/ssl/ssl_x509.cc?format=TEXT" | base64 --decode > ssl_x509.cc
```

Explanation:

- `+/COMMIT_HASH/` pins the exact revision from `DEPS`.
- `/ssl/ssl_x509.cc` is the file path inside the repo.
- `?format=TEXT` makes the server return base64-encoded content, which we decode into the file.

Search for `ssl_crypto_x509_session_verify_cert_chain`:

- This is the BoringSSL routine that performs the certificate chain verification for a session.
- Flutter's TLS verification path eventually calls this function, so forcing its return value to success disables the check.

First locate the function and its line number:

```
grep -n "ssl_crypto_x509_session_verify_cert_chain" ssl_x509.cc
```

Example output:

```
201:static bool ssl_crypto_x509_session_verify_cert_chain(SSL_SESSION *session,
357: ssl_crypto_x509_session_verify_cert_chain,
```

The line that contains `static bool ...` is the function definition (line 201 in this case). The other line is just a reference. Use that line number to print a small window around the function:

```
nl -ba ssl_x509.cc | sed -n '201,266p'
```

The function body (abridged) looks like:

```c
static bool ssl_crypto_x509_session_verify_cert_chain(SSL_SESSION *session,
                                                      SSL_HANDSHAKE *hs,
                                                      uint8_t *out_alert) {
  *out_alert = SSL_AD_INTERNAL_ERROR;
  STACK_OF(X509) *const cert_chain = session->x509_chain;
  if (cert_chain == nullptr || sk_X509_num(cert_chain) == 0) {
    return false;
  }
  // ... store/ctx setup, verify params inheritance ...
  int verify_ret;
  if (ssl_ctx->app_verify_callback != nullptr) {
    verify_ret = ssl_ctx->app_verify_callback(ctx.get(), ssl_ctx->app_verify_arg);
  } else {
    verify_ret = X509_verify_cert(ctx.get());
  }
  session->verify_result = X509_STORE_CTX_get_error(ctx.get());
  // If |SSL_VERIFY_NONE|, the error is non-fatal, but we keep the result.
  if (verify_ret config->verify_mode != SSL_VERIFY_NONE) {  // (as captured; see source)
    *out_alert = SSL_alert_from_verify_result(session->verify_result);
    return false;
  }
  ERR_clear_error();
  return true;
}
```

You should see the `OPENSSL_PUT_ERROR` call around line 239 in that function.

Note why the line number matters:

- `OPENSSL_PUT_ERROR` encodes the source line number into the error path.
- That line number becomes a constant in the compiled code.
- We search for that constant (239 in this example) to find the function in `libflutter.so`. If your line number is different, use your line number instead of 239.

## 5. Locate the function in Ghidra

Open `libflutter.so` in Ghidra and let analysis complete.

- Search for scalar value 239 (either Search All or Search Selection).
- Filter by `mov` instructions.
- Click through candidates until the decompiler shows a function with 3 parameters that matches the BoringSSL signature above.

In this case, the candidate function appears in Ghidra as:

```c
void FUN_00840950(undefined8 param_1, undefined8 param_2, undefined1 *param_3) {
  char *pcVar1; int iVar2; int iVar3; long lVar4; undefined1 uVar5;
  // ...
}
```

This is a strong candidate because the function has three parameters, which matches the source signature:

```c
static bool ssl_crypto_x509_session_verify_cert_chain(
    SSL_SESSION *session, SSL_HANDSHAKE *hs, uint8_t *out_alert)
```

In the compiled binary, argument types are not preserved, so Ghidra only marks an argument as a pointer when it can prove pointer-style usage. That is why the source shows three pointers while the decompiler may show two raw 64-bit arguments and one pointer. The count and usage still match the source, which makes this candidate more convincing.

After we identify a candidate from the `mov` results, double-click the function (`FUN_00840950`) in the decompiler to jump to its address.

The address is `0x00840950`. Keep this address, because we will use it to compute the final offset.

## 6. Convert the Ghidra address to a Frida offset

The address shown by Ghidra is an absolute address based on the image base used during analysis. Frida needs a module-relative offset from the loaded base address of `libflutter.so`.

Find the image base used by Ghidra: open Window -> Memory Map and read the Image Base value. In the example the header shows `Image Base: 00100000` (so the base is `0x100000`).

Compute the final offset using `FUNCTION_ADDRESS - 0x00100000`:

```
0x00840950 - 0x00100000 = 0x00740950
```

So the final offset is: `0x00740950`

## 7. Hook the function with Frida

Before the hook is applied, HTTPS requests fail because the application rejects the proxy certificate.

Use Frida to hook the verification function and force it to return success. Replace `<OFFSET>` with the offset from the offset calculation above:

```javascript
function attachNow() {
  var module = Process.findModuleByName("libflutter.so");
  if (!module) return false;
  console.log(`[+] libflutter is loaded at ${module.base}`);
  session_verify_cert_chain(module.base.add(<OFFSET>));
  return true;
}

function session_verify_cert_chain(address) {
  Interceptor.attach(address, {
    onLeave: function (retval) {
      retval.replace(0x1);
      console.log(`[+] session_verify_cert_chain retval: ${retval}`);
    }
  });
}

if (!attachNow()) {
  var do_dlopen = null;
  var call_constructor = null;
  Process.findModuleByName("linker64").enumerateSymbols().forEach(function (symbol) {
    if (symbol.name.indexOf("do_dlopen") >= 0) { do_dlopen = symbol.address; }
    if (symbol.name.indexOf("call_constructor") >= 0) { call_constructor = symbol.address; }
  });
  if (!do_dlopen || !call_constructor) {
    console.log("[-] Could not find do_dlopen/call_constructor");
  } else {
    var lib_loaded = false;
    Interceptor.attach(do_dlopen, function () {
      // wait for libflutter.so to be loaded, then attach (article continues in source)
      // [truncated at fetch time]
```

The remainder of the article (full delayed-attach logic and verification screenshots) is available at the source URL.
