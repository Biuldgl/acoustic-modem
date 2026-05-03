import sounddevice as sd
import numpy as np

# Device numbers we found using findmic.py

#These devices can be edited
INPUT_DEVICE = 1   # Microphone Array (Intel built-in mic, or my Microphone, this can be edited)
OUTPUT_DEVICE = 3  # Speakers (Realtek)

# This script just records 5 seconds of audio and plays it back
# We used it to confirm the mic and speakers were actually working
# before we started building the real transmission code

print("Recording for 5 seconds... say something!")
sample_rate = 44100
duration = 5

recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate,
                   channels=1, device=INPUT_DEVICE)
sd.wait()
print("Playing back...")

sd.play(recording, sample_rate, device=OUTPUT_DEVICE)
sd.wait()
print("Did you hear yourself?")
