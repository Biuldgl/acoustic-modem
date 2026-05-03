# Acoustic Modem - Transmit Data over Sound

A Python implementation of an acoustic modem that transmits text messages using sound frequencies (FSK modulation) and decodes them back into the original text. Built as a Final Project for a Computer Networks course to demonstrate Physical Layer concepts.

**Authors:** Biuld Gonzalez-Lopez & Andres Cazares
**Course:** Computer Networks CSCI-4345
**Date:** May 2026

---

## How It Works

The sender converts a text message into binary bits and plays each bit as a distinct audio tone:
- **500 Hz** - Is the start of transmission
- **1000 Hz** - binary 0
- **2000 Hz** - binary 1

The receiver analyzes the audio, detects which tones are present, reconstructs the bits, and decodes them back into text. A checksum is included to verify the message arrived without corruption.

---

## Project Files

| File | Description |
|------|-------------|
| `sender.py` | Main transmitter. Converts text to tones, saves to WAV, plays through speakers |
| `receiver.py` | Main decoder. Reads WAV file, detects frequencies, reconstructs message, verifies checksum |
| `findmic.py` | Development tool. Lists all available audio devices on the system |
| `test_audio.py` | Development tool. Records 5 seconds and plays back to verify mic and speakers work |
| `diagnose.py` | Development tool. Records audio and prints dominant frequencies with power levels, which used to debug the live microphone issue |
| `transmission.wav` | Generated automatically by sender.py, contains the encoded audio signal |

---

## Requirements

- Python 3.12+
- numpy
- sounddevice
- scipy

Install all dependencies with:

```
pip install numpy sounddevice scipy
```

---

## How to Run

**Step 1 - Run the sender:**
```
python sender.py
```
Type your message when prompted. The script will encode it as tones, save to `transmission.wav`, and play it through your speakers.

**Step 2 - Run the receiver:**
```
python receiver.py
```
The receiver reads `transmission.wav`, decodes the message, and verifies the checksum.

---

## Example Output

**Sender:**
```
Type a message to send: Hello, World!!!
Sending: 'Hello, World!!!'
Checksum: 162
Bits: 0100100001100101...
Saved to transmission.wav
Playing tones through speakers...
Done! Run receiver.py now.
```

**Receiver:**
```
Reading transmission.wav...
Scanning for preamble...
Preamble found! Decoding message...
Bits received: 0100100001100101...
Message decoded: 'Hello, World!!!'
Checksum received: 162
Checksum computed: 162
✓ Transmission verified! Message arrived intact.
```

---

## Signal Design

| Parameter | Value |
|-----------|-------|
| Sample Rate | 44100 Hz |
| Bit Duration | 0.1 seconds |
| Preamble Frequency | 500 Hz |
| Frequency for 0 | 1000 Hz |
| Frequency for 1 | 2000 Hz |
| Frequency Tolerance | ±80 Hz |
| Modulation Scheme | FSK (Frequency Shift Keying) |
| Checksum | ASCII sum mod 256 |

---

## Notes

The original design used a live microphone to capture tones in real time. During testing the microphone was not picking up the speaker tones clearly enough, with power levels returning as 0.000000 across all frequencies. The design was revised so the sender saves the audio to a WAV file and the receiver reads from that file directly. The full encoding and decoding pipeline stayed identical, only the audio source changed. The sender still plays the tones audibly through the speakers during every transmission.
