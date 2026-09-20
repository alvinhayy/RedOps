---
title: Ansible
source_url: https://notes.incendium.rocks/pentesting-notes/linux-pentesting/ansible
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: linux
---

## Vault hashes

If you stumble on some vault hashes, you might be able to decrypt them.

### Example of hash

```jsx
ldap_uri: ldap://127.0.0.1/
ldap_base_dn: "DC=authority,DC=htb"
ldap_admin_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          63303831303534303266356462373731393561313363313038376166336536666232626461653630
          3437333035366235613437373733316635313530326639330a643034623530623439616136363563
          34646237336164356438383034623462323531316333623135383134656263663266653938333334
          3238343230333633350a646664396565633037333431626163306531336336326665316430613566
          3764
```

Save the hash and use ansible2john to create a hash for john the ripper:

```jsx
ansible2john vaulthash > vaultforjohn
```

And use john:

```jsx
┌──(kali㉿kali)-[~/htb/authority/hashes]
└─$ sudo john vaultforjohn --wordlist=/usr/share/wordlists/rockyou.txt
Created directory: /root/.john
Using default input encoding: UTF-8
Loaded 1 password hash (ansible, Ansible Vault [PBKDF2-SHA256 HMAC-256 128/128 AVX 4x])
Cost 1 (iteration count) is 10000 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
!@#$%^&*         (vault)
```

Now that we have the vault password, we can decrypt the vault passwords using ansible-vault:

```jsx
┌──(kali㉿kali)-[~/htb/authority/hashes]
└─$ ansible-vault decrypt pw3
Vault password:
Decryption successful

┌──(kali㉿kali)-[~/htb/authority/hashes]
└─$ ansible-vault decrypt pw2
Vault password:
Decryption successful

┌──(kali㉿kali)-[~/htb/authority/hashes]
└─$ ansible-vault decrypt pw3
Vault password:
Decryption successful
```

* By default it will store the password in the hash input file
