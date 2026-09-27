---
title: Runtime Mobile Security (RMS) – How To Instrument Android Java Classes And Methods At Runtime
source_url: https://securitycafe.ro/2022/03/07/runtime-mobile-security-rms-how-to-instrument-android-java-classes-and-methods-at-runtime/
fetched_at: 2026-09-20T01:59:49Z
license: unspecified
category: mobile/android
---

Runtime Mobile Security (RMS) is a powerful web interface powered by Frida that helps you manipulate **Android and iOS Applications** at **Runtime**. If you don’t know what Frida is, I recommend you take a look at the previous article, ROOT DETECTION AND SSL PINNING BYPASS. Basically, what RMS does is that it allows you to easily dump all the loaded classes and their methods, hook every class and method on the fly, load custom-made scripts, and many more.

## Prerequisites

1. NodeJS installed on your computer

sudo apt update
sudo apt install nodejs
sudo apt install npm

1. FRIDA’s CLI tools installed on your computer

python3 -m pip install frida-tools

1. **FRIDA server up and running** on the target device

## Installation

As per their GitHub, the steps are pretty straightforward

1. Open the terminal and run the following command
  - `npm install -g rms-runtime-mobile-security`
2. Make sure frida-server is up and running on the target device.
3. Launch RMS via the following command
  - `rms` (or`RMS-Runtime-Mobile-Security` )
4. Open your browser at `http://127.0.0.1:5000/`
5. Start enjoying RMS

## Explore The Web Interface

If you successfully installed and ran the tool, you should be able to see the following interface

As can be seen from the above screenshot, the RMS already identified the target device as *Samsung A50* with the corresponding specifications. You should note that there is another tab, which is used to configure your target device, e.g. set the IP address and the listening port if you are using a remote device.

### Hooking The Target Application

Since everything is set up and the RMS successfully detected your testing device, you should be able to launch the RMS instance by hooking it into the target package. Just for testing purposes, I created a simple Android application that requires its users to provide an encryption key and a password to access hidden functionalities. The application can be found on my GitHub page, https://github.com/St3v3nsS/AndroidTestRMSApp. If you successfully installed the application in the target device, you should be able to select it from the *package name* field by typing in *st3v3nss*.

### Interact With The Application

Now that we started the RMS, another view pops up and allows us to select one of the multiple functionalities such as dumping classes, analyzing changes inside classes, hooking specific classes, and so on. Going back to the testing application, we can see that it has one security protection: we are not allowed to run the application on rooted or broken devices.

If you read the previous article that teaches you how to bypass Root Detection mechanisms, you are good to go to bypass this restriction. But as we are discovering a new tool, I want to show you a bypass method using the RMS’s built-in functionality for on-the-fly hooking. First, go to the *Load Frida Script* tab, select the built-in script for *system_exit_bypass* and run that.

### Jadx-Gui And The Dynamic Instrumentation

Inspecting the application further using *jadx-gui*, we discover that firstly, it checks if the input key is equal with a key returned by the *getKey()* method, and finally, if the input password is equal with the decrypted password stored on the shared preference file. The following lines are responsible for the aforementioned: `if (!obj.equals(getKey()))` and `String decrypt = Crypto.decrypt(obj, getSharedPreferences("pref", 0).getString("password", ""));`. With that said, let’s hook the above methods and see if any sensitive data is passing by. In the *Dump TAB*, select *Load classes*, then *Insert a Filter* to filter only for specific classes, then *Load Methods* for the filtered classes, and then press the *Hook all methods* button.

### Exploit The Application

The RMS is now fully set up and ready to perform the requested actions. It would allow us to bypass the detection mechanism and intercept the sensitive data exchanged between methods. Go ahead and press the *Quit* button in the application and check if you can interact with the Login interface. By now, you should have the same output in RMS as in the following screenshot:

By pressing the *Login* button, an error is shown, indicating that we entered the wrong encryption key, but looking at the RMS output, we can see the output of the *getKey()* method.

Using the same approach on the *Password* field, we can intercept the *Crypto.decrypt()* method and obtain the plain-text password after it was decrypted and before it is compared to the input value. We can send the same random password, but this time using the right encryption key, and we will be able to obtain the original password from the RMS output.

Finally, using the genuine encryption key and password, we can log in to the application and discover the new attack surface. As this is a mock application specifically built to learn the RMS tool, there is no other attack surface, but in your testing application, this could be just the initial steps.

## Further Steps

As you have already seen, the Runtime Mobile Security platform combines multiple functionalities of the Frida framework and offers you a collection of methods to aid with your penetration tests. Runtime instrumentation can help you find issues that might otherwise go undetected. Of course, RMS has much more functionalities that I didn’t present and could be the subject of another blog post. But until then, I hope you learned something today that will help you pentesting the mobile applications, both Android and iOS, at runtime. If you have further questions, don’t hesitate to ask.
