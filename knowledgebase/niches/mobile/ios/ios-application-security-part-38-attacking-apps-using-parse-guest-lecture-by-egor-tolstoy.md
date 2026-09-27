---
title: "iOS Application Security Part 38 - Attacking apps using Parse (Guest Lecture by Egor Tolstoy)"
source: highaltitudehacks.com
source_url: https://highaltitudehacks.com/2015/01/24/ios-application-security-part-38-attacking-apps-using-parse-guest-lecture-by-egor-tolstoy.html
fetched_at: 2026-09-20T08:36:31Z
license: unspecified
category: mobile/ios
---

Published on 24 Jan 2015

  **This is a guest lecture by [Egor Tolstoy](http://etolstoy.ru). Egor is a full-time iOS developer working at Rambler&Co and living with his lovely wife in Moscow, Russia. In his spare time he investigate iOS applications for different vulnerabilities and blogs about my research.**

[Parse](http://parse.com/) is a wonderful BaaS which helps with setting up backend infrastructure for your mobile application as fast as possible. Maybe just because of this simplicity many developers forget about a number of new security issues and vulnerabilities.

![](/images/posts/ios38/8822BC1A-FA0D-4BFF-8DC0-8CC103DFB92D.png)

For those who don’t know what this service is, let’s make a brief introduction. Parse provides a lot of useful capabilities to mobile developer: cloud data storage, push notifications, usage statistics and crash logs gathering, code hosting, background jobs and a many other things. Within the boundaries of thes research we are interested in the cloud data storage, named _Cloud Core_.

All the data in Cloud Core is stored in so called custom classes (ordinary database tables).

![](/images/posts/ios38/8879CA5B-B494-43CD-A136-1DB8059F5AC1.png)

You can set a number of different client permissions for each of these classes: _GET, FIND, UPDATE, CREATE, DELETE_ and _ADD FIELDS_. All of them are _Public_ by default. Of course, most of the developers forget about the need of setting client access permissions once they configure their tables.

![](/images/posts/ios38/FDF17B0E-CD2B-47AB-BB46-F0D0BE9BDE7E.png)

I’ve closely faced Parse during one of my work projects and spent a lot of time configuring ACLs properly - so I became interested in how other developers maintain their Parse accounts. I’ve found the object for my little research right on [parse.com/customers](https://parse.com/customers). It was [Cubefree](http://cubefreeapp.com/) - a service for locating cowering spaces.

A pair of keys is used for connecting to Parse account from a mobile application: _Application ID_ and _Client Key_. We’ve got to find out these strings in order to manipulate the data in Cloud Core. Let’s decrypt the application binary with the help of [idb](https://github.com/dmayer/idb) - an awesome iOS pentesting utility. While the decryption process is going on, we can check _NSUserDefaults_ - a rather common place for storing such kind of data (only for reckless developers, of course).

![](/images/posts/ios38/03B3C111-1C51-4330-899E-7E5873D94B7F.png)

As you can see, nothing criminal was found - no signs of confidential data. Let’s get back to our decrypted application binary and feed it to [Hopper](http://www.hopperapp.com/) - a well known disassembler, specialized in reverse-engineering Objective-C applications. Our quest for Parse keys will begin in _application:didFinishLaunchingWithOptions method_ of _App Delegate._ One of the noteworthy Hopper features is the ability to represent any procedure in pseudocode form, which flattens the reversed code understanding curve.

![](/images/posts/ios38/AB772C3F-377A-4B02-BA39-946D0B54831C.png)

As expected, the connection to Parse is initiated right here. Now we’ll analyse the structure of Parse data and its client permissions.

The next step is identification of Parse tables names. Actually, we can see them on the same screenshot as client keys - there is a plenty of _registerSubclass_ method calls. These classes are children of the root _PFObject_ class. Each of them has a method _parseClassName, _which returns a corresponding Parse table name.

![](/images/posts/ios38/FC415E09-109A-460B-9E04-763532556FDB.png)

Let’s inspect the structure of these tables:

[https://gist.github.com/igrekde/cb8e2c12408715c9f739#file-parse-security-1](https://gist.github.com/igrekde/cb8e2c12408715c9f739#file-parse-security-1)

The knowledge of classes organization, however, is not enough. We should try to inspect access permissions for all the Parse classes to determine how we can influence the application behaviour. It’s quite simple - all we have to do is to make a couple of queries to Parse and analyse their results. I’ve wrote a small utility - [Parse Revealer](https://github.com/igrekde/ParseRevealer), which simplifies these routine actions and automatically determines the access permissions for all known classes.

![](/images/posts/ios38/E171D146-358B-41FD-98E2-FBC293EBAFEF.png)

We can create a table using all the derived data:

![](/images/posts/ios38/%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%202015-01-24%2020.41.30.png)

As we can see from the list of permissions, the developers tried to implement a security policy, but it wasn’t enough. Let’s show what we can achieve by manipulating the _ChatMessage_ class.

The most obvious vulnerability is that the attacker is able to modify the text of any message in any chatroom. After the execution of this code block the reasonable statement turns into a nonsense:

[https://gist.github.com/igrekde/cb8e2c12408715c9f739#file-parse-security-2](https://gist.github.com/igrekde/cb8e2c12408715c9f739#file-parse-security-2)

![](/images/posts/ios38/cubefree-screen.png)

We can also post new messages to any chat by providing a new _PFObject_ with a correct chatId. But we are noble pentesters, so let’s pay attention to the fact that we aren’t able to delete any message due to developers paranoia :).

A much more serious vulnerability consists in incorrect data mapping algorithm. When a _ChatMessage_ object doesn’t have anything in the sender field, the Cubefree application crashes. So, it’s possible to loop through all the chatrooms, post an invalid _ChatMessage_ - and the application will always crash when somebody opens the chat screen. It’s fraught with bad App Store ratings, users outflow and a complete project failure.

There are same vulnerabilities in other classes - but they are not within the scope of current investigation.

As for security of your own applications - everything is quite transparent, just follow these simple rules:

- Always configure client permissions for all of your Parse classes.
- Make use of user-based ACLs - it’s a great Parse feature.
- If a client should be able to modify only one property of your class, think of encapsulating this field in the separate class. By doing it you will circumvent the possibility of illegal changes in your objects.
- Don’t rely on Parse - always do a proper validity check of the data it returns you.
- Remember that, theoretically, applicationID and clientKey can be found by any attacker, so you should build your application security grounding on this knowledge.
- The previous advice doesn’t cancel the necessarily of obfuscating strings in code :)
- Use Cloud Code in more complex situations.

If you recognise some of your applications in this research, don’t blame Parse - it’s the amazing service, which minimize backend developing costs. All of the examined vulnerabilities lie heavy on the developers conscience.

Further reading:
