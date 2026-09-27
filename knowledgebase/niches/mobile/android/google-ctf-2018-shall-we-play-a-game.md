---
title: "Google CTF 2018 - Shall We Play a Game?"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/android-app-pentesting/google-ctf-2018-shall-we-play-a-game.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile/android
---

## **Smali changes**

**Smali changes**

### **Call m() the first time**

**Call m() the first time**

To make the application call `m()` when `this.o != 1000000`, invert the branch condition:

```
 if-ne v0, v9, :cond_2
```
to:

```
 if-eq v0, v9, :cond_2
```
Follow the [Android pentesting](README.html) workflow to rebuild and sign the APK, then run it again:

The displayed flag is not fully decrypted because the per-win transformation must run 1,000,000 times; merely bypassing the comparison does not reproduce those iterations.[\[2\]](#references)

Another approach is to leave the branch instruction intact and change its operands:

**Another way** is instead of comparing with 1000000, set the value to 1 so this.o is compared with 1:

A fourth approach is to move the value of `v9` (1,000,000) into `v0` (`this.o`):

## Solution

Make the application run the win/decryption loop **1,000,000 times** after the first win. Create the `:goto_6` loop and jump back while `this.o` has not reached 1,000,000:[\[2\]](#references)

The original experiment succeeded on a physical device but not its emulator. That is an observation about that setup rather than an inherent requirement; emulator CPU speed, watchdogs, or service limits can make the million-iteration loop appear to hang.

## References

- [1] [Google CTF challenge repository](https://github.com/google/google-ctf/tree/master/2018)
- [2] [CTFtime — Google CTF 2018 “Shall we play a game?” write-up](https://ctftime.org/writeup/10277)
- [3] [Appetize.io Android emulator](https://appetize.io/)
