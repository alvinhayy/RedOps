---
title: "Filesystem, Inodes and Recovery"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/linux-hardening/main-system-information/filesystem-inodes-and-recovery.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: linux
---

## Disk Images and Loop Mounts

A regular file can contain a complete filesystem, so a disk image can expose a second filesystem tree when mounted.[\[1\]](#references)

Backup images, copied block devices, VM artifacts, or renamed blobs can therefore contain credentials, scripts, SSH keys, configuration files, or flags even when they do not look useful from the outside.

Identify likely images with `file` to classify a candidate, `blkid` to probe recognized filesystem metadata, and `strings -a` to scan the whole file for printable sequences.[\[10\]](#references)[\[11\]](#references)[\[12\]](#references)

```
file ./candidate
ls -lh ./candidate
blkid ./candidate 2>/dev/null
strings -a ./candidate | head -n 50
```
When mounting is allowed, use a loop mount with `ro` so the image is attached read-only; the `find` command below limits the inspection depth and file type.[\[1\]](#references)[\[4\]](#references)

```
mkdir -p /tmp/imgmnt
sudo mount -o loop,ro ./candidate /tmp/imgmnt
find /tmp/imgmnt -maxdepth 3 -type f -ls 2>/dev/null
sudo umount /tmp/imgmnt
```
If mounting is not available and the image is ext2/ext3/ext4, inspect its metadata directly with `debugfs`.[\[2\]](#references)

```
debugfs -R 'ls -l /' ./candidate 2>/dev/null
debugfs -R 'stat /' ./candidate 2>/dev/null
```
The technique is useful because it turns a normal-looking file into a second filesystem tree.<sup>[\[1\]](#references)</sup> Treat it as a way to recover hidden data, not as a privilege escalation by itself.

## Writable Mount Abuse

A writable mount becomes dangerous when a more privileged context later trusts something inside it. The important question is not only “can I write here?”, but “who later reads, executes, imports, or loads from here?”.

Use `findmnt` to inspect mounted filesystems and their options.[\[9\]](#references)

Find writable mounts and suspicious consumers with the documented `find` permission, type, and filesystem-boundary predicates, then use recursive `grep` to search likely consumer configuration.[\[4\]](#references)[\[20\]](#references)

```
findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS
find /mnt /media /srv /opt -xdev -type d -writable -ls 2>/dev/null
find /mnt /media /srv /opt -xdev -type f -writable -ls 2>/dev/null | head -n 50
grep -RniE 'cron|systemd|ExecStart|backup|hook|plugin|sh |bash |python' /mnt /media /srv /opt 2>/dev/null | head -n 50
```
Common abuse patterns:

- A cron job or systemd service runs a writable script from the mount.<sup>[\[13\]](#references)[\[14\]](#references)</sup>
- A privileged service loads plugins, config, templates, or helper binaries from the mount.
- A mount contains SUID files and allows modification, replacement, or path manipulation.
- A container or chroot exposes a host-backed path that is writable from the restricted environment. Mount namespaces provide distinct mount hierarchies, while `chroot()` only changes pathname resolution and is not a full sandbox.<sup>[\[15\]](#references)[\[16\]](#references)</sup>

Generic validation pattern using the same `find` predicates.[\[4\]](#references)

```
find /mnt /media /srv /opt -xdev -perm -4000 -type f -ls 2>/dev/null
find /mnt /media /srv /opt -xdev -type f -writable -ls 2>/dev/null | head -n 50
```
When proving impact in an authorized lab, keep the payload observable and minimal, for example writing `id` output to a temporary file.<sup>[\[23\]](#references)</sup> The core technique is delayed execution through a trusted writable location.

## Inodes and Path Confusion

An inode is the filesystem object; a path is only a name pointing to it. Device and inode metadata let you distinguish objects across filesystems, while link counts expose multiple hard links.<sup>[\[3\]](#references)</sup> A deleted pathname does not always mean the data is gone while a process still has the file open.[\[5\]](#references)

The `find` predicates below compare inode identity, link counts, device boundaries, and timestamps.[\[4\]](#references)

Compare files by inode and device with `ls -i` and `stat` metadata formats.[\[17\]](#references)[\[18\]](#references)

```
ls -li /path/a /path/b
stat -c 'dev=%d inode=%i links=%h mode=%A owner=%U:%G path=%n' /path/a /path/b
```
Find every visible pathname for the same inode with `find -samefile`.[\[4\]](#references)

```
find / -xdev -samefile /path/to/file -ls 2>/dev/null
```
Search directly by inode number with `find -inum` when you only have metadata.[\[4\]](#references)

```
find / -xdev -inum <inode_number> -ls 2>/dev/null
```
This technique is useful when a file appears under an unexpected name, when an application validates one path but uses another, or when a privileged wrapper interacts with an inode that is also reachable somewhere else.

## Hardlink Abuse

Hardlinks create multiple names for the same inode. They do not point to a target path like symlinks do; they are equal names for the same file object.[\[3\]](#references)

Find SUID files with multiple hardlinks using `find`’s permission and link-count predicates.[\[4\]](#references)

```
find / -xdev -perm -4000 -type f -links +1 -ls 2>/dev/null
```
Inspect one suspicious file with `stat` and `find -samefile`.[\[4\]](#references)[\[17\]](#references)

```
stat /path/to/suspicious
find / -xdev -samefile /path/to/suspicious -ls 2>/dev/null
```
Why it matters:

- A sensitive file may be reachable through a less obvious path.
- A SUID wrapper may be hidden behind a name that does not look privileged.
- Cleanup that removes one pathname may leave another hardlink alive.

Linux’s `fs.protected_hardlinks` sysctl can restrict hardlink creation across privilege boundaries.<sup>[\[7\]](#references)</sup> Existing hardlinks still merit review.

## Deleted File Recovery Through Open FDs

When a process keeps a file open, unlinking its last pathname leaves the file alive until the last descriptor closes; Linux exposes those descriptors under `/proc/<pid>/fd/`.[\[5\]](#references)[\[6\]](#references)

Find deleted open files by listing `/proc` descriptors and filtering open-file output.[\[5\]](#references)[\[6\]](#references)[\[18\]](#references)[\[19\]](#references)[\[20\]](#references)

```
ls -l /proc/*/fd/* 2>/dev/null | grep ' (deleted)' | head -n 50
lsof 2>/dev/null | grep deleted | head -n 50
```
Recovering through these links is permission-dependent because dereferencing `/proc/<pid>/fd` is subject to ptrace access checks and file permissions.[\[6\]](#references)

When permitted, `readlink` shows the descriptor target and `cp` copies its contents.[\[21\]](#references)[\[22\]](#references)

```
readlink /proc/<pid>/fd/<fd>
cp /proc/<pid>/fd/<fd> /tmp/recovered-file
file /tmp/recovered-file
```
This is a practical technique for recovering deleted logs, temporary secrets, dropped binaries, rotated files, or scripts removed after execution.

## ext Recovery With debugfs

On ext2/ext3/ext4 filesystems, `debugfs` can inspect inode metadata and dump inode contents from a block device or image; without `-w`, it opens the filesystem read-only.<sup>[\[2\]](#references)</sup> Work on a copy or a read-only image whenever possible.

List entries and inspect inodes with `debugfs` requests for directory listings, inode status, and inode-to-path checks.[\[2\]](#references)

```
debugfs -R 'ls -l /' ./disk.img
debugfs -R 'stat <inode_number>' ./disk.img
debugfs -R 'ncheck <inode_number>' ./disk.img
```
Dump a known inode with the `debugfs dump` command, then classify the recovered output with `file`.[\[2\]](#references)[\[10\]](#references)

```
debugfs -R 'dump <inode_number> /tmp/recovered.bin' ./disk.img
file /tmp/recovered.bin
```
This is not guaranteed recovery. It depends on filesystem state, whether blocks were reused, and whether the metadata still exists. For ext3/ext4, the `debugfs` manual notes that deleted-inode recovery may fail because released inode data blocks are no longer available.<sup>[\[2\]](#references)</sup> The technique is still valuable because it lets you inspect inode-level state without relying on normal path traversal.

## Inode Exhaustion and Ordering

Inode exhaustion happens when a filesystem runs out of file nodes even if free disk space remains.<sup>[\[8\]](#references)[\[17\]](#references)</sup> It usually causes reliability failures, but it can also explain strange behavior during incident response or lab triage.

Use `df -i` to report inode information instead of block usage.[\[8\]](#references)

Check inode pressure with `df` and a `find` count of directory parents.[\[4\]](#references)[\[8\]](#references)

```
df -h
df -i
find /var /tmp /home -xdev -printf '%h\n' 2>/dev/null | sort | uniq -c | sort -n | tail
```
Inode numbers and timestamps can also help reconstruct activity in simple lab environments.

The `find` format directives below expose those fields.[\[4\]](#references)

```
find /path -xdev -printf '%i %TY-%Tm-%Td %TH:%TM %p\n' 2>/dev/null | sort -n | tail -n 50
find /path -xdev -newermt '2026-01-01' -ls 2>/dev/null
```
Treat ordering as a clue, not proof. Copy operations, archive extraction, filesystem type, restores, and concurrent writes can all change allocation patterns.

## Defensive Notes

- Mount unknown images read-only during analysis.<sup>[\[1\]](#references)</sup>
- Keep privileged scripts, service units, plugins, and helper paths outside user-writable mounts.
- Use `nosuid` ,`nodev` , and`noexec` where operationally appropriate; these options disable set-ID/capability execution, device interpretation, or direct binary execution on the mount.<sup>[\[1\]](#references)</sup> Do not treat them as a complete boundary.
- Restrict access to `/proc/<pid>/fd` ; dereferencing those links is controlled by ptrace access checks and file permissions.<sup>[\[6\]](#references)</sup> Restrict broader process metadata and cross-user inspection where possible.
- Monitor writable mount points, unexpected hardlinks to privileged files, and deleted-but-open sensitive files.

## References

- [1] [mount(8) — Linux manual page](https://man7.org/linux/man-pages/man8/mount.8.html)
- [2] [debugfs(8) — Linux manual page](https://man7.org/linux/man-pages/man8/debugfs.8.html)
- [3] [inode(7) — Linux manual page](https://man7.org/linux/man-pages/man7/inode.7.html)
- [4] [find(1) — Linux manual page](https://man7.org/linux/man-pages/man1/find.1.html)
- [5] [unlink(2) — Linux manual page](https://man7.org/linux/man-pages/man2/unlink.2.html)
- [6] [proc_pid_fd(5) — Linux manual page](https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html)
- [7] [Documentation for /proc/sys/fs/ — The Linux Kernel documentation](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html)
- [8] [df(1) — Linux manual page](https://man7.org/linux/man-pages/man1/df.1.html)
- [9] [findmnt(8) — Linux manual page](https://man7.org/linux/man-pages/man8/findmnt.8.html)
- [10] [file(1) — Linux manual page](https://man7.org/linux/man-pages/man1/file.1.html)
- [11] [blkid(8) — Linux manual page](https://man7.org/linux/man-pages/man8/blkid.8.html)
- [12] [strings(1) — Linux manual page](https://man7.org/linux/man-pages/man1/strings.1.html)
- [13] [crontab(5) — Linux manual page](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [14] [systemd.service(5) — Linux manual page](https://man7.org/linux/man-pages/man5/systemd.service.5.html)
- [15] [mount_namespaces(7) — Linux manual page](https://man7.org/linux/man-pages/man7/mount_namespaces.7.html)
- [16] [chroot(2) — Linux manual page](https://man7.org/linux/man-pages/man2/chroot.2.html)
- [17] [stat(1) — Linux manual page](https://man7.org/linux/man-pages/man1/stat.1.html)
- [18] [ls(1) — Linux manual page](https://man7.org/linux/man-pages/man1/ls.1.html)
- [19] [lsof(8) — Linux manual page](https://man7.org/linux/man-pages/man8/lsof.8.html)
- [20] [grep(1) — Linux manual page](https://man7.org/linux/man-pages/man1/grep.1.html)
- [21] [readlink(1) — Linux manual page](https://man7.org/linux/man-pages/man1/readlink.1.html)
- [22] [cp(1) — Linux manual page](https://man7.org/linux/man-pages/man1/cp.1.html)
- [23] [id(1) — Linux manual page](https://man7.org/linux/man-pages/man1/id.1.html)
