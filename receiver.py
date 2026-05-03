import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import welch

# These settings must match the sender exactly
# Both sides need to agree on the same frequencies and timing

BIT_DURATION = 0.1  # how long each bit tone lasts (same as sender)
FREQ_0 = 1000  # frequency that means binary 0
FREQ_1 = 2000  # frequency that means binary 1
FREQ_START = 500   # the starting preamble tone to look for
TOLERANCE = 80   # how close a detected frequency needs to be to count as a match for example if we detect 1050 Hz we still count it as 1000 Hz
INPUT_FILE = "transmission.wav"  # the audio file to read from


# This function figures out what the main frequency is in a small chunk of audio
# It uses a math technique called Welch power spectral density
# Think of it like asking "what note is this?" for a short audio clip
def get_dominant_frequency(samples, sample_rate):
    freqs, power = welch(samples, sample_rate, nperseg=len(samples))
    return freqs[np.argmax(power)]



# This function takes a list of 1s and 0s and converts them back to text
# Every 8 bits becomes one character using ASCII
def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(''.join(str(b) for b in byte), 2)))
    return ''.join(chars)



# Same checksum function as the sender
# We use this to verify the message after decoding

def compute_checksum(text):
    return sum(ord(c) for c in text) % 256



# This is the main function that reads the audio file and decodes the message

def receive_message():
    print(f"Reading {INPUT_FILE}...")

    # Load the WAV file
    sample_rate, data = wav.read(INPUT_FILE)

    # Convert the audio data to floating point numbers between -1 and 1
    samples = data.astype(np.float32) / 32767.0

    # Figure out how many audio samples fit in one bit duration
    samples_per_bit = int(sample_rate * BIT_DURATION)

    print("Scanning for preamble...")
    preamble_found = False
    start_index = 0


    # Go through the audio chunk by chunk looking for the 500 Hz preamble tone
    # Once we find it we know the message is about to start
    
    for i in range(0, len(samples) - samples_per_bit, samples_per_bit):
        chunk = samples[i:i + samples_per_bit]
        freq = get_dominant_frequency(chunk, sample_rate)
        if abs(freq - FREQ_START) < TOLERANCE:
            print("Preamble found! Decoding message...")
            preamble_found = True
            start_index = i + samples_per_bit
            break



    if not preamble_found:
        print("No preamble found in file.")
        return

    bits = []
    silence_count = 0
    i = start_index

    # Now read each chunk after the preamble and figure out if it is a 0 or a 1
    # If we get 5 chunks in a row that don't match either frequency, we consider the message done
    while i + samples_per_bit <= len(samples) and silence_count < 5:
        chunk = samples[i:i + samples_per_bit]
        freq = get_dominant_frequency(chunk, sample_rate)

        if abs(freq - FREQ_1) < TOLERANCE:
            bits.append(1)
            silence_count = 0
        elif abs(freq - FREQ_0) < TOLERANCE:
            bits.append(0)
            silence_count = 0
        else:
            silence_count += 1

        i += samples_per_bit

    # Convert all the bits back into text
    full_text = bits_to_text(bits)

    if len(full_text) < 2:
        print("Message too short to verify.")
        return


    # The last character is the checksum, everything before it is the actual message
    
    received_text = full_text[:-1]
    received_checksum = ord(full_text[-1])
    computed_checksum = compute_checksum(received_text)

    print(f"Bits received: {''.join(str(b) for b in bits)}")
    print(f"Message decoded: '{received_text}'")
    print(f"Checksum received: {received_checksum}")
    print(f"Checksum computed: {computed_checksum}")


    # Compare the two checksums to verify the message arrived correctly
    
    if received_checksum == computed_checksum:
        print("✓ Transmission verified! Message arrived intact.")
    else:
        print("✗ Warning: Checksum mismatch! Possible corruption detected.")


receive_message()