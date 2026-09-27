---
title: "From zero to tfp0 - Part 1: Prologue"
source: highaltitudehacks.com
source_url: https://highaltitudehacks.com/2020/06/01/from-zero-to-tfp0-part-1-prologue.html
fetched_at: 2026-09-20T08:36:31Z
license: unspecified
category: mobile/ios
---

On Jan 22, 2019, Google Project Zero researcher @_bazad tweeted the following.

If you’re interested in bootstrapping iOS kernel security research (including the ability to forge PACs and call arbitrary kernel functions), keep an A12 research device on iOS 12.1.2.

It was a reference counting bug in MIG (Message Interface generator) generated code. The PoC included a code snippet that would trigger the bug and cause a kernel panic. This was followed later by a complete PoC that provided the Kernel task port (tfp0) to userland thereby enabling arbitrary kernel read and write.

The A12, now with more kernel code execution; introducing voucher_swap: https://t.co/rVkwo50fgd

The bug was then used to develop a complete jailbreak for iOS 12 using various contributions from the community. This blog series is divided into three parts.

Part 1 deals with iOS security basics, which are fundamental in understanding the next two parts. It discusses kernelcache analysis, Mach messaging, Mach Ports, MIG, Heap allocation basics, CoreTrust, PAC, etc and some popular exploitation techniques such as creating a fake kernel task port, task_for_pid() arbitrary kernel read, etc. If you are already aware of these techniques, you can skip to Part 2 directly. During Part 1, I will be giving references which will link to the other two parts which will further reiterate why these concepts are essential to understand.

Part 2 will discuss the actual vulnerability and the whole exploitation steps leading up to the Kernel task port (tfp0).

Part 3 will discuss the steps taken to achieve a jailbreak such as bypassing sandboxing, CoreTrust, enabling rootfs remount etc.

Downloadables

Before we get started, you will need the following files to follow along.

Hopper, IDA Pro, Or Binary-Ninja, whichever reversing tool you prefer.

jtool2

XNU Kernel

The iOS Kernelcache comprises of the core kernel and it’s kernel extensions. The kernel code in itself is closed source; however, it is based on a fork of the open source XNU Kernel which is also used on Mac OS. The XNU kernel can be downloaded from opensource.apple.com.

Since the last couple of years, Apple has been open sourcing the ARM specific code as well, that can be found under ifdef CONFIG_EMBEDDED statements. Apple however still decides to keep some implementations to itself.

It is possible to identify some vulnerabilities in the kernel by just auditing the source code. Some vulnerabilities can, however, be identified only by compiling the kernel (e.g., voucher_swap) and looking under the BUILD directory, which provides access to MIG generated code. Vulnerabilities that are present in kernel extensions are usually identified by reverse engineering since the Kexts code is not usually open source. Some vulnerabilities might be relevant only on Mac OS while some will be relevant only for iOS.

Kernelcache

The kernelcache is a single Mach-O binary which includes the core kernel along with its kernel extensions. It used to be encrypted until iOS 10, after which Apple surprisingly decided to release the kernelcache unencrypted, citing performance reasons as the primary factor. It can now be easily unpacked and extracted from the IPSW file. Before this, the kernelcache was usually dumped from the memory once a kernel vulnerability was identified, or by getting access to the encryption keys (from theiphonewiki or using a bootrom exploit).

To find the decompressed kernelcache, simple unzip the ipsw file and look for the kernelcache file.

To list all the kernel extensions and split them into corresponding kext files, you can use **jtool2**.

IDA detects a kernelcache by its magic value and gives you an option to split the kernelcache into its corresponding kext files as well. You can now reverse these kernel extensions separately in order to find vulnerabilities within them.

On a jailbroken iOS device, the decompressed kernelcache can be found under /System/Library/Caches/com.apple.kernelcaches/kernelcache. Some jailbreaks use this file in order to find the address of certain symbols and offsets dynamically rather than using hardcoded offsets. An excellent example of this is the Qilin toolkit created by @morpheus.

Symbolicating Kernelcache

Symbolicating a binary can involve a lot of manual effort. Until iOS 11, the kernelcache used to ship with certain symbols. Since iOS 12, Apple decided to strip the kernelcache of all symbols, but not before mistakingly releasing a beta version with all symbols intact. The IPSW was later removed from the downloads section. The following image shows the symbol count obtained by jtool2 on an iOS 12 kernelcache (stripped) and the iOS 12 beta kernelcache that was released with all symbols intact.

