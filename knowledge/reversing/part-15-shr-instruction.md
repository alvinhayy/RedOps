---
title: "x64 Course \u2014 Part 15 - SHR Instruction"
source: 0xInfection/reversing
source_url: https://raw.githubusercontent.com/0xInfection/reversing/gh-pages/pages/part-15-shr-instruction.md
fetched_at: 2026-09-20T19:09:00Z
license: unspecified
category: reversing
---

For a complete table of contents of all the lessons please click below as it will give you a brief of each lesson in addition to the topics it will cover.&nbsp;https://github.com/mytechnotalent/Reverse-Engineering-Tutorial

The SHR command stands for shift right.

Let’s assume the register __al__ holds 00010100b which is an 8-bit binary value.&nbsp;Let’s assume the instruction is __shr al, 2__.&nbsp;Below is what transpires as we see the values move two bits to the left.

&nbsp;00010100

&nbsp;&nbsp;&nbsp;00010100

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1542995744073.jpg"/></div>

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1542995747116.jpg"/></div>

<div class="slate-resizable-image-embed slate-image-embed__resize-full-width"><img src="/imgs/1542995744391.jpg"/></div>

00000101

Next week we will dive into ROL! Stay tuned!

_Upstream: mytechnotalent/Reverse-Engineering (Reverse Engineering For Everyone series), rendered by the 0xInfection/reversing gitbook._
