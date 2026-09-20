---
title: Reverse Engineering and Instrumenting React Native Apps
source_url: https://pilfer.github.io/mobile-reverse-engineering/react-native/reverse-engineering-and-instrumenting-react-native-apps/
fetched_at: 2026-09-20T02:00:05Z
license: unspecified
category: mobile/react-native
---

# Update: Use Bytecode Studio

I’ve launched Bytecode Studio - a comprehensive tool built for reverse engineering, analyzing, disassembling, and decompiling React Native applications and Hermes binaries.

**Table of Contents**

## What is React Native?

React Native is a cross-platform mobile application framework that was created by Facebook/Meta. It has a bespoke JavaScript runtime embedded within it called “Hermes”, which also has the ability to compile JavaScript to a bespoke bytecode. Said bytecode is loaded up into the VM and executed at runtime.

The usage of Hermes’ binary format is now default for all new React Native apps. Gone are the days of simply formatting and deobfuscating JavaScript in the shipped bundle.

Practical Example:

```
eval(`console.log(1+1)`);
```
Compiles to:

```
Function<global>(1 params, 11 registers, 0 symbols):
  GetGlobalObject  r0
  TryGetById  r2,  r0,  1,  "eval"
  LoadConstUndefined  r1
  LoadConstString  r0,  "console.log(1+1)"
  Call2  r0,  r2,  r1,  r0
  Ret  r0
```
*Note*: The strings above are typically used by reference to their index - I populated them with `hermes_rs`.

Obviously this has thrown a wrench into the gears of many reverse engineers and researchers out there. So, how do we hack on React Native apps now? Let’s take a look at the current tooling that we have available to us.

## Tooling Landscape

At the time of me writing this post, the landscape for RE/DI tooling for React Native is lacking - especially when compared to what is available for other frameworks.

### Bytecode Studio - Hermes disassembler, decompiler, and all-in-one Reverse Engineering tool

**Link**: Bytecode Studio - React Native Reverse Engineering

Bytecode Studio is hands down the most comprehensive, user-friendly too for reverse engineering React Native applications and Hermes binaries.

- Find cross-references
- Visually stunning hex and bytecode views
- IR output
- Decompiler
- Visualized data structures such as objects and arrays
- Metro module visualization
- …and way more features.

Seriously, we’re seeing anywhere from 1-10x productivity in the folks who are using it now.

### Mine: hermes_rs - Hermes disassembler and assembler

**Link & Source**: https://github.com/Pilfer/hermes_rs**Crate**: https://crates.io/crates/hermes_rs

`hermes_rs` is my (nearly) dependency-free Hermes disassembler and assembler. This is the tool I use most frequently for my hermes/RN-related shenanigans, which has helped immensely with the development.

As of right now it supports HBC versions 89, 90, 93, 94, 95, and 96. Like `hasmer` and others, updating it to support newer HBC versions is trivial - just drop a .def file into the `def_versions` directory and execute the generator script.

### Mine: heresy - Hermes Engine instrumentation utility

`heresy` is a simple utility that allows you to inject JavaScript into the hermes engine to inspect data and hook functions at runtime. It’s essentially the same thing as evaluating JavaScript in your devtools console.

You can inspect HTTP traffic and even hook React component composition with it. It was built based on the research I covered in this blog post.

**Link & Source**: https://github.com/Pilfer/heresy**Blog Post + Tutorial**: https://pilfer.github.io/mobile-reverse-engineering/react-native/heresy-inspect-and-instrument-react-native-apps/

### Official Hermes Resources

**Docs**: https://hermesengine.dev/**Source**: https://github.com/facebook/hermes

The official Hermes source code repository contains a ton of very useful content. The hermes binary itself has a method to dump the bytecode of a pure .hbc file. It unfortunately rarely (if ever) works with Android/iOS bundles.

If you’re dealing with binary compiled with hermes directly, you could simply do `hermes ./some_file.hbc -dump-bytecode` and view the instructions, strings, etc.