The one kernelcache that was released with symbols was then later used by jtool2 in creating symbols for the newer iOS kernelcaches. One of the most useful features of jtool2 is its analyze command where you can feed it an iOS 12 kernelcache, and it will spit out the symbols for it.

As we can see, the companion file generated has about 12000 symbols.

In case you have the $$$, one of the easiest ways is to use the Lumina feature introduced with IDA 7.2 to get the symbols.

Building the Kernel

Building the kernel is quite important in finding vulnerabilities. In fact, the bug that we are discussing here (voucher_swap) wouldn’t have been identified with just a source code review of the xnu kernel. It’s a little complicated to build the kernel because of the dependencies and the reliance on the built version to be the same version of the host machine, but a quick google search will land you on many articles with step by step instruction to compile the kernel including this automation script written by @_bazad for XNU version 4570.1.46 (MacOS High Sierra 10.13). We will look into the actual vulnerability in Part 2 where we will look into the vulnerable source code present in one of the MIG generated files.

Mach Messaging

One of the unique features of the XNU kernel is its extensive use of Mach IPC, which is derived from the Mach microkernel, and is easily one of the fastest IPC mechanisms developed till date. A lot of the frequently used IPC mechanisms on iOS such as XPC still use Mach messaging under the hood. Here are some essential points about Mach messaging.

Mach IPC is based on unidirectional communication

Communication in Mach IPC happens between Ports (endpoints) in the form of Mach messages. Mach messages can be simple or complex, depending on a certain bit set in the message header.

In order to send messages, you must have an associated port right to it. The same applies for receiving a message, in order to receive a message, you must have a receive right to the port. The different types of rights are

MACH_PORT_RIGHT_SEND - Send right to a port allowing unlimited messages

MACH_PORT_RIGHT_RECEIVE - Receive rights to a port

MACH_PORT_RIGHT_SEND_ONCE - Send right allowing only one message to a port

MACH_PORT_RIGHT_PORT_SET - A set of rights to a port

MACH_PORT_RIGHT_DEAD_NAME - If the receiver dies, then the SEND right to it becomes MACH_PORT_RIGHT_DEAD_NAME. The same applies when the sender has SEND_ONCE to the port and one message gets sent.

Mach Port rights can be embedded and sent over Mach messages.

There can be multiple SEND rights but only one RECEIVE right for a PORT. SEND rights can also be cloned whereas RECEIVE rights cannot.

When Mach messages are sent, they are held in a queue in the kernel unless received by the receiver. This technique has been used in the past for Heap-feng-shui.

One of the most important binaries in iOS is launchd, which acts as the bootstrap server and allows processes to communicate with each other. launchd can help one process look up another process since all the processes check in with launchd and register themselves once they boot up. Consequently, launchd can also implement throttling and allow or deny lookup in certain situations, thereby acting as a security control. The importance of launchd cannot be underestimated and hence it is the first daemon to be launched (PID 1) and any crash in launchd would immediately trigger a kernel panic.

Messages are sent and received by threads within a process, which acts as the execution unit within a process. However, the port right is held on a task level, and is mentioned in the task’s ipc_space (discussed later)

Let’s have a look at the kernel to find the Mach IPC related code. Navigate to xnu-4903.221.1/osfmk/mach/message.h. As discussed before, messages can be simple or complex in nature. In the image below, you can see the structure of a simple mach message (mach_msg_base_t), which includes a header(mach_msg_header_t) and a body(mach_msg_body_t). However, for a simple message, the body is ignored by the kernel.

The mach message header structure has the following attributes.

msgh_bits: It’s a bitmap containing various properties of the message, such as whether the message is simple or complex, the action to be performed (such as moving or copying port rights). The complete logic can be found in osfmk/mach/message.h

msgh_size: Size of (header + body)

msgh_remote_port: Send right to the destination port

msgh_local_port: Receive right to the port where message needs to be received

msgh_voucher_port: Vouchers are used to pass arbitrary data in messages over key-value pairs

msgh_id: An arbitrary 32-bit field

Complex messages are specified with the complex bit set to 1 in the msgh_bits as defined in message.h

