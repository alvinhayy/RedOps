---
title: "Sub-GHz RF"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/todo/radio-hacking/sub-ghz-rf.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Garage Doors

Garage-door remotes use several region- and product-specific sub-GHz allocations. Frequencies such as 300, 310, 315, 390, and 433.92 MHz are encountered, but there is no universal “300–190 MHz” garage-door band. Identify the target’s label, regulatory region, and observed signal before transmitting.[\[1\]](#references)

## Car Doors

Many car key fobs use **315 MHz or 433.92 MHz**, with regional rules and vehicle design influencing the choice. Frequency alone does not make 433 MHz longer-range than 315 MHz: transmit power, antenna efficiency, modulation, receiver sensitivity, propagation, and local regulations all matter. Europe commonly uses 433.92 MHz, while 315 MHz is common in North America and Japan.[\[1\]](#references)

## **Brute-force Attack**

**Brute-force Attack**

In the demonstrated fixed-code system, sending each code once instead of five times reduces the estimated time to six minutes:

Removing the 2 ms wait between signals reduces that demonstration to approximately three minutes.

Using a De Bruijn sequence to overlap candidate bit strings reduces the demonstrated attack to approximately eight seconds when the receiver accepts the continuous sequence without a required preamble or frame reset.[\[3\]](#references)

OpenSesame implements this attack against compatible fixed-code systems.[\[5\]](#references)

Requiring **a preamble will avoid the De Bruijn Sequence** optimization and **rolling codes will prevent this attack** (supposing the code is long enough to not be bruteforceable).

## Sub-GHz Attack

To attack these signals with Flipper Zero check:

## Rolling Codes Protection

Automatic garage door openers typically use a wireless remote control to open and close the garage door. The remote control **sends a radio frequency (RF) signal** to the garage door opener, which activates the motor to open or close the door.

It is possible for someone to use a device known as a code grabber to intercept the RF signal and record it for later use. This is known as a **replay attack**. To prevent this type of attack, many modern garage door openers use a more secure encryption method known as a **rolling code** system.

The **RF signal is typically transmitted using a rolling code**, which means that the code changes with each use. This makes it **difficult** for someone to **intercept** the signal and **use** it to gain **unauthorised** access to the garage.

In a rolling code system, the remote control and the garage door opener have a **shared algorithm** that **generates a new code** every time the remote is used. The garage door opener will only respond to the **correct code**, making it much more difficult for someone to gain unauthorised access to the garage just by capturing a code.

### **Missing Link Attack**

**Missing Link Attack**

Basically, you listen for the button and **capture the signal whilst the remote is out of range** of the device (say the car or garage). You then move to the device and **use the captured code to open it**.[\[2\]](#references)

### Full Link Jamming Attack

Caution

Intentional RF interference is illegal in many jurisdictions and can disrupt safety-relevant systems. Perform jamming tests only in a shielded, authorized laboratory and under the applicable radio regulations.[\[6\]](#references)

An attacker could **jam the signal near the vehicle or receiver** so the receiver cannot decode the code, capture the blocked transmission separately, stop jamming, and then replay the captured code.[\[2\]](#references)

The victim at some point will use the **keys to lock the car**, but then the attack will have **recorded enough “close door” codes** that hopefully could be resent to open the door (a **change of frequency might be needed** as there are cars that use the same codes to open and close but listens for both commands in different frequencies).

Warning

**Jamming works**, but it’s noticeable as if the **person locking the car simply tests the doors** to ensure they are locked they would notice the car unlocked. Additionally if they were aware of such attacks they could even listen to the fact that the doors never made the lock **sound** or the cars **lights** never flashed when they pressed the ‘lock’ button.

### **Code Grabbing Attack ( aka ‘RollJam’ )**

**Code Grabbing Attack ( aka ‘RollJam’ )**

This is a more **stealth Jamming technique**. The attacker will jam the signal, so when the victim tries to lock the door it won’t work, but the attacker will **record this code**. Then, the victim will **try to lock the car again** pressing the button and the car will **record this second code**.[\[2\]](#references)[\[4\]](#references)

Instantly after this the **attacker can send the first code** and the **car will lock** (victim will think the second press closed it). Then, the attacker will be able to **send the second stolen code to open** the car (supposing that a **“close car” code can also be used to open it**). A change of frequency might be needed (as there are cars that use the same codes to open and close but listens for both commands in different frequencies).

One RollJam implementation exploits receiver bandwidth: the jammer transmits near enough to the remote’s carrier to desensitize the vehicle’s wider receiver, while the attacker’s narrower receiver remains centered on the remote and can still record it. The exact offset and bandwidth depend on the target hardware.[\[2\]](#references)

Warning

Other implementations seen in specifications show that the **rolling code is a portion** of the total code sent. Ie the code sent is a **24 bit key** where the first **12 are the rolling code**, the **second 8 are the command** (such as lock or unlock) and the last 4 is the **checksum**. Vehicles implementing this type are also naturally susceptible as the attacker merely needs to replace the rolling code segment to be able to **use any rolling code on both frequencies**.

Caution

Note that if the victim sends a third code while the attacker is sending the first one, the first and second code will be invalidated.

### Alarm Sounding Jamming Attack

Testing against an aftermarket rolling code system installed on a car, **sending the same code twice** immediately **activated the alarm** and immobiliser providing a unique **denial of service** opportunity. Ironically the means of **disabling the alarm** and immobiliser was to **press** the **remote**, providing an attacker with the ability to **continually perform DoS attack**. Or mix this attack with the **previous one to obtain more codes** as the victim would like to stop the attack asap.[\[2\]](#references)

## References
