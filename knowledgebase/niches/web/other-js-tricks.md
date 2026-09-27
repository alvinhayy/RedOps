---
title: "Misc JS Tricks & Relevant Info"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/xss-cross-site-scripting/other-js-tricks.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## Javascript Fuzzing

### Valid JS Comment Chars

```
//This is a 1 line comment
/* This is a multiline comment*/
#!This is a one-line comment, but "#!" must be at the beginning of the line
-->This is a one-line comment, but "-->" must be at the beginning of the line
for (let j = 0; j < 128; j++) {
  for (let k = 0; k < 128; k++) {
    for (let l = 0; l < 128; l++) {
      if (j == 34 || k ==34 || l ==34)
        continue;
      if (j == 0x0a || k ==0x0a || l ==0x0a)
        continue;
      if (j == 0x0d || k ==0x0d || l ==0x0d)
        continue;
      if (j == 0x3c || k ==0x3c || l ==0x3c)
        continue;
      if (
         (j == 47 && k == 47)
         ||(k == 47 && l == 47)
        )
        continue;
  try {
      var cmd = String.fromCharCode(j) + String.fromCharCode(k) + String.fromCharCode(l) + 'a.orange.ctf"';
      eval(cmd);
  } catch(e) {
      var err = e.toString().split('\n')[0].split(':')[0];
      if (err === 'SyntaxError' || err === "ReferenceError")
        continue
      err = e.toString().split('\n')[0]
  }
     console.log(err,cmd);
  }
  }
}
//From: https://balsn.tw/ctf_writeup/20191012-hitconctfquals/#bounty-pl33z
// From: Heyes, Gareth. JavaScript for hackers: Learn to think like a hacker (p. 43). Kindle Edition.
log=[];
for(let i=0;i<=0xff;i++){
  for(let j=0;j<=0xfff;j++){
    try {
      eval(`${String.fromCodePoint(i,j)}%$£234$`)
      log.push([i,j])
    }catch(e){}
  }
}
console.log(log)//[35,33],[47,47]
```
### Valid JS New Lines Chars

```
//Javascript interpret as new line these chars:
String.fromCharCode(10) //0x0a
String.fromCharCode(13) //0x0d
String.fromCharCode(8232) //0xe2 0x80 0xa8
String.fromCharCode(8233) //0xe2 0x80 0xa8
for (let j = 0; j < 65536; j++) {
  try {
    var cmd = '"aaaaa";' + String.fromCharCode(j) + '-->a.orange.ctf"'
    eval(cmd)
  } catch (e) {
    var err = e.toString().split("\n")[0].split(":")[0]
    if (err === "SyntaxError" || err === "ReferenceError") continue
    err = e.toString().split("\n")[0]
  }
  console.log(`[${err}]`, j, cmd)
}
//From: https://balsn.tw/ctf_writeup/20191012-hitconctfquals/#bounty-pl33z
```
### Valid JS Spaces in function call

```
// Heyes, Gareth. JavaScript for hackers: Learn to think like a hacker (pp. 40-41). Kindle Edition.
// Check chars that can be put in between in func name and the ()
function x(){}
log=[];
for(let i=0;i<=0x10ffff;i++){
    try {
        eval(`x${String.fromCodePoint(i)}()`)
        log.push(i)
    }catch(e){}
}
console.log(log)v//9,10,11,12,13,32,160,5760,8192,8193,8194,8195,8196,8197,8198,8199,8200,8201,8202,813 232,8233,8239,8287,12288,65279
```
### **Valid chars to Generate Strings**

**Valid chars to Generate Strings**

```
// Heyes, Gareth. JavaScript for hackers: Learn to think like a hacker (pp. 41-42). Kindle Edition.
// Check which pairs of chars can make something be a valid string
log = []
for (let i = 0; i <= 0x10ffff; i++) {
  try {
    eval(`${String.fromCodePoint(i)}%$£234${String.fromCodePoint(i)}`)
    log.push(i)
  } catch (e) {}
}
console.log(log) //34,39,47,96
//single quote, quotes, backticks & // (regex)
```
### **Surrogate Pairs BF**

