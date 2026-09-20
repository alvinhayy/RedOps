---
title: "x86 Course \u2014 Part 38 - ASM Debugging 6 [CMOV Instructions]"
source: 0xInfection/reversing
source_url: https://raw.githubusercontent.com/0xInfection/reversing/gh-pages/pages/part-38-asm-debugging-6-cmov-instructions.md
fetched_at: 2026-09-20T19:09:00Z
license: unspecified
category: reversing
---

## Part 38 - ASM Debugging 6 \[CMOV Instructions\]

For a complete table of contents of all the lessons please click below as it will give you a brief of each lesson in addition to the topics it will cover.&nbsp;https://github.com/mytechnotalent/Reverse-Engineering-Tutorial

Lets re-examine some source code.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520234974923.jpg"/></div>

Lets break on 0x08048092 which is line 31. Lets do a r to run and then type __print $ebx__. We can see the value of 7.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520240729383.jpg"/></div>

Ok now lets break on 0x080480b1 which is line 46. Remember when we are examining the value of __answer__, it has been converted to its ascii printable equivalent so in order to see the value of ‘7’ you would type __x/1c &amp;answer__.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520498895208.jpg"/></div>

I look forward to seeing you all next week when we dive into hacking our sixth assembly program!

_Upstream: mytechnotalent/Reverse-Engineering (Reverse Engineering For Everyone series), rendered by the 0xInfection/reversing gitbook._
