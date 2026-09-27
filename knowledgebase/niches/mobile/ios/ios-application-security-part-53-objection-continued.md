---
title: "iOS Application Security Part 53 - Objection continued"
source: highaltitudehacks.com
source_url: https://highaltitudehacks.com/2018/07/29/ios-application-security-part-53-objection-continued.html
fetched_at: 2026-09-20T08:36:31Z
license: unspecified
category: mobile/ios
---

In this article, we will continue looking into Objection and some of the use cases it provides.

One of the most useful features objection provides is the ability to bypass jailbreak detection. This might not be always effective since it’s only looking for certain checks that an application will do to detect a jailbroken device and hooks them to return a false value. But any application can deploy a check not looked into by objection and the jailbreak detection bypass will fail. Neverthless, this feature might be useful in many cases where the apps are doing basic checks only.

It is also important to note that an application can just use some native C code to detect all the injected dylibs into the application and simply exit the app without any warning if it finds a dylib with the name FridaGadget. This has been observed in some apps that i have tested. A simple bypass would be to just change the name of the Frida dylib file to something else.

You can also simulate a jailbroken environment to understand how an application behaves in a jailbroken environment.

Objection uses jobs to list all the tasks that it is performing in the background. You can use the command *jobs list* to list the tasks and *jobs kill UDID* to kill them.

The hooking module is one of the most useful modules as it allows you to list the classes, methods, trace all the function calls and even dump the args or modify the return value.

Use the command *ios hooking list classes* to list all the classes.

Use the command *ios hooking list class_methods classname* to list all the methods for a particular class.

Use the command *ios hooking watch classname* to trace all the methods for a particular class.

We can now look for certain methods and dump the arguments (–dump-args) and return value (–dump-return). And the –dump-backtrace command will give you a list of the previous methods being called.

Let’s try and solve the Jailbreak Detection challenge in Damn Vulnerable iOS App.

And you can also set return values of methods. In this case, it is used to bypass Jailbreak Detection in Damn Vulnerable iOS App.

You can also enable Touch ID Bypass which as discussed in previous articles can be bypassed by hooking into the method -[LAContext evaluatePolicy:localizedReason:reply:]. This hooking technique will only work in some cases as discussed in a previous article on Touch ID bypass in this series. On devices with FaceID do some incorrect attmepts and then click on Enter passcode which will trigger the bypass.

Use the command *ios pasteboard monitor* to monitor the contents of the Pasteboard.

Use the command *ios sslpinning disable* to disable sslpinning. Ofcourse this method is not foolproof and tries to hook into some low level methods that are called while doing SSL pinning validation.

And finally, you can use the *ios ui* module to take a screenshot or just dump the view hierarchy.

In this article, we had a good look at some of the advanced functionalities that objection provides. In the next article, we will look at another essential framework named Needle to help with iOS security assessments.

**References**

1. https://github.com/sensepost/objection
