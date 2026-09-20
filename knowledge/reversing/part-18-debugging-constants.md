---
title: "ARM-32 Course 2 \u2014 Part 18 \u2013 Debugging Constants"
source: 0xInfection/reversing
source_url: https://raw.githubusercontent.com/0xInfection/reversing/gh-pages/pages/part-18-debugging-constants.md
fetched_at: 2026-09-20T19:09:00Z
license: unspecified
category: reversing
---

For a complete table of contents of all the lessons please click below as it will give you a brief of each lesson in addition to the topics it will cover.&nbsp;https://github.com/mytechnotalent/Reverse-Engineering-Tutorial

Let’s review last week’s code.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520147783406.jpg"/></div>

Let’s debug!

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520194203208.jpg"/></div>

As we can see the value in the memory address __0x10730 __is equal to __2017__.&nbsp;Let’s continue and watch the value print to the standard output (terminal) as it did last week when we ran it.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520152068447.jpg"/></div>

We can see very clearly that we move the value from memory into __r1 __and then we branch to our __cout__ function to print to the terminal.&nbsp;At this stage you should feel a little more comfortable with understanding what the assembly is doing above.

Next week we will dive into Hacking Constants.

_Upstream: mytechnotalent/Reverse-Engineering (Reverse Engineering For Everyone series), rendered by the 0xInfection/reversing gitbook._
