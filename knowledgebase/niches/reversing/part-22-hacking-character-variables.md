---
title: "ARM-32 Course 2 \u2014 Part 22 \u2013 Hacking Character Variables"
source: 0xInfection/reversing
source_url: https://raw.githubusercontent.com/0xInfection/reversing/gh-pages/pages/part-22-hacking-character-variables.md
fetched_at: 2026-09-20T19:09:00Z
license: unspecified
category: reversing
---

For a complete table of contents of all the lessons please click below as it will give you a brief of each lesson in addition to the topics it will cover.&nbsp;https://github.com/mytechnotalent/Reverse-Engineering-Tutorial

Let’s review our code.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520232430320.jpg"/></div>

Let’s hack!

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520194771044.jpg"/></div>

We again see the direct value of __0x6e__ moved into __r3__ at __main+12__ which is our ‘__n__’.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520195499705.jpg"/></div>

After stepping into 4 times and verify the value in __r3__ which we clearly see as ‘__n__’.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520233196032.jpg"/></div>

Let’s hack the value in __r3__ to a ‘__y__’ and then reexamine the value in __r3__.&nbsp;We can now clearly see it has been changed to ‘__y__’.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520232999022.jpg"/></div>

As we continue we successfully see our hack worked!&nbsp;We see the value of ‘__y__’ printing to the standard output.

Next week we will dive into Boolean Variables.

_Upstream: mytechnotalent/Reverse-Engineering (Reverse Engineering For Everyone series), rendered by the 0xInfection/reversing gitbook._
