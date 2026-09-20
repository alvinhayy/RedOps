---
title: "iOS Application Security Part 47 - Inspecting Apps with Frida"
source: highaltitudehacks.com
source_url: https://highaltitudehacks.com/2018/07/23/ios-application-security-part-47-inspecting-apps-with-frida.html
fetched_at: 2026-09-20T08:36:31Z
license: unspecified
category: mobile/ios
---

In this article, we will talk about Frida. Frida is a dynamic instumentation toolkit which can prove to be extremely useful in iOS application assessments. It can be used to assess apps on jailbroken and non-jailbroken devices (provided you have the source code) .We will look at all these examples in this and the coming few articles.

Let’s start first with assessment over jailbroken devices. Frida basically works on a client-server model. The client is running on your computer and the server on the iOS device. To install frida on your computer, simple issue the following command.

On your jailbroken device, add the source https://build.frida.re. Then go to search and search for Frida.

One of the important things is to make sure both the Frida versions on the iOS device and the computer are same. Otherwise, frida won’t work. Now ssh into your jailbroken device and you will see a process with the name frida-server which is running.

From your computer, simply issue the command *frida-ps -U*. Make sure the jailbroken device is connected to your computer over USB. If you get similar output, it means Frida is all set up and running.

Actually, frida comes with a bunch of command line tools as can be seen here.

Issuing the command frida-ps will just show you a list of the processes running on your computer. But we are interested in i-devices. Running the command frida-ls-devices will show all the devices connected to the computer. We can interface with this device with frida-ps -U command. If there are more than one devices, you will need to specify the UDID.

Ok, so we are all set. Let’s now look at what we can do with Frida. In this case, we will be using the application Damn Vulnerable iOS app which you can download from [damnvulnerableiosapp.com](http://damnvulnerableiosapp.com). You might face issues with installing the older Objective C version of the app on iOS 10 or later versions because the original app was signed with SHA-1 but since iOS 10 Apple is using SHA-256 hashing algorithm. So you might need to unzip the IPA file, strip out the 64 bit architecture using jtool (or lipo) and then sign it. You can then repackage the app and install it again to the device using Cydia Impactor.

To see a list of all the applications installed on the device along with their unique identifier, run the *frida-ps -Uai* command.

To see all the running apps, use the *frida-ps -Ua* command.

To attach to a specific process, run the *frida -U processname* command. Make sure that the application is running in foreground on the device. The frida CLI can be used to emulate a lot of the features of Cycript.

However, in this article, we will look at the frida-trace CLI. This CLI can help you trace various method calls during the application runtime. This can be extremely useful in understanding the inner workings of the application. Its always a good idea to look at the help output as there are many options here.

To trace a particular function, you can specify it with the -i option. You can also provide a regex in the method section as shown in the figure below. For e.g, in the example below, you can trace the Crypto calls.

If you use the -I option, you can determine which module from Frida do you want to include, which is essentially the dylib from where all functions will be retrieved.

In case of DVIA (Objective-C version), you can go to the Broken Cryptography section and start the challenge. To trace a particular Objective C method, you can specify it with the -m option. If the method calls match the provided regex, you will see the output as shown in the image below.

This is extremely useful in understanding the inner working of the application and the same info can be used to patch or bypass certain methods. In the next article, we will look at more examples of using Frida.
