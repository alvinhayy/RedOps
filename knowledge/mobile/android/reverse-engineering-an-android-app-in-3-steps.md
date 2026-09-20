---
title: Reverse-Engineering An Android App In 3 Steps
source_url: https://devilslane.com/reverse-engineering-an-android-app-in-3-steps/
fetched_at: 2026-09-20T01:59:47Z
license: unspecified
category: mobile/android
---

Ever wondered what an app is doing under the hood? Curious about what API it is talking to? Suspicious about network activity? Want to bypass dodgy paywall features? Well, you don't have to be an elite haXX0r to break things down. But you run into annoying snags on the way.

## Getting an APK from the Google Play Store

The Android app itself - the legacy version anyway - is a zip file with the extension changed to to .apk (Android Package Kit). The newer version, called a "bundle" which includes that next to other assets, has the extension .xapk. Developers may use a simplified language like Kotlin or a Javascript web "bridge" like React Native for rapid authoring, but the end result is a set of Java class files.

Google, rather cleverly, doesn't give the end user - you - the raw apk installer file. It uses a download service on the device to request and receive it in the background to ensure an automatic installation.

So, once you have found your app in the Google Play Store, copy its full URL or namespace, then head to: https://apps.evozi.com/apk-downloader/

You can of consult other app stores for direct downloads, such as:

Other app stores: https://en.wikipedia.org/wiki/List_of_Android_app_stores

## What's in the APK file?

It's a zip file, so all you need to do is extract the contents as you normally would. Or you can open it directly in Android Studio as a project, using its "inspect" feature.

- `assets` — directory with application assets (images, fonts etc).
- `com` — directory with application code (could also be org).
- `res` — directory with all resources that are not compiled into`resources.arsc` . These are all resources except the files in`res/values` . All XML resources are converted to binary XML, and all`.png` files are optimized (crunched) to save space and improve runtime performance when inflating these files.
- `lib` — directory with compiled native libraries used by the app. Contains multiple directories — one for each supported CPU architecture (ABI).
- `META-INF` — directory with APK metadata, such as its signature.
- `AndroidManifest.xml` — application manifest in the binary XML file format. This contains application metadata — for example, its name, version, permissions, etc.
- `classes.dex` — file with app code in the Dex file format. There can be additional .dex files (named`classes2.dex` , etc.) when the application uses multidex.
- `resources.arsc` — file with precompiled resources, such as strings, colors, or styles.
- `some-name.properties` - file with metadata, such as version numbering.

## Decompiling back to the raw source code

Code written in Java, like C, is compiled into binary. The source code, written in a text editor, is compiled into Java Bytecode (.class files) so it can run in the Java Virtual Machine (VM) on the device. What you have in the APK is compiled bytecode, which we can't read as text.

The index and contents of all the .class files is found in classes.dex. It's a combined central repository of compiled Java bytecode for the entire app. It may have been built in React or Kotlin, but it ends up here.

We need to convert the combined `classes.dex` file into a standard Java archive file (.jar).

For that, we can use **dex2jar**: https://github.com/pxb1988/dex2jar

Download into the same directory, extract, etc, then run:

`sh d2j-dex2jar.sh -f ~/location/of/your/app.apk -o /where/to/save/app.jar`
Now we have a .jar file, and we can read its contents with a Java Decompiler. An example is **JD-JUI**.: https://java-decompiler.github.io/

Once you open the .jar, you can browse the decompiled source code as normal text. Voila!

## Intercepting the live network traffic

This is a bit trickier. What is it sending, to whom, and where? If the code is making network requests, we want to see the raw GET and POST http traffic. For this, we need to launch a **Man-In-The-Middle** (MITM) eavesdropping attack.

### Removing developer security measures

The first thing to know is Android apps often use a technique known as **Certificate Pinning** to avoid it.  As NetGuru explains:

*To avoid this [MITM] exploit, developers should implement Certificate Pinning. It’s a method that depends on server certificate verification on the client side. This verification requires the server certificate or its fingerprint to be previously known to the mobile app. When establishing a connection with the server, the app should compare the fingerprint with a certificate from the remote server. If the fingerprints are identical, then the connection is valid and the data transfer can proceed. If the fingerprints are not identical, then the app should reject the connection immediately, as it’s compromised.*

