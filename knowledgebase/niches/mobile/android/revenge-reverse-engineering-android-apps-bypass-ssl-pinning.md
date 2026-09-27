---
title: RevEnge! Reverse Engineering android apps to bypass SSL pinning for mobile app pen-testing
source_url: https://medium.com/@shaddy43/revenge-reverse-engineering-android-apps-to-bypass-ssl-pinning-for-mobile-app-pen-testing-eeef2ce22682
fetched_at: 2026-09-20T02:00:12Z
license: unspecified
category: mobile/android
---
This is the second part of my 2 part blog series on mobile app pen-testing and reverse engineering. In the first part, I have explained how to bypass and patch root detection code for running android apps in rooted emulator devices. In this second part, i will bypass **SSL pinning** manually by patching the APK file.

Before reading this blog, I recommend to check out my first blog post provided below:

There are two requirements for bypassing SSL pining in most of the android apps:

- Configure BURP CA as a system level trusted certificate
- Patch SSL pinning code to add the hash of your BURP certificate

## System Level Burp Certificate

Lets focus on the first part, which is to add Burp as a system level certificate on the rooted emulator device on which the application would be tested. To check the system level certificates, you can go to the settings, security, credentials and check if Port Swigger or BURP certificate is installed or not. By default, it is not installed therefore you can add it manually by the following method:

1. Go to the proxy tab in Burp Suite
2. Click on Import/Export CA Certificate
3. Export Certificate in DER format

1. Android wants the certificate to be in PEM format and the filename must also be equal to the subject_hash_old value appended with 0. So we need to convert the DER certificate to PEM certificate
2. For conversion, we can use openSSL
3. We must also find subject_old_hash of the converted certificate using openSSL
4. Finally rename the converted certificate to subject_old_hash appended with .0
5. In the screenshot, I have used these commands to convert DER to PEM, then using openSSL found the **subject_hash_old** and renamed the PEM file to that hash with .0 extension for the android to accept it as trusted CA

1. Copy the certificate to the android device. Since the certificate is to be copied in /system therefore we need root
2. Using adb we can copy the certificate over with the following commands:
3. ***adb root***
4. ***adb remount***
5. ***adb push <cert>.0 /sdcard/***
6. And then use adb shell to copy the certificate to desired path and change its permissions with the following commands:
7. ***mv /sdcard/<cert>.0 /system/etc/security/cacerts***
8. ***chmod 644 /system/etc/security/cacerts/<cert>.0***
9. Finally reboot the device

1. You can verify if the certificate has been successfully installed by going to the Trusted Credentials in settings of rooted device

## Patch SSL pinning code

We will first check if all the traffic from android emulator device is being redirected to the burp suite or not. I’ve set the emulator proxy to my local IP on specified port on which burpsuite is listening.

It looks like the traffic is being redirected to the burpsuite proxy. Now lets see if the android app’s traffic is being redirected to burpsuite or not.

As the error message says, there is an unexpected error that occurred and we can not see any traffic being redirected to bupsuite proxy as well. It means the SSL pinning is available in the application code.

We need to find the pinned certificate in APK file and change it to our burpsuite certificate. For that I used adb logcat to log all messages and errors that occurred while logging into the APK. It shows that the APIs that it is contacting has a different certificate and our Burpsuite has different. Like in the screenshot below:

The certificate of my BurpSuite PortSwigger starts with u8Q1BC….. And certificate pinned in app for the API is fkwx01…..

Along with hash, the URL is also listed which is blurred in the screenshot. I just need to locate and change this hash in the APK file. In order to locate the SSL pinning code. I searched the API that it is sending the requests to in JADX GUI. It showed me the API and a class of **WebServiceFactoryV2** where the SSL pinning code along with its hashes is available.

Now the only thing to do is to replace these hashes to my burpsuite certificate hash after decompiling the apk using apktool and patching in smali language.

In the screenshot below, the 2 hashes are available that are being checked before contacting to the API. I have located the same WebServiceFactoryV2 class in smali packages and found the hashes used for SSL pinning. I replaced those hashes with my burpsuit hash and repackaged and resigned the apk.

After repackaging the app, I’ve setup burp proxy and started intercepting traffic again. In the screenshot you can see all the traffic is being intercepted through my burpsuite proxy; The SSL pinning has been successfully bypassed.

The SSL pinning has been bypassed successfully, the app has been logged-in and traffic is being intercepted on my proxy.
