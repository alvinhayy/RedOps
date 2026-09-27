---
title: "Spoofing your location in Play Store"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/mobile-pentesting/android-app-pentesting/spoofing-your-location-in-play-store.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: mobile/android
---

# Spoofing Your Location in Google Play Store

## What Google Play Actually Checks

- **Current network location** (the country seen from the exit IP).
- The **Google Play country/profile** attached to the account and Google Payments profile.
- Cached state in **`com.android.vending`** ,**`com.google.android.gms`** , and**Download Manager** .
- Whether the package is **published in that country** by the developer.
- In some cases, **device certification / integrity** (this is a different problem from pure region spoofing).

If an app is hidden because the device is not **Play-certified** or fails attestation, check [Play Integrity attestation spoofing](play-integrity-attestation-bypass.html).

## Fast Path on a Non-Rooted Device

1. **Connect to a VPN** endpoint in the target country.
2. Prefer a **fresh test Google account** already configured for that country. Reusing an account from another country often triggers the*selected Play country matches your country of residence* error.
3. **Clear Play state** from the GUI or directly with`adb` :

```
adb shell am force-stop com.android.vending
adb shell pm clear com.android.vending
adb shell am force-stop com.google.android.gms
adb shell pm clear com.google.android.gms
adb shell am force-stop com.android.providers.downloads
adb shell pm clear com.android.providers.downloads
```
1. Re-open **Play Store** and inspect**Settings –> General –> Account and device preferences –> Country and profiles** .<sup>[\[1\]](#references)</sup>
2. If the target country/profile appears, switch to it and retry the install. Google Play profile changes can take **up to 48 hours** to fully update.
3. If the country/profile does not appear, remember that Google expects you to be **in the target country** and to have a**payment method from that country** when creating a new Play country/profile.

## Rooted / Emulator Workflow

When the target app checks GPS after installation, align the device geolocation with the storefront country:

- **Android Emulator** : send a GPS fix directly to the emulator:<sup>[\[3\]](#references)</sup>

```
adb -e emu geo fix -3.7038 40.4168   # longitude latitude (Madrid)
```
- **Physical device** : enable**Developer options –> Select mock location app** and set your GPS spoofer as the mock provider. If you need to do it from the shell:

```
adb shell appops set <MOCK_LOCATION_APP_PKG> android:mock_location allow
```
## Bypassing App-Side Mock-Location Checks

Modern Android apps can detect lab GPS spoofing by calling **`Location.isMock()`** (API 31+) or the legacy **`isFromMockProvider()`**. On an authorized rooted lab, LSPosed modules such as **HideMockLocation** or a Frida hook can neutralize these checks:[\[2\]](#references)[\[4\]](#references)

```
Java.perform(function () {
  const L = Java.use('android.location.Location');
  try { L.isMock.implementation = function () { return false; }; } catch (e) {}
  try { L.isFromMockProvider.implementation = function () { return false; }; } catch (e) {}
});
```
Keep the hook scoped to the **target app** when possible: the Play Store itself is mostly country/profile/IP driven, while the **installed app** is the component that commonly performs the GPS/mock-location check.

## Common Failure Modes

- A **VPN only changes the IP** ; it does not rewrite the Google Payments profile behind the account.
- Clearing only **Play Store** is frequently insufficient; also reset**Google Play services** and**Download Manager** .
- Google currently enforces a **cooldown between Play country changes** , and**Family group** membership can block switching countries.
- Even after installation, the app backend may still geofence you using **GPS, IP, SIM MCC/MNC, phone number, locale, or server-side KYC** .
- Some install failures are actually **Play Integrity / certification** failures rather than country failures.

## References

- [1] [Google Play Help: How to change your Google Play country](https://support.google.com/googleplay/answer/7431675?hl=en)
- [2] [HideMockLocation (LSPosed/Xposed)](https://modules.lsposed.org/module/io.github.auag0.hidemocklocation/)
- [3] [Android Emulator console - `geo fix`](https://developer.android.com/studio/run/emulator-console#geo)
- [4] [Android `Location.isMock()` API](<https://developer.android.com/reference/android/location/Location#isMock()>)
