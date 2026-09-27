---
title: "Audio"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/stego/audio/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

## Quick triage

Before specialized tooling:

- Confirm codec/container details and anomalies:
  - `file audio`
  - `ffmpeg -v info -i audio -f null -`
- If the audio contains noise-like content or tonal structure, inspect a spectrogram early.

```
ffmpeg -v info -i stego.mp3 -f null -
```
## Spectrogram steganography

### Technique

Spectrogram stego hides data by shaping energy over time/frequency so it becomes visible in a time-frequency plot, while the audio may sound like tones or noise.[\[3\]](#references)

### Sonic Visualiser

Primary tool for spectrogram inspection:

### Alternatives

- Audacity (spectrogram view and filters).<sup>[\[6\]](#references)</sup>
- `sox` can generate spectrograms from the CLI:

```
sox input.wav -n spectrogram -o spectrogram.png
```
## FSK / modem decoding

Frequency-shift keyed audio often looks like alternating single tones in a spectrogram. Once you have a rough center/shift and baud estimate, brute force with `minimodem`:[\[1\]](#references)

```
# Visualize the band to pick baud/frequency
sox noise.wav -n spectrogram -o spec.png
# Try common bauds until printable text appears
minimodem -f noise.wav 45
minimodem -f noise.wav 300
minimodem -f noise.wav 1200
minimodem -f noise.wav 2400
```
`minimodem` supports Bell and other FSK modes plus custom mark/space frequencies; consult its options rather than assuming every recording can be autodetected. Try `--rx-invert`, an explicit baud mode, or `--samplerate <Hz>` when output is garbled.[\[4\]](#references)

## WAV LSB

### Technique

For uncompressed PCM (WAV), each sample is an integer. Modifying low bits changes the waveform very slightly, so attackers can hide:

- 1 bit per sample (or more)
- Interleaved across channels
- With a stride/permutation

Other audio-hiding families you may encounter:

- Phase coding
- Echo hiding
- Spread-spectrum embedding
- Codec-side channels (format-dependent and tool-dependent)

### WavSteg

The following commands use WavSteg from the `ragibson/Steganography` toolkit.[\[2\]](#references)

```
python3 WavSteg.py -r -b 1 -s sound.wav -o out.bin
python3 WavSteg.py -r -b 2 -s sound.wav -o out.bin
```
### DeepSound

- DeepSound’s official repository and releases.<sup>[\[7\]](#references)</sup>

## DTMF / dial tones

### Technique

DTMF represents each keypad signal using one frequency from a low group and one from a high group. If the audio resembles keypad tones or regular dual-frequency beeps, test DTMF decoding early.[\[5\]](#references)

Online decoders:

## References

- [1] [Flagvent 2025 (Medium) — pink, Santa’s Wishlist, Christmas Metadata, Captured Noise](https://0xdf.gitlab.io/flagvent2025/medium)
- [2] [ragibson/Steganography](https://github.com/ragibson/Steganography#WavSteg)
- [3] [Sonic Visualiser — documentation](https://www.sonicvisualiser.org/documentation.html)
- [4] [kamalmostafa/minimodem — command-line FSK modem](https://github.com/kamalmostafa/minimodem)
- [5] [ITU-T Recommendation Q.23 — technical features of push-button telephone sets](https://www.itu.int/rec/T-REC-Q.23/en)
- [6] [Audacity](https://www.audacityteam.org/)
- [7] [Jpinsoft/DeepSound — official repository and releases](https://github.com/Jpinsoft/DeepSound)
- [8] [`dtmf-detect`](https://unframework.github.io/dtmf-detect/)
- [9] [ribt/dtmf-decoder](https://github.com/ribt/dtmf-decoder)