The `hermes` binary is also quite useful for compiling your own kitchen sink JavaScript functions and using the generated instructions as a template to patch into existing binaries, assuming the HBC version is the same (currently at v96).

### Third Party: hermes-dec

**Link & Source**: https://github.com/P1sec/hermes-dec

`hermes-dec` describes itself as “A reverse engineering tool for decompiling and disassembling the React Native Hermes bytecode”, and the disassembler is quite good. The project structure is such that updating it to support newer versions of the bytecode is trivial.

The decompiler isn’t really fleshed out at this time (Oct 4, 2024), and the last commit was 6 months ago.

### Third Party: hbctool

**Link & Source**: https://github.com/bongtrop/hbctool

`hbctool` is a Hermes disassembler and assembler. You can decompile the binary, modify it in its textual format, reassemble it, and execute. The more recent supported HBC version is v85, so it’s woefully out of date with the current HBC version of 96.

I’ve personally used it a couple of times on older applications and it met the need quite well, but felt like it wasn’t a “complete” tool.

### Third Party: hasmer

**Docs**: https://lucasbaizer2.github.io/hasmer/**Link & Source**: https://github.com/lucasbaizer2/hasmer

`hasmer` is still a WIP, but I’m very hopeful for this project. It has a suite of tooling built around it, and the approach the author has taken for the decompiler seems solid.

I haven’t used it personally, but it:

- Has a VSCode extension
- Has an autogenerator for updating Hermes versions (by reading the Bytecode macro definition “def” file)
- Supports disassembling and assembling

# Fun Instrumentation Methods

## Injecting JavaScript into the React Native Global Context

In an Android React Native application, you can inject JS into the global context of the engine by using frida targeting the `CatalystInstanceImpl` class.

The `loadScriptFromAssets` method is what loads the compiled hermes bundle into the runtime within `libhermes.so`.
Hooking this function and calling `loadScriptFromFile` with a valid script that exists in a directory the app has access to will immediately evaluate it.

Alternatively, you could simply patch the `index.android.bundle` file to do this same eval with better success - but that requires repackaging of the app and all that jazz. I’ll probably make a helper tool for this in `hermes_rs` eventually.

Source code of: `example.js`

```
// This is the app identifier you're trying to hook
const package_name = 'com.foo.bar';
// Write the hermes-hook.js payload to file
const f = new File(`/data/data/${package_name}/files/hermes-hook.js`, 'w');
f.write(`console.log(Object.keys(this)); console.log('hello from React Native!');`);
f.close();
Java.perform(function () {
  // Lazily wait for the class to be available to us
  var looper = setInterval(function () {
    try {
      const CatalystInstanceImpl = Java.use("com.facebook.react.bridge.CatalystInstanceImpl");
      CatalystInstanceImpl.loadScriptFromAssets.implementation = function (assetManager, assetURL, z) {
        // Load the original index.android.bundle
        this.loadScriptFromAssets(assetManager, assetURL, z);
        // Load custom JS into the global hermes context
        this.loadScriptFromFile(`/data/data/${package_name}/files/hermes-hook.js`, `/data/data/${package_name}/files/hermes-hook.js`, z);
      };
      clearInterval(looper);
    } catch (error) {
      console.log('failed');
    }
  }, 10);
});
```
Then you’d simply run: `frida -U -f com.foo.bar -l example.js`.

Output should be something like:

```
[12:51:42] I | ReactNativeJS ▶︎ [ 'Promise',
                             │ '__jsiExecutorDescription',
                             │ 'nativePerformanceNow',
                             │ 'nativeModuleProxy',
                             │ 'nativeFlushQueueImmediate',
                             │ 'nativeCallSyncHook',
                             │ 'globalEvalWithSourceUrl',
                             │ 'nativeLoggingHook',
                             │ 'nativeRuntimeScheduler',
                             │ '__BUNDLE_START_TIME__',
                             │ '__DEV__',
                             │ 'process',
                             │ '__METRO_GLOBAL_PREFIX__',
                             │ '__r',
                             │ '__d',
                             │ '__c',
                             │ '__registerSegment',
                             │ 'console',
                             │ 'ErrorUtils',
                             │ 'window',
                             │ 'self',
                             │ 'DOMRect',
                             │ 'DOMRectReadOnly',
                             │ '__fbGenNativeModule',
                             │ 'performance',
                             │ 'setTimeout',
                             │ 'clearTimeout',
                             │ 'setInterval',
                             │ 'clearInterval',
                             │ 'requestAnimationFrame',
                             │ 'cancelAnimationFrame',
                             │ 'requestIdleCallback',
                             │ 'cancelIdleCallback',
                             │ 'queueMicrotask',
                             │ 'setImmediate',
                             │ 'clearImmediate',
                             │ 'XMLHttpRequest',
                             │ 'FormData',
                             │ 'fetch',
                             │ 'Headers',
                             │ 'Request',
                             │ 'Response',
                             │ 'WebSocket',
                             │ 'Blob',
                             │ 'File',
                             │ 'FileReader',
                             │ 'URL',
                             │ 'URLSearchParams',
                             │ 'AbortController',
                             │ 'AbortSignal',
                             │ 'alert',
                             │ 'navigator',
                             │ '__fetchSegment',
                             │ 'RN$AppRegistry',
                             │ 'RN$SurfaceRegistry' ]
                             │ hello from React Native!
```
As you can see, there are a variety of globals available to us. From what I can tell, `this`, `self`, and `window` all reference the same object.

I believe most of these are defined here: https://github.com/facebook/react-native/blob/main/packages/react-native/types/modules/globals.d.ts

If we look around a bit, we can find some potentially interesting things:

```
// Dump environment variables?
console.log(JSON.stringify(this.process)); // {"env":{"NODE_ENV":"production"}}
```
### Intercepting React Native HTTP Traffic

In the section above, the output of `Object.keys(this)` showed `XMLHTTPRequest`. I’ve had some success hooking this in the past on frontend apps I’ve worked on - maybe this will work for React Native, too?

In my test React Native app, I have a button that fetches a remote API using `axios` when pressed.

```
import axios from 'axios';
// ....
const makeRequest = () => {
  axios.get('https://jsonplaceholder.typicode.com/todos/1').then((response) => {
    console.log(response.data);
  }).catch((error) => {
    console.error(error);
  });
};
// ....
<Button title="Make A Request" onPress={makeRequest} />
```
So let’s try hooking XMLHTTPRequest…

```
(function() {
  var origOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function() {
    let output = {};
    console.log('[*] Hooked XMLHttpRequest.prototype.open');
    output.method = arguments[0];
    output.url = arguments[1];
    console.log(Object.keys(this));
    console.log(JSON.stringify(arguments));
    this.addEventListener('load', function() {
      output.response = {
        status: this.status,
        statusText: this.statusText,
        responseText: this.responseText,
      };
      console.log(JSON.stringify(output));
    });
    origOpen.apply(this, arguments);
  };
})();
```
Aaaaand we get:

```
[13:07:23] I | ReactNativeJS ▶︎ {
  "method": "GET",
  "url": "https://jsonplaceholder.typicode.com/todos/1",
  "response": {
    "status": 200,
    "responseText": "{\n  \"userId\": 1,\n  \"id\": 1,\n  \"title\": \"delectus aut autem\",\n  \"completed\": false\n}"
  }
}
```
With just a little bit of extra code, one could get the full request and response - with headers included. Since `WebSocket` also exists in the global context, you can quite easily pipe all of those requests from your lab device or emulator and ingest it in whatever tooling you choose (ex: forward it to burp).

**Edit**: It looks like the React Native folks left interceptor function in the codebase. You can get the full request and response with:

