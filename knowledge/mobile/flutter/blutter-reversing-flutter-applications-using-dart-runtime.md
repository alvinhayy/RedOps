---
title: "B(l)utter: Reversing Flutter Applications by using Dart Runtime (HITB SecConf 2023 HKT - Worawit Wangwarunyoo)"
source_url: https://conference.hitb.org/hitbsecconf2023hkt/materials/D2%20COMMSEC%20-%20B(l)utter%20%e2%80%93%20Reversing%20Flutter%20Applications%20by%20using%20Dart%20Runtime%20-%20Worawit%20Wangwarunyoo.pdf
fetched_at: 2026-09-20T02:06:51Z
license: unspecified
category: mobile/flutter
---

# B(l)utter - Reversing Flutter Applications by using Dart Runtime

> Slide deck text extraction (48 pages) from the HITB conference materials PDF. Slide layout is not preserved.

## Slide page 1

B(l)utter
Reversing Flutter Application
by using Dart Runtime
Worawit Wangwarunyoo
Security Researcher, Datafarm
1

## Slide page 2

Agenda
● What is Flutter Application?
● Reverse Engineering Challenges
● Building Dart (AOT) Runtime for Reversing
● Getting Information from Dart Snapshot
● Intro to Dart Internal (ARM64)
● Dumping Objects at Runtime with Frida
2

## Slide page 3

whoami
● Worawit Wangwarunyoo (@sleepya_)
● Security Researcher
● Working for Datafarm Co., Ltd.
● Public exploits and tools on
○ https://github.com/worawit
3

## Slide page 4

What is Flutter Application?
4

## Slide page 5

What is Flutter?
● Flutter is an open source framework by Google
○ For building beautiful, natively compiled, multi-platform
applications from a single codebase
● Flutter code is powered by Dart platform
● Flutter app developers write code in Dart Language
5

## Slide page 6

Flutter Architectural Overview
6
Ref: https://raw.githubusercontent.com/flutter/engine/main/docs/flutter_overview.svg

## Slide page 7

Scope of This Talk
● Target only Mobile Application (Android, iOS)
● ARM64 architecture only
● Release build only
○ Symbols are stripped
○ Full optimization
7

## Slide page 8

Flutter Mobile App in Installer Package
8
Embedder
Engine
Framework
App
Dart
C/C++
Android: libapp.so
IOS: App.Framework
Android: libflutter.so
IOS: Flutter.Framework

## Slide page 9

Flutter Mobile Application
● Use Dart Ahead-Of-Time (AOT) compiler
○ for producing machine code (in release build)
● The AOT-compiled code still runs inside a Dart VM
○ Precompiled runtime (a stripped version of Dart VM)
● The code and data are serialized into a binary snapshot
9

## Slide page 10

Dart Snapshot
● Serialized state of the Dart VM at a specific point in its
execution
● A Dart snapshot is taken just before calling main
10

## Slide page 11

Problems
11

## Slide page 12

Problem 1: Parsing Dart Snapshots
● Universal parser for Dart snapshots cannot be written
○ Dart is constantly evolving
○ The format of snapshots keeps changing
● The snapshot deserialization code is in Dart VM
○ Always included in an installer package
○ Check if the deserializing snapshot is a same version (from hash)
● Known public Dart snapshot parsers
○ Doldrums - https://github.com/rscloura/Doldrums
○ darter - https://github.com/mildsunrise/darter
● Both tools do not work with new Dart versions
○ Updating parser take times
12

## Slide page 13

Problem 2: Analyzing Dart (ABI) Code
● Use general purpose registers as special purpose
○ ARM64 R15 -> Dart VM stack pointer
○ ARM64 R27 -> Object pool pointer
○ …
● Use pool pointer to access object pool
○ No direct references to static data
● Custom calling convention
● Utilize Dart VM functions by calling Dart Stubs
○ Dart stubs are entry points for entering Dart VM from compiled code
● Inline Dart Stubs
13

## Slide page 14

// Register aliases.
const Register TMP = R16;  // Used as scratch register by assembler.
const Register TMP2 = R17;
const Register PP = R27;  // Caches object pool pointer in generated code.
const Register DISPATCH_TABLE_REG = R21;  // Dispatch table register.
const Register CODE_REG = R24;
// Set when calling Dart functions in JIT mode, used by LazyCompileStub.
const Register FUNCTION_REG = R0;
const Register FPREG = FP;          // Frame pointer register.
const Register SPREG = R15;         // Stack pointer register.
const Register IC_DATA_REG = R5;    // ICData/MegamorphicCache register.
const Register ARGS_DESC_REG = R4;  // Arguments descriptor register.
const Register THR = R26;           // Caches current thread in generated code.
const Register CALLEE_SAVED_TEMP = R19;
const Register CALLEE_SAVED_TEMP2 = R20;
const Register HEAP_BITS = R28;  // write_barrier_mask << 32 | heap_base >> 32
const Register NULL_REG = R22;   // Caches NullObject() value.
#define DART_ASSEMBLER_HAS_NULL_REG 1
// ABI for catch-clause entry point.
const Register kExceptionObjectReg = R0;
const Register kStackTraceObjectReg = R1;
Register Usages on ARM64
14From <dart_v3.0.3>/runtime/vm/constants_arm64.h

