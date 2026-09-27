---
title: "Reverse Engineering iOS Apps with Hopper Disassembler: From IPA to Jailbreak Detection"
source_url: https://medium.com/@Infosec-Arsenal-Diaries/reverse-engineering-ios-apps-with-hopper-disassembler-from-ipa-to-jailbreak-detection-b913511bfb0d
fetched_at: 2026-09-20T02:00:13Z
license: unspecified
category: mobile/ios
---

With these easy set up and help of Hopper Disassembler tool we will read between the binaries…

*“Our dead are never dead to us, until we have forgotten them.”* *-*George Elio

Welcome back, Security Scholars ! Previously in Infosec Arsenal Diaries, we learnt how to set up Hopper Disassembler on our Ubuntu machine. Now, it’s time to find out what’s hidden inside an IPA file. In today’s blog we will download Damn Vulnerable iOS App (DVIA-v2) and load its binary into Hopper to start reverse engineering. By the end of the blog we will be able to detect Jailbreak detection, Storage & Serialization and find hardcoded credential.

If you haven’t read the first part on How to Install and Use Hopper Disassembler on Linux no worries you can read it here : *click here to read first part*

**Targets that we will be covering today :**

1. Downloading DVIA v2 and Extracting the Binary ( cause hopper can’t digest IPA, gut issues)
2. Loading the Binary into Hopper ( No its not your drag and drop thing)
3. Getting Familiar with Hopper’s Loader prompt ( being less dumb )
4. Finding Vulnerabilities for starters

**About DVIA :** It’s an iOS app designed to be vulnerable, the ultimate sandbox for learning reverse engineering.

**Step 1 : Pilot**

**Step 2 : Installing the Unzip Utility**

`sudo apt-get install unzip`
Command to ensure the unzip utility is installed on VM, which is necessary for extracting the contents of the zip file.

**Step 3 : Setting Up the File Base**

 `cd ~/Downloads`
The ***cd*** command changes the current working directory to ***~/Downloads***, which is the ***Downloads*** folder in the user’s home directory (***~*** is a shortcut for the home directory). This command is used to navigate to the directory where the ZIP file (DVIA-v2-master.zip) is located

`unzip DVIA-v2-master.zip -d DVIA-v2`
The unzip command extracts the contents of the ***DVIA-v2-master.zip*** file into a directory named ***DVIA-v2*** (specified by the ***-d*** flag). This is done to organize the extracted files into a specific folder (***DVIA-v2***) rather than scattering them in the current directory.

**Step 4 : Surveying the Unzipped Files**

Hopper Disassembler is designed to analyze compiled binaries (Mach-O executables), not IPA files, which are ZIP archives containing the app’s binary and resources. You need to extract the IPA to access the Mach-O binary (e.g., DVIA-v2) inside the Payload/DVIA-v2.app folder, then load that binary into Hopper.

**Step 5: Extracting the DVIA-v2.ipa**

`unzip DVIA-v2.ipa -d DVIA-v2-extracted`
Create a new directory to keep things organized

**Step 6: Navigate to the Binary**

```
cd DVIA-v2-extracted/Payload
ls
cd DVIA-v2.app
ls
```
Look for DVIA-v2 (the Mach-O binary).

**Step 7: Load the Binary in Hopper**

A. First launch the Hopper and click on **File**. Then choose **Read Executable to Disassemble**.

**B.** Navigate to **~/Downloads/DVIA-v2/DVIA-v2-master/DVIA-v2-extracted/Payload/DVIA-v2.app. Select the DVIA-v2 file**

**C. Setting Disassembly Parameters**

The dialog has two main sections: **Options** and **Mach-O AARCH64 Options**, with the loader set to **Mach-O AARCH64**

Let’s look at each option and understand what they mean for our context. And if you have kept your brain in a safe locker then you can skip it.

## **Section 1: Options**

1. **Start automatic analysis after the file is loaded** : This tells Hopper to automatically analyze the binary (e.g., identify functions, strings, and Objective-C structures) after loading. This saves time and ensures you get a usable view of the code (e.g., pseudo-code, strings) without manual setup.
2. **Parse Objective-C sections if present** : DVIA-v2 is written in Objective-C, and this option ensures Hopper processes Objective-C metadata (e.g., class names, method names like checkJailbreak). This makes analysis easier, as you’ll see meaningful class and method names in the “Types” and “Labels” tabs. Without this, you’d see raw symbols, which are harder to interpret.
3. **Parse exceptions information if present** : This option processes exception-handling data (e.g., try-catch blocks), which can help Hopper reconstruct more accurate control flow in the pseudo-code. It improves the quality of the pseudo-code view (F5).
4. **Code sections contain procedures ONLY** : If checked, Hopper assumes code sections only contain procedures (functions), ignoring data mixed with code. For iOS apps, code sections may include inline data (e.g., constants), so leaving this unchecked allows Hopper to interpret the binary more accurately. This is the default for most analyses.
5. **Branch always stops procedures** : If checked, Hopper assumes branches (jumps) always mark the end of a procedure, which can fragment functions incorrectly. Leaving this unchecked lets Hopper better reconstruct procedures, especially in complex methods. It avoids splitting functions unnecessarily.

## **Section 2: Mach-O AARCH64 Options**

1. **Resolve LAZY bindings** : Lazy bindings in Mach-O binaries are references to external symbols (e.g., iOS framework functions like NSUserDefaults) resolved at runtime. Resolving them helps Hopper display meaningful names (e.g., [NSUserDefaults standardUserDefaults]) instead of raw symbols in the pseudo-code.

With these settings click **OK** to load the DVIA-v2 binary into Hopper.

## Time to find some bugs

There are so many key words that you can look for but for now lets look at Jailbreak detection and Serialization specific key words.

### Jailbreak/root detection:

Keywords you will look for :

`isJailbroken, Cydia,  /Applications/Cydia.app`
### Storage & Serialization

NSUserDefaults/Keyed Archiving:

`NSUserDefaults unarchiveObjectWithData NSKeyedUnarchiver`
### Hard-coded credentials

Thanks for hanging in there with me till the end. Hope you enjoyed the blog.

As with all things in cybersecurity, nothing is truly secure, only misunderstood or never explored. Keep looking, keep learning, and may your packets always find their route.
