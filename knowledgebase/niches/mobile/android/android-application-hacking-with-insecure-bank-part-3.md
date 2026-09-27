---
title: "Android Application hacking with Insecure Bank Part 3"
source: highaltitudehacks.com
source_url: https://highaltitudehacks.com/2015/03/28/android-application-hacking-with-insecure-bank-part-3.html
fetched_at: 2026-09-20T08:36:31Z
license: unspecified
category: mobile/android
---

In this article, we will look at attacking components in Android applications, starting with activities. But first, it is essential to understand what Android application components are. Android application components are the essential building blocks of an Android application. The behaviour and interaction between these components is defined in the manifest.xml file in the application. Mainly there are 4 types of components and it is important to understand their purpose and function.

The description of the 4 components given below has been taken from [this](http://www.tutorialspoint.com/android/android_application_components.htm) link.

1.
    Activities - They dictate the UI and handle the user interaction to the smartphone screen
2.
    Services - They handle background processing associated with an application.
3.
    Broadcast Receivers - They handle communication between Android OS and applications.
4.
    Content Providers - They handle data and database management issues.

#### Activities

An activity represents a single screen with a user interface. For example, an email application might have one activity that shows a list of new emails, another activity to compose an email, and another activity for reading emails. If an application has more than one activity, then one of them should be marked as the activity that is presented when the application is launched. An activity is implemented as a subclass of Activity class as follows:

```
public class MainActivity extends Activity {
}
```
#### Services

A service is a component that runs in the background to perform long-running operations. For example, a service might play music in the background while the user is in a different application, or it might fetch data over the network without blocking user interaction with an activity. A service is implemented as a subclass of Service class as follows:

```
public class MyService extends Service {
}
```
#### Broadcast Receivers

Broadcast Receivers simply respond to broadcast messages from other applications or from the system. For example, applications can also initiate broadcasts to let other applications know that some data has been downloaded to the device and is available for them to use, so this is broadcast receiver who will intercept this communication and will initiate appropriate action. A broadcast receiver is implemented as a subclass of BroadcastReceiver class and each message is broadcasted as an Intent object.

```
public class MyReceiver  extends  BroadcastReceiver {
}
```
#### Content Providers

A content provider component supplies data from one application to others on request. Such requests are handled by the methods of the ContentResolver class. The data may be stored in the file system, the database or somewhere else entirely. A content provider is implemented as a subclass of ContentProvider class and must implement a standard set of APIs that enable other applications to perform transactions.

```
public class MyContentProvider extends  ContentProvider {
}
```
#### Additional Components

There are additional components which will be used in the construction of above mentioned entities, their logic, and wiring between them. These components are:

1.
    Fragments - Represents a behavior or a portion of user interface in an Activity.
2.
    Views - UI elements that are drawn onscreen including buttons, lists forms etc.
3.
    Layouts - View hierarchies that control screen format and appearance of the views.</td>
4.
    Intents - Messages wiring components together.
5.
    Resources - External elements, such as strings, constants and drawables pictures.
6.
    Manifest - Configuration file for the application.

#### One of the most important attributes of components is the exported property. Here is the documentation from android about it.

#### android:exported

Whether or not the activity can be launched by components of other applications — “true” if it can be, and “false” if not. If “false”, the activity can be launched only by components of the same application or applications with the same user ID.The default value depends on whether the activity contains intent filters. The absence of any filters means that the activity can be invoked only by specifying its exact class name. This implies that the activity is intended only for application-internal use (since others would not know the class name). So in this case, the default value is “false”. On the other hand, the presence of at least one filter implies that the activity is intended for external use, so the default value is “true”.This attribute is not the only way to limit an activity’s exposure to other applications. You can also use a permission to limit the external entities that can invoke the activity (see the permission attribute).

Hence, if an activity is exported, it can be called by external applications. In order to test the vulnerable activity exercise in InsecureBank application, let’s first start the application on Genymotion emulator and start the backend server as well.

Once we start the app, we are presented with this login page. If the activity after a successful login is exported, then we can call that activity directly.

Let’s have a look at the manifest file of the application to see if we can find the relevant activity. To look at the manifest file, first decompress the application using apktool as shown in the image below. This will create an application folder and the manifest file will be located inside it.

Here is how the manifest file looks like. As you can see, there is an activity named *.PostLogin* which is set as exported.

We can call this activity directly using the activity manager tool in the emulator. Let’s have a look at the usage first.

To start an activity with the am tool, here is the command.

adb shell
am start -n com.package.name/com.package.name.ActivityName

In this case, the package name is com.android.insecurebankv2 as can be seen from the manifest file.

So let’s call the PostLogin activity by using the command shown below.

In the application, you can see that you have successfully bypassed the login page.

You can also call activity or other components using drozer. We will look at drozer in the next article.

There are a couple of ways to prevent from these kinds of vulnerabilities. First of all, the android:exported property should always be set to FALSE unless really necessary. Secondly, if the application needs to be called from some specific external applications, you can add custom permissions to the activity and only allow applications that requests that permission to call the activity.

Before we move on to the next article, make sure you have a proper understanding of the [Android manifest](http://developer.android.com/guide/topics/manifest/manifest-intro.html) file and the different components in an andorid application.
