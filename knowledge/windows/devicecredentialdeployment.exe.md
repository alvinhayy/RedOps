---
title: "DeviceCredentialDeployment.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/DeviceCredentialDeployment/
fetched_at: 2026-09-20T17:09:52Z
license: unspecified
category: windows
---

Device Credential Deployment

## Paths
- C:\Windows\System32\DeviceCredentialDeployment.exe

## Acknowledgements
- Elliot Killick ([@elliotkillick](https://twitter.com/@elliotkillick))

## Detections
- IOC: DeviceCredentialDeployment.exe should not be run on a normal workstation
- Sigma: [https://github.com/SigmaHQ/sigma/blob/ff5102832031425f6eed011dd3a2e62653008c94/rules/windows/process_creation/proc_creation_win_lolbin_device_credential_deployment.yml](https://github.com/SigmaHQ/sigma/blob/ff5102832031425f6eed011dd3a2e62653008c94/rules/windows/process_creation/proc_creation_win_lolbin_device_credential_deployment.yml)

## Conceal

1. Grab the console window handle and set it to hidden

```
DeviceCredentialDeployment
```

   - Use case: Can be used to stealthily run a console application (e.g. cmd.exe) in the background

   - Privileges required: User

   - Operating systems: Windows 10

   - ATT&CK® technique: T1564