```
const XHRInterceptor = {
  requestSent: (id, url, method, headers) => {
    console.log(`Request Sent: ID=${id}, URL=${url}, Method=${method}, Headers=${JSON.stringify(headers)}`);
  },
  responseReceived: (id, url, status, headers) => {
    console.log(`Response Received: ID=${id}, URL=${url}, Status=${status}, Headers=${JSON.stringify(headers)}`);
  },
  dataReceived: (id, data) => {
    console.log(`Data Received: ID=${id}, Data=${data}`);
  },
  loadingFinished: (id, encodedDataLength) => {
    console.log(`Loading Finished: ID=${id}, Encoded Data Length=${encodedDataLength}`);
  },
  loadingFailed: (id, error) => {
    console.log(`Loading Failed: ID=${id}, Error=${error}`);
  },
};
this.XMLHttpRequest._interceptor = XHRInterceptor;
```
Which produces:

```
▶︎ Request Sent: ID=1, URL=https://jsonplaceholder.typicode.com/todos/1,
  Method=GET,
  Headers={"accept":"application/json, text/plain, */*"}
▶︎ Response Received: ID=1,
  URL=https://jsonplaceholder.typicode.com/todos/1, Status=200,
  Headers={"x-ratelimit-limit":"1000","x-content-type-options":"nosniff","x-ratelimit-remaining":"999","vary":"Origin, Accept-Encoding","x-ratelimit-reset":"1726774762","etag":"W/\"53-foobar+s\"","date":"Mon, 07 Oct 2024 19:35:13 GMT","via":"1.1 vegur","nel":"{\"report_to\":\"heroku-nel\",\"max_age\":3600,\"success_fraction\":0.005,\"failure_fraction\":0.05,\"response_headers\":[\"Via\"]}","age":"28539","cf-ray":"8cf05544aed66763-ATL","x-powered-by":"Express","server":"cloudflare","access-control-allow-credentials":"true","report-to":"{\"group\":\"heroku-nel\",\"max_age\":3600,\"endpoints\":[{\"url\":\"https://nel.heroku.com/reports?ts=<foo>\"}]}","pragma":"no-cache","cache-control":"max-age=43200","content-type":"application/json; charset=utf-8","reporting-endpoints":"heroku-nel=https://nel.heroku.com/reports?ts=<foo>","expires":"-1","cf-cache-status":"HIT","alt-svc":"h3=\":443\"; ma=86400"}
▶︎ Data Received: ID=1, Data={
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
  Loading Finished: ID=1, Encoded Data Length=83
```
### What about `JSON.parse` and `JSON.stringify`?

```
var originalJSONStringify = JSON.stringify;
var originalJSONParse = JSON.parse;
JSON.stringify = function() {
  console.log('[*] Hooked JSON.stringify');
  let result = originalJSONStringify.apply(this, arguments);
  console.log(result);
  return result;
};
JSON.parse = function() {
  console.log('[*] Hooked JSON.parse');
  console.log(arguments[0]);
  return originalJSONParse.apply(this, arguments);
};
```
Returns:

```
[13:24:52] I | ReactNativeJS ▶︎ [*] Hooked JSON.stringify
[13:24:52] I | ReactNativeJS ▶︎ {
  "NativeModules": ["HeadlessJsTaskSupport", "UIManager", "PlatformConstants", "DeviceInfo", "DeviceEventManager", "Timing", "BlobModule", "Appearance", "SoundManager", "ImageLoader"],
  "TurboModules": [],
  "NotFound": ["NativePerformanceObserverCxx", "NativePerformanceCxx", "NativeReactNativeFeatureFlagsCxx", "RedBox", "BugReporting"]
}
# It looks like we captured the HTTP response body, too!
[13:27:41] I | ReactNativeJS ▶︎ [*] Hooked JSON.parse
                             │ {
                             │ "userId": 1,
                             │ "id": 1,
                             │ "title": "delectus aut autem",
                             │ "completed": false
                             └ }
[13:27:41] I | ReactNativeJS ▶︎ [*] Hooked JSON.stringify
                             │ "userId"
                             │ [*] Hooked JSON.stringify
                             │ "id"
                             │ [*] Hooked JSON.stringify
                             │ "delectus aut autem"
                             │ [*] Hooked JSON.stringify
                             │ "title"
                             │ [*] Hooked JSON.stringify
                             │ "completed"
                             │ { userId: 1,
                             │ id: 1,
                             │ title: 'delectus aut autem',
                             └ completed: false }
```
### Built-ins? Yes, please!

