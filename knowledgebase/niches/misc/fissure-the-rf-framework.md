---
title: "FISSURE - The RF Framework"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/todo/radio-hacking/fissure-the-rf-framework.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Getting Started

**Supported**

Current FISSURE uses the **`Python3`** branch for active development with PyQt5 and GNU Radio 3.8 or 3.10. The deprecated **`Python2_maint-3.7`** branch remains available for older operating systems and third-party tools that require GNU Radio 3.7. The former `Python3_maint-3.8` and `Python3_maint-3.10` branch names are historical; GNU Radio maintenance selection is now handled from the `Python3` branch.[\[1\]](#references)[\[3\]](#references)

| Operating System | FISSURE Branch | Default GNU Radio branch |
|---|---|---|
| DragonOS Noble (24.04) | Python3 | maint-3.10 |
| Kali | Python3 | maint-3.10 |
| Raspberry Pi OS | Python3 | maint-3.10 |
| Ubuntu 18.04 | Python2_maint-3.7 | maint-3.7 |
| Ubuntu 20.04 | Python3 | maint-3.8 |
| Ubuntu 22.04 | Python3 | maint-3.10 |
| Ubuntu 24.04 / Ubuntu ARM | Python3 | maint-3.10 |
| Windows 11 WSL2 | use a supported Linux version | use the matching version |

**In-Progress (beta)**

These operating systems are still in beta status. They are under development and several features are known to be missing. Items in the installer might conflict with existing programs or fail to install until the status is removed.

| Operating System | FISSURE Branch | Default GNU Radio branch |
|---|---|---|
| BackBox Linux | Python3 | maint-3.10 |
| KDE neon | Python3 | maint-3.10 |
| Parrot Security 6.1 | Python3 | maint-3.10 |

Certain third-party tools do not work on every OS. Check the current [Known Conflicts and Third-Party Software](https://fissure.readthedocs.io/en/latest/pages/installation.html#known-conflicts) documentation before installing.[\[3\]](#references)

**Installation**

```
git clone https://github.com/ainfosec/FISSURE.git
cd FISSURE
git checkout Python3  # optional; use Python2_maint-3.7 only for legacy requirements
git submodule update --init
./install
```
The submodule step downloads the GNU Radio out-of-tree modules used by FISSURE and is required when installing those modules. The installer will also install missing PyQt dependencies needed to launch its installation GUIs.[\[3\]](#references)

Next, select the option that best matches your operating system (should be detected automatically if your OS matches an option).

| Python2_maint-3.7 | Python3_maint-3.8 | Python3_maint-3.10 |
|---|---|---|

It is recommended to install FISSURE on a clean operating system to avoid existing conflicts. Select all the recommended checkboxes (Default button) to avoid errors while operating the various tools within FISSURE. There will be multiple prompts throughout the installation, mostly asking for elevated permissions and user names. If an item contains a “Verify” section at the end, the installer will run the command that follows and highlight the checkbox item green or red depending on if any errors are produced by the command. Checked items without a “Verify” section will remain black following the installation.

**Usage**

Open a terminal and enter:

```
fissure
```
Refer to the FISSURE Help menu for more details on usage.

## Details

**Components**

- Dashboard
- Central Hub (HIPRFISR)
- Target Signal Identification (TSI)
- Protocol Discovery (PD)
- Flow Graph & Script Executor (FGE)

**Capabilities**

| ***Signal Detector*** | ***IQ Manipulation*** | ***Signal Lookup*** | ***Pattern Recognition*** |
|---|---|---|---|
| ***Attacks*** | ***Fuzzing*** | ***Signal Playlists*** | ***Image Gallery*** |
| ***Packet Crafting*** | ***Scapy Integration*** | ***CRC Calculator*** | ***Logging*** |

**Hardware**

The following hardware has varying levels of integration in FISSURE:[\[1\]](#references)[\[3\]](#references)

- USRP: X3xx, B2xx, B20xmini, USRP2, N2xx, X410
- HackRF
- RTL2832U
- 802.11 Adapters
- LimeSDR
- bladeRF, bladeRF 2.0 micro
- Open Sniffer
- PlutoSDR
- SDRplay: RSPduo, RSPdx, RSPdx R2

## Lessons

FISSURE comes with several helpful guides to become familiar with different technologies and techniques. Many include steps for using various tools that are integrated into FISSURE.

## Roadmap

- Add more hardware types, RF protocols, signal parameters, analysis tools
- Support more operating systems
- Develop class material around FISSURE (RF Attacks, Wi-Fi, GNU Radio, PyQt, etc.)
- Create a signal conditioner, feature extractor, and signal classifier with selectable AI/ML techniques
- Implement recursive demodulation mechanisms for producing a bitstream from unknown signals
- Transition the main FISSURE components to a generic sensor node deployment scheme

## Contributing

Suggestions for improving FISSURE are strongly encouraged. Leave a comment in the [Discussions](https://github.com/ainfosec/FISSURE/discussions) page or in the Discord Server if you have any thoughts regarding the following:

- New feature suggestions and design changes
- Software tools with installation steps
- New lessons or additional material for existing lessons
- RF protocols of interest
- More hardware and SDR types for integration
- IQ analysis scripts in Python
- Installation corrections and improvements

Contributions to improve FISSURE are crucial to expediting its development. Any contributions you make are greatly appreciated. If you wish to contribute through code development, please fork the repo and create a pull request:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature` )
3. Commit your changes (`git commit -m 'Add some AmazingFeature'` )
4. Push to the branch (`git push origin feature/AmazingFeature` )
5. Open a pull request

Creating [Issues](https://github.com/ainfosec/FISSURE/issues) to bring attention to bugs is also welcomed.

## Collaborating

Contact Assured Information Security, Inc. (AIS) Business Development to propose and formalize any FISSURE collaboration opportunities–whether that is through dedicating time towards integrating your software, having the talented people at AIS develop solutions for your technical challenges, or integrating FISSURE into other platforms/applications.

## License

GPL-3.0

For license details, see LICENSE file.

## Contact

Join the Discord Server: [https://discord.gg/JZDs5sgxcG](https://discord.gg/JZDs5sgxcG)

Follow on Twitter: [@FissureRF](https://twitter.com/fissurerf), [@AinfoSec](https://twitter.com/ainfosec)

Chris Poore - Assured Information Security, Inc. - poorec@ainfosec.com

Business Development - Assured Information Security, Inc. - bd@ainfosec.com

## Credits

We acknowledge and are grateful to these developers:

## Acknowledgments

Special thanks to Dr. Samuel Mantravadi and Joseph Reith for their contributions to this project.

## References

- [1] [FISSURE - The RF Framework (GitHub)](https://github.com/ainfosec/FISSURE)
- [2] [FISSURE Paper (GRCon22)](https://events.gnuradio.org/event/18/contributions/246/attachments/84/167/FISSURE_Paper_Poore_GRCon22.pdf)
- [3] [FISSURE documentation - Installation](https://fissure.readthedocs.io/en/latest/pages/installation.html)
