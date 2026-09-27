---
title: "iOS Basic Testing Operations"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/ios-pentesting/basic-ios-testing-operations.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile/ios
---

## **Summary of iOS Device Identification and Access**

**Summary of iOS Device Identification and Access**

### **Identifying the UDID of an iOS Device**

**Identifying the UDID of an iOS Device**

To identify an iOS device uniquely, a 40-digit sequence known as the UDID is used. On macOS Catalina or newer, this can be found in the **Finder app**, as iTunes is no longer present. The device, once connected via USB and selected in Finder, reveals its UDID among other information when the details under its name are clicked through.[\[1\]](#references)

For versions of macOS prior to Catalina, iTunes facilitates the discovery of the UDID. Detailed instructions can be found [here](http://www.iclarified.com/52179/how-to-find-your-iphones-udid).[\[7\]](#references)

Command-line tools offer alternative methods for retrieving the UDID:[\[1\]](#references)

- **Using I/O Registry Explorer tool `ioreg`:**

```
$ ioreg -p IOUSB -l | grep "USB Serial"
```
- **Using `ideviceinstaller` for macOS (and Linux):**

```
$ brew install ideviceinstaller
$ idevice_id -l
```
- **Utilizing `system_profiler`:**

```
$ system_profiler SPUSBDataType | sed -n -e '/iPad/,/Serial/p;/iPhone/,/Serial/p;/iPod/,/Serial/p' | grep "Serial Number:"
```
- **Employing `instruments` to list devices:**

```
$ instruments -s devices
```
### **Accessing the Device Shell**

**Accessing the Device Shell**

**SSH access** is enabled by installing the **OpenSSH package** post-jailbreak, allowing connections via `ssh root@<device_ip_address>`. It’s crucial to change the default passwords (`alpine`) for users `root` and `mobile` to secure the device.[\[2\]](#references)

**SSH over USB** becomes necessary in the absence of Wi-Fi, using `iproxy` to map device ports for SSH connections. This setup enables SSH access through USB by running:[\[2\]](#references)

```
$ iproxy 2222 22
$ ssh -p 2222 root@localhost
```
**On-device shell applications**, like NewTerm 2, facilitate direct device interaction, especially useful for troubleshooting. **Reverse SSH shells** can also be established for remote access from the host computer.[\[2\]](#references)

### **Resetting Forgotten Passwords**

**Resetting Forgotten Passwords**

To reset a forgotten password back to the default (`alpine`), editing the `/private/etc/master.passwd` file is necessary. This involves replacing the existing hash with the hash for `alpine` next to the `root` and `mobile` user entries.[\[2\]](#references)

## **Data Transfer Techniques**

**Data Transfer Techniques**

### **Transferring App Data Files**

**Transferring App Data Files**

**Archiving and Retrieval via SSH and SCP:** It’s straightforward to archive the application’s Data directory using `tar` and then transfer it using `scp`. The command below archives the Data directory into a .tgz file, which is then pulled from the device:[\[3\]](#references)

```
tar czvf /tmp/data.tgz /private/var/mobile/Containers/Data/Application/8C8E7EB0-BC9B-435B-8EF8-8F5560EB0693
exit
scp -P 2222 root@localhost:/tmp/data.tgz .
```
### **Graphical User Interface Tools**

**Graphical User Interface Tools**

**Using iFunbox and iExplorer:** These GUI tools are useful for managing files on iOS devices. However, starting with iOS 8.4, Apple restricted these tools’ access to the application sandbox unless the device is jailbroken.[\[3\]](#references)

### **Using Objection for File Management**

**Using Objection for File Management**

**Interactive Shell with Objection:** Launching objection provides access to the Bundle directory of an app. From here, you can navigate to the app’s Documents directory and manage files, including downloading and uploading them to and from the iOS device.[\[3\]](#references)

```
objection --gadget com.apple.mobilesafari explorer
cd /var/mobile/Containers/Data/Application/72C7AAFB-1D75-4FBA-9D83-D8B4A2D44133/Documents
file download <filename>
```
## **Obtaining and Extracting Apps**

**Obtaining and Extracting Apps**

### **Acquiring the IPA File**

**Acquiring the IPA File**

**Over-The-Air (OTA) Distribution Link:** Apps distributed for testing via OTA can be downloaded using the ITMS services asset downloader tool, which is installed via npm and used to save the IPA file locally.

```
npm install -g itms-services
itms-services -u "itms-services://?action=download-manifest&url=https://s3-ap-southeast-1.amazonaws.com/test-uat/manifest.plist" -o - > out.ipa
```
### **Extracting the App Binary**

**Extracting the App Binary**

1. **From an IPA:** Unzip the IPA to access the decrypted app binary.
2. **From a Jailbroken Device:** Install the app and extract the decrypted binary from memory.<sup>[\[4\]](#references)</sup>

### **Decryption Process**

**Decryption Process**

**Manual Decryption Overview:** iOS app binaries are encrypted by Apple using FairPlay. To reverse-engineer, one must dump the decrypted binary from memory. The decryption process involves checking for the PIE flag, adjusting memory flags, identifying the encrypted section, and then dumping and replacing this section with its decrypted form.[\[4\]](#references)

**Checking and Modifying PIE Flag:**

```
otool -Vh Original_App
python change_macho_flags.py --no-pie Original_App
otool -Vh Hello_World
```
**Identifying Encrypted Section and Dumping Memory:**

Determine the encrypted section’s start and end addresses using `otool` and dump the memory from the jailbroken device using gdb.

```
otool -l Original_App | grep -A 4 LC_ENCRYPTION_INFO
dump memory dump.bin 0x8000 0x10a4000
```
**Overwriting the Encrypted Section:**

Replace the encrypted section in the original app binary with the decrypted dump.

```
dd bs=1 seek=<starting_address> conv=notrunc if=dump.bin of=Original_App
```
**Finalizing Decryption:** Modify the binary’s metadata to indicate the absence of encryption using tools like **MachOView**, setting the `cryptid` to 0.

### **FairPlay-aware partial analysis**

**FairPlay-aware partial analysis**

FairPlay does not make the complete `.app` bundle opaque: it protects a byte range of each encrypted Mach-O, described by `LC_ENCRYPTION_INFO` or `LC_ENCRYPTION_INFO_64` (`cryptoff`, `cryptsize`, and `cryptid`). Therefore, failure to obtain a decrypted main executable should switch the assessment to a **partial** mode instead of stopping it.[\[8\]](#references)[\[9\]](#references)

Check every executable Mach-O independently because the main executable and embedded frameworks can have different encryption states. `cryptid 1` identifies an encrypted range; a successfully dumped output should be re-parsed and report `cryptid 0`.[\[8\]](#references)

```
APP=Payload/Example.app
find "$APP" -type f -perm -111 -exec sh -c '
  file "$1" | grep -q "Mach-O" || exit 0
  echo "### $1"
  otool -l "$1" | grep -A 4 -E "LC_ENCRYPTION_INFO(_64)?"
' sh {} \;
```
#### Apple Silicon acquisition attempt

On Apple Silicon, first try acquiring the **official Mac-targeted copy** of a compatible iPhone/iPad app. This path is available only when the developer permits Mac distribution in App Store Connect under **Pricing and Availability → iPhone and iPad Apps on Apple Silicon Mac**; it is an optimization, not a universal replacement for device dumping.[\[8\]](#references)[\[9\]](#references)[\[10\]](#references)

[MobHunt](https://github.com/ivRodriguezCA/MobHunt) automates this workflow. Its acquisition helper uses `ipatool --device-family mac` to request a Mac-platform package, then attempts `mremap_encrypted`-based decryption and verifies the resulting Mach-O files.[\[8\]](#references)

```
brew install ipatool
ipatool auth login -e <apple-id-email> # Password and 2FA are prompted interactively
ipatool download -b <bundle-id> -o ./ipas --device-family mac
# From a MobHunt checkout:
./tools/decryption/decrypt_ipa.sh --ipa ./ipas/<app>.ipa --output ./decrypted
```
Do not infer success merely because an IPA was downloaded or a tool produced output. Record `analysis_mode: full` only after checking the required Mach-O outputs; otherwise record `analysis_mode: partial` and constrain subsequent tools to plaintext inputs.[\[8\]](#references)[\[9\]](#references)

#### Productive partial-mode triage

The following bundle artifacts remain useful without native-code decryption and should be analyzed before seeking a jailbreak-based dump.[\[8\]](#references)[\[9\]](#references)

| Artifact | High-signal review |
|---|---|
| `Info.plist` | URL schemes, associated domains, ATS exceptions, app groups, permission strings and routing configuration |
| Entitlements and `embedded.mobileprovision` | Keychain groups, application groups, capabilities, Team ID and provisioning constraints |
| `.plist` ,`.json` ,`.strings` ,`Settings.bundle` and Core Data models | Endpoints, cloud configuration, feature/debug flags, credentials and local schemas |
| `Frameworks/` and`.dylib` files | SDK inventory; test each Mach-O separately because some embedded code may be unencrypted |
| React Native JavaScript or Hermes bundles | Business logic, endpoints and secrets that remain outside the protected native-code range |

```
plutil -p "$APP/Info.plist"
codesign -d --entitlements :- "$APP" 2>/dev/null
security cms -D -i "$APP/embedded.mobileprovision" 2>/dev/null | plutil -p -
find "$APP" -type f \( -name '*.plist' -o -name '*.json' -o -name '*.strings' \
  -o -name '*.jsbundle' -o -name '*.bundle' \) -print
```
In partial mode, do **not** trust disassembly/decompilation of encrypted code, Swift metadata recovered from protected sections, or `strings` output attributed to encrypted `__TEXT`; these operations can produce noise that looks like valid evidence. Run them only against binaries or ranges whose decrypted state was verified.[\[8\]](#references)[\[9\]](#references)

### **Decryption (Automatically)**

**Decryption (Automatically)**

#### **frida-ios-dump**

**frida-ios-dump**

The [**frida-ios-dump**](https://github.com/AloneMonkey/frida-ios-dump) tool is employed for **automatically decrypting and extracting apps** from iOS devices. Initially, one must configure `dump.py` to connect to the iOS device, which can be done through localhost on port 2222 via **iproxy** or directly via the device’s IP address and port.[\[4\]](#references)

Applications installed on the device can be listed with the command:

```
$ python dump.py -l
```
To dump a specific app, such as Telegram, the following command is used:

```
$ python3 dump.py -u "root" -p "<PASSWORD>" ph.telegra.Telegraph
```
This command initiates the app dump, resulting in the creation of a `Telegram.ipa` file in the current directory. This process is suitable for jailbroken devices, as unsigned or fake-signed apps can be reinstalled using tools like [**ios-deploy**](https://github.com/ios-control/ios-deploy).

#### **frida-ipa-extract**

**frida-ipa-extract**

Frida-based IPA extractor for jailbroken devices; uses USB Frida sessions and optional SSH/SFTP for faster pulls.[\[6\]](#references)

- Requirements: Python **3.9+** ,`frida` ,`paramiko` , jailbroken device with**frida-server** (OpenSSH for SSH mode).
- Setup:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
- Usage:

```
python extract.py -U -f com.example.app -o MyApp.ipa
python extract.py -U -f com.example.app -o MyApp.ipa --sandbox --no-resume
python extract.py -H 192.168.100.32 -P 2222 -u root -p password -f com.example.app
```
- Flags: `-f <bundle>` spawns/attaches (or`--pid` for PID);`-o` sets output name.`-U` uses USB;`-H/-P/-u/-p` opens an SSH tunnel to`frida-server` 27042 and pulls via SFTP (can combine with`-U` ).`--sandbox` dumps the sandbox;`--no-resume` keeps the app suspended to avoid crashes and retries via a system process if the session drops.
- Troubleshooting: `Frida attach timed out` → use`-f` or`--no-resume` ;`script has been destroyed` →`--no-resume` or SSH transfer;`No running apps found` → start or spawn the app.

#### **flexdecrypt**

**flexdecrypt**

The [**flexdecrypt**](https://github.com/JohnCoates/flexdecrypt) tool, along with its wrapper [**flexdump**](https://gist.github.com/defparam/71d67ee738341559c35c684d659d40ac), allows for the extraction of IPA files from installed applications. Installation commands for **flexdecrypt** on the device include downloading and installing the `.deb` package. **flexdump** can be used to list and dump apps, as shown in the commands below:

```
apt install zip unzip
wget https://gist.githubusercontent.com/defparam/71d67ee738341559c35c684d659d40ac/raw/30c7612262f1faf7871ba8e32fbe29c0f3ef9e27/flexdump -P /usr/local/bin; chmod +x /usr/local/bin/flexdump
flexdump list
flexdump dump Twitter.app
```
#### **bagbak**

**bagbak**

[**bagbak**](https://github.com/ChiChou/bagbak), another Frida-based tool, requires a jailbroken device for app decryption:

```
bagbak --raw Chrome
```
#### **r2flutch**

**r2flutch**

**r2flutch**, utilizing both radare and frida, serves for app decryption and dumping. More information can be found on its [**GitHub page**](https://github.com/as0ler/r2flutch).

### **Installing Apps**

**Installing Apps**

**Sideloading** refers to installing applications outside the official App Store. This process is handled by the **installd daemon** and requires apps to be signed with an Apple-issued certificate. Jailbroken devices can bypass this through **AppSync**, enabling the installation of fake-signed IPA packages.[\[5\]](#references)

#### **Sideloading Tools**

**Sideloading Tools**

-
**Cydia Impactor** : A tool for signing and installing IPA files on iOS and APK files on Android. Guides and troubleshooting can be found on[yalujailbreak.net](https://yalujailbreak.net/how-to-use-cydia-impactor/) .
-
**libimobiledevice** : A library for Linux and macOS to communicate with iOS devices. Installation commands and usage examples for ideviceinstaller are provided for installing apps over USB.
-
**ipainstaller** : This command-line tool allows direct app installation on iOS devices.
-
**ios-deploy** : For macOS users, ios-deploy installs iOS apps from the command line. Unzipping the IPA and using the`-m` flag for direct app launch are part of the process.
-
**Xcode** : Utilize Xcode to install apps by navigating to**Window/Devices and Simulators** and adding the app to**Installed Apps** .

#### **Allow Application Installation on Non-iPad Devices**

**Allow Application Installation on Non-iPad Devices**

To install iPad-specific applications on iPhone or iPod touch devices, the **UIDeviceFamily** value in the **Info.plist** file needs to be changed to **1**. This modification, however, requires re-signing the IPA file due to signature validation checks.

**Note**: This method might fail if the application demands capabilities exclusive to newer iPad models while using an older iPhone or iPod touch.[\[5\]](#references)

## References
