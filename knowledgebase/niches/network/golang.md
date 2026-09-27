---
title: "Golang"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-web/golang.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

# Go `net/http` path handling with `CONNECT`

`net/http` path handling with `CONNECT`

## Historical `ServeMux` behavior

`ServeMux` behavior
In the referenced version of Go’s `net/http` package, `ServeMux.Handler` canonicalizes the URL path for ordinary HTTP methods. It calls `cleanPath` and redirects the client when the clean result differs from the supplied path. This removes `.` and `..` segments and repeated slashes.[\[1\]](#references)

For example, ordinary requests for `/flag/`, `/../flag`, or `/flag/.` can be redirected to the canonical `/flag` path, depending on the registered handler and trailing-slash behavior.[\[1\]](#references)

The historical implementation treats `CONNECT` specially and does not run its path through this canonicalization branch. Consequently, middleware or routing logic that assumes every request has already received a cleaned path may interpret a `CONNECT` target differently from another method. Whether this produces a security bypass depends on the Go version, handler registrations, proxies, and authorization checks in the application.[\[1\]](#references)

Use curl’s `--path-as-is` option to prevent curl from normalizing the target before sending it.<sup>[\[2\]](#references)</sup> For example:

```
curl --path-as-is -X CONNECT http://gofs.web.jctf.pro/../flag
```
Compare the response with requests using a normal method and a canonical path. A different response is only an indicator; confirm that the discrepancy crosses an authorization boundary before reporting it.

## References