**Surrogate Pairs BF**

This technique won’t be very useful for XSS but it could be useful to bypass WAF protections. This python code receive as input 2bytes and it search a surrogate pairs that have the first byte as the the last bytes of the High surrogate pair and the the last byte as the last byte of the low surrogate pair.

```
def unicode(findHex):
    for i in range(0,0xFFFFF):
        H = hex(int(((i - 0x10000) / 0x400) + 0xD800))
        h = chr(int(H[-2:],16))
        L = hex(int(((i - 0x10000) % 0x400 + 0xDC00)))
        l = chr(int(L[-2:],16))
        if(h == findHex[0]) and (l == findHex[1]):
            print(H.replace("0x","\\u")+L.replace("0x","\\u"))
```
### `javascript{}:` Protocol Fuzzing

`javascript{}:` Protocol Fuzzing```
// Heyes, Gareth. JavaScript for hackers: Learn to think like a hacker (p. 34). Kindle Edition.
log=[];
let anchor = document.createElement('a');
for(let i=0;i<=0x10ffff;i++){
    anchor.href = `javascript${String.fromCodePoint(i)}:`;
    if(anchor.protocol === 'javascript:') {
        log.push(i);
    }
}
console.log(log)//9,10,13,58
// You can also brute-force other positions containing repeated characters
// Test one option
let anchor = document.createElement('a');
anchor.href = `javascript${String.fromCodePoint(58)}:alert(1337)`;
anchor.append('Click me')
document.body.append(anchor)
// Another way to test
<a href="javascript:alert(1337)">Test</a>
```
### [URL Fuzzing](#url-fuzzing)

