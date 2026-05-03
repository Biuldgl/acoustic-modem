import sounddevice as sd

# This just prints every audio device Python can find on your computer
# We used this at the start to figure out which device number was the mic
# and which one was the speaker so we could use them in the other scripts

print(sd.query_devices())