---
title: "ARM-32 Course 2 \u2014 Part 24 \u2013 Debugging Boolean Variables"
source: 0xInfection/reversing
source_url: https://raw.githubusercontent.com/0xInfection/reversing/gh-pages/pages/part-24-debugging-boolean-variables.md
fetched_at: 2026-09-20T19:09:00Z
license: unspecified
category: reversing
---

For a complete table of contents of all the lessons please click below as it will give you a brief of each lesson in addition to the topics it will cover.&nbsp;https://github.com/mytechnotalent/Reverse-Engineering-Tutorial

Let’s re-examine our code.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520236715844.jpg"/></div>

Let’s debug.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520194325794.jpg"/></div>

Let’s step 4 times and disassemble.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520190876822.jpg"/></div>

Let’s examine what is now in __r3__.

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1520171350771.jpg"/></div>

As we can clearly see the value in __isHacked__ is __0__ or __false__ which makes sense based on our c++ source code.

I know these lessons may seem trivial however Reverse Engineering is all about breaking things down in their most basic components.&nbsp;Reverse Engineering is about patience and logical flow.&nbsp;It is critical that you take the time and work through all of these examples with a Raspberry Pi device so that you can have a proper appreciation for how the process actually works.

Next week we will dive into Hacking Boolean Variables.

_Upstream: mytechnotalent/Reverse-Engineering (Reverse Engineering For Everyone series), rendered by the 0xInfection/reversing gitbook._
