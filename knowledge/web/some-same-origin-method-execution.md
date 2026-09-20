---
title: "SOME - Same Origin Method Execution"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/xss-cross-site-scripting/some-same-origin-method-execution.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## Same Origin Method Execution

Sometimes an application provides only constrained JavaScript execution, such as control of a callback identifier that the server inserts into a script response.

If that execution occurs in a page with a useful DOM, it may invoke sensitive methods or click controls. The vulnerable callback endpoint itself, however, is often a minimal document with no valuable UI.

SOME bridges that gap: the constrained script runs in a same-origin auxiliary window and uses its `window.opener` reference to reach a more interesting document in the opener.[\[1\]](#references)

Basically, the attack flow is the following:

- Find a **callback that you can abuse** (potentially limited to [\w\._]).
  - If it is not limited and arbitrary JavaScript is possible, treat it as ordinary XSS.
- Make the **victim open a page** controlled by the**attacker**
- The **page will open itself** in a**different window** (the new window will have the object**`opener`** referencing the initial one)
- The **initial page** will load the**page** where the**interesting DOM** is located.
- The **second page** will load the**vulnerable page abusing the callback** and using the**`opener`** object to**access and execute some action in the initial page** (which now contains the interesting DOM).

Caution

A window reference can survive navigation of the referenced browsing context, although same-origin policy checks are evaluated against the documents’ current origins. Modern isolation features such as `Cross-Origin-Opener-Policy` and `rel=noopener` can sever the relationship.

To dereference the opener’s DOM, the auxiliary page and the opener’s current document must be **same-origin**. The chain therefore needs same-origin script execution, such as the vulnerable callback endpoint itself.

### Exploitation

- Use the SOME Generator to build a PoC for this attack class.<sup>[\[3\]](#references)</sup>
- Use the targeting tool to derive a clickable element’s DOM method path.<sup>[\[4\]](#references)</sup>

### Example

- The SOME Playground provides a deliberately vulnerable example.<sup>[\[5\]](#references)</sup>  - In this example the server generates JavaScript from the callback parameter: `<script>opener.{callback_content}</script>` . That is why the callback itself does not need to repeat`opener` .
- In this example the server generates JavaScript from the callback parameter:
- Also check this CTF writeup: [https://ctftime.org/writeup/36068](https://ctftime.org/writeup/36068)<sup>[\[2\]](#references)</sup>

## References
