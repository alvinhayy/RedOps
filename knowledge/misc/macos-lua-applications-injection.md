---
title: "macOS Lua Applications Injection"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-proces-abuse/macos-lua-applications-injection.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## `LUA_INIT`

`LUA_INIT`
Before processing command-line options or the target script, the standalone Lua interpreter executes `LUA_INIT_<major>_<minor>` or, if the versioned variable is absent, `LUA_INIT`. A value beginning with `@` names a file; any other value is evaluated directly as Lua code. This gives both file-backed and fileless startup execution.[\[1\]](#references)

```
# File-backed
echo 'os.execute("touch /tmp/lua-init-executed")' >/tmp/lua-init.lua
LUA_INIT_5_4=@/tmp/lua-init.lua lua victim.lua
# Fileless
LUA_INIT='os.execute("touch /tmp/lua-inline-executed")' lua victim.lua
```
The exact versioned name changes with the interpreter, for example `LUA_INIT_5_4`. `lua -E` ignores all environment variables, including startup code and Lua module paths.

## References
