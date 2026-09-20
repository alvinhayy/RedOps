---
title: "Vuejs"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/vuejs.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## XSS Sinks in Vue.js

### v-html Directive

The `v-html` directive renders **raw** HTML. `<script>` elements inserted through the underlying `innerHTML` operation are normally inert, but active attributes and elements such as an image `onerror` can still produce XSS. Never pass unsanitized user input to `v-html`.[\[1\]](#references)[\[3\]](#references)

```
<div id="app">
  <div v-html="htmlContent"></div>
</div>
<script>
  new Vue({
    el: '#app',
    data: {
      htmlContent: '<img src=x onerror=alert(1)>'
    }
  })
</script>
```
### v-bind with src or href

Binding a user string to URL-bearing attributes (`href`, `src`, `xlink:href`, `formaction` …) lets payloads such as `javascript:alert(1)` run when the link is followed.[\[2\]](#references)[\[3\]](#references)

```
<div id="app">
  <a v-bind:href="userInput">Click me</a>
</div>
<script>
  new Vue({
    el: '#app',
    data: {
      userInput: 'javascript:alert(1)'
    }
  })
</script>
```
### v-on with user-controlled handlers

If an attacker controls a Vue **template**, directive expressions such as `v-on:click="..."` become code in the compiled render function. Merely storing the string `alert(1)` in a data property does not execute it as JavaScript; the dangerous condition is untrusted template source.[\[3\]](#references)

```
<div id="app">
  <!-- Dangerous if an attacker controls this template expression: -->
  <button v-on:click="alert(document.domain)">Click me</button>
</div>
<script>
  new Vue({
    el: '#app',
    data: {}
  })
</script>
```
### Dynamic attribute / event names

User-supplied names in `v-bind:[attr]` or `v-on:[event]` expand the attack surface and can bypass application allowlists. Vue applies its own attribute/event handling and CSP still applies, so validate behavior against the deployed Vue version rather than assuming every `on*` name becomes a native handler.[\[3\]](#references)

```
<img v-bind:[userAttr]="payload">
<!-- userAttr = 'onerror', payload = 'alert(1)' -->
```
### SSR attribute-name splitting in object `v-bind`

`v-bind`
When auditing SSR, test the **keys** of objects spread with `v-bind="attrs"`, not only their values. `@vue/server-renderer` through 3.5.41 checked dynamic attribute names against a blacklist that omitted carriage return (`U+000D`). A raw CR in an attacker-controlled key therefore reached the HTML response; the browser normalised it to LF and split one intended name into several attributes. This can create a zero-interaction XSS when an object from a CMS, form builder, API or stored JSON is spread onto an element. The published advisory listed no patched version at publication time.[\[9\]](#references)

```
// Reaches <input v-bind="attrs"> during SSR
const attrs = {
  ['x\rautofocus\ronfocus']: 'alert(document.domain)'
}
// Browser parses: x="" autofocus="" onfocus="alert(document.domain)"
```
This is an **SSR-only** parser differential: client-side Vue uses `setAttribute()`, which rejects such a name. Send the key through the real input path (for example, JSON `"x\rautofocus\ronfocus"`), inspect the raw response bytes before hydration, and verify whether intermediaries preserve the CR. A source-code review should trace both property names and values into `v-bind="object"` or equivalent render-function props.[\[9\]](#references)

### Dynamic component (`<component :is>`)

`<component :is>`)
Allowing an untrusted component identifier in `:is` may expose components that were not intended for the user. A string containing `<script>` is not automatically compiled as an inline template; server compromise requires a separate path that treats attacker input as template source.[\[3\]](#references)

```
<component :is="userChoice"></component>
<!-- userChoice must be restricted to an allowlist of intended components -->
```
### Untrusted templates in SSR

During server-side rendering, the template runs **on your server**; injecting user HTML can escalate XSS to full Remote Code Execution (RCE). CVEs in `vue-template-compiler` prove the risk.[\[3\]](#references)

```
// DANGER – never do this
const app = createSSRApp({ template: userProvidedHtml })
```
Vue CSTI payloads and version-specific compiler gadgets are documented in [Client Side Template Injection](../../pentesting-web/client-side-template-injection-csti.html); keep this page focused on Vue-specific sinks and SSR boundaries.

### Filters / render functions that eval

Legacy filters that build render strings or call `eval`/`new Function` on user data are another XSS vector—replace them with computed properties.[\[3\]](#references)

```
Vue.filter('run', code => eval(code))   // DANGER
```
## Other Common Vulnerabilities in Vue Projects

### Prototype pollution and HTML-context confusion in `vue-i18n`

`vue-i18n`
`vue-i18n`’s flat-JSON resolver has accepted `__proto__` paths that write to `Object.prototype`. Trace whether an attacker can supply locale objects or remote translation bundles, then look for polluted properties reaching a secondary gadget rather than treating the write alone as code execution.[\[4\]](#references)

```
handleFlatJson({ '__proto__.polluted': 'yes' })
console.log(({}).polluted) // "yes" on affected versions
```
Do not treat `escapeParameterHtml: true` as a sanitizer for the **final translation string**. Affected `vue-i18n` releases escaped interpolated parameters as text but could still produce executable markup when a translation placed the parameter in an HTML attribute and the result was passed to `v-html`. This is particularly relevant for remotely managed translations and low-privileged locale editors.[\[10\]](#references)

```
<!-- message: <img src=x onerror="{payload}"> -->
<p v-html="$t('warning', { payload: 'alert(document.domain)' })"></p>
```
Audit every `$t()`/`t()` flow into `v-html` and sanitize the complete rendered HTML under an explicit policy. The reviewed advisory identifies 9.14.5, 10.0.8 and 11.1.10 as the first patched release in each maintained branch.[\[10\]](#references)

### Open redirects with vue-router

Applications sometimes use an unchecked `next` value with `window.location` or an external-navigation helper, creating an open redirect. The earlier page specifically named `router.push`, `<router-link>`, and a `javascript:` destination. Preserve those as test inputs for application wrappers and dynamic URL props, but Vue Router navigation is normally route-oriented, so do not assume the bare router accepts every external scheme without validating the deployed version and normalization path.[\[3\]](#references)[\[6\]](#references)

```
window.location.assign(this.$route.query.next) // DANGER: validate origin/scheme
```
Prefer a server-side mapping from a short identifier to an approved destination; if a URL must be accepted, apply an allowlist rather than a denylist.[\[6\]](#references)

### CSRF in Axios / fetch

SPAs still need deliberate CSRF defenses. `SameSite=Lax` or `Strict` blocks cookies on many cross-site requests, but coverage depends on method, navigation context, browser behavior, and whether sibling subdomains are attacker-controlled.[\[7\]](#references)

```
axios.post('/api/transfer', data, {
  headers: { 'X-CSRF-TOKEN': token }
})
```
### Click-jacking

Prevent framing with CSP `frame-ancestors`; `X-Frame-Options` is a useful legacy fallback. Sending both is defense in depth, not a requirement for standards-compliant modern browsers.[\[8\]](#references)

```
X-Frame-Options: DENY
Content-Security-Policy: frame-ancestors 'none';
```
### Content-Security-Policy pitfalls

Runtime template compilation can conflict with a strict CSP. Prefer a runtime-only build with precompiled templates so the application does not need eval-like compilation; confirm the exact Vue version and build rather than adding `'unsafe-eval'` blindly.[\[3\]](#references)

```
Content-Security-Policy: default-src 'self'; script-src 'self';
```
### Supply-chain attacks (node-ipc – March 2022)

The sabotage of **node-ipc**—pulled by Vue CLI—showed how a transitive dependency can run arbitrary code on dev machines. Pin versions and audit often.[\[5\]](#references)

```
npm ci --ignore-scripts   # safer install
```
## Hardening Checklist

1. **Sanitise** every string before it hits`v-html` (DOMPurify).
2. **Whitelist** allowed schemes, attributes, components, and events; never spread attacker-controlled property names into SSR elements.
3. **Avoid `eval`** and dynamic templates altogether.
4. **Patch dependencies weekly** and monitor advisories.
5. **Send strong HTTP headers** (CSP, HSTS, XFO, CSRF).
6. **Lock your supply chain** with audits, lockfiles, and signed commits.

## References
