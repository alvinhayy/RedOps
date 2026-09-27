---
title: "Radio"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/todo/hardware-hacking/radio.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## SigDigger

[**SigDigger**](https://github.com/BatchDrake/SigDigger) is a free digital-signal analyzer for GNU/Linux and macOS designed to extract information from unknown radio signals. It supports SDR devices through SoapySDR and provides real-time demodulation and analysis tools for FSK, PSK, ASK, analog video, bursty signals, and analog voice channels.[\[1\]](#references)

### Basic Config

After installing there are a few things that you could consider configuring.

In settings (the second tab button), select an **SDR device** or an input file, the frequency to tune, and the sample rate. A rate up to 2.56 Msps may be practical if the host supports it.

In the GUI behaviour it’s recommended to enable a few things if your PC support it:

If you realise that your PC is not capturing things try to disable OpenGL and lowering the sample rate.

### Uses

- Just to **capture some time of a signal and analyze it** just maintain the button “Push to capture” as long as you need.

- The **Tuner** of SigDigger helps to**capture better signals** (but it can also degrade them). Ideally start with 0 and keep**making it bigger until** you find the**noise** introduce is**bigger** than the**improvement of the signal** you need).

### Synchronize with radio channel

With [**SigDigger**](https://github.com/BatchDrake/SigDigger) synchronize with the channel you want to hear, configure “Baseband audio preview” option, configure the bandwith to get all the info being sent and then set the Tuner to the level before the noise is really starting to increase:[\[1\]](#references)

## Interesting tricks

- When a device is sending bursts of information, usually the **first part is going to be a preamble** so you**don’t** need to**worry** if you**don’t find information** in there**or if there are some errors** there.
- In frames of information you usually should **find different frames well aligned between them** :

- **After recovering the level transitions, you may need to decode them.** For Manchester encoding, one transition direction represents`0` and the opposite direction represents`1` ; the exact polarity depends on the convention in use.
- A preamble may contain a run of the same sampled level even when the payload uses Manchester encoding, so identify the frame boundary before decoding.

### Uncovering modulation type with IQ

There are 3 ways to store information in signals: Modulating the **amplitude**, **frequency** or **phase**.

If you are checking a signal there are different ways to try to figure out what is being used to store information (fin more ways below) but a good one is to check the IQ graph.

- **Detecting AM** : If in the IQ graph appears for example**2 circles** (probably one in 0 and other in a different amplitude), it could means that this is an AM signal. This is because in the IQ graph the distance between the 0 and the circle is the amplitude of the signal, so it’s easy to visualize different amplitudes being used.
- **Detecting PM** : Like in the previous image, if you find small circles not related between them it probably means that a phase modulation is used. This is because in the IQ graph, the angle between the point and the 0,0 is the phase of the signal, so that means that 4 different phases are used.
  - Note that if the information is hidden in the fact that a phase is changed and not in the phase itself, you won’t see different phases clearly differentiated.
- **Detecting FM** : IQ doesn’t have a field to identify frequencies (distance to centre is amplitude and angle is phase).
 Therefore, to identify FM, you should**only see basically a circle** in this graph.
Moreover, a frequency offset changes the rotation rate around the IQ circle. In SigDigger, a change in rotation speed or direction can therefore indicate FM.

## AM Example

### Uncovering AM

#### Checking the envelope

When inspecting AM data with [**SigDigger**](https://github.com/BatchDrake/SigDigger), the signal **envelope** can reveal distinct amplitude levels. The sample signal sends information as amplitude-modulated pulses; one pulse looks like this:[\[1\]](#references)

And this is how part of the symbol looks like with the waveform:

#### Checking the Histogram

You can **select the whole signal** where information is located, select **Amplitude** mode and **Selection** and click on **Histogram.** You can observer that 2 clear levels are only found

For example, if you select Frequency instead of Amplitude in this AM signal you find just 1 frequency (no way information modulated in frequency is just using 1 freq).

If you find a lot of frequencies potentially this won’t be a FM, probably the signal frequency was just modified because of the channel.

#### With IQ

In this example you can see how there is a **big circle** but also **a lot of points in the centre.**

### Get Symbol Rate

#### With one symbol

Select the smallest interval that clearly contains one symbol and check **Selection freq**. In this example it is 1.013 kHz, approximately 1 kHz.

#### With a group of symbols

You can also indicate the number of symbols you are going to select and SigDigger will calculate the frequency of 1 symbol (the more symbols selected the better probably). In this scenario I selected 10 symbols and the “Selection freq” is 1.004 Khz:

### Get Bits

After identifying AM and estimating the **symbol rate**, select the signal region, configure amplitude sampling and the decision levels, choose **Gardner clock recovery**, and press **Sample**:

- **Sync to selection intervals** means that if you previously selected intervals to find the symbol rate, that symbol rate will be used.
- **Manual** means that the indicated symbol rate is going to be used
- In **Fixed interval selection** you indicate the number of intervals that should be selected and it calculates the symbol rate from it
- **Gardner clock recovery** is a useful default, but it still needs an approximate symbol rate.

Pressing sample this appears:

Now, to make SigDigger understand **where is the range** of the level carrying information you need to click on the **lower level** and maintain clicked until the biggest level:

If there would have been for example **4 different levels of amplitude**, you should have need to configure the **Bits per symbol to 2** and select from the smallest to the biggest.

Finally **increasing** the **Zoom** and **changing the Row size** you can see the bits (and you can select all and copy to get all the bits):

If the signal has more than 1 bit per symbol (for example 2), SigDigger has **no way to know which symbol is** 00, 01, 10, 11, so it will use different **grey scales** the represent each (and if you copy the bits it will use **numbers from 0 to 3**, you will need to treat them).

For line encodings such as **Manchester**, translate each valid transition pair (`01` or `10`) into a data bit according to the convention used by the protocol.

## FM Example

### Uncovering FM

#### Checking the frequencies and waveform

Signal example sending information modulated in FM:

The spectrum clearly shows **two frequencies**, although they may be difficult to distinguish in the time-domain waveform:

This happens because the capture is centered between both frequencies, so their frequency offsets are approximately opposite:

If the synchronized frequency is **closer to one frequency than to the other** you can easily see the 2 different frequencies:

#### Checking the histogram

Checking the frequency histogram of the signal with information you can easily see 2 different signals:

In this case if you check the **Amplitude histogram** you will find **only one amplitude**, so it **cannot be AM** (if you find a lot of amplitudes it might be because the signal has been losing power along the channel):

And this is would be phase histogram (which makes very clear the signal is not modulated in phase):

#### With IQ

IQ doesn’t have a field to identify frequencies (distance to centre is amplitude and angle is phase).

Therefore, to identify FM, you should **only see basically a circle** in this graph.

Moreover, a frequency offset changes the rotation rate around the IQ circle. In SigDigger, a change in rotation speed or direction can therefore indicate FM:

### Get Symbol Rate

You can use the **same technique as the one used in the AM example** to get the symbol rate once you have found the frequencies carrying symbols.

### Get Bits

You can use the **same technique as the one used in the AM example** to get the bits once you have **found the signal is modulated in frequency** and the **symbol rate**.

## References
