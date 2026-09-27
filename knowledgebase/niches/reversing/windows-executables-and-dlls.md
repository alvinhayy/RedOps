---
title: "Windows executables and DLL's"
source_url: https://notes.incendium.rocks/pentesting-notes/reversing/windows-executables-and-dlls
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: reversing
---

## dnSpy

dnSpy is a debugger and .NET assembly editor. You can use it to edit and debug assemblies even if you don't have any source code available.

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FJayH2pq1H4neJCKwlpmV%2Fdebug-animated.gif?alt=media&amp;token=6411c4e3-6c18-4d72-80cf-1f5461555255" alt=""><figcaption></figcaption></figure>

## Python compiled executable

If a executable was compiled with pyinstaller, we can extract the python compiled code and actually decompile it.

To extract use:

```
python pyinstxtractor.py <filename>
```

And to decompile use Uncompyle6

* Tip: use a python venv

```
uncompyle6 *compiled-python-file-pyc-or-pyo*
```
