---
title: "Service Triggers"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/windows-hardening/windows-local-privilege-escalation/service-triggers.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: windows
---

## Enumerating Service Triggers

- sc.exe (local)
  - List a service’s triggers: `sc.exe qtriggerinfo <ServiceName>`
- List a service’s triggers:
- Registry (local)
  - Triggers live under: `HKLM\SYSTEM\CurrentControlSet\Services\<ServiceName>\TriggerInfo`
  - Dump recursively: `reg query HKLM\SYSTEM\CurrentControlSet\Services\<ServiceName>\TriggerInfo /s`
- Triggers live under:
- Win32 API (local)
  - Call QueryServiceConfig2 with SERVICE_CONFIG_TRIGGER_INFO (8) to retrieve SERVICE_TRIGGER_INFO.
    - Docs: QueryServiceConfig2[W/A] and SERVICE_TRIGGER/SERVICE_TRIGGER_SPECIFIC_DATA<sup>[\[2\]](#references)</sup>
  - Docs: QueryServiceConfig2[W/A] and SERVICE_TRIGGER/SERVICE_TRIGGER_SPECIFIC_DATA
- Call QueryServiceConfig2 with SERVICE_CONFIG_TRIGGER_INFO (8) to retrieve SERVICE_TRIGGER_INFO.
- RPC over MS‑SCMR (remote)
- PowerShell (bulk enumeration)
  - Quickly list every service exposing a `TriggerInfo` key:```
Get-ChildItem 'HKLM:\SYSTEM\CurrentControlSet\Services' |
  Where-Object { Test-Path "$($_.PSPath)\TriggerInfo" } |
  ForEach-Object { sc.exe qtriggerinfo $_.PSChildName }
```
- Quickly list every service exposing a
- PowerShell (programmatic)
  - James Forshaw’s `NtObjectManager` module exposes`Get-Win32ServiceTrigger` for parsing trigger metadata without scraping`sc.exe` output.
- James Forshaw’s

## [High-Value Trigger Types and How to Activate Them](#high-value-trigger-types-and-how-to-activate-them)

### [Network Endpoint Triggers](#network-endpoint-triggers)

These start a service when a client attempts to talk to an IPC endpoint. Useful to low-priv users because the SCM will auto-start the service before your client can actually connect.[\[1\]](#references)

-
Named pipe trigger
  - Behavior: A client connection attempt to \.\pipe<PipeName> causes the SCM to start the service so it can begin listening.
  - Activation (PowerShell):
```
$pipe = new-object System.IO.Pipes.NamedPipeClientStream('.', 'PipeNameFromTrigger', [System.IO.Pipes.PipeDirection]::InOut)
try { $pipe.Connect(1000) } catch {}
$pipe.Dispose()
```
  - Internals note: named-pipe triggers are backed by `npsvctrig.sys` , a filesystem minifilter that watches for opens against registered trigger pipe names. This is why the open attempt can start the service even before the service itself has created/listened on the pipe.<sup>[\[5\]](#references)</sup>
  - See also: Named Pipe Client Impersonation for post-start abuse.
-
RPC endpoint trigger (Endpoint Mapper)
  - Behavior: Querying the Endpoint Mapper (EPM, TCP/135) for an interface UUID associated with a service causes the SCM to start it so it can register its endpoint.
  - Activation (Impacket):
```
# Queries local EPM; replace UUID with the service interface GUID
python3 rpcdump.py @127.0.0.1 -uuid <INTERFACE-UUID>
```

### [Custom (ETW) Triggers](#custom-etw-triggers)

A service can register a trigger bound to an ETW provider/event. If no additional filters (keyword/level/binary/string) are configured, any event from that provider will start the service.[\[1\]](#references)

- Example (WebClient/WebDAV): provider {22B6D684-FA63-4578-87C9-EFFCBE6643C7}<sup>[\[6\]](#references)</sup>  - List trigger: `sc.exe qtriggerinfo webclient`
  - Verify provider is registered: `logman query providers | findstr /I 22b6d684-fa63-4578-87c9-effcbe6643c7`
  - Emitting matching events typically requires code that logs to that provider; if no filters are present, any event suffices.
  - Minimal C shape for firing the provider (when no additional ETW filters are configured):
```
GUID g = {0x22B6D684,0xFA63,0x4578,{0x87,0xC9,0xEF,0xFC,0xBE,0x66,0x43,0xC7}};
REGHANDLE h; EVENT_DESCRIPTOR d;
EventRegister(&g, NULL, NULL, &h);
EventDescCreate(&d, 1, 0, 0, 4, 0, 0, 0);
EventWrite(h, &d, 0, NULL);
EventUnregister(h);
```
- List trigger:

### [Group Policy Triggers](#group-policy-triggers)

Subtypes: Machine/User. On domain-joined hosts where the corresponding policy exists, the trigger runs at boot. `gpupdate` alone won’t trigger without changes, but:[\[1\]](#references)

- Activation: `gpupdate /force`  - If the relevant policy type exists, this reliably causes the trigger to fire and start the service.

### [IP Address Available](#ip-address-available)

Fires when the first IP is obtained (or last is lost). Often triggers at boot.[\[1\]](#references)

- Activation: Toggle connectivity to retrigger, e.g.:
```
netsh interface set interface name="Ethernet" admin=disabled
netsh interface set interface name="Ethernet" admin=enabled
```

### [Device Interface Arrival](#device-interface-arrival)

Starts a service when a matching device interface arrives. If no data item is specified, any device matching the trigger subtype GUID will fire the trigger. Evaluated at boot and upon hot‑plug.[\[1\]](#references)

- Activation: Attach/insert a device (physical or virtual) that matches the class/hardware ID specified by the trigger subtype.

### [Domain Join State](#domain-join-state)

Despite confusing MSDN wording, this evaluates domain state at boot:[\[1\]](#references)

- DOMAIN_JOIN_GUID → start the service if domain-joined
- DOMAIN_LEAVE_GUID → start the service only if NOT domain-joined

### [System State Change – WNF (undocumented)](#system-state-change--wnf-undocumented)

Some services use undocumented WNF-based triggers (SERVICE_TRIGGER_TYPE 0x7). Activation requires publishing the relevant WNF state; specifics depend on the state name. Research background: Windows Notification Facility internals.

### [Aggregate Service Triggers (undocumented)](#aggregate-service-triggers-undocumented)

Observed on Windows 11 for some services (e.g., CDPSvc). The aggregated configuration is stored in:

- HKLM\SYSTEM\CurrentControlSet\Control\ServiceAggregatedEvents

A service’s Trigger value is a GUID; the subkey with that GUID defines the aggregated event. Triggering any constituent event starts the service.[\[1\]](#references)

### [Firewall Port Event (quirks and DoS risk)](#firewall-port-event-quirks-and-dos-risk)

A trigger scoped to a specific port/protocol has been observed to start on any firewall rule change (disable/delete/add), not just the specified port. Worse, configuring a port without a protocol can corrupt BFE startup across reboots, cascading into many service failures and breaking firewall management. Treat with extreme caution.[\[1\]](#references)

## [Practical Workflow](#practical-workflow)

1. Enumerate triggers on interesting services (RemoteRegistry, WebClient, EFS, …):

- `sc.exe qtriggerinfo <Service>`
- `reg query HKLM\SYSTEM\CurrentControlSet\Services\<Service>\TriggerInfo /s`

1. If a Network Endpoint trigger exists:

- Named pipe → attempt a client open to \.\pipe<PipeName>
- RPC endpoint → perform an Endpoint Mapper lookup for the interface UUID

1. If an ETW trigger exists:

- Check provider and filters with `sc.exe qtriggerinfo` ; if no filters, any event from that provider will start the service

1. For Group Policy/IP/Device/Domain triggers:

- Use environmental levers: `gpupdate /force` , toggle NICs, hot-plug devices, etc.

## [Related](#related)

- After starting a privileged service via a Named Pipe trigger, you may be able to impersonate it:

[Named Pipe Client Impersonation](named-pipe-client-impersonation.html)

## [Quick command recap](#quick-command-recap)

- List triggers (local): `sc.exe qtriggerinfo <Service>`
- Registry view: `reg query HKLM\SYSTEM\CurrentControlSet\Services\<Service>\TriggerInfo /s`
- Win32 API: `QueryServiceConfig2(..., SERVICE_CONFIG_TRIGGER_INFO, ...)`
- RPC remote (Titanis): `Scm.exe qtriggers`
- ETW provider check (WebClient): `logman query providers | findstr /I 22b6d684-fa63-4578-87c9-effcbe6643c7`

## [Gotchas / Operator Notes](#gotchas--operator-notes)

- Check the service start type first with `sc.exe qc <Service>` . If it is`DISABLED` , firing the trigger is not enough; you must first find a way to change the configuration.
- Trigger-start services may stop again after they become idle. If your follow-on action depends on a short-lived listener (RPC/named pipe/WebDAV), trigger and consume it immediately.
- `sc.exe qtriggerinfo` does not fully understand every undocumented trigger type. For aggregate triggers on newer Windows builds, confirm the backing GUID and constituent events in`HKLM\SYSTEM\CurrentControlSet\Control\ServiceAggregatedEvents` .

## [Detection and Hardening Notes](#detection-and-hardening-notes)

- Baseline and audit TriggerInfo across services. Also review HKLM\SYSTEM\CurrentControlSet\Control\ServiceAggregatedEvents for aggregate triggers.
- Monitor for suspicious EPM lookups for privileged service UUIDs and named-pipe connection attempts that precede service starts.
- Restrict who can modify service triggers; treat unexpected BFE failures after trigger changes as suspicious.

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
