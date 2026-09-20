---
title: Bypass SSL Pinning for Flutter
source_url: https://medium.com/@appsecwarrior/bypass-ssl-pinning-for-flutter-a2f9ae85762e
fetched_at: 2026-09-20T02:00:10Z
license: unspecified
category: mobile/flutter
---

## What is Flutter?

Flutter is an open source framework by Google for building beautiful, natively compiled, multi-platform applications from a single codebase.

When Flutter launched in 2018, it mainly supported mobile app development. Flutter now supports application development on six platforms: iOS, Android, the web, Windows, MacOS, and Linux.

## What is SSL Pinning Bypass?

SSL pinning bypass is a technique used to bypass the security feature known as SSL pinning, which is also called certificate pinning. SSL pinning is a security measure that ensures the client only trusts a specific certificate for a particular domain. This is done to prevent man-in-the-middle (MiTM) attacks where an attacker could use a forged certificate to intercept the traffic between the client and the server.

In SSL pinning bypass, an attacker or a security researcher can bypass this security measure to inspect the traffic between the client and the server. This can be done using various techniques such as using a proxy, modifying the app’s code, or using a tool like Frida to disable the SSL pinning feature.

## **How to determine if a mobile application was developed using Flutter or Android Studio?**

1. You can determine if an APK was developed using Android Studio or Flutter by examining the APK’s AndroidManifest.xml file. If the APK was developed using Android Studio, you will typically find attributes such as android:versionCode, android:versionName, and package in the manifest. If the APK was developed using Flutter, the package attribute will have a flutter prefix, and there will also be a meta-data element with a flutterEmbedding attribute. This attribute will have a value of 2 if the APK was developed using Flutter
2. **Upload the APK File** : Upload the APK file on a website like javadecompilers.com. If you find a folder named`flutter` in sources, then the app is a Flutter app
3. Another way to determine if an APK was developed using Flutter is to look for the presence of a **libapp.so** file in the APK. This file is a shared object (SO) file that is used by Flutter. If this file is present, it’s a strong indication that the APK was developed using Flutter.

## **Testing Lab Environment**

