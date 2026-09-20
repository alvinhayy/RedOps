---
title: "x64 Course \u2014 Part 30 - x64 Assembly [Part 4]"
source: 0xInfection/reversing
source_url: https://raw.githubusercontent.com/0xInfection/reversing/gh-pages/pages/part-30-x64-assembly-part-4.md
fetched_at: 2026-09-20T19:09:00Z
license: unspecified
category: reversing
---

## Part 30 - x64 Assembly \[Part 4\]

For a complete table of contents of all the lessons please click below as it will give you a brief of each lesson in addition to the topics it will cover.&nbsp;https://github.com/mytechnotalent/Reverse-Engineering-Tutorial

Today we will code our simple, "hello world" program in x64 Assembly.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1552041593157.jpg"/></div>

We simply create a string in the __.data __section and add a return character at the end of the statement. We then perform a simple write call which utilizes the OS's interrupt vector table to spit out our string in the standard output or terminal.

We will compile and run below:

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1552041719716.jpg"/></div>

As we can see "__Hello World__!" has been echoed to the terminal. Next week we will debug this simple program in GDB.

_Upstream: mytechnotalent/Reverse-Engineering (Reverse Engineering For Everyone series), rendered by the 0xInfection/reversing gitbook._
