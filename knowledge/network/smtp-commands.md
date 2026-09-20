---
title: "SMTP - Commands"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/network-services-pentesting/pentesting-smtp/smtp-commands.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: network
---

# SMTP Commands

## Core commands<sup>\[\\[1\\]\](#references)</sup>

[\[1\]](#references)
- **`EHLO <domain>`** : Identifies an Extended SMTP client and requests the server’s extension list.
- **`HELO <domain>`** : Legacy greeting used when ESMTP is unavailable.
- **`MAIL FROM:<reverse-path>`** : Starts a transaction and sets its envelope sender. This is not the message’s`From:` header.
- **`RCPT TO:<forward-path>`** : Adds one envelope recipient; repeat it for additional recipients.
- **`DATA`** : Requests permission to transmit the message headers and body. A`354` reply means the client may send the content, terminated by a line containing only a dot.
- **`RSET`** : Aborts the current transaction and clears its sender, recipients, and data without closing the SMTP connection.
- **`VRFY <string>`** : Requests confirmation that a string identifies a user or mailbox. Servers commonly disable useful responses to reduce enumeration.
- **`EXPN <string>`** : Requests expansion of a mailing list. Servers may disable it.
- **`HELP [command]`** : Requests general or command-specific help.
- **`NOOP`** : Requests a successful reply without changing transaction state.
- **`QUIT`** : Ends the SMTP session.

## Common extensions

- **`SIZE [bytes]`** : The server advertises its maximum accepted message size; the client may declare the planned message size on`MAIL FROM` .<sup>[\[2\]](#references)</sup>
- **`AUTH <mechanism>`** : Starts SMTP authentication using a mechanism advertised in the`EHLO` response. Credentials are not necessarily encrypted, so negotiate TLS first unless the selected mechanism provides adequate protection.<sup>[\[3\]](#references)</sup>
- **`STARTTLS`** : Requests an upgrade of the connection to TLS. After a successful TLS negotiation, the client sends`EHLO` again because the advertised extensions can change.<sup>[\[4\]](#references)</sup>

The obsolete `TURN` command from RFC 821 reversed the client and server roles on an existing connection. RFC 5321 no longer defines it, so do not expect current servers to support it.[\[1\]](#references)[\[5\]](#references)

For a shorter operator-oriented catalog of these commands, the original page used ServerSMTP’s command overview.[\[6\]](#references)

## References