```
// Heyes, Gareth. JavaScript for hackers: Learn to think like a hacker (pp. 36-37). Kindle Edition.
// Before the protocol
a = document.createElement("a")
log = []
for (let i = 0; i <= 0x10ffff; i++) {
  a.href = `${String.fromCodePoint(i)}https://hacktricks.wiki`
  if (a.hostname === "hacktricks.xyz") {
    log.push(i)
  }
}
console.log(log) //0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32
// Between the slashes
a = document.createElement("a")
log = []
for (let i = 0; i <= 0x10ffff; i++) {
  a.href = `/${String.fromCodePoint(i)}/hacktricks.xyz`
  if (a.hostname === "hacktricks.xyz") {
    log.push(i)
  }
}
console.log(log) //9,10,13,47,92
```
### [HTML Fuzzing](#html-fuzzing)

```
// Heyes, Gareth. JavaScript for hackers: Learn to think like a hacker (p. 38). Kindle Edition.
// Fuzzing chars that can close an HTML comment
let log = []
let div = document.createElement("div")
for (let i = 0; i <= 0x10ffff; i++) {
  div.innerHTML = ``
  if (div.querySelector("span")) {
    log.push(i)
  }
}
console.log(log) //33,45,62
```
## [**Analyzing attributes**](#analyzing-attributes)

**Analyzing attributes**

The tool **Hackability inspector** from Portswigger helps to **analyze** the **attributtes** of a javascript object. Check: [https://portswigger-labs.net/hackability/inspector/?input=x.contentWindow&html=%3Ciframe%20src=//subdomain1.portswigger-labs.net%20id=x%3E](https://portswigger-labs.net/hackability/inspector/?input=x.contentWindow&html=%3Ciframe%20src=//subdomain1.portswigger-labs.net%20id=x%3E)[\[6\]](#references)

## [**.map js files**](#map-js-files)

**.map js files**

- Trick to download .map js files: [https://medium.com/@bitthebyte/javascript-for-bug-bounty-hunters-part-2-f82164917e7](https://medium.com/@bitthebyte/javascript-for-bug-bounty-hunters-part-2-f82164917e7)<sup>[\[7\]](#references)</sup>
- You can use this tool to analyze these files [https://github.com/paazmaya/shuji](https://github.com/paazmaya/shuji)<sup>[\[8\]](#references)</sup>

## [“–” Assignment](#-assignment)

The decrement operator `--` is also an assignment. It converts a value to a number and decrements it by one; a nonnumeric value becomes `NaN`. This can be used to **replace variable contents in the environment**.

## [Functions Tricks](#functions-tricks)

### [.call and .apply](#call-and-apply)

The **`.call`** method of a function is used to **run the function**.

The **first argument** it expects by default is the **value of `this`** and if **nothing** is provided, **`window`** will be that value (unless **`strict mode`** is used).

```
function test_call() {
  console.log(this.value) //baz
}
new_this = { value: "hey!" }
test_call.call(new_this)
// To pass more arguments, just pass then inside .call()
function test_call() {
  console.log(arguments[0]) //"arg1"
  console.log(arguments[1]) //"arg2"
  console.log(this) //[object Window]
}
test_call.call(null, "arg1", "arg2")
// If you use the "use strict" directive "this" will be null instead of window:
function test_call() {
  "use strict"
  console.log(this) //null
}
test_call.call(null)
//The apply function is pretty much exactly the same as the call function with one important difference, you can supply an array of arguments in the second argument:
function test_apply() {
  console.log(arguments[0]) //"arg1"
  console.log(arguments[1]) //"arg2"
  console.log(this) //[object Window]
}
test_apply.apply(null, ["arg1", "arg2"])
```
### [Arrow functions](#arrow-functions)

Arrow functions allow you to generate functions in a single line more easily (if you understand them)

```
// Traditional
function (a){ return a + 1; }
// Arrow forms
a => a + 100;
a => {a + 100};
// Traditional
function (a, b){ return a + b + 1; }
// Arrow
(a, b) => a + b + 100;
// Tradictional no args
let a = 4;
let b = 2;
function (){ return a + b + 1; }
// Arrow
let a = 4;
let b = 2;
() => a + b + 1;
```
So, most of the previous functions are actually useless because we aren’t saving them anywhere to save and call them. Example creating the `plusone` function:

```
// Traductional
function plusone(a) {
  return a + 1
}
//Arrow
plusone = (a) => a + 100
```
### [Bind function](#bind-function)

The bind function allow to create a **copy** of a **function modifying** the **`this`** object and the **parameters** given.

```
//This will use the this object and print "Hello World"
var fn = function (param1, param2) {
  console.info(this, param1, param2)
}
fn("Hello", "World")
//This will still use the this object and print "Hello World"
var copyFn = fn.bind()
copyFn("Hello", "World")
//This will use the "console" object as "this" object inside the function and print "fixingparam1 Hello"
var bindFn_change = fn.bind(console, "fixingparam1")
bindFn_change("Hello", "World")
//This will still use the this object and print "fixingparam1 Hello"
var bindFn_thisnull = fn.bind(null, "fixingparam1")
bindFn_change("Hello", "World")
//This will still use the this object and print "fixingparam1 Hello"
var bindFn_this = fn.bind(this, "fixingparam1")
bindFn_change("Hello", "World")
```

Note that using **`bind`** you can manipulate the **`this`** object that is going to be used when calling the function.

### [Function code leak](#function-code-leak)

If you can **access the object** of a function you can **get the code** of that function

```
function afunc() {
  return 1 + 1
}
console.log(afunc.toString()) //This will print the code of the function
console.log(String(afunc)) //This will print the code of the function
console.log(this.afunc.toString()) //This will print the code of the function
console.log(global.afunc.toString()) //This will print the code of the function
```
In cases where the **function doesn’t have any name**, you can still print the **function code** from within:

```
;(function () {
  return arguments.callee.toString()
})()(function () {
  return arguments[0]
})("arg0")
```
Some **random** ways to **extract the code** of a function (even comments) from another function:

```
;(function () {
  return (retFunc) => String(arguments[0])
})((a) => {
  /* Hidden comment */
})()(function () {
  return (retFunc) => Array(arguments[0].toString())
})((a) => {
  /* Hidden comment */
})()(function () {
  return String(this)
}).bind(() => {
  /* Hidden comment */
})()((u) => String(u))((_) => {
  /* Hidden comment */
})((u) => (_) => String(u))((_) => {
  /* Hidden comment */
})()
```
## [Sandbox Escape - Recovering window object](#sandbox-escape---recovering-window-object)

The Window object allows to reach globally defined functions like alert or eval.

```
// Some ways to access window
window.eval("alert(1)")
frames
globalThis
parent
self
top //If inside a frame, this is top most window
// Access window from document
document.defaultView.alert(1)
// Access document from a node object
node = document.createElement('div')
node.ownerDocument.defaultView.alert(1)
// There is a path property on each error event whose last element is the window
<img src onerror=event.path.pop().alert(1337)>
// In other browsers the method is
<img src onerror=event.composedPath().pop().alert(1337)>
// In case of svg, the "event" object is called "evt"
<svg><image href=1 onerror=evt.composedPath().pop().alert(1337)>
// Abusing Error.prepareStackTrace to get Window back
Error.prepareStackTrace=function(error, callSites){
2   callSites.shift().getThis().alert(1337);
3 };
4 new Error().stack
// From an HTML event
// Events from HTML are executed in this context
with(document) {
    with(element) {
        //executed event
    }
}
// Because of that with(document) it's possible to access properties of document like:
<img src onerror=defaultView.alert(1337)>
<img src onerror=s=createElement('script');s.append('alert(1337)');appendChild(s)>
```
## [Breakpoint on access to value](#breakpoint-on-access-to-value)

```
// Stop when a property in sessionStorage or localStorage is set/get
// via getItem or setItem functions
sessionStorage.getItem = localStorage.getItem = function (prop) {
  debugger
  return sessionStorage[prop]
}
localStorage.setItem = function (prop, val) {
  debugger
  localStorage[prop] = val
}
```
```
// Stop when anyone sets or gets the property "ppmap" in any object
// For example sessionStorage.ppmap
// "123".ppmap
// Useful to find where weird properties are being set or accessed
// or to find where prototype pollutions are occurring
function debugAccess(obj, prop, debugGet = true) {
  var origValue = obj[prop]
  Object.defineProperty(obj, prop, {
    get: function () {
      if (debugGet) debugger
      return origValue
    },
    set: function (val) {
      debugger
      origValue = val
    },
  })
}
debugAccess(Object.prototype, "ppmap")
```
## [Automatic Browser Access to test payloads](#automatic-browser-access-to-test-payloads)

```
//Taken from https://github.com/svennergr/writeups/blob/master/inti/0621/README.md
const puppeteer = require("puppeteer")
const realPasswordLength = 3000
async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}
;(async () => {
  const browser = await puppeteer.launch()
  const page = await browser.newPage()
  //Loop to iterate through different values
  for (let i = 0; i < 10000; i += 100) {
    console.log(`Run number ${i}`)
    const input = `${"0".repeat(i)}${realPasswordLength}`
    console.log(
      `  https://challenge-0621.intigriti.io/passgen.php?passwordLength=${input}&allowNumbers=true&allowSymbols=true×tamp=1624556811000`
    )
    //Go to the page
    await page.goto(
      `https://challenge-0621.intigriti.io/passgen.php?passwordLength=${input}&allowNumbers=true&allowSymbols=true×tamp=1624556811000`
    )
    //Call function "generate()" inside the page
    await page.evaluate("generate()")
    //Get node inner text from an HTML element
    const passwordContent = await page.$$eval(
      ".alert .page-content",
      (node) => node[0].innerText
    )
    //Transform the content and print it in console
    const plainPassword = passwordContent.replace("Your password is: ", "")
    if (plainPassword.length != realPasswordLength) {
      console.log(i, plainPassword.length, plainPassword)
    }
    await sleep(1000)
  }
  await browser.close()
})()
```
## [References](#references)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