It also contains certain descriptors in addition to the header, and the number of descriptors is specified in the body (msgh_descriptor_count).

The mach_msg_type_descriptor_t field specifies what type of descriptor it is, and the other fields contains the corresponding data. The following types of descriptors are present:

MACH_MSG_PORT_DESCRIPTOR: Sending a port in a message

MACH_MSG_OOL_DESCRIPTOR: Sending OOL data in a message

MACH_MSG_OOL_PORTS_DESCRIPTOR: Sending OOL ports array in a message

MACH_MSG_OOL_VOLATILE_DESCRIPTOR: Sending volatile data in a message

The OOL (Out-of-line) Ports descriptor has been used extensively in spraying the heap with user-controlled data. Whenever MACH_MSG_OOL_PORTS_DESCRIPTOR is used, it allocates (kalloc) an array in the kernel heap with all the port pointers. This technique was used in the voucher_swap exploit and will be discussed in Part 2 of this series.

Ports are represented by mach_port_t or mach_port_name_t in userland, but not in the kenrel, and this is why it is important to understand the difference between them when used in exploits. mach_port_name_t represents the local namespace identity but without associating any port rights, and it is essentially meaningless outside of the task’s namespace. However, whenever a process receives a mach_port_t from the kernel, it maps the associated port rights to the receiver, whereas in case of mach_port_name_t this is not the case. mach_port_t will usually always have at least one right, which could be **RECEIVE, SEND or SEND_ONCE. This is the reason when we are referring to the kernel task port in exploits; we use mach_port_t because it does associate the port rights with the object. Obtaining a handle to **mach_port_t automatically creates the associated send rights in the caller’s namespace.

In order to send or receive a message, the mach_msg and mach_msg_overwrite APIs can be used as defined in osfmk/mach/message.h. Let’s have a look at some code samples to get a better understanding. The following code snippet shows the creation of a mach port using the mach_port_allocate API and getting a receive right to that port.

The message can then be sent using the mach_msg Mach trap.

And can be received with mach_msg

If you have a send right to a port, you can insert that send right into another task using mach_port_insert_right and then sending the message using mach_msg. As discussed before, mach_port_name_t is meanigless outside a task’s namespace, this is why the task (ipc_space_t) needs to be specified along with the mach_port_name_t so that the kernel can put the specified name (mach_port_name_t) into that task’s namespace.

MIG - Mach Interface Generator

A lot of the code written using Mach APIs involves the same boilerplate code, doing which many times might cause complications and even lead to security flaws, and this is where the Mach Interface Generator comes in very handy. It implements a stub function based on a MIG specification file (defs). The client can call this stub function just like any other C function call, and the stub function handles marshaling and un-marshaling data in and out of the mach messages, thereby controlling all the Mach IPC implementation happening underneath.

MIG’s specification files have the extension defs, and when the kernel is compiled, these files get processed by mig and result in addition of extra files, which contains the autogenerated MIG wrappers. For e.g, let’s have a look at the task.defs file in osfmk/mach/task.defs. As you can see, each defs file has a subsystem name followed by an arbitrary number, which is declared at the very beginning of the file. In this case, the subsystem name is task and is the number is 3400. The stub function may also check the validity of the arguments that are passed to it.

If you want to generate the MIG wrappers, you can simple run mig on any def file from a clean directory.

During compilation, the mig tool creates three files based on the subsystem name. For e.g, for the task subsystem, the following files are created

taskUser.c - This file contains the implementations for the proxy functions which is responsible for marshalling the data into a message and sending it. It is also responsible for unmarshalling the returned data and getting it sent back to the client.

task.c - Prototype for the proxy functions

taskServer.c - Implementations for the stub functions are contained in this file.

There are many routines defined in the generated file and these are basically the functions. Let’s look at one specific Mach API routine task_set_exception_ports and have a look at the auto-generated MIG code.

It’s quite important to audit the code in these functions as well. In the next article, we will discuss a vulnerability identified in the autogenerated MIG code obtained after building the kernel.

Task Ports

One of the other useful features of Mach Ports is that they serve as an abstraction over Objects, and the abstraction is provided by Mach Messages which mostly translate over MIG. For example, the Host Mach ports provide many APIs to get information about the host. The host_kernel_version() function will print out the kernel version. This is the same API used by the uname -r command. Looking at the file osfmk/mach/mach_host.defs will show all the routines provided by the host port APIs.

