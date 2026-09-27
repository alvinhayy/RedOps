---
title: "Debugging Client Side JS"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/xss-cross-site-scripting/debugging-client-side-js.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

# Debugging Client-Side JavaScript

## `debugger;`

`debugger;`
When developer tools are open, a `debugger;` statement pauses execution at that point unless breakpoints are disabled. Adding the statement to a persistent local copy is one way to keep the pause point across reloads.[\[1\]](#references)

## Overrides

Chrome DevTools Local Overrides stores a local replacement for a network resource and serves that replacement on subsequent page loads.[\[2\]](#references)

1. Open **DevTools > Sources > Overrides** .
2. Select an empty local folder and allow DevTools to access it.
3. In the **Page** tree, right-click the target script and select**Override content** or**Save for overrides** , depending on the Chrome version.
4. Add `debugger;` , save the file, and reload the page.

The saved local copy now replaces the matching network resource while overrides are enabled. Changes therefore persist across reloads, but they affect only your local browser profile.[\[2\]](#references)

The XSS challenge walkthrough in reference 3 demonstrates this `debugger;` and Local Overrides workflow during a practical client-side analysis.[\[3\]](#references)

## References

- [1] [Chrome for Developers - JavaScript debugging reference](https://developer.chrome.com/docs/devtools/javascript/reference)
- [2] [Chrome for Developers - Override web content and HTTP response headers locally](https://developer.chrome.com/docs/devtools/overrides/)
- [3] [YouTube - 4 hackers, one XSS challenge](https://www.youtube.com/watch?v=BW_-RCo9lo8&t=1529s)
