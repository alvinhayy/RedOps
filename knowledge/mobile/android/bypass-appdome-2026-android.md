---
title: Bypass Appdome 2026 (Android)
source_url: https://medium.com/@farimarwat/bypass-appdome-2026-android-a55df53a52f0
fetched_at: 2026-09-20T02:00:14Z
license: unspecified
category: mobile/android
---

How to get inside an Appdome-protected Android app far enough to read its traffic, its secrets, and its detection logic — at both the Java and native level. This is a starting point for research, not a finished bypass.

**Disclosure & ethics** This is defensive security research. No live secrets — tokens, keys, or credentials — are published here; only *how* one would locate them and *that* they are exposed. Reverse engineering may conflict with an app’s Terms of Service, so this is shared for educational and research purposes. If you reproduce it, disclose responsibly: notify the vendor before publishing anything sensitive, and never post extracted production values.

**Test environment**

- Target: Appdome-hardened Android app, (Marriott Hotel) version **10.73.0**
- Tooling: **Frida 17.11.0** , rooted ARM64 emulator
- Date: **7 June 2026**

## What you walk away with

By the end, you can do three things to an Appdome-wrapped app that you couldn’t before:

- **Recover the hidden code.** Appdome’s real protection logic lives in an encrypted JAR that’s loaded and instantly deleted at runtime. You’ll grab it intact.
- **Buy a working window.** A handful of Java and native hooks suppress the self-kill long enough — roughly**12 seconds** — to navigate the app and run your own instrumentation.
- **Read the secrets.** Inside that window you can call Appdome’s own decryption routines and watch them hand you authorization tokens, crypto keys, and backend URLs in plaintext — alongside the live network traffic.

That’s enough to expand the research in any direction you want. None of it is a one-click bypass: Appdome’s detection runs in native code on threads that keep respawning, so the window is a *surface for analysis*, not a permanent defeat. That honesty matters — anyone telling you otherwise hasn’t watched the watchdog come back.

## 1. The hidden JAR — where the real code lives

Appdome doesn’t ship its protection logic in the open. It packs it encrypted inside the APK, decrypts it at launch into a throwaway folder, loads it, and **deletes it immediately** so you can’t pull it off disk later.

`/data/user/0/<pkg>/<random+pid>/pnqYFtamhD4eORGf6k0u.jar   ← decrypted, then unlinked`
The trick to catching it: the file has to exist on disk for the split second before it’s deleted. Hook the delete, copy the file first, then let the delete happen normally — blocking the delete itself trips other checks.

```
// hook libc remove/unlink/unlinkat; on the jar path, copy it out before deletion
function recoverDynamicJar() {
    var libc   = Process.getModuleByName("libc.so");
    var fopen  = new NativeFunction(libc.findExportByName("fopen"),  'pointer', ['pointer','pointer']);
    var fread  = new NativeFunction(libc.findExportByName("fread"),  'ulong',   ['pointer','ulong','ulong','pointer']);
    var fwrite = new NativeFunction(libc.findExportByName("fwrite"), 'ulong',   ['pointer','ulong','ulong','pointer']);
    var fclose = new NativeFunction(libc.findExportByName("fclose"), 'int',     ['pointer']);
    ['remove','unlink','unlinkat'].forEach(function (fn) {
        var p = libc.findExportByName(fn); if (!p) return;
        Interceptor.attach(p, { onEnter: function (a) {
            var path = (fn === "unlinkat" ? a[1] : a[0]).readUtf8String();
            if (path && path.indexOf(".jar") !== -1 && path.indexOf(".marriott.") !== -1) {
                var dst = "/data/data/<pkg>/files/recovered.jar";   // the app's own dir is writable
                var fi = fopen(Memory.allocUtf8String(path), Memory.allocUtf8String("rb"));
                var fo = fopen(Memory.allocUtf8String(dst),  Memory.allocUtf8String("wb"));
                var b = Memory.alloc(65536), n;
                while ((n = fread(b, 1, 65536, fi).valueOf()) > 0) fwrite(b, 1, n, fo);
                fclose(fi); fclose(fo);
                console.log("[+] jar recovered -> " + dst);
            }
        }});
    });
}
```
Pull it out and decompile:

```
adb shell su -c "cp /data/data/<pkg>/files/recovered.jar /sdcard/ && chmod 644 /sdcard/recovered.jar"
adb pull /sdcard/recovered.jar
jadx recovered.jar -d ./src
```
**Why not just grab it from** **/proc/<pid>/fd****?** The descriptor is already closed by the time the app is up, and chasing per-launch PIDs is slow. Hooking the delete is the reliable, repeatable method.

**Names rotate.** Every Appdome build renames its classes. The package prefix and the *behavior* stay the same, so you re-find things by what they do, not what they’re called — grep the decompiled source for `finishAndRemoveTask` + `killProcess` (the killer), `System.loadLibrary("loader")` (the bootstrap), or a class full of `public static native` methods (the native bridge).

## 2. The window — silence the kill, get time to work

The moment Appdome decides something’s wrong, it kills the app — from two directions:

- **Native:** raw`kill` /`exit` syscalls from its loader library.
- **Java:** a controller that finishes the activity and calls`Process.killProcess` .

Suppress both and you get a usable window — long enough to navigate a few screens and run your hooks before the native monitor respawns and re-asserts.