## Slide page 15

Previous Public Works
● reFlutter
○ https://github.com/Impact-I/reFlutter
○ https://swarm.ptsecurity.com/fork-bomb-for-flutter/
● flutter-re-demo
○ https://github.com/Guardsquare/flutter-re-demo
○ https://www.guardsquare.com/blog/current-state-and-future-of-
reversing-flutter-apps
● Andre Lipke’s Blog
○ https://blog.tst.sh/reverse-engineering-flutter-apps-part-1/
● Introduction to Dart VM
○ https://mrale.ph/dartvm/
15

## Slide page 16

reFlutter Approach
● Patch the Dart Runtime source code to dump a snapshot
information while launching an application
○ To avoid writing snapshots parser
● Recompile the flutter engine
16
Embedder
Engine
Framework
App
Dart
C/C++
Android: libapp.so
IOS: App.Framework
Android: libflutter.so
IOS: Flutter.Framework
Patched

## Slide page 17

reFlutter Limitation
● Very difficult to develop and debug patched code
○ Hinder the further code analysis development
● Recompiling consumes a lot of resources
○ Disk, CPU
○ Time
● An application must be repackaged and executed
17

## Slide page 18

The Idea
● We only want snapshot deserialization functions
● The functions are only in Dart Runtime
● Can we build Dart SDK as library?
18

## Slide page 19

Building Dart Runtime
19

## Slide page 20

First Attempt: Building Dart SDK (Failed)
● Following the steps in the Dart wiki page
● Building Dart SDK requires Google’s depot tools
● The tools will fetch all dependencies
○ fetch dart
● The final source code size is >10GB
○ Not good if we have to build multiple versions of Dart Runtime
● The built command builds too many binaries
○ Take times and disk space
20

## Slide page 21

Minimize Build to Dart Runtime Only
● Focus on files only in runtime/vm directory
21

## Slide page 22

Minimize Build to Dart Runtime Only
● Create our own CMakeLists.txt
● The defined macros from
○ Generated build files of previous failed attempt
● The source and header files from
○ Parsing the Google’s build script
○ Listing all source file in a subdirectory
○ Adding the missing source files manually (after compiling errors)
● The 3rd party library from
○ Linking error message (only ICU)
○ Use a precompiled one
22

## Slide page 23

The Build Result
● Dart SDK clone directory with git sparse checkout
○ Size <100MB
● Building time
○ Less than 5 minutes on my laptop
● Dart Runtime as static library on Windows
○ Size ~20MB
● The target OS and architecture can be selected from
○ DART_TARGET_OS_ANDROID, DART_TARGET_OS_MACOS_IOS
○ TARGET_ARCH_ARM64, TARGET_ARCH_X64
● No source code patching
23

## Slide page 24

24
Start fetching and compiling Dart Runtime
Finished compiling Dart Runtime
Dart Runtime Static Library

## Slide page 25

Getting Information from
Dart Snapshot
25

## Slide page 26

Using Dart Runtime Internal API
● To access all loaded information in detail
○ Then fill the information into machine code
● Read Dart SDK source code
○ To learn how to use Internal API
● Use only public class methods
○ Their interfaces should not be changed in a new Dart version
26

## Slide page 27

Loading Dart Snapshot
27
char* error = NULL;
Dart_InitializeParams init_params = { 0 };
init_params.version = DART_INITIALIZE_PARAMS_CURRENT_VERSION;
init_params.vm_snapshot_data = vm_snapshot_data;
init_params.vm_snapshot_instructions = vm_snapshot_instructions;
init_params.start_kernel_isolate = false;
// other params are no needed if snapshot is not run
error = Dart_Initialize(&init_params);
Dart_IsolateFlags flags;
Dart_IsolateFlagsInitialize(&flags);
flags.is_system_isolate = false;
flags.snapshot_is_dontneed_safe = true;
flags.null_safety = true;
auto isolate = Dart_CreateIsolateGroup(nullptr, nullptr,
  isolate_snapshot_data, isolate_snapshot_instructions,
  &flags, nullptr, nullptr, &error);

## Slide page 28

Getting Classes
28
auto table = dart::Isolate::Current()->group()->class_table();
auto& library = dart::Library::Handle();
auto& cls = dart::Class::Handle();
// load from class table
for (intptr_t i = 0; i < table->NumCids(); i++) {
    auto clsPtr = table->At(i);
    if (clsPtr == nullptr)
        continue;
    cls = clsPtr;
    library = cls.library();
    // ...
}

## Slide page 29

