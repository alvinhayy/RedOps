---
title: "Online Platforms with API"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/todo/online-platforms-with-api.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## [Project Honey Pot](https://www.projecthoneypot.org/) <sup>[\[1\]](#references)</sup>

[\[1\]](#references)

Query whether an IP address has been associated with suspicious or malicious activity. Access may require an account or API key.

## [**BotScout**](https://botscout.com/api.htm) <sup>[\[2\]](#references)</sup>

**BotScout**

[\[2\]](#references)

Check whether an IP address, username, or email address has been associated with automated account registration or other reported bot activity.

## [Hunter](https://hunter.io/) <sup>[\[3\]](#references)</sup>

[\[3\]](#references)

Find and verify professional email addresses and domain-related contact patterns. Check the current plan for request limits and permitted uses.

## [AlienVault OTX](https://otx.alienvault.com/api) <sup>[\[4\]](#references)</sup>

[\[4\]](#references)

Search threat-intelligence indicators and activity associated with IP addresses and domains.

## [Clearbit](https://dashboard.clearbit.com/) <sup>[\[5\]](#references)</sup>

[\[5\]](#references)

Enrich an email address, domain, or company with available business/profile data. Coverage, access, and privacy constraints depend on the current product and plan.

## [BuiltWith](https://builtwith.com/) <sup>[\[6\]](#references)</sup>

[\[6\]](#references)

Identify technologies observed on websites and obtain historical or relationship data where the selected plan permits it.

## [FraudGuard](https://fraudguard.io/) <sup>[\[7\]](#references)</sup>

[\[7\]](#references)

Check whether an IP address is associated with suspicious or malicious activity. Confirm current API plans and limits.

## [FortiGuard](https://fortiguard.com/) <sup>[\[8\]](#references)</sup>

[\[8\]](#references)

Look up FortiGuard categorization and threat intelligence for domains, URLs, or IP addresses. Availability differs by service.

## [SpamCop](https://www.spamcop.net/) <sup>[\[9\]](#references)</sup>

[\[9\]](#references)

Check whether an IP address is listed for reported spam activity.

## [myWOT](https://www.mywot.com/) <sup>[\[10\]](#references)</sup>

[\[10\]](#references)

Retrieve a domain’s reputation based on the service’s community and other signals.

## [IPinfo](https://ipinfo.io/) <sup>[\[11\]](#references)</sup>

[\[11\]](#references)

Obtain geolocation, ASN, organization, and related metadata for an IP address. Check the current plan for quotas.

## [SecurityTrails](https://securitytrails.com/app/account) <sup>[\[12\]](#references)</sup>

[\[12\]](#references)

This platform provides DNS and infrastructure intelligence such as historical resolutions, domains associated with IPs or name servers, and related records. Historical DNS may reveal an earlier origin address, but it does not reliably bypass a CDN and must be validated.

## [FullContact](https://www.fullcontact.com/) <sup>[\[13\]](#references)</sup>

[\[13\]](#references)

Enrich an email address, domain, or company name with available identity and business attributes. Handle personal data according to authorization and privacy requirements.

## RiskIQ / Microsoft Defender Threat Intelligence (legacy transition) <sup>\[\\[14\\]\](#references)</sup>

[\[14\]](#references)
RiskIQ’s PassiveTotal capabilities transitioned into Microsoft Defender Threat Intelligence. Product access, APIs, and retained functionality have changed, so use Microsoft’s current documentation rather than legacy PassiveTotal assumptions.

## [Intelligence X](https://intelx.io/) <sup>[\[15\]](#references)</sup>

[\[15\]](#references)

Search domains, IP addresses, email addresses, and indexed historical or leaked data, subject to the service’s access controls.

## [IBM X-Force Exchange](https://exchange.xforce.ibmcloud.com/) <sup>[\[16\]](#references)</sup>

[\[16\]](#references)

Search IP addresses and other indicators for threat-intelligence and reputation data.

## [GreyNoise](https://viz.greynoise.io/) <sup>[\[17\]](#references)</sup>

[\[17\]](#references)

Search IP addresses or ranges for observations of internet scanning and common service activity. Check current trial and community-access terms.

## [Shodan](https://www.shodan.io/) <sup>[\[18\]](#references)</sup>

[\[18\]](#references)

Retrieve internet-scan and service information for an IP address, host, or search query. API access depends on the account plan.

## [Censys](https://censys.io/) <sup>[\[19\]](#references)</sup>

[\[19\]](#references)

Search host, certificate, domain, and internet-service datasets; its data model and coverage differ from Shodan’s.

## [GrayHatWarfare bucket search](https://buckets.grayhatwarfare.com/) <sup>[\[20\]](#references)</sup>

[\[20\]](#references)

Search the provider’s index of publicly observed cloud-storage objects and buckets by keyword.

## [DeHashed](https://www.dehashed.com/data) <sup>[\[21\]](#references)</sup>

[\[21\]](#references)

Search indexed breach data for email addresses, usernames, domains, and related records. Use only with authorization and avoid unnecessary exposure of breach data.

## [psbdmp](https://psbdmp.ws/) <sup>[\[22\]](#references)</sup>

[\[22\]](#references)

Search indexed paste content for occurrences of an email address or other term. Verify that the service is still available before integrating it.

## [EmailRep](https://emailrep.io/key) <sup>[\[23\]](#references)</sup>

[\[23\]](#references)

Retrieve reputation and risk signals for an email address.

## GhostProject (historical) <sup>\[\\[24\\]\](#references)</sup>

[\[24\]](#references)
Historically advertised searches of leaked email/password data. Treat the service as high-risk third-party handling and verify its availability, legality, and authorization before use.

## [BinaryEdge](https://www.binaryedge.io/) <sup>[\[25\]](#references)</sup>

[\[25\]](#references)

Obtain internet-scan, exposure, and threat-intelligence data for IP addresses and related assets.

## [Have I Been Pwned](https://haveibeenpwned.com/) <sup>[\[26\]](#references)</sup>

[\[26\]](#references)

Check whether an email address or verified domain appears in known breaches. The separate Pwned Passwords service checks password hashes by prefix; it does **not** reveal plaintext passwords.

### [IP2Location.io](https://www.ip2location.io/) <sup>[\[27\]](#references)</sup>

[\[27\]](#references)

Retrieve IP geolocation, data-center, ASN, proxy/VPN, and related enrichment fields. Quotas depend on the current plan.

### [IPQuery.io](https://www.ipquery.io/) <sup>[\[28\]](#references)</sup>

[\[28\]](#references)

IP geolocation and OSINT-oriented enrichment with selected data points. Check current terms for commercial use.

[DNSDumpster](https://dnsdumpster.com/) provides DNS-reconnaissance results.[\[29\]](#references)

[Netcraft](https://www.netcraft.com/) provides site, hosting, and internet-infrastructure intelligence.[\[30\]](#references)

[NMMapper](https://www.nmmapper.com/sys/tools/subdomainfinder/) provides an online subdomain-discovery interface.[\[31\]](#references)

## References

- [1] [Project Honey Pot](https://www.projecthoneypot.org/)
- [2] [BotScout API](https://botscout.com/api.htm)
- [3] [Hunter API](https://hunter.io/api-documentation)
- [4] [AlienVault OTX API](https://otx.alienvault.com/api)
- [5] [Clearbit](https://dashboard.clearbit.com/)
- [6] [BuiltWith](https://builtwith.com/)
- [7] [FraudGuard](https://fraudguard.io/)
- [8] [FortiGuard Labs](https://www.fortiguard.com/)
- [9] [SpamCop](https://www.spamcop.net/)
- [10] [Web of Trust](https://www.mywot.com/)
- [11] [IPinfo](https://ipinfo.io/)
- [12] [SecurityTrails](https://securitytrails.com/)
- [13] [FullContact](https://www.fullcontact.com/)
- [14] [Microsoft Defender Threat Intelligence](https://learn.microsoft.com/en-us/defender/threat-intelligence/what-is-microsoft-defender-threat-intelligence-defender-ti)
- [15] [Intelligence X](https://intelx.io/)
- [16] [IBM X-Force Exchange](https://exchange.xforce.ibmcloud.com/)
- [17] [GreyNoise](https://www.greynoise.io/)
- [18] [Shodan](https://www.shodan.io/)
- [19] [Censys](https://censys.com/)
- [20] [GrayHatWarfare](https://buckets.grayhatwarfare.com/)
- [21] [DeHashed](https://www.dehashed.com/)
- [22] [psbdmp](https://psbdmp.ws/)
- [23] [EmailRep](https://emailrep.io/)
- [24] [Cornell research — Protocols for Checking Compromised Credentials (includes GhostProject)](https://rist.tech.cornell.edu/papers/c3.pdf)
- [25] [BinaryEdge](https://www.binaryedge.io/)
- [26] [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)
- [27] [IP2Location.io](https://www.ip2location.io/)
- [28] [IPQuery](https://www.ipquery.io/)
- [29] [DNSDumpster](https://dnsdumpster.com/)
- [30] [Netcraft](https://www.netcraft.com/)
- [31] [NMMapper Subdomain Finder](https://www.nmmapper.com/sys/tools/subdomainfinder/)
