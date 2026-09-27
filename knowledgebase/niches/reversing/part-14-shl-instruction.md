---
title: "x64 Course \u2014 Part 14 - SHL Instruction"
source: 0xInfection/reversing
source_url: https://raw.githubusercontent.com/0xInfection/reversing/gh-pages/pages/part-14-shl-instruction.md
fetched_at: 2026-09-20T19:09:00Z
license: unspecified
category: reversing
---

For a complete table of contents of all the lessons please click below as it will give you a brief of each lesson in addition to the topics it will cover.&nbsp;https://github.com/mytechnotalent/Reverse-Engineering-Tutorial

The SHL command stands for shift left.

Let’s assume the register __al__ holds __01010101b__ which is an 8-bit binary value.&nbsp;Let’s assume the instruction is __shl al, 2__.&nbsp;Below is what transpires as we see the values move two bits to the left.

&nbsp;&nbsp;&nbsp;00010101

00010101

Therefore the new value will be:

10100000

Next week we will dive into SHR! Stay tuned!

_Upstream: mytechnotalent/Reverse-Engineering (Reverse Engineering For Everyone series), rendered by the 0xInfection/reversing gitbook._
