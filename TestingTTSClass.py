from v02 import Transcribe
import time

tts = Transcribe()
tts.produce_transcript()
print("Timer")
time.sleep(35)
tts.end_transcript()