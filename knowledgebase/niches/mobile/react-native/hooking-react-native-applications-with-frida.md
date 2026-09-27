---
title: Hooking React Native Applications with Frida | BeDefended Newsroom
source_url: https://newsroom.bedefended.com/hooking-react-native-applications-with-frida/
fetched_at: 2026-09-20T01:59:58Z
license: unspecified
category: mobile/react-native
---
Dynamic instrumentation is the ability to modify the behavior of a program by injecting code into its process. It happens while the app is running, without the need to recompile the application. Among the tools available, Frida is one of the most commonly used for instrumenting applications regardless of their platform. It works with Windows applications, MacOS, iOS, Android ones, as well as embedded systems like smart watches and TVs. It’s one of the go-to choices when doing Penetration Testing thanks to the fact that it’s open source and freely available.

## Why Dynamic instrumentation?

Having the ability to modify a program at runtime it’s the preferred way to interact with an application for reverse engineering and instrumentation purposes since only the bits of the application that we want to change are actually changed.

In the context of Android applications, which will be the focus of this article, the APK files (Android Packaging Format) can also be extracted into the individual Java files of the application and later repackaged. However, by doing so, we are modifying more than what we need: an extraction and then a re-bundle back into an “.apk” file can cause compatibility issues since the process sometimes doesn’t have a 1:1 match. This, in turn, can cause our target app to differ than the original in some functionalities or even not run at all if the extraction or the repackaging had errors.

With dynamic instrumentation the above downsides don’t happen, and, since we didn’t modify the files of the application but only the in-memory code, we don’t need to take care of many anti-tampering protections.

## The problem with React Native

React Native is a JavaScript framework created with the goal of cross-platform compatibility, which helps the developers to focus on the application logic instead of platform specific differences and implementations. React Native applications are increasingly common, with Fortune 500 companies often choosing this technology to develop their apps. For this reason, as Pentesters, we need to keep ourselves updated and understand better the inner workings of this framework. This article aims to do just that, with a focus on how to instrument a React Native Android application with Frida to modify its behavior at runtime.

*We have also mentioned about the importance of understanding more deeply the tested application in a recent article that talked about JavaScript Obfuscation, which you can find here.*

These kind of applications are mostly developed in JavaScript, so they have a different internal structure than the usual Java applications. React Native apps still have Java modules and classes, but they also have another file, called `index.android.bundle`, that contains the main logic and it’s written in JavaScript. Since we are not dealing just with Java code, our goal becomes to modify this JS Bundle file at runtime, without repacking the application. There are many guides online for debugging React Native applications, but only a few cover this topic from the point of view of a Reverse Engineer or Penetration Tester. Nonetheless, we had to find a way to test our clients applications in a comprehensive way rather than just on the surface, so we went deeper into the topic to find a solution.

## Initial workarounds

One of the first approaches that we have tried was using Frida to enable the developer mode of the React Native application and use `react-native-debugger` to attach to it. This turned out not to be working for applications of which you don’t have the original source code. That is mainly the case when doing penetration tests. On top of not having the source code, there would be another problem to take care of: the `NetworkSecurityPolicy`. Recent Android versions, starting from A9 (API 28), block by default clear-text HTTP connections, which is the easiest way you can go for using a local web-server hosting the Bundle file.

What about HTTPS instead? In our testing, there were some cases that would require additional tweaks to bypass the self signed certificate, so we didn’t go this route. We were aiming at something more portable that could apply to more applications and would be easy to run. Due to the presence of confidential information, uploading an index Bundle file to an online service that has a valid certificate or hosting it on our own production website is out of scope.

In case the above would’ve been viable, it’s possible to bypass the failure of the cleartext HTTP request by hooking into the `onFailure` method of the OkHttp library and manually making another request to a resource that would be known to work. It’s a quick workaround that takes advantage of the OkHttp library in order to easily have an object of type `okhttp3.Response`.

