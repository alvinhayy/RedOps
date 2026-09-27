---
title: "macOS Users & External Accounts"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-users.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Common Users

-
**Daemon accounts** : Reserved for system daemons. Their short names commonly start with an underscore (`_` ):```
_amavisd, _analyticsd, _appinstalld, _appleevents, _applepay, _appowner, _appserver, _appstore, _ard, _assetcache, _astris, _atsserver, _avbdeviced, _calendar, _captiveagent, _ces, _clamav, _cmiodalassistants, _coreaudiod, _coremediaiod, _coreml, _ctkd, _cvmsroot, _cvs, _cyrus, _datadetectors, _demod, _devdocs, _devicemgr, _diskimagesiod, _displaypolicyd, _distnote, _dovecot, _dovenull, _dpaudio, _driverkit, _eppc, _findmydevice, _fpsd, _ftp, _fud, _gamecontrollerd, _geod, _hidd, _iconservices, _installassistant, _installcoordinationd, _installer, _jabber, _kadmin_admin, _kadmin_changepw, _knowledgegraphd, _krb_anonymous, _krb_changepw, _krb_kadmin, _krb_kerberos, _krb_krbtgt, _krbfast, _krbtgt, _launchservicesd, _lda, _locationd, _logd, _lp, _mailman, _mbsetupuser, _mcxalr, _mdnsresponder, _mobileasset, _mysql, _nearbyd, _netbios, _netstatistics, _networkd, _nsurlsessiond, _nsurlstoraged, _oahd, _ondemand, _postfix, _postgres, _qtss, _reportmemoryexception, _rmd, _sandbox, _screensaver, _scsd, _securityagent, _softwareupdate, _spotlight, _sshd, _svn, _taskgated, _teamsserver, _timed, _timezone, _tokend, _trustd, _trustevaluationagent, _unknown, _update_sharing, _usbmuxd, _uucp, _warmd, _webauthserver, _windowserver, _www, _wwwproxy, _xserverdocs
```
-
**Guest** : A restricted, temporary account whose availability can be controlled locally or by an MDM Accounts payload.<sup>[\[1\]](#references)</sup>

```
state=("automaticTime" "afpGuestAccess" "filesystem" "guestAccount" "smbGuestAccess")
for i in "${state[@]}"; do sysadminctl -"${i}" status; done;
```
- **Nobody** : A deliberately unprivileged identity used by services that require minimal filesystem permissions.
- **Root** : The superuser. Interactive root login is disabled by default, although administrators can perform privileged operations through authorization and`sudo` .<sup>[\[2\]](#references)</sup>

## [User Privileges](#user-privileges)

- **Standard user:** The normal, non-administrative account type. Administrative changes require authorization from an administrator.
- **Admin user** : A member of the local`admin` group. Admin users still run ordinary processes with their user identity, but can authorize privileged operations. Do not assume that membership alone makes every command run as root;`sudo` , Authorization Services, policy, and application-specific checks still apply.<sup>[\[2\]](#references)</sup>
- **Root** : Root is a user allowed to perform almost any action (there are limitations imposed by protections like System Integrity Protection).
  - For example, System Integrity Protection and the signed system volume prevent even root from persistently modifying protected `/System` content during normal operation.
- For example, System Integrity Protection and the signed system volume prevent even root from persistently modifying protected

## [External Accounts](#external-accounts)

macOS also supports application accounts from external providers. The `accountsd` daemon (`/System/Library/Frameworks/Accounts.framework/Versions/A/Support/accountsd`) brokers Accounts-framework data, and authentication plug-ins can be found under `/System/Library/Accounts/Authentication/`. These are application/service accounts, not necessarily identities that can log in at the macOS login window. `accountsd` also reads the known account types from `/Library/Preferences/SystemConfiguration/com.apple.accounts.exists.plist`.

## [References](#references)

- [1] [Apple Developer — Accounts device-management payload](https://developer.apple.com/documentation/devicemanagement/accounts)
- [2] [Apple — BSD permissions and ownership: administrative and root accounts](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPFileSystem/Articles/BSDInfluences.html)

Learn & practice AWS Hacking:**HackTricks Training AWS Red Team Expert (ARTE)**

Learn & practice GCP Hacking: **HackTricks Training GCP Red Team Expert (GRTE)**

Learn & practice Az Hacking: **HackTricks Training Azure Red Team Expert (AzRTE)**

Browse the [**full HackTricks Training catalog**](https://hacktricks-training.com/courses/).

## Support HackTricks

- Check the
[**subscription plans**](https://github.com/sponsors/carlospolop)!
**Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f), the [**telegram group**](https://t.me/peass), **follow** [**@hacktricks_live**](https://twitter.com/hacktricks_live) on **X/Twitter**, or check the [**LinkedIn page**](https://www.linkedin.com/company/hacktricks/) and [**YouTube channel**](https://www.youtube.com/@hacktricks_LIVE).
**Share hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.
