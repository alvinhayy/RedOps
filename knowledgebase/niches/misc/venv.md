---
title: "venv"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/generic-methodologies-and-resources/python/venv.html
fetched_at: 2026-09-20T08:53:25Z
license: unspecified
category: misc
---

```
sudo apt-get install python3-venv
#Now, go to the folder you want to create the virtual environment
python3 -m venv <Dirname>
python3 -m venv pvenv #In this case the folder "pvenv" is going to be created
source <Dirname>/bin/activate
source pvenv/bin/activate #Activate the environment
#You can now install whatever python library you need
deactivate #To deactivate the virtual environment
```
```
error: invalid command 'bdist_wheel'
```
```
# Legacy workaround for older setuptools-based projects:
python3 -m pip install wheel
# Current build workflow:
python3 -m pip install build
python3 -m build --wheel
```
## References

- [1] [venv — Creation of virtual environments — Python 3.14 documentation](https://docs.python.org/3/library/venv.html)
- [2] [Package: python3-venv — Ubuntu Packages](https://packages.ubuntu.com/noble/python/python3-venv)
- [3] [wheel 0.24.0 — PyPI](https://pypi.org/project/wheel/0.24.0/)
- [4] [wheel — PyPI](https://pypi.org/project/wheel/)
- [5] [Is setup.py deprecated? — Python Packaging User Guide](https://packaging.python.org/en/latest/discussions/setup-py-deprecated/)