1. Windows 11 64 bit
2. Android Studio 2022.3.1 (Build #AI-223.8836.35.2231.10406996, built on June 29, 2023)
3. AVD x86_64,arm64_v8a (rooted)
4. API level 31
5. Java (openjdk version “17.0.8” 2023–07–18)
6. App.apk (developed in Flutter)
7. Burp Suite (pro 2023.3)
8. uber-apk signer v 1.3.0

## What Is The Deference SSL Pinning — Flutter vs Android apk application.

Flutter applications have unique characteristics that make SSL pinning bypass more challenging. However, there are several techniques available to circumvent SSL pinning in Flutter apps. One such method involves the use of the ReFlutter framework.

**ReFlutter** is a tool designed to aid in the reverse engineering of Flutter applications. It utilizes a pre-compiled, patched version of the Flutter library that is primed for repackaging applications. This library has been modified in its snapshot deserialization process, enabling dynamic analysis to be performed. This makes it a valuable resource in bypassing SSL pinning in Flutter applications.

## **Flutter SSL bypass Demo**

Lets begin the Flutter App.SSL pinning.

1. Install **reFlutter** framework via Terminal

`pip3 install reflutter`
2. Install app in AVD (adb install <file name> or simply drag N drop)and set proxy in emulator and test if your burp suite intercept traffic. (If you not have idea how to set up burp for intercept traffic kindly check URL)

3. Set Proxy in AVD like below IP =192.168.1.2 i.e. your base machine address (get base address via terminal cmd will be **ipconfig**) and set any 4 digit number as a port no.

3. Now we will check the traffic intercept for HTTP. we successfully get the request and response.

4. Now we will do same thing for HTTPS. We’ve come across an HTTPS error due to a failed SSL handshake. You can view the details of this issue in the **Event log**, as shown in the screenshot.

5. Lets Bypass this using **reFlutter** framework. run reflutter <application.apk> and select option 1 and set burp suite IP.

6. Now we will get release.RE.apk but this apk is not sign yet. We have to sign manually and we can used any tool like uber-apk-signer in here.

`java -jar uber-apk-signer-1.2.1.jar - apk release.RE.apk`
7. How to run .jar file **java -jar jarfilename.jar**

This Java JAR run command assumes the JAR is located in the current folder. If the JAR file to run is located in a different folder, you’ll need to provide a full path to the file.

8. Now, install newly signed apk and remove previous one.

9. Lets configure the burp Suite (open Burp suite > proxy > proxy setting > add > binding > enter port no > select base machine IP address from list.

10. Now configure request handling (open Burp suite > proxy > proxy setting > add > request handling > click on support invisible proxying.

Invisible proxying allows non-proxy-aware clients to connect directly to a Proxy listener. This is useful when the target application uses a thick client component that runs outside of the browser, or a browser plugin that makes HTTP requests outside of the browser’s framework

11. Remember we need to turn off all the proxies (that we setup in point no 3)because reflutter is already modified and set the proxy settings in the patched app.

12. Now we can success fully bypass the SSL Pinning in app.

## **Other way to Bypass**

1. Modifying the App’s Code: If the SSL pinning is implemented in the app’s code, you can modify the code to disable the SSL pinning. This requires decompiling the app, which is often protected by obfuscation.
2. Using a Dynamic Instrumentation Tool: Tools like Frida can be used to inject scripts into the app and disable the SSL pinning. This works even if the app’s code is obfuscated.

SSL pinning bypass in Flutter apps can be achieved by using the `flutter_inappwebview` plugin. This plugin provides a powerful WebView for Flutter that allows you to intercept and modify the requests made by the WebView.

```
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
Future main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await FlutterDownloader.initialize(
      debug: true // optional: set false to turn off printing logs to console
      );
  runApp(new MyApp());
}
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      home: new MyHome(),
    );
  }
}
class MyHome extends StatefulWidget {
  @override
  _MyHomeState createState() => new _MyHomeState();
}
class _MyHomeState extends State<MyHome> {
  InAppWebViewController webView;
  String url = '';
  double progress = 0;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Container(
            child: Column(children: <Widget>[
      Container(
        padding: EdgeInsets.all(20.0),
        child: Text(
          "URL: $url",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      (progress != 1.0)
          ? LinearProgressIndicator(value: progress)
          : Container(),
      Expanded(
        child: InAppWebView(
          initialUrl: "https://www.example.com",
          initialHeaders: {},
          initialOptions: InAppWebViewGroupOptions(
            crossPlatform: InAppWebViewOptions(
                debuggingEnabled: true,
                useShouldInterceptRequest: true),
          ),
          onWebViewCreated: (InAppWebViewController controller) {
            webView = controller;
          },
          onLoadStart: (InAppWebViewController controller, String url) {
            print("started $url");
            setState(() {
              this.url = url;
            });
          },
          onLoadStop: (InAppWebViewController controller, String url) async {
            print("stopped $url");
            setState(() {
              this.url = url;
            });
          },
          onProgressChanged: (InAppWebViewController controller, int progress) {
            setState(() {
              this.progress = progress / 100;
            });
          },
          shouldInterceptRequest: (controller, request) async {
            if (request.url.toString().contains("example.com")) {
              return InterceptionResponse(
                  action: InterceptionAction.CONTINUE, data: null);
            }
            var modifiedHeaders = request.headers;
            modifiedHeaders['header_key'] = 'header_value';
            return InterceptionResponse(
                action: InterceptionAction.USE_NEW_REQUEST,
                data: new WebResourceRequest(
                    url: request.url, method: 'POST', headers: modifiedHeaders),
                isDownload: false,
                isForMainFrame: true);
          },
        ),
      )
    ])));
  }
}
```
In this example, the `shouldInterceptRequest` method is used to intercept the requests made by the WebView. If the request's URL contains `example.com`, the method returns `InterceptionAction.CONTINUE`, which allows the request to continue. If the URL does not contain `example.com`, the method modifies the request's headers and returns `InterceptionAction.USE_NEW_REQUEST`, which uses a new request with the modified headers.

How to implement SLL Pining there is good resource , you can use ssl_pinning_plugin: ^2.0.0

**References**: https://securitycafe.ro/2022/02/01/root-detection-and-ssl-pinning-bypass/

**Application Credit (**Jeroen Beckers**)** : https://blog.nviso.eu/2020/05/20/intercepting-flutter-traffic-on-android-x64/