Similarly, the task ports serve as an abstraction over the task. The APIs can be found under osfmk/mach/task.defs or osfmk/mach/task.defs in the BUILD folder in the kernel.

These APIs are quite powerful and allow full interaction with the target task. Having a send right to the task port of a process will give full control over that task, which includes reading, writing and allocating of memory in the target tasks memory region. Btw, we are mentioning Task (coming from Mach) ports of a process (coming from BSD), this might seem wierd and it is important to note that while these are 2 different flavours of Mach, they are internally linked. Every associated BSD process has a corresponding Mach task and vice versa. The task struct can be found under osfmk/kern/task.h , this has a bsd_info field which is a pointer to the proc structure in bsd/sys/proc_internal.h. Similarly, the task field in the proc structure is a pointer to the task structure of that process.

Using the Mach Trap task_for_pid, it is possible to get a send right to the task port corresponding to the target PID to the caller. As can be seen from the comments below in the implementation in the file bsd/vm/vm_unix.c, it is only permitted to privileged processes or processes with the same user ID. Apart from being privileged, calling this API also requires certain entitlements (get-task-allow and task_for_pid-allow).

Another thing you will notice here is the check for pid=0. This is done to prevent user specified process from accessing the send right to the kernel task port (tfp0) by specifying the pid 0. Previously, once kernel r/w was obtained, the jailbreaks used to kill this check and call task_for_pid(0). However, with the advent of KPP and AMCC/KTRR, patching wasn’t possible anymore, and hence other techniques were used but the name tfp0 still stuck and is still used to signify read and write access to kernel memory.

The other API very commonly used is the pid_for_task() Mach Trap, which is used to find the pid for the process corresponding to a given Mach Task. What it basically does is looks up the task struct, looks up the bsd_info field which points to the corresponding BSD proc struct in the kernel, and reads the p_pid value from the proc struct. This technique has been widely used to read arbitrary kernel memory four bytes at a time (since the pid field is 32 bits) by creating a fake task port, which is discussed later in this article.

Kernel Task Port

The kernel is assigned the PID 0, and the corresponding process-less task is dubbed as the kernel task. Having a send right to the Kernel task gives you complete control of the kernel memory, it is possible to read and write into kernel memory and also inject arbitrary code by allocating memory. This is what exploits try to obtain.