```
// Array.push - you can get clever with typeof and toString() here
const originalPush = Array.prototype.push;
Array.prototype.push = function(item) {
  console.log(item);
  originalPush.call(this, item);
};
```
### Hooking `onPress` Events, and potential partial reclaimation of JSX?

So this one is pretty cool. `Map.set` is being used for what I assume is some kind of UI state functionality. While logging data and poking around, I started seeing some strings that were unique to my UI.

```
{
  style: {
    backgroundColor: "#F3F3F3"
  },
  children: [
    {
        "$$typeof": {},
        type: {
          [Function: StatusBar]
          _propsStack: [],
          _updateImmediate: null,
          _currentValues: null,
          currentHeight: 0,
          _updatePropsStack: [Function]
        },
        key: null,
        ref: null,
        props: {
          barStyle: "dark-content",
          backgroundColor: "#F3F3F3"
        },
        _owner: null
      },
      // .... more junk
            {
              "$$typeof": {},
              type: {
                "$$typeof": {},
                render: [Function],
                displayName: "View"
              },
              key: null,
              ref: null,
              props: {
                style: {
                  backgroundColor: "#FFF"
                },
                children: [{
                    "$$typeof": {},
                    type: {
                      "$$typeof": {},
                      render: [Function],
                      displayName: "Button"
                    },
                    key: null,
                    ref: null,
                    props: {
                      title: "Do Thing",
                      onPress: [Function: doThing]
                    },
                    _owner: null
                  },
// .... more stuff
```
The key for that datastructure being used was `275` for me, so I hardcoded it and started writing conditionals down the datastructure until I found my `Button`, which exists in `App.tsx` as:

```
<Button title="Do Thing" onPress={doThing} />
```
Once I had the button, I was able to actually call `doThing()` *from my global context code that I loaded from the filesystem*!

I won’t even try to lie to you, I was absolutely pumped that this worked.

```
// Sorry for the spaghetti - nullish coalescing was being a pain in the runtime, so I went old school
const originalMapSet = Map.prototype.set;
Map.prototype.set = function(key, value) {
  if (key == 275) {
    try {
      let child = value.children[1];
      if (child && child.props) {
        if (child.props.children) {
          child.props.children.map(c => {
            if (c.type.displayName === 'View') {
              console.log('Found a view!')
              if (c.props && c.props.children) {
                let first = c.props.children[0];
                if (first.type.displayName === 'Button') {
                  console.log('[*] Found button', first)
                  console.log('[*] onPress handler:', first.props.onPress);
                  let originalOP = first.props.onPress;

                  first.props.onPress = function() {
                    console.log('[*] We hooked onPress! Woohoo!');
                    originalOP.call(this, arguments)
                  };
                  console.log('[*] onPress handler called!', first.props.onPress());
                }
              }
            }
          })
        }
      }
    } catch (error) {
      console.error(error);
    }
  }
  originalMapSet.call(this, key, value);
};
```
I was unable to override the `onPress` function to hook it, nor was I able to modify any of the other props on the element to the point where they changed visually (I tried the button title). This could be due to the fact that a re-render needs to take place, or that this datastructure is merely a copy of the original that stores some function references.

There are *so many* cool objects to play with in this data structure. One could theoretically take it, parse it recursively, and “decompile” the frontend of a React Native app as it exists within the Hermes engine.

That may be a different task for a different day.
