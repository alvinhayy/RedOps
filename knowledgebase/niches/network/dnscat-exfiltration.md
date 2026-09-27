---
title: "DNSCat pcap analysis"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/basic-forensic-methodology/pcap-inspection/dnscat-exfiltration.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: network
---

```
from scapy.all import rdpcap, DNSQR, DNSRR
import struct
f = ""
last = ""
for p in rdpcap('ch21.pcap'):
	if p.haslayer(DNSQR) and not p.haslayer(DNSRR):
		qry = p[DNSQR].qname.replace(".jz-n-bs.local.","").strip().split(".")
		qry = ''.join(_.decode('hex') for _ in qry)[9:]
		if last != qry:
			print(qry)
			f += qry
		last = qry
#print(f)
```
```
python3 dnscat_decoder.py sample.pcap bad_domain
```
## References

- [1] [dnscat2 protocol documentation](https://github.com/iagox86/dnscat2/blob/master/doc/protocol.md)
- [2] [DNSCat2 pcap forensics writeup – BSidesSF 2017 CTF](https://github.com/jrmdev/ctf-writeups/tree/master/bsidessf-2017/dnscap)
- [3] [DNScat-Decoder](https://github.com/josemlwdf/DNScat-Decoder)
