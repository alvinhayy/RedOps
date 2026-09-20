---
title: "iOS Application Security Part 55 - Inspecting iOS apps with Passionfruit"
source: highaltitudehacks.com
source_url: https://highaltitudehacks.com/2018/07/31/ios-application-security-part-55-inspecting-ios-apps-with-passionfruit.html
fetched_at: 2026-09-20T08:36:31Z
license: unspecified
category: mobile/ios
---

In this article, we will have a look at passionfruit which is an iOS blackbox app analysis tool based on Frida . It also provides a really nice web GUI which makes analysis relatively easy. Here is the list of features as per their [Github](https://github.com/chaitin/passionfruit) page.

- Cross plarform web GUI!
- Also supports non-jailbroken device (see Non-jailbroken device).
- List all url schemes.
- Check signature entitlements.
- List human readable app meta info (Info.plist).
- Capture screenshot.
- Checksec: see if target app is encrypted, and has enabled PIE, ARC and stack canary.
- App sandbox file browser. Directly preview images, SQLite databases and plist files on device. You can always download the file for further investigation.
- Check the loaded frameworks. Hook exported native functions from these dylib to print the arguments and stack trace.
- Log SQLite operations.
- Log and try to bypass jailbreak detection.
- List Objective-C classes from app, hook the methods and inspect the arguments and stack trace.
- Dump KeyChain, BinaryCookies and UserDefaults.

To install Passionfruit, simple run the command *npm install -g passionfruit*

Once installed, just run the command *passionfruit* to run it. It will start a server on localhost.

Head over to the address mentioned. Please note that you need to have a jailbroken device connected over USB which has Frida installed on it. However, if there is no jailbroken device connected, then the app to be inspected needs to have the FridaGadget.dylib file injected into it. This has been explained in a lot of detail in the previous articles in the same series. You will be greeted with a UI like this.

Clicking on any app will just spawn the app on the device. And you will see a lot of useful information about the app, which includes the Bundle and the Data Directory, the entitlements used by the app, the URL schemes and the contents of the Info.plist file.

This is extremely useful information. On the top you can also see some options about the binary (PIE, ENC, ARC, Stack Canary etc). Ideally you will be scrambling for this infomration from the command line. You can also just browse the contents of the device filesystem using this web GUI. For e.g, let’s click on the Data directory.

Now let’s head onto the Documents directory.

We can view plist or sqlite files using the inbuilt viewers that come with passionfruit.

The Modules tab will show you all the loaded modules with this application.

And the Classes tab will show you all the loaded classes into this application.

Clicking on any class will show you the corresponding methods for that class. If you click on any of these methods, it will create a hook for it. If this method gets called, you will see it in the Console Tab. You can manage these hooks using the *Manage Hooks* tab on the top right.

The code runner tab will allow you to run Frida scripts in javascript.

The Storage section will show you all the data stored via Keychain, UserDefaults or Cookies APIs.

This was an intro to using Passionfruit. As it can be seen, this tool can be extremely useful in assessing the security of iOS apps because of its nice UI that gives a plethora of info about the application which would normally require some decent effort to gather.

The following tests were performed on a jailbroken iPhone6 device running iOS 10.0.1.

**References**

1. https://github.com/chaitin/passionfruit
