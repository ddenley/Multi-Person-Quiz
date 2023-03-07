import pyaudio
import wave

# Define recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 8192
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Create PyAudio object
audio = pyaudio.PyAudio()

# Open input stream and start recording
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("Recording started...")
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

# Stop recording and close input stream
print("Recording stopped.")
stream.stop_stream()
stream.close()

# Save recorded audio to file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Terminate PyAudio object
audio.terminate()
