---
title: "macOS Authorizations DB & Authd"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-security-protections/macos-authorizations-db-and-authd.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Authorization Database

The Security framework’s Authorization Services let privileged helpers and other components evaluate named authorization rights. On current macOS versions, many of those rules are persisted in `/var/db/auth.db` and evaluated by `authd`; this file and its SQLite schema are implementation details and can change between releases.[\[2\]](#references)[\[3\]](#references)

System defaults have historically been seeded from `/System/Library/Security/authorization.plist`, and installers or privileged services may add named rights. Prefer the supported `security authorizationdb read|write|remove` interface over editing the database directly.[\[3\]](#references)

The `rules` table observed on the documented build contains the following columns. Treat this as a forensic map, not a stable public schema:

- **id** : A unique identifier for each rule, automatically incremented and serving as the primary key.
- **name** : The unique name of the rule used to identify and reference it within the authorization system.
- **type** : Specifies the type of the rule, restricted to values 1 or 2 to define its authorization logic.
- **class** : Categorizes the rule into a specific class, ensuring it is a positive integer.
  - Common rule classes include `allow` ,`deny` ,`user` ,`rule` , and`evaluate-mechanisms` . Mechanisms can be built-ins or Security Agent plug-ins under`/System/Library/CoreServices/SecurityAgentPlugins/` or`/Library/Security/SecurityAgentPlugins/` .<sup>[\[2\]](#references)</sup>
- Common rule classes include
- **group** : Indicates the user group associated with the rule for group-based authorization.
- **kofn** : Represents the “k-of-n” parameter, determining how many subrules must be satisfied out of a total number.
- **timeout** : Defines the duration in seconds before the authorization granted by the rule expires.
- **flags** : Contains various flags that modify the behavior and characteristics of the rule.
- **tries** : Limits the number of allowed authorization attempts to enhance security.
- **version** : Tracks the version of the rule for version control and updates.
- **created** : Records the timestamp when the rule was created for auditing purposes.
- **modified** : Stores the timestamp of the last modification made to the rule.
- **hash** : Holds a hash value of the rule to ensure its integrity and detect tampering.
- **identifier** : Provides a unique string identifier, such as a UUID, for external references to the rule.
- **requirement** : Contains serialized data defining the rule’s specific authorization requirements and mechanisms.
- **comment** : Offers a human-readable description or comment about the rule for documentation and clarity.

### Example

```
# List by name and comments
sudo sqlite3 /var/db/auth.db "select name, comment from rules"
# Get rules for com.apple.tcc.util.admin
security authorizationdb read com.apple.tcc.util.admin
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>class</key>
	<string>rule</string>
	<key>comment</key>
	<string>For modification of TCC settings.</string>
	<key>created</key>
	<real>701369782.01043606</real>
	<key>modified</key>
	<real>701369782.01043606</real>
	<key>rule</key>
	<array>
		<string>authenticate-admin-nonshared</string>
	</array>
	<key>version</key>
	<integer>0</integer>
</dict>
</plist>
```
The following decoded rule illustrates `authenticate-admin-nonshared` on a documented macOS version:[\[1\]](#references)

```
{
  "allow-root": "false",
  "authenticate-user": "true",
  "class": "user",
  "comment": "Authenticate as an administrator.",
  "group": "admin",
  "session-owner": "false",
  "shared": "false",
  "timeout": "30",
  "tries": "10000",
  "version": "1"
}
```
## Authd

`authd` is the XPC service that evaluates Authorization Services requests. On current macOS builds its bundle can be inspected at `/System/Library/Frameworks/Security.framework/XPCServices/authd.xpc`; the path is an implementation detail and may differ across releases. Older releases wrote `/var/log/authd.log`; current releases primarily use the unified logging system, which can be queried with `log show`/`log stream` using an `authd` process predicate.[\[2\]](#references)[\[5\]](#references)

The `security` tool exposes several Authorization Services operations. A historical example invokes `AuthorizationExecuteWithPrivileges` with `security execute-with-privileges /bin/ls`. Apple deprecated that API in macOS 10.7; modern privileged helpers should use a launchd-managed helper and XPC authorization instead.[\[2\]](#references)[\[4\]](#references)

On releases that still support it, this uses `/usr/libexec/security_authtrampoline` and displays an authorization prompt before running the command as root:

## References
