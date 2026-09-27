---
title: "macOS Office Sandbox Bypasses"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-security-protections/macos-sandbox/macos-sandbox-debug-and-bypass/macos-office-sandbox-bypasses.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

### Word sandbox bypass via LaunchAgents

The affected application used a custom sandbox rule through `com.apple.security.temporary-exception.sbpl`. It allowed regular files whose basename started with `~$`: `(require-any (require-all (vnode-type REGULAR-FILE) (regex #"(^|/)~$[^/]+$")))`.[\[1\]](#references)

Therefore, escaping was as easy as **writing a `plist`** LaunchAgent in `~/Library/LaunchAgents/~$escape.plist`.

Check the [**original report here**](https://www.mdsec.co.uk/2018/08/escaping-the-sandbox-microsoft-office-on-macos/).[\[1\]](#references)

### Word Sandbox bypass via Login Items and zip

Remember that from the first escape, Word can write arbitrary files whose name start with `~$` although after the patch of the previous vuln it wasn’t possible to write in `/Library/Application Scripts` or in `/Library/LaunchAgents`.

The affected sandbox allowed creation of a **Login Item**, which launches when the user logs in. The demonstrated path required an acceptable signed/notarized application and did not permit arbitrary arguments, so adding `bash` with a reverse-shell argument was insufficient.[\[2\]](#references)

From the previous Sandbox bypass, Microsoft disabled the option to write files in `~/Library/LaunchAgents`. However, it was discovered that if you put a **zip file as a Login Item** the `Archive Utility` will just **unzip** it on its current location. So, because by default the folder `LaunchAgents` from `~/Library` is not created, it was possible to **zip a plist in `LaunchAgents/~$escape.plist`** and **place** the zip file in **`~/Library`** so when decompress it will reach the persistence destination.

Check the [**original report here**](https://objective-see.org/blog/blog_0x4B.html).[\[2\]](#references)

### Word Sandbox bypass via Login Items and .zshenv

(Remember that from the first escape, Word can write arbitrary files whose name start with `~$`).

However, the previous technique had a limitation, if the folder **`~/Library/LaunchAgents`** exists because some other software created it, it would fail. So a different Login Items chain was discovered for this.

An attacker could create **`.bash_profile`** and **`.zshenv`** containing the payload, archive them, and write the ZIP to the **victim’s** home directory as **`~/~$escape.zip`**.

Then add the ZIP and **Terminal** as Login Items. At the next login, Archive Utility extracts the dotfiles into the user’s home directory and Terminal’s shell evaluates the applicable startup file (`.bash_profile` for the demonstrated Bash path or `.zshenv` for Zsh).[\[3\]](#references)

Check the [**original report here**](https://desi-jarvis.medium.com/office365-macos-sandbox-escape-fcce4fa4123c).[\[3\]](#references)

### Word Sandbox Bypass with Open and env variables

Sandboxed processes could still request application launches through **`open`**. The launched application ran in its own security context rather than inheriting Word’s exact sandbox profile.[\[4\]](#references)

The affected `open` utility had an **`--env`** option for supplying environment variables. The exploit created `.zshenv` inside the sandbox, set `HOME` to that directory, and launched Terminal so Zsh evaluated it. The reported chain also set the misspelled private variable `__OSINSTALL_ENVIROMENT`; preserve that exact spelling when reproducing the historical PoC.[\[4\]](#references)

Check the [**original report here**](https://perception-point.io/blog/technical-analysis-of-cve-2021-30864/).[\[4\]](#references)

### Word Sandbox Bypass with Open and stdin

The **`open`** utility also supported the **`--stdin`** param (and after the previous bypass it was no longer possible to use `--env`).

Although Apple’s Python application would reject a quarantined script file, the vulnerable workflow could feed the same script over standard input, avoiding the file-based quarantine check:[\[5\]](#references)

1. Drop a **`~$exploit.py`** file with arbitrary Python commands.
2. Run `open --stdin='~$exploit.py' -a Python` . The launched Python application receives the dropped code on standard input and, in the vulnerable versions, runs outside Word’s sandbox because LaunchServices creates it under`launchd` .<sup>[\[5\]](#references)</sup>

## References