As discussed before, one of the earlier ways to use task_for_pid(0) was by Patching out the check for pid 0. There was also the processer_set_tasks() API on Mac OS that on a not secure kernel (#if defined SECURE_KERNEL), i.e. Mac OS, returned the kernel task port as the first argument.

Once the kernel task port is obtained, the following five MACH APIs are frequently used to interact with the memory. It is important to note that to execute this function successfully, the caller must have a send right to the task port of the target task. If you look at the function prototype, the first argument is the target task (vm_map_t target_task). You can pass the kernel task port (mach_port_t tfp0) as the first argument, and the API will gladly accept it.

hsp4 Patch

One of the other techniques Apple implemented for preventing jailbreakers from getting the kernel task was a pointer check for the kernel_task. In this case, while the handle to the kernel task was obtained, the Mach VM calls would not work. The check starts from the ipc_kmsg_trace_send function. This calls the function convert_port_to_task_with_exec_token(Line 356) in osfmk/kern/ipc_kobject.c.

The function convert_port_to_task_with_exec_token then calls task_conversion_eval(Line 1543).

This is where the check happens. The victim is the task on which operation is being performed and the caller is the one calling the function. The first check assumes if the caller is the kernel, and returns success if so. The second check is whether the caller is the same as the victim, which should be fine as a task should be able to perform operations on itself. The third check is where it makes a difference, if you make a change to the kernel_task and you are not kernel_task yourself, then the check will fail. However, this is just a pointer check with the kernel_task.

So while the kernel task is still obtained, you won’t be able to call the Mach APIs on it since it goes through the conversion APIs which will return KERN_INVALID_SECURITY and the previous function will return a TASK_NULL. There is another check by the way, which is that on embedded platforms, the code checks for the TF_PLATFORM flag in the code signature, which is nothing but the platform-application entitlement, which means that a caller without this entitlement cannot perform an operation on the victim that has this entitlement. We will discuss this in Part 3 of this series.

Hence, one of the more recent techniques has been to use the host_get_special_port() function. To understand this, head over to the file osfmk/mach/host_special_ports.h.

This contains a bunch of special ports, which as you might have guessed already from the comments, are used for special purposes. From the comments, it is clear that the first seven ports are reserved for the kernel itself. However, only three of them are being used so far. The HOST_PORT provides an abstraction over the host and HOST_PRIV is used for privileged operations, while the HOST_IO_MASTER_PORT is used to interact with devices. Each Host special port is mentioned with a particular number, which is of quite a significance. We can note that #4 is not being used anywhere.

Another thing worth mentioning is that in order to get send right to a host special port, you need to call host_get_special_port with an int node parameter, which is the number allocated to that special port.

Looking at the function, we can see that it requires the host_priv port as a parameter, and hence executing this call requires root permissions, in addition to all the sandbox checks. The host_get_special_port function essentially gets the port value from realhost.special[node] and returns it back to the caller.

Coming back to the pointer check, if we can do a remap on the kernel task, write it to the unused port space, which is realhost.special[4], and then call host_get_special_port(4), this should give us a remapped and working kernel task.

The following code snippet from cl0ver written by Siguza does exactly that

.

This technique is also known as the hsp4 patch and widely used in some of the recent jailbreaks.

Faking Task Ports

One of the most common techniques used in some of the recent jailbreaks is that of using Fake ports. The idea is to make the kernel look up a user controlled memory space thinking that it is a port. Using certain APIs, we can then extract data out of the kernel.

Let’s have a look at the stripped port structure which can be found in osfmk/ipc/ipc_port.h.

The first attribute is an ipc_object struct that can be found in osfmk/ipc/ipc_object.h.

The first field is io_bits, the details about these bits can be found under osfmk/ipc/ipc_object.h

The IO_BITS_ACTIVE needs to be set to make sure the object is alive. The IO_BITS_OTYPE specifies the object type. The IO_BITS_KOTYPE field that determines what kind of port it is, whether it is a task port, or a clock port etc. While creating a fake port, you need to specify these values in the io_bits field. A full list can be found under osfmk/kern/ipc_kobject.h

Setting the io_bits field of the ports would look as simple as this.

The io_references field of the ipc_object would also need to be set to anything other than 0, just to make sure the object isn’t deallocated.

Coming back to the port structure, one of the other important fields is the struct ipc_space *receiver field which points to the ipc_space struct. The ipc_space structure for a task defines its IPC abilities. Each IPC capability is represented by an ipc_entry and put in a table, which is pointed to by the is_table field in the ipc_space struct. The port rights or capablities in the is_table are 16 bits and have a name which is actually an index onto the is_table. It is important to note that within the kernel, port rights (mach_port_t) are represented by passing a pointer to the appropriate port data structure (ipc_port_t).

The IPC space is a very important struct, and hence most exploits look for the kernel ipc_space in order to get a proper (yet fake) kernel task port. The trick has been to copy the ipc_space_kernel to a new memory and make your fake port’s receiver field point to it.

The kobject field points to different data structures depending on the kobject type set in the io_bits field. Hence if you are faking a task port, you need to point the kobject field to a struct task, and in case of a clock, a struct clock.

That’s it, so you need to fake the port until you make it :). Here is an example of creating a fake port from the async_wake exploit.

For more details, i highly recommend checking out the this talk from CanSecWest here.

pid_for_task() arbitrary read technique

As discussed earlier, the pid_for_task Mach Trap will give out the PID of the corresponding task. It looks up the bsd_info field in the task struct which points to the corresponding BSD proc struct in the kernel, and reads the p_pid value. Assuming the p_pid field is at an offset of 0x10, and let’s say the address you want to read is addr, you can create a fake port, which then links to a fake task such that the bsd_info field in the task is addr - 0x10.

The following code from the voucher_swap exploit tries to do just that.

Just combine the method twice and you can now read 64 bits at a time.

It is important to note that the offsets keep changing with different versions of iOS and its even different for different devices. These offsets are found both by looking at the kernel source code and also by looking at the kernelcache file.

