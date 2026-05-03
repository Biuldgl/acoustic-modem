import numpy as np
import sounddevice as sd
from scipy.signal import welch
import time

SAMPLE_RATE = 44100
INPUT_DEVICE = 1  # the microphone we were testing with

# This script was built specifically to debug why the live mic wasn't working
# It gives you 10 seconds to switch to the sender window and start playing tones
# Then it records and tells you what frequencies it actually heard and how loud they were
# If the power values come back as 0.000000 it means the mic heard nothing useful

print("Starting in 10 seconds... switch to sender window and get ready!")
time.sleep(10)
print("Recording now for 10 seconds... run sender.py!")

recording = sd.rec(int(SAMPLE_RATE * 5), samplerate=SAMPLE_RATE,
                   channels=1, device=INPUT_DEVICE)
sd.wait()

samples = recording[:, 0]

# Welch method breaks the audio into frequency components and measures each one's strength

freqs, power = welch(samples, SAMPLE_RATE, nperseg=4096)


# Show the top 5 strongest frequencies detected

top5 = np.argsort(power)[-5:][::-1]
print("\nTop frequencies detected:")
for i in top5:
    print(f"  {freqs[i]:.1f} Hz — power: {power[i]:.6f}")