Getting Stubs
● Dart Runtime helper functions
● The symbol names are not in the Dart Snapshot
○ They are in Dart Runtime source code
29
#define DO(member, name) \
  ptr = store->member(); \
  code = ptr; \
  ep_addr = code.EntryPoint(); \
  stub = new DartStub(ptr, DartStub::name ## Stub, ep_addr, code.Size(), #name); \
  stubs[ep_addr] = stub;
  OBJECT_STORE_STUB_CODE_LIST(DO);
#define OBJECT_STORE_STUB_CODE_LIST(DO)                                        \
  DO(dispatch_table_null_error_stub, DispatchTableNullError)                   \
  DO(late_initialization_error_stub_with_fpu_regs_stub,                        \
     LateInitializationErrorSharedWithFPURegs)                                 \
  DO(late_initialization_error_stub_without_fpu_regs_stub,                     \
     LateInitializationErrorSharedWithoutFPURegs)                              \
  DO(null_error_stub_with_fpu_regs_stub, NullErrorSharedWithFPURegs)           \
From <dart_v3.0.3>/runtime/vm/object_store.h

## Slide page 30

30

## Slide page 31

Object Pool (PP)
● Global constant objects
○ Also includes immediates and addresses
● Strings are immutable (constants)
31

## Slide page 32

32

## Slide page 33

Dart Thread Offsets
● List of VM-global objects/addresses cached in each Dart
Thread object
● Many objects are accessed through Dart Thread object
● The names are not in the Dart Snapshot
33
#define DEFINE_OFFSET_INIT(type_name, member_name, expr, default_init_value) \
  threadOffsetNames[dart::Thread::member_name##offset()] = #member_name;
  CACHED_CONSTANTS_LIST(DEFINE_OFFSET_INIT);
#undef DEFINE_OFFSET_INIT
#define DEFINE_OFFSET_INIT(name) \
  threadOffsetNames[dart::Thread::name##_entry_point_offset()] = #name;
  RUNTIME_ENTRY_LIST(DEFINE_OFFSET_INIT);
#undef DEFINE_OFFSET_INIT

## Slide page 34

34

## Slide page 35

35
Before After

## Slide page 36

Intro to Dart Internal (ARM64)
36

## Slide page 37

Pointer Compression
● Allocate an aligned 4GB region of address space as heap
○ Only lower 32 bits of object pointer is stored in memory
○ Lower memory usage with smaller pointer
○ Not enabled on iOS because it requires an additional application
entitlement
● The decompress pointer instruction always be after the
loading object instruction
37

## Slide page 38

Dart Object Memory Layout (64 bit)
38
Object tags
Compressed Ptr
Compressed Ptr
0x00
0x08
0x0c
0x14
Native int
Object class: size, class id, hash
Instance variable (object)
Instance variable (object)
Instance variable (int)

## Slide page 39

Dart Calling Convention
● Use R15 register as Dart VM Stack Pointer
● All call arguments are stored in Stack
● Store arguments in reversed order from a typical one
39
arg 0
arg 1
arg 2
Top of stack
saved LR
saved FP
local var x
local var y
Example for stack frame of function with 3 arguments

## Slide page 40

Dart Calling with Named Parameters
● Use R4 register as Arguments Descriptor
40
arg 3
arg 4
arg 5
saved LR
saved FP
local var x
[0, 0x6, 0x6, 0x2,
"caseSensitive", 0x3,
"dotAll", 0x5,
"multiLine", 0x2,
"unicode", 0x4,
Null]
arg 0
arg 1
arg 2
Total arguments
Number of
positional argument

## Slide page 41

Calling Dart Stub
● Use selected registers as Stub arguments
● Most of them are defined in constants_<arch>.h
● Some of them is fixed in compiler
41
struct InitStaticFieldABI {
  static const Register kFieldReg = R2;
  static const Register kResultReg = R0;
};
struct AllocateObjectABI {
  static const Register kResultReg = R0;
  static const Register kTypeArgumentsReg = R1;
static const Register kTagsReg = R2;
};
struct AllocateClosureABI {
  static const Register kResultReg = AllocateObjectABI::kResultReg;
  static const Register kFunctionReg = R1;
static const Register kContextReg = R2;
  static const Register kScratchReg = R4;
};
From <dart_v3.0.3>/runtime/vm/constants_arm64.h

## Slide page 42

Dump Object with Frida
42

## Slide page 43

Frida Hooking
● Auto generating script for accessing Dart objects
○ Target application information such as classes
○ Functions for accessing Dart object in memory
● Current support only dumping an Dart object
43

## Slide page 44

44
Frida script for dumping
Client.post1 argument
Disassembled code from libapp.so

## Slide page 45

45

## Slide page 46

Conclusion
● Using Dart Runtime is allowed us to get a lot of
information from a Flutter application
○ All symbol names in a Dart Snapshot
○ Names of fixed value/constants that only used in Runtime code
■ Stub names
■ Thread offset names
● These information make further analysis easier
○ This part requires studying Dart internals
● The Blutter tool will be released at
○ https://github.com/worawit/Blutter
46

## Slide page 47

DEMO
47

## Slide page 48

THANK
YOU!
48
