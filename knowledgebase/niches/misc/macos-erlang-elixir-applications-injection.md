---
title: "macOS Erlang and Elixir Applications Injection"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-proces-abuse/macos-erlang-elixir-applications-injection.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## `ERL_AFLAGS`, `ERL_FLAGS`, and `ERL_ZFLAGS`

`ERL_AFLAGS`, `ERL_FLAGS`, and `ERL_ZFLAGS`
The `erl` launcher adds `ERL_AFLAGS` to the beginning of its command line and `ERL_FLAGS` / `ERL_ZFLAGS` to the end. Because `-eval` evaluates an Erlang expression during VM initialization, these variables can provide fileless code execution before the intended workload.[\[1\]](#references)

```
ERL_AFLAGS="-noshell -eval 'file:write_file(\"/tmp/erl-aflags-executed\", <<\"ok\">>).' -s init stop" erl
```
Elixir, Mix, Phoenix and many Elixir releases ultimately start the Erlang VM and may inherit these flags. Confirm the exact release wrapper: it may rebuild or sanitize VM arguments, while some tooling explicitly supports `ERL_AFLAGS`, `ERL_ZFLAGS`, or `ELIXIR_ERL_OPTIONS`.[\[2\]](#references)

Unlike most file-backed techniques, the `-eval` payload needs no attacker-controlled file. A trusted wrapper should clear all three Erlang flag variables (and `ELIXIR_ERL_OPTIONS` for Elixir) before starting the runtime; do not try to allowlist individual VM flags unless the parser and ordering are fully understood.

## References
