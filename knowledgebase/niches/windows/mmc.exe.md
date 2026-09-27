---
title: "Mmc.exe"
source: lolbas-project.github.io
source_url: https://lolbas-project.github.io/lolbas/Binaries/Mmc/
fetched_at: 2026-09-20T17:10:37Z
license: unspecified
category: windows
---

Load snap-ins to locally and remotely manage Windows systems

## Paths
- C:\Windows\System32\mmc.exe
- C:\Windows\SysWOW64\mmc.exe

## Resources
- [https://bohops.com/2018/08/18/abusing-the-com-registry-structure-part-2-loading-techniques-for-evasion-and-persistence/](https://bohops.com/2018/08/18/abusing-the-com-registry-structure-part-2-loading-techniques-for-evasion-and-persistence/)
- [https://offsec.almond.consulting/UAC-bypass-dotnet.html](https://offsec.almond.consulting/UAC-bypass-dotnet.html)
- [https://www.youtube.com/watch?v=LFgZOTmhzeA](https://www.youtube.com/watch?v=LFgZOTmhzeA)

## Acknowledgements
- Jimmy ([@bohops](https://twitter.com/@bohops))
- clem ([@clavoillotte](https://twitter.com/@clavoillotte))
- Fredrik H. Brathen

## Detections
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_mmc_susp_child_process.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/process_creation/proc_creation_win_mmc_susp_child_process.yml)
- Sigma: [https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/file/file_event/file_event_win_uac_bypass_dotnet_profiler.yml](https://github.com/SigmaHQ/sigma/blob/c04bef2fbbe8beff6c7620d5d7ea6872dbe7acba/rules/windows/file/file_event/file_event_win_uac_bypass_dotnet_profiler.yml)

## Execute

1. Launch a ‘backgrounded’ MMC process and invoke a COM payload

```
mmc.exe -Embedding {PATH_ABSOLUTE:.msc}
```

   - Use case: Configure a snap-in to load a COM custom class (CLSID) that has been added to the registry

   - Privileges required: User

   - Operating systems: Windows 10 (and possibly earlier versions), Windows 11

   - ATT&CK® technique: T1218.014

   - Tags: Execute: COM

2. Load an arbitrary payload DLL by configuring COR Profiler registry settings and launching MMC to bypass UAC.

```
mmc.exe gpedit.msc
```

   - Use case: Modify HKCU\Environment key in Registry with COR profiler values then launch MMC to load the payload DLL.

   - Privileges required: Administrator

   - Operating systems: Windows 10 (and possibly earlier versions), Windows 11

   - ATT&CK® technique: T1218.014

   - Tags: Execute: DLL

3. Download and save an executable to disk

```
mmc.exe -Embedding {PATH_ABSOLUTE:.msc}
```

   - Use case: Download file from Internet

   - Privileges required: User

   - Operating systems: Windows 10 (and possibly earlier versions), Windows 11

   - ATT&CK® technique: T1218.014

   - Tags: Application: GUI