```
let BundleDownloader = Java.use(
    "com.facebook.react.devsupport.BundleDownloader$1"
  );
  BundleDownloader["onFailure"].implementation = function (call2, iOException) {
    console.log(
      `BundleDownloader.onFailure is called: call2=${call2}, iOException=${iOException}`
    );
    console.log("Send manual HTTP request");
    let req = "https://bedefended.com/";
    let OkHttpClient =  Java.use("okhttp3.OkHttpClient");
    let Builder = Java.use("okhttp3.Request$Builder").$new();
    let request = Builder.url(Java.use("java.lang.String").$new(req)).build();
    let response = OkHttpClient.$new().newCall(request).execute();
    console.log("Call onResponse");
    let obj = Java.use('com.facebook.react.devsupport.BundleDownloader$1').$new();
    obj["onResponse"](call2, response);
  };
```
From here, we have shifted our focus on the request to this Bundle file that is required in order to debug a React Native application. We have been trying to work around the security policy and we have ended up intercepting the HTTP request and replacing its answer with a modified JS file directly, rather than doing it via an HTTP request. It seemed like a good idea, until the limitations of this technique came not long after. At the beginning, this file was taken from the host machine, but we have moved it to be on the device once we have noticed it would be faster to load the new Bundle straight from the phone, as these files can easily be of a few hundred megabytes.

```
var str = Java.use("java.lang.String");
var file = Java.use("java.io.File").$new("/data/user/0/com.myproject/files/BridgeReactNativeDevBundle.js");
  var fis = Java.use("java.io.FileInputStream").$new("/data/user/0/com.myproject/files/BridgeReactNativeDevBundle.js");
  var bis = Java.use("java.io.BufferedInputStream").$new(fis);
  var bytes = [];
  var byteArr = Java.array("byte", [0x00]);
  var ch;
  while ((ch=bis.read()) != -1) {
    bytes.push(ch);
  }
  var str = "";
  for (var i = 0; i < bytes.length; i++) {
    str += String.fromCharCode(bytes[i]);
  }
```
Even with the file taken from the device and using it with a simple “Hello world” React Native application, this was extremely slow and it certainly wouldn’t scale well at all with bigger applications. We knew there has to be a better way, so we took a step back and went back to basics, which is the decompiled Java application with its official RN classes. An easier way than decompiling, since React Native is open source, is to visit the React Native repository on GitHub. This is the preferable way since it also contains comments that help giving more context to the code.

## First technique – react.devsupport

After studying more in detail the developer classes of a RN app, it turns out that when running the app with the Metro server running on the computer, the Bundle is also cached locally. Thus, even without a live Metro server, the cached Bundle would be used if available. This means that it would be enough to put our modified Bundle file in the location expected by the developer React Native classes and force the necessary conditions in order for the file to be loaded from there.

The original code that takes care of loading the Bundle from the cache is as follows, taken from the React Native GitHub repository:

```
if (packagerIsRunning) {
    mDevSupportManager.handleReloadJS();
} else if (mDevSupportManager.hasUpToDateJSBundleInCache()
        && !devSettings.isRemoteJSDebugEnabled()
        && !mUseFallbackBundle) {
    // If there is a up-to-date bundle downloaded from server,
    // with remote JS debugging disabled, always use that.
    onJSBundleLoadedFromServer();
} else {
    // If dev server is down, disable the remote JS debugging.
    devSettings.setRemoteJSDebugEnabled(false);
    recreateReactContextInBackgroundFromBundleLoader();
}
```
As the comments also explain it, the method we need to reach is `onJSBundleLoadedFromServer()`. The value of `mUseFallbackBundle` was found to be false already inside the application, so there is no need to change anything here. In case it is set to `true` instead, it is enough to search for the existing instance of `com.facebook.react.ReactInstanceManager` where `mUseFallbackBundle` has been initialized and change it to `false`.

Example:

```
const ReactInstanceManagerInstance = Java.choose("com.facebook.react.ReactInstanceManager", {
        onMatch: function (instance) {
            console.log("Found an instance of ReactInstanceManagerInstance:", instance);
            instance.setUseFallbackBundle(false);
        }
    });
```
For the other two functions, the override looks like this:

```
let DevSupportManagerBase = Java.use("com.facebook.react.devsupport.DevSupportManagerBase");
DevSupportManagerBase["hasUpToDateJSBundleInCache"].implementation = function () {
    return true;
};
let DevInternalSettings = Java.use("com.facebook.react.devsupport.DevInternalSettings");
DevInternalSettings["isRemoteJSDebugEnabled"].implementation = function () {
    return false;
};
```
Since these methods will be called only when the developer mode is enabled, the last override will be of the React Native application’s debug mode:

```
let AnonymousClass3 = Java.use("com.myproject.MainApplication$1");
AnonymousClass3["getUseDeveloperSupport"].implementation = function () {
    return true;
};
```
The method `getUseDeveloperSupport()` is usually found in the `MainApplication` class, but that’s not always the case. To find the right class, it’s possible to either use a decompiler like JADX and perform a full-text search or do it dynamically with a Frida snippet similar to:

```
Java.perform(function () {
  function searchClass(className) {
    try {
      var class1 = Java.use(className);
      var methods = class1.class.getDeclaredMethods();
      for (var i = 0; i < methods.length; i++) {
        if (methods[i].getName() === "getUseDeveloperSupport") {
          console.log("Found getUseDeveloperSupport in class:", className);
          break;
        }
      }
    } catch (err) {
      console.error("Error accessing class:", className, err);
    }
  }
  Java.enumerateLoadedClasses({
    onMatch: function (className) {
      if (className.startsWith("com.myproject")) {
        setTimeout(function () {
          searchClass(className);
        }, 100);
      }
    }
  });
});
```
*The timeout was added to avoid searching too fast and crash the application, which it seemed to occur during internal tests. For performance reasons, we also want to limit the search for classes from our application, in this example it’s `com.myproject`.*

Our modified `index.android.bundle` will need to be copied inside the application’s path from where it will be picked up and used instead of the original JS Bundle. In our example, the path will be `/data/user/0/com.myproject/files/BridgeReactNativeDevBundle.js`. The filename `BridgeReactNativeDevBundle.js` it’s the expected one, so the Bundle file needs to be renamed like this.

Now, we have a working version of the JS Bundle replacement at runtime on a RN application!

## Second technique – react.ReactNativeHost

Once we moved onto testing it on a real application during a Penetration Testing engagement, it was a fun discovery that not all applications have the React Native developer classes, because production applications may have them stripped from the final APK. We have realized that it’s only at this point that we were going closer to that more universal solution we were aiming for.

We’ve relied so far on the `com.facebook.react.devsupport` package to replace the index Bundle at runtime. But what if there was another way that uses more common classes? One of the base classes is `com.facebook.react.ReactNativeHost` and here is where the second, better technique comes in. Inside the `createReactInstanceManager()` method we read as follows:

```
protected ReactInstanceManager createReactInstanceManager() {
    [...]
    String jsBundleFile = getJSBundleFile();
    if (jsBundleFile != null) {
        builder.setJSBundleFile(jsBundleFile);
    } else {
        builder.setBundleAssetName(Assertions.assertNotNull(getBundleAssetName()));
    }
    [...]
}
```
By default, the method `getJSBundleFile()` will always return `null`, so the JS bundle will be loaded from the Assets of the APK. However, when this method returns a file path, the JS bundle will be loaded from any readable file-system path instead of the APK’s Assets files. This behavior is what we were after. It’s a more straightforward solution and, more importantly, there is no reliance on any React Native packages that are meant for developers nor does it need to have the developer mode enabled in order to work.

The Frida script is now like the following:

```
let ReactNativeHost = Java.use("com.facebook.react.ReactNativeHost");
ReactNativeHost["getJSBundleFile"].implementation = function () {
    console.log(`ReactNativeHost.getJSBundleFile is called`);
    return "/data/local/tmp/BridgeReactNativeDevBundle.js";
};
```
This version is also more universal because there is no need to find the class where to set the `getUseDeveloperSupport()` or for the JS Bundle file to be at an application specific path, as long as the file is in a readable location.

## Python script for live-reloading

We are big fans of scripting and automation, which in our experience is often a must in Penetration Testing. Understanding the logic of the application and exploiting an issue can be a complex and long process. A process that often can be applied to other, similar applications. Automation is like creating a blueprint for the steps you’ve already taken once. For these reasons, we wrote a Python script and thanks to it we’re back to focus more on doing actual Pentesting!

The script takes care of watching for changes in the local JS bundle, pushing it to the device every time it is modified and re-spawning the application while hooking it with the necessary changes so that our Bundle is used instead of the original.

You can find the final script at `https://github.com/BeDefended/file-inject`.

Demo:

## Conclusion

Trends and technologies often change and new things are created every year but, as a cyber security consultants, it is necessary to stay updated. Sometimes, there is little to no previous research that you can start from. That was the case with runtime hooking of React Native applications using Frida.

**Note**: this technique targets React Native’s legacy (Bridge) architecture, where the app is instantiated through `ReactInstanceManager` / `ReactNativeHost`. Since RN 0.76 (October 2024) the New Architecture (bridgeless, `ReactHost`) is the default, and on those apps this instantiation path may not exist, so the hooks would need a different entry point. The approach still applies to the many apps on the legacy architecture; check which one your target uses.

*Be aware of new programming framerworks. BeDefended.*

<sub>Further reading on reversing React Native applications:</sub> <sub>https://laripping.com/blog-posts/2020/04/17/debugging-react-native-apps.html</sub>
