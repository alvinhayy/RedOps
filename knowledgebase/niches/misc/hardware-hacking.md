---
title: "Hardware Hacking"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/todo/hardware-hacking/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## JTAG

JTAG (IEEE 1149.1) supports boundary-scan testing through cells placed around a device’s I/O pins. Many processors also expose vendor-specific debug functions through the same Test Access Port (TAP); boundary scan and CPU debugging are related uses of JTAG, not synonyms.[\[1\]](#references)

The JTAG standard defines **specific commands for conducting boundary scans**, including the following:

- **BYPASS** selects a one-bit bypass register so other devices in a scan chain can be reached with minimal overhead.
- **SAMPLE/PRELOAD** captures pin values during normal operation and can preload the boundary-scan register before another instruction.
- **EXTEST** sets and reads pin states.

It can also support other commands such as:

- **IDCODE** for identifying a device
- **INTEST** for the internal testing of the device

You might come across these instructions when you use a tool like the JTAGulator.

### The Test Access Port

The **Test Access Port (TAP)** provides access to a component’s JTAG test logic. Four signals are required and `TRST` is optional:[\[1\]](#references)

- Test clock input (**TCK** ) The TCK is the**clock** that defines how often the TAP controller will take a single action (in other words, jump to the next state in the state machine).
- Test mode select (**TMS** ) input TMS controls the**finite state machine** . On each beat of the clock, the device’s JTAG TAP controller checks the voltage on the TMS pin. If the voltage is below a certain threshold, the signal is considered low and interpreted as 0, whereas if the voltage is above a certain threshold, the signal is considered high and interpreted as 1.
- Test data input (**TDI** ) shifts serial instruction or test data into the selected TAP register. IEEE 1149.1 defines the TAP transfer behavior, while vendors define optional instructions and debug registers.
- Test data output (**TDO** ) TDO is the pin that sends**data out of the chip** .
- Test reset (**TRST** ) input The optional TRST resets the finite state machine**to a known good state** . Alternatively, if the TMS is held at 1 for five consecutive clock cycles, it invokes a reset, the same way the TRST pin would, which is why TRST is optional.

Sometimes you will be able to find those pins marked in the PCB. In other occasions you might need to **find them**.

### Identifying JTAG pins

A fast, purpose-built—but comparatively expensive—option for detecting JTAG ports is the **JTAGulator**, which can also identify UART pinouts.[\[2\]](#references)

It has **24 channels** that can be connected to board test points. It enumerates candidate pin combinations using **IDCODE** and **BYPASS** scans and reports the channels corresponding to the detected JTAG signals.

A cheaper but much slower way of identifying JTAG pinouts is by using the [**JTAGenum**](https://github.com/cyphunk/JTAGenum/) loaded on an Arduino-compatible microcontroller.

With **JTAGenum**, first define the probing microcontroller pins used for enumeration. Consult its pinout, then connect those pins to candidate test points on the target board.[\[3\]](#references)

A **third way** to identify JTAG pins is by **inspecting the PCB** for a known footprint. Some boards expose a **Tag-Connect** footprint, although Tag-Connect is a connector system that can carry JTAG, SWD, UART, or another interface—it is not proof by itself that the pins are JTAG. Component datasheets and continuity measurements can then identify the actual signals.[\[5\]](#references)

## SDW

SWD is Arm’s two-pin, packet-based debug interface.[\[4\]](#references)

The interface uses bidirectional **SWDIO** for data and **SWCLK** for the clock. Many devices implement a **Serial Wire/JTAG Debug Port (SWJ-DP)** that permits selection between SWD and JTAG on shared pins.[\[4\]](#references)

## References