This technique is very powerful and allows you to scour the kernel memory 4 bytes at a time. Another very important use case for is function is to find the kernel slide. All they have to do is to start reading the kernel memory backwards four bytes at a time until you get to the magic value 0xfeedfacf. This address will denote the base address of the kernel, subtract it from the start address on the kernelcache when opened with IDA or Hopper and you will get the kernel slide. The following code from the Yalu jailbreak does just that.

Once kernel base is obtained, you can find some important structures in the kernel memory, such as extern struct proclist allproc;, which can be found in the file /bsd/sys/proc_internal.h, since even though the kernel is slid because of KASLR, the structs are still at a fixed offset from the kernel base. As we can see from the kernel code, this struct contains a list of the prcesses. The symbol addresses can also be found using **jtool2 –analyze** feature, which utilizes the unstripped kernelcache that Apple mistakenly pushed out as a facilitator.

One can then scour these structs using again the same function pid_for_task() to find the current proc struct by checking for pid = getpid() (so we can change the creds in the proc struct later to escape the sandbox), and kernproc by checking for pid = 0 (so we can get kern proc creds, find kernel task, ipc_space_kernel etc).

Heap Allocation Basics

This is a very brief discussion about Heap Allocation in iOS. In iOS, the heap memory is divided into various zones. Allocations of same size will go into same zones, unless for certain objects which have their own special zones (ports, vouchers etc). These zones grow as more objects are allocated, with the new pages being fetched from the zone map. One can see the zones allocated with the zprint command on Mac OS. It is assumed that a lot of heap allocation techniques will still be the same in iOS. Another thing is to note that iOS has zone garbage collection as well.

As discussed, certain objects have their own special zones. A zone is a collection of fixed size data blocks for which quick allocation and deallocation is possible. For e.g, in the image below, we can see that the a lot of the IPC objects, which includes ports, vouchers etc have their own zones. Hence if you are able to free a voucher let’s say, you won’t be able to overlap it with another object, unless you trigger zone garbage collection and move the page containing that address somewhere else to be reallocated again with a different kind of object.

The heap has been hardened significantly in the last few iOS versions. I highly recommend checking out this talk on iOS Kernel Heap by Stefan Esser. Additionally, you can also check out the kernel source code. Start by looking osfmk/kern/zalloc.c which has some comments on heap allocation and just follow along from there.

One of the common techniques used in recent exploits for heap spraying is to fill the memory with an array of Port pointers by sending a Mach message with the option MACH_MSG_OOL_PORTS_DESCRIPTOR. This calls the method ipc_kmsg_copyin_ool_ports_descriptor in ipc/ipc_kmsg.c which has a kalloc call (kalloc(ports_length)) that fills the heap with port pointers. The advantage of this is in the voucher_swap exploit was that while the allocation of Ports would have put them into their own ipc.port zones, in the case of port pointers this is not the case and hence reallocation on top of freed objects with port pointers is possible. Well, again this is not entirely true and reallocation with ports is possible as you can do enough spraying with Ports such that the kernel is force to do garbage collection and allocate fresh pages from the zone map which might include the freed objects. This is discussed in Part 2 of this series.

Pointer Authentication Check and CoreTrust

The ARM 8.3 instruction set added a new feature called Pointer Authentication Check (PAC). It’s purpose is to check the integrity of the pointers. It works by attaching a cryptographic signature to pointer values in its unused bits, and then those signatures are verified before a pointer is used. Since the attacker doesn’t have the keys to create the signatures for these pointers, he is not able to create valid pointers.

CoreTrust on the other hand is a separate kernel extension (com.apple.kext.CoreTrust) that doesn’t allow self-signed binaries (jtool2 –sign) to run on the device. Previously, Apple Mobile File Integrity Kext (AMFI.kext) would work in conjunction with the amfid daemon which is in userland to check for code signatures. This was bypassed in many ways by injecting the code signature hash into the AMFI trust cache, hooking onto amfid exception ports and allowing code execution to continue etc. CoreTrust imposes some additional checks that only allow Apple signed binaries to run on the device. It is still possible ro run binaries signed with Apple certificates, which anyone can get for free and run the binary once signed with it.

Conclusion

In this article, we looked at some of the basic fundamentals of iOS security which will serve as building blocks for the next two articles. The next article will discuss the voucher_swap exploit in detail whereas the third part would discuss Jailbreaking.

References

Project Zero Issue tracker - https://bugs.chromium.org/p/project-zero/issues/detail?id=1731
