import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav

# These are the settings for the whole project

SAMPLE_RATE = 44100 # (CD quality)
OUTPUT_DEVICE = 4   # which speaker to use
BIT_DURATION = 0.1 # how long each tone plays
FREQ_0 = 1000 # the sound frequency we use to mean binary 0 (1000 Hz), but this one can be changed
FREQ_1 = 2000 # the sound frequency we use to mean binary 1 (2000 Hz)
FREQ_START = 500  # a special tone we play at the start so the receiver knows the message is beginning
PREAMBLE_DURATION = 0.5 # how long we play that starting tone (half a second)
OUTPUT_FILE = "transmission.wav" # the name of the audio file we save


# This function builds a single tone (a pure sound at one frequency)

def make_tone(frequency, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    return 0.5 * np.sin(2 * np.pi * frequency * t)



# This function converts text into a list of 1s and 0s (binary)
# Every character in the message becomes 8 bits based on its ASCII value
# For example the letter H is 72 in ASCII which is 01001000 in binary

def text_to_bits(text):
    bits = []
    for char in text:
        ascii_val = ord(char)
        for i in range(7, -1, -1):
            bits.append((ascii_val >> i) & 1)
    return bits



# This function computes a checksum for the message
# It adds up the ASCII value of every character and takes the remainder when divided by 256
# This gives us a single number that represents the whole message
# The receiver will compute the same number and compare, if they match the message is intact

def compute_checksum(text):
    return sum(ord(c) for c in text) % 256


# This is the main function that puts everything together and sends the message
def send_message(text):

    # First compute the checksum and attach it to the end of the message
    checksum = compute_checksum(text)
    full_message = text + chr(checksum)


    print(f"Sending: '{text}'")
    print(f"Checksum: {checksum}")


    # Convert the full message (including checksum) to bits

    bits = text_to_bits(full_message)
    print(f"Bits: {''.join(str(b) for b in bits)}")


    # Start building the audio with the preamble tone (500 Hz)
    # This is like saying "hey receiver, a message is coming!"
    audio = make_tone(FREQ_START, PREAMBLE_DURATION)


    # For each bit, add either a 2000 Hz tone (for 1) or a 1000 Hz tone (for 0)

    for bit in bits:
        freq = FREQ_1 if bit == 1 else FREQ_0
        audio = np.concatenate([audio, make_tone(freq, BIT_DURATION)])


    # Save the audio to a WAV file so the receiver can read it

    audio_int16 = (audio * 32767).astype(np.int16)
    wav.write(OUTPUT_FILE, SAMPLE_RATE, audio_int16)
    print(f"Saved to {OUTPUT_FILE}")


    # Also play the tones through the speakers so you can hear the transmission

    print("Playing tones through speakers...")
    sd.play(audio, SAMPLE_RATE, device=OUTPUT_DEVICE)
    sd.wait()
    print("Done! Run receiver.py now.")



# Ask the user to type a message and send it

message = input("Type a message to send: ")
send_message(message)