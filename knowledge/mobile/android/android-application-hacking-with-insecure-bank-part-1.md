---
title: "Android Application hacking with Insecure Bank Part 1"
source: highaltitudehacks.com
source_url: https://highaltitudehacks.com/2014/11/24/android-application-hacking-with-insecure-bank-part-1.html
fetched_at: 2026-09-20T08:36:31Z
license: unspecified
category: mobile/android
---

In this article series, we will learn at various concepts of Android application security while exploiting a vulnerable app InsecureBankv2. We will be looking at all the concepts from a noob’s perspective and hence i would recommend this blog series to beginners as well.

However, the first thing to do is set up a proper mobile pentesting platform for android application testing.

The first thing to do is download the Eclipse ADT bundle. You can then follow the instructions [here](https://developer.android.com/sdk/installing/index.html?pkg=adt) to install the ADT bundle. Once this is done, make sure you install the necessary sdk packages and libraries by following the instructions [here](https://developer.android.com/sdk/installing/adding-packages.html).

Inside the adt bundle folder and inside the sdk folder, there will be two folders, one with the name *tools* and the other with the name *platform-tools*. It’s important to add the location of your SDK platform tools and tools folder to the PATH environment variable. This is because you will be using most of the command line tools included in these directories and its good to have them added in the path environment variable. The command to add any path as an environment variable is *export PATH=/path/to/dir:$PATH*.

Do this for both the tools and the platform-tools folder. Once this is done, you can access all the command line tools without actually browsing over to their directory. To check if this is working, type the command *adb* and see if you are able to get an output like this.

To run the application on your computer, it is important to have a good emulator. Now the android virtual device manager utility in Eclipse allows you to create your own emulators. To know how to create these virtual devices, i would recommend you check [this](https://developer.android.com/tools/devices/index.html) article out. However, for this series, i am going to be using Genymotion to create my own emulators. There are many reasons for this. First of all, it is lightning fast and not as slow as the android emulators. Secondly, it is a rooted emulator unlike the android emulators. This means you have much more freedom of installing your own custom applications that can be used for auditing other android apps.

Once you install genymotion, you should sign up for a new account (it’s free) and create different emulators based on your need. Here is what my emulators look like.

Now get the latest code for the InsecureBankv2 application from [here](https://github.com/dineshshetty/Android-InsecureBankv2).

Start one of your genymotion emulators and see if you are able to get them running. Starting an emulator is as simple as clicking on the play button.

Inside the folder that you just cloned from github, there will be an apk file. You can install that application onto your emulator using the command *adb install InsecureBankv2.apk*

You will see that it successfully installed. And you can see the same on the emulator as well. But sometimes you might want to compile the application rather than run it with an apk file. To do that, open Eclipse and go to *File -> Switch Workspace*, and choose the Insecure bank folder that you just created. Now go to *File -> Import* and select *Existing Android code into workspace*.

Select your application folder and you will see that Eclipse will import the application into your workspace. Now click on the play button on the top to run your application. Make sure your genymotion emulator is running as well. Select to run it as an android application.

You will see that the application starts successfully on the genymotion emulator.

Also start the backend python server that the android application communicates with using the command *python app.py –port 8888*

In the application, go to Preferences and enter the IP address and port number of your system.

And now you can login to the application using the default credentials.

- dinesh/Dinesh@123$
- jack/Jack@123$

Also make sure that you install the following utilities. We will cover them in detail as and when they are required.

Also, connect to your emulator using the command *adb shell* and see what are the things you can do. I would really recommend you to have a look [here](http://developer.android.com/tools/help/adb.html) and try out all the commands possible with the Android debug bridge.

Another thing that you can read up is what you can do with all the command line tools available in Android. You can read it from [here](http://developer.android.com/tools/projects/projects-cmdline.html). In the next article, we will start at actual exploitation of the InsecureBankv2 application.