```
// (a) native backstop — block self-directed kill/exit signals
function nativeKillBlock() {
    var libc = Process.getModuleByName("libc.so");
    ["raise", "kill"].forEach(function (name) {
        var p = libc.findExportByName(name); if (!p) return;
        var orig = new NativeFunction(p, 'int', name === "kill" ? ['int','int'] : ['int']);
        Interceptor.replace(p, new NativeCallback(function () {
            var sig = name === "kill" ? arguments[1] : arguments[0];
            if (sig === 9 || sig === 6 || sig === 19) { console.log("[+] blocked " + name); return 0; }
            return orig.apply(null, arguments);
        }, 'int', name === "kill" ? ['int','int'] : ['int']));
    });
}
// (b) java executor — neutralize the kill chain + process exit
function javaKillBlock() {
    var J = Java.use("fGMwW2.fMjau6.jlvUS4");          // the killer (rotated name)
    ["jeeUH7", "lLanC4", "wUxb72", "fHLTp1"].forEach(function (m) { J[m].implementation = function () {}; });
    var P = Java.use("android.os.Process");
    P.killProcess.implementation = function (pid) { if (pid === P.myPid()) return; return this.killProcess(pid); };
    Java.use("java.lang.System").exit.implementation = function (c) {};
    Java.use("android.app.Activity").finishAndRemoveTask.implementation = function () {};
}
```
What’s inside the jar you just recovered is the real payoff: **heavy, sensitive detection logic** — root checks, Frida detection, Magisk detection, emulator detection, and device fingerprinting. A single logging pass over the native bridge prints Appdome’s entire threat model:

`RootedDevice` · `FridaDetected` · `MagiskManagerDetected` · `EmulatorFound` · `CodeInjectionDetected` · `ActiveDebuggerThreatDetected` · `AppIsDebuggable` · `DeveloperOptionsEnabled` · `NetworkProxyConfigured` · `AppIntegrityError` · plus a dozen SSL / certificate-pinning checks

You can watch each one being queried, and force the verdict to “clean”:

```
// the native threat-state query: (String[] threats) -> boolean[] answers
function blindThreatChecks() {
    var A = Java.use("fGMwW2.fMjau6.al0wb9");
    A.xUvJ60.overload('[Ljava.lang.String;').implementation = function (arr) {
        return Java.array('boolean', new Array(arr ? arr.length : 0).fill(false));  // all "not detected"
    };
}
```
That blinds the verdict the Java side reads. It does *not* stop the native threads from re-checking — which is exactly why the window is finite, and why this is a launchpad rather than a bypass.

## 3. The secrets — make Appdome decrypt its own data for you

Every meaningful string in the Appdome layer is encrypted and fetched through one decryptor function — here, something like `hcRLd3("pw6q")`, where the keys are tiny 3–5 character strings. You don't reverse the algorithm. **You just call it and watch.**

javascript

```
// hook the string decryptor and dump every key -> plaintext it resolves
function dumpSecrets() {
    var V = Java.use("fGMwW2.vovvx1.vl7l72");
    V.hcRLd3.implementation = function (key) {
        var out = this.hcRLd3(key);
        send(key + "  ==  " + out);
        return out;
    };
}
```
Run that with a little navigation and the decryptor pours out the crown jewels in cleartext — the things you actually want for research:

- **Authorization tokens** and embedded credentials
- **Encryption / decryption keys** the app uses for its own data
- **Backend URL endpoints** — the app’s APIs and Appdome’s own analytics
- Config flags, pinned-certificate identifiers, asset names

Pair that with a network hook — intercept `OkHttpClient` / the bridge interceptor and `peekBody()` the responses — and you can read the live traffic *and* the secrets that protect it, side by side.

*(Reminder: in your own write-up, describe that these exist — never publish the live values.)*

**Finding the decryptor in any build:** it’s the one static method called everywhere with a short string-literal argument, backed by a `static{}` initializer, a small alphabet / lookup table, and a string cache. Rotated name, same shape.

## 4. SharedPreferences

Shared Preferences keeps some sensitive data like sensor_data which is sent via the url request. Find in jadx for *getString(shared* and it will list methods for it. pick the one which takes three params. First as SharedPreferences Object and the second and third are string object.

## 5. Where to go from here

You now have the hidden code, a working window, and the keys. That’s a platform, not a destination. Natural next steps:

- **Go native.** The Java bridge methods are bound via`RegisterNatives` ; capture their addresses as they register and you get each detection routine's offset inside`libloader.so` — load that in Ghidra and read the actual root / Frida / Magisk logic.
- **Map the traffic.** With endpoints, tokens, and keys in hand, decode the app’s protected requests end to end.
- **Generalize.** Every Appdome app has this same skeleton — hidden jar, dual kill, one decryptor, one native bridge. The names change; the recipe doesn’t. Re-point the hooks by behavior and the same harness works on the next target.

The one thing to keep honest: the kill suppression is a **delay, not a kill switch**. The native watchdog comes back. Treat the window as your lab bench — get in, get what you need, and build the deeper analysis from there.

## Join in

I’ll keep expanding this in my free time, and **you’re welcome to join** — issues, PRs, and new findings all welcome:

🔗 **https://github.com/farimarwat/bypass-appdome-2026**

If you push an Appdome build forward — especially on the native `libloader.so` side — open a PR. The more builds we map, the more the behavioral fingerprints hold up across the name rotation.

*Run everything spawned —* *frida -U -f <pkg> -l harness.js* *— because the protection boots inside the Application class before anything else. Attach late and you've already missed*
