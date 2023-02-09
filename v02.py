from google.cloud import speech
from threading import Thread
import pyaudio
import os
from queue import Queue

# This class currently records conversation for a given time and then appends to a Queue for use
# In the future the class should in-real time transcribe speech and append to the Queue every conversation turn
class Transcribe:

    def __init__(self):
        pass

    # BOOLEAN FOR TESTING
    print_to_console = True

    active = True

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "zeta-buckeye-377214-7075b17aba9f.json"
    client = speech.SpeechClient()

    # Configuration for microphone
    CHANNELS = 1
    FRAME_RATE = 16000
    RECORD_SECONDS = 10
    AUDIO_FORMAT = pyaudio.paInt16
    SAMPLE_SIZE = 2
    CHUNK = 1024
    DEVICE_INDEX = 1

    # How frequently transcription takes place
    RETURN_FREQ = 15

    # Queue to hold each line of dialog
    dialog = Queue()

    recordings = Queue()

    # Configuration settings for Google STT
    diar_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=2
    )

    config = speech.RecognitionConfig(
        sample_rate_hertz=16000,
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # enable_automatic_punctuation=True,
        language_code='en-UK',
        diarization_config=diar_config
    )

    # Run this method to initiate conversation listening and transcription
    def produce_transcript(self):
        record = Thread(target=self.record_microphone)
        record.start()
        transcribe = Thread(target=self.transcribe)
        transcribe.start()
        if self.print_to_console:
            print_q = Thread(target=self.print_from_queue)
            print_q.start()

    # Method ran in thread that streams audio from microphone
    def record_microphone(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.AUDIO_FORMAT,
                        channels=self.CHANNELS,
                        rate=self.FRAME_RATE,
                        input=True,
                        input_device_index=self.DEVICE_INDEX,
                        frames_per_buffer=self.CHUNK)
        frames = []

        if self.print_to_console:
            print("RECORDING BEGINNING...")

        # While loop will keep thread open until active set to False
        while self.active:
            data = stream.read(self.CHUNK)
            frames.append(data)
            if len(frames) >= (self.FRAME_RATE * self.RECORD_SECONDS) / self.CHUNK:
                self.recordings.put(frames.copy())
                frames = []

        stream.stop_stream()
        stream.close()
        p.terminate()
        print("RECORDING ENDED")
        return

    # Method ran in thread that will incrementally add conversation to the dialog queue
    def transcribe(self):
        # While loop will keep thread open until active set to False
        while self.active:
            frames = self.recordings.get()
            frames_bytes = b''.join(frames)
            # Convert the bytes to an audio file for TTS API
            audio_file = speech.RecognitionAudio(content=frames_bytes)

            response = self.client.recognize(
                config=self.config,
                audio=audio_file
            )
            result = response.results[-1]
            words_info = result.alternatives[0].words
            current_speaker = 1
            current_line = ""
            conversation = []
            for word_info in words_info:
                word = word_info.word
                word_speaker = word_info.speaker_tag

                if current_speaker == word_speaker:
                    current_line += (word + " ")
                else:
                    conversation.append("{}: {}".format(current_speaker, current_line))
                    current_speaker = word_speaker

            conversation.append("{}: {}".format(current_speaker, current_line))
            self.dialog.put(conversation)
        print("TRANS ENDED")
        return

    def take_line_from_queue(self):
        print("TAKEN FROM Q")
        return self.dialog.get()

    # Method that will print from the queue to show the class is working
    def print_from_queue(self):
        while self.active:
            if not self.dialog.empty():
                print(self.take_line_from_queue())

    def end_transcript(self):
        self.active = False