In essence, the app has a copy of the SHA-256 signature of the API's SSL cert embedded within it (i.e. as a whitelist), and will only establish HTTP connections with an end server for which it can verify.

More: https://docs.mitmproxy.org/stable/concepts-certificates/#certificate-pinning

To remove all of this, including the new Android 7+ Network Security Configuration, we can use the handy tool **apk-mitm** project: https://github.com/shroudedcode/apk-mitm

From the docs:

`apk-mitm` automates the entire process. All you have to do is give it an APK file and `apk-mitm` will:

- decode the APK file using Apktool
- replace the app's Network Security Configuration to allow user-added certificates
- modify the source code to disable various certificate pinning implementations
- encode the patched APK file using Apktool
- sign the patched APK file using uber-apk-signer

```
$ apk-mitm example.apk
  ✔ Decoding APK file
  ✔ Modifying app manifest
  ✔ Replacing network security config
  ✔ Disabling certificate pinning
  ✔ Encoding patched APK file
  ✔ Signing patched APK file
   Done!  Patched APK: ./example-patched.apk
```
Voila. We now have an APK which we can fool into trusting our middleman.

### Trapping the traffic with a network proxy server

What we have to do at this point is establish a middleman server to record and relay HTTP requests. This is surprisingly difficult. Raw HTTP without SSL is simplistic if you are using something like *Squid* (http://www.squid-cache.org/), but things get difficult when it comes to HTTPS.

For a secure TLS connection, a proxy has to create an encrypted SSL tunnel with the other server through the proxy. Beyond that. **it cannot see what is being requested through the tunnel**. There is no URI or body visibility.

Squid, for example, will only log an SSL tunnel connection to a host, but nothing else. No GET, no POST, no PUT. Just where it connected to.

This is where the excellent **mitmproxy** comes in: https://mitmproxy.org/

From the docs:

***mitmproxy** is a console tool that allows interactive examination and modification of HTTP traffic. It differs from mitmdump in that all flows are kept in memory, which means that it’s intended for taking and manipulating small-ish samples.
**mitmweb** is mitmproxy’s web-based user interface that allows interactive examination and modification of HTTP traffic. Like mitmproxy, it differs from mitmdump in that all flows are kept in memory, which means that it’s intended for taking and manipulating small-ish samples.*

Using it is simple: download the binaries onto your proxy machine, and run one of them. The proxy server runs on port 8080, and the web viewer on 8081.

`mitmweb --web_host 0.0.0.0`
Open your browser to `http://your_machine:8081/` and you have a DevTools-style interface. Make sure to enable "show event log" in the options.

All we need to do now is tell Android to send all network requests through that proxy server, and to trust it. Add a proxy server to the Wifi connection through its settings (more: https://www.howtogeek.com/295048/how-to-configure-a-proxy-server-on-android/). Your host is the IP, and the port is 8080.

If you use your device's web browser now, you will get a warning saying the connection is not secure and being eavesdropped on. Because, of course!

In mitmproxy's event logs, you will see entries such as:

`Client TLS handshake failed. The client does not trust the proxy's certificate for domain.com`
These will appear against Google's underlying "online" status checker, which looks like GET `client3.google.com/generate_204`.

At this point, you can go back to the original APK and add a SHA256 signature of the end servers you want it to recognise, or simply make it trust the proxy.

Visit http://mitm.it/ in the device web browser. You will see one of two things:

1. Raw text informing you traffic is not going through the proxy;
2. A list of CA certificates to download.

We need to tell Android to *trust* the proxy server middleman by storing its CA certificate.

- Download the `.cer` file for your device onto disk.
- Add the CA certificate into Android:

More: https://docs.mitmproxy.org/stable/concepts-certificates/

Now, start browsing and/or using your app, and the traffic will appear in your *mitmweb* browser page.

## Practical example: a random "swipe" dating app

*Match* is easily the king of these, but we could also try *Tinder* (hookups), *eHarmony* (a con), Hinge (snobby), *Bumble* (gender studies graduates), and more. For demonstration purposes, let's use the relatively new **Upward** app, which is now owned by Match.

Our goal here? These apps are expensive to use, and ask you to upgrade to see your "matches" or "likes", which are blurred out. *Question: Are there enough good matches to pay for it?*

Moreover, how frequently are the accounts powered by ML chatbots and AI deepfake imagery?

App URL: https://play.google.com/store/apps/details?id=com.affinityapps.twozerofour

First, let's get the APK. Enter `com.affinityapps.twozerofour` into https://apps.evozi.com/apk-downloader/  . Download.

What's inside? Unzip it.

We have Kotlin, Firebase, and 13MB of compiled app classes. There's a LOT more in there than you see in the app, which implies it might be a white-label product.

Second, let's strip the security from it.

`apk-mitm com.affinityapps.twozerofour_977_apps.evozi.com.apk`
Which will give us a new file: `com.affinityapps.twozerofour_977_apps.evozi.com-patched.apk`.

Third, let's get at its source code.

`sh d2j-dex2jar.sh -f ./com.affinityapps.twozerofour_977_apps.evozi.com.apk -o /./upward.jar`
Open up that in our Java Decompiler and we can see it was written originally in Kotlin. The source code is under `com` > `aa` > `swipe`. We can see it uses an encrypted SQLite for storing user settings.

It's Kotlin, so it's not exactly too friendly for exploration. What we really want is the network activity, not the UI. The picture blurring will take place on the client side because it's simply too expensive to store them as duplicates in the cloud.

Fourth, let's set up the proxy in Android, trust its certificate, and start using the patched version of the app installed on the device.

We have an immediate request:

`GET https://www.upward-app.com/api/application/countrycodes`
What we can learn from the response:

- The SSL cert signature is `c59132567a7940bc9b83394d0f36fe4ffc0f8be85bab9ef260a4ffd890432ba7`
- The backend web server is `Microsoft-IIS/10.0` (which means Windows Server)
- The API code sends the header `x-powered-by: ASP.NET` .
- The user agent is `Dalvik/2.1.0 (Linux; U; Android 10; CP10 Build/QP1A.190711.020) Upward/2.6.0b977`

Upward claim to be based at *8750 N. Central Expressway, Suite 1400, Dallas, TX 75205*.

But who are Affinity Apps we keep seeing in the network requests? They are a subsidiary of Serif (Europe) Ltd --> https://affinity.serif.com/en-us/ , a British software outfit based in West Bridgeford, Nottinghamshire: https://en.wikipedia.org/wiki/Serif_Europe .

At this point, we can deduce the tech stack:

- AWS (Route 53, S3, Cloudfront)
- SQL Server (or DynamoDB, Aurora)
- ASP.Net (API)
- Kotlin (Android)
- Swift (iOS)
- Facebook Analytics etc

Step one, you are asked for your phone number.

```
POST https://www.upward-app.com/api/verify/sms
authorization: PM204.O2r1HFiGJ3 2vFKy6dgx8GqHKr4
{
    "countryCode": 1,
    "deviceId": "d31a4c00-8ef0-44e5-XXXX-6865803e83d2",
    "phoneNumber": "5550001234"
}
```
Once you enter the SMS, it requests a temporary token:

```
POST https://www.upward-app.com/api/verify/sms
authorization: PM204.O2r1HFiGJ3 2vFKy6dgx8GqHKr4
{
    "countryCode": 1,
    "deviceId": "d31a4c00-8ef0-44e5-XXXX-6865803e83d2",
    "phoneNumber": "5550001234",
    "verificationCode": "374117"
}
```
Which results in a token:

```
{
    "accessToken": "QzRjdmZFcUd4NnYvdkhwQ2R1....",
    "expires": "2022-12-30T05:52:02.24Z",
    "status": 0
}
```
Next step is authentication:

```
POST https://www.upward-app.com/api/authenticate
authorization: PM204.O2r1HFiGJ3 2vFKy6dgx8GqHKr4
{
    "accessToken": "QzRjdmZFcUd4NnYvdkhwQ2R....",
    "deviceId": "d31a4c00-8ef0-44e5-XXXX-6865803e83d2",
    "platform": "Android",
    "tokenType": "SMS"
}
```
Which provides a long-term token:

```

{
    "expires": "2023-03-30T05:42:02.90Z",
    "token": "7twvRLvcnsDYYCft6cNcZ...."
}
```
Everything you do is being logged:

```
POST https://www.upward-app.com/api/analytics
authorization: PM204.O2r1HFiGJ3 2vFKy6dgx8GqHKr4
{
    "additionalInfo": {
        "PublicUserId": "",
        "screenId": "SmsPhoneFragment"
    },
    "deviceId": "d31a4c00-8ef0-44e5-88d4-6865803e83d2",
    "eventAction": "ScreenViewed",
    "eventCategory": "ApplicationEvents"
}
```
After that it's pretty simple sailing with your token, and we can rebuild and map the API:

- `GET https://www.upward-app.com/api/user/me`
- `GET https://www.upward-app.com/api/features/transient`
- `GET https://www.upward-app.com/api/features/configurable`
- `GET https://www.upward-app.com/api/activity/new`
- `GET https://www.upward-app.com/api/user/preferences`
- `GET https://www.upward-app.com/api/features/status`
- `GET https://www.upward-app.com/api/application/notifications`
- `PUT https://www.upward-app.com/api/pushnotificationconfig`
- `GET https://www.upward-app.com/api/community`
- `GET https://www.upward-app.com/api/application/config/datacollection`
- `GET https://www.upward-app.com/api/search?latitude=37.0633203&longitude=-112.375209&numberOfResults=40`
- `GET https://www.upward-app.com/api/notification/rtc/channels`
- `GET https://www.upward-app.com/api/connections/list?maxMessages=1`
- `GET https://www.upward-app.com/api/user/preferences`
- `GET https://www.upward-app.com/api/user/likes/pending?numberOfResults=1&refresh=true&imageWidth=200`
- `GET https://www.upward-app.com/api/messages/6d805-9eba-4cf-8e25-18f6/list?max=40`
- `GET https://www.upward-app.com/api/user/6d39e805-9eba-4cfa-8e25-18e6d80G22f6`

There's a lot of chaos available here. As long as we can get a legit token, we can start sending "likes", messages, and other obnoxious spam items.

We can see it does a regular "ping" or "keep alive" to a backend endpoint:

```
POST https://rtn.services.peoplemedia.com/websync.ashx?token=19748544&src=java&AspxAutoDetectCookieSupport=1
[
    {
        "channel": "/meta/handshake",
        "id": "1",
        "minimumVersion": "1.0",
        "supportedConnectionTypes": [
            "long-polling"
        ],
        "version": "1.0"
    }
]
```
Who are PeopleMedia? According to https://peoplemedia.com/About

*Operated by IAC, People Media is the sister company to Match.com and OkCupid.*

Also, endless requests to Facebook with detailed device fingerprinting:

```
POST https://www.facebook.com/adnw_sync2
"payload":{
   "request":{
      "bidder_token_info":"fill",
      "prefetch_urls":"fill"
   },
   "bundles":{

   },
   "context":{
      "COPPA":"false",
      "APPBUILD":"977",
      "ID_CACHE_TS_MS":"1672378960932",
      "KG_RESTRICTED":"false",
      "CAPPED_IDS":"[]",
      "VALPARAMS":"{\"is_emu\":\"false\",\"apk_size\":\"54024183\",\"timezone_offset\":\"-28800000\",\"app_started_reason\":\"LAUNCHER_FOUND_API21\",\"is_debuggable\":\"false\",\"debug_value\":\"N\\\/A\",\"build_type\":\"N\\\/A\"}",
      "UNITY":"false",
      "ACCESSIBILITY_ENABLED":"false",
      "APPNAME":"Upward",
      "HAS_EXOPLAYER":"true",
      "AFP":"52c5f03f8b384b039c535f4c302f8b5f",
      "SESSION_TIME":"1672378960.965",
      "PLACEMENT_ID":"",
      "MAKE":"Shenzhen E-dong Technology Co.,Ltd",
      "REQUEST_TIME":"1672379865.597",
      "CARRIER":"",
      "SDK_CAPABILITY":"[3,4,5,7,11,16,17,18]",
      "TEMPLATE_ID":"0",
      "CLIENT_REQUEST_ID":"11ba3c22-b2a6-48d4-bfd5-0b99cdda5ed8",
      "DENSITY":"1.3312501",
      "AD_REPORTING_CONFIG_LAST_UPDATE_TIME":"0",
      "SCREEN_HEIGHT":"913",
      "SDK_VERSION":"5.11.0",
      "SCREEN_WIDTH":"600",
      "ID_SOURCE":"DIRECT",
      "SDK":"android",
      "OSVERS":"10",
      "APP_MIN_SDK_VERSION":"21",
      "OS":"Android",
      "ANALOG":"{\"total_memory\":\"1491820544\",\"accelerometer_y\":\"0.7278373\",\"accelerometer_x\":\"-0.89064306\",\"accelerometer_z\":\"9.643845\",\"charging\":\"0\",\"available_memory\":\"589492224\",\"battery\":\"88.0\",\"free_space\":\"20714143744\"}",
      "DATA_PROCESSING_OPTIONS":"null",
      "ROOTED":"1",
      "MODEL":"CP10",
      "BUNDLE":"com.affinityapps.twozerofour",
      "ASHAS":"67c2a2aece338209c9ee20735fff4252d2c9489b;",
      "LOCALE":"en_US",
      "NETWORK_TYPE":"1",
      "IDFA":"d31a4c00-8ef0-44e5-88d4-6865803e83d2",
      "ATTRIBUTION_ID":"",
      "APPVERS":"2.6.0",
      "DATA_PROCESSING_OPTIONS_COUNTRY":"null",
      "INSTALLER":"com.google.android.apps.nbu.files",
      "DATA_PROCESSING_OPTIONS_STATE":"null",
      "IDFA_FLAG":"1",
      "SESSION_ID":"7085af68-9372-4e45-b95f-dcf29d6e0cbb"
   }
}
```
But what about those photos we wanted to look at, to see if we want to subscribe?

Well, we can see a peculiar type of request being made repetitively:

`GET https://photos.affinity-apps.com/eyJrZXkiOiJjZDI0NTIyNDQwNjA0NzIzOGZiMDY4MjZkNWYzMGFjNiIsImVkaXRzIjp7ImNyb3AiOnsibGVmdCI6MCwidG9wIjowLCJ3aWR0aCI6ODk4LCJoZWlnaHQiOjEzNDh9LCJyZXNpemUiOnsid2lkdGgiOjg5OCwiaGVpZ2h0IjoxMzQ4LCJmaXQiOiJpbnNpZGUifX19`
The response is interesting:

```
HTTP/2.0 200
content-type: text/plain
date: Sat, 03 Dec 2022 22:00:29 GMT
x-amzn-requestid: 7359ddf5-6d16-4011-9d91-34e83d28
last-modified: Thu, 13 Oct 2022 21:47:11 GMT
access-control-allow-headers: Content-Type, Authorization
x-amz-apigw-id: clwHnHL3IAMF3Mw=
cache-control: max-age=31536000,public
access-control-allow-methods: GET
x-amzn-trace-id: Root=1-638bc6fd-5df8ad705926a93
access-control-allow-credentials: true
content-encoding: gzip
vary: Accept-Encoding
x-cache: Hit from cloudfront
via: 1.1 1b0ec06e2dc8a07d495632f96e0234b4.cloudfront.net (CloudFront)
x-amz-cf-pop: LAX53-P3
x-amz-cf-id: 21P-ZcAhhLFHeO_iFr0izgcaijFmW7axhyFGDH-fouMWPeRStw==
age: 2274989
```
OK, `photos.affinity-apps.com` is a CNAME for an AWS Cloudfront bucket.

What about that Base64 string in the URL? It's an AWS formatting config.

```
{
   "key":"cd245224406047238fb06826d5f30ac6",
   "edits":{
      "crop":{
         "left":0,
         "top":0,
         "width":898,
         "height":1348
      },
      "resize":{
         "width":898,
         "height":1348,
         "fit":"inside"
      }
   }
}
```
Oh dear, oh dear. All we have to do is visit the URL in a browser. Zero protection, and the blurring is done with CSS. No signatures. no expiry, no thought to discovery escalation.

We can now visit that screen in the app, see the list of images it downloads, and view them separately to see if we want to upgrade. Done.

Then, we can ban these two URLs at router level to stop data being leaked:

- `https://rtn.services.peoplemedia.com/websync.ashx`
- `https://www.upward-app.com/api/analytics`

Time: roughly forty-five minutes or so. Not bad.
