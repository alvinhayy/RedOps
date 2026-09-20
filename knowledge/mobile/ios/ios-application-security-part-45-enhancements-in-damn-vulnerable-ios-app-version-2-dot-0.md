---
title: "iOS Application Security Part 45 - Enhancements in Damn Vulnerable iOS app version 1.5"
source: highaltitudehacks.com
source_url: https://highaltitudehacks.com/2015/05/31/ios-application-security-part-45-enhancements-in-damn-vulnerable-ios-app-version-2-dot-0.html
fetched_at: 2026-09-20T08:36:31Z
license: unspecified
category: mobile/ios
---

In this article, i would like to give a quick walkthrough of the new vulnerabilities and challenges that we have added in version 1.5 of [Damn Vulnerable iOS app](http://damnvulnerableiosapp.com).

In the Insecure Data storage section, we have added challenges for the following databases.

- Realm Database
- Couchbase Lite
- YapDatabase

We have also added a new section on *Extension vulnerabilities*, which covers vulnerabilities in different application extensions, a feature that was introduced with iOS 8.

In the *Runtime Manipulation section*, we have added a challenge where you can write a cycript script to brute force a login screen.

Another new section is *Attacks on third party libraries*, which demonstrates the security gaps that can occur in your application when you use third party libraries in your project.

In the section on *Side Channel Data leakage*, we have added another vulnerability demonstrating insecure storage of cookies.

The current downloadable IPA file from the website is a fat binary that will work on both 32 bit and 64 bit devices. This app will work on all iOS versions starting from iOS 7.0.

Some important links

We are working on getting the new solutions out as soon as possible so please be patient. For previous vulnerabilities, you can download the solutions for free from [here](http://damnvulnerableiosapp.com#solutions).

For any bugs, suggestions etc, please don’t hesitate to contact me. Also, a very special thanks to [Egor](http://twitter.com/igrekde) for his contributions to the project.
