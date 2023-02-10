import queue

import pyaudio
from google.cloud import speech
import os
from queue import Queue


# This class will handle the stream of audio data to be transcribed
# Acts as a generator method
# REFERENCE OF CODE:
# The code for this class has been taken and adapted from the following documentation:
# https://cloud.google.com/speech-to-text/docs/transcribe-streaming-audio
# Set instance variable instance.closed = True to end when ready
class MicrophoneStream:

    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "zeta-buckeye-377214-7075b17aba9f.json"
        self.rate = 16000
        self.chunk = int(self.rate / 10)
        self.buffer = Queue()
        self.closed = True
        # ***** CHANGE THIS VARIABLE DEPENDING ON DEVICE
        self.device_index = 1
        self.audio_format = pyaudio.paInt16

    # Interesting documentation on how the __enter__ and __exit__ methods work:
    # https://peps.python.org/pep-0343/
    # Enter method must return self
    # Will open connections required on call of with
    def __enter__(self):
        # Create an instance var of the audio interface and stream to later close on __exit__
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
            format=self.audio_format,
            # API only supports one channel
            channels=1,
            rate=self.rate,
            frames_per_buffer=self.chunk,
            stream_callback=self.stream_callback,
            input_device_index=self.device_index,
            input=True
        )
        self.closed = False
        return self


    # Clean down code when with statement goes out of scope - closes connections
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.closed = True
        # Place a none into buffer so that generator is indicated to stop iteration
        # i.e. This is the end of the audio stream
        # Causes the generator to terminate so that streaming_recognize does not block process termination
        self.buffer.put(None)
        self.audio_interface.terminate()

    # Callback for the pyaudio stream
    # Allows asynchronous filling of the buffer object
    # Documentation for callback here:
    # https://people.csail.mit.edu/hubert/pyaudio/docs/#example-callback-mode-audio-i-o
    def stream_callback(self, in_data, *args, **kwargs):
        self.buffer.put(in_data)
        # Return out data and port audio callback flag return code
        return (None, pyaudio.paContinue)

    # Yields the audio data as bytes for later use in the API calls
    def generator(self):
        # Keep yielding until instance is closed via instance.close = True
        while not self.closed:
            data = []
            data_chunk = self.buffer.get()
            # If chunk is none end iteration of the generator
            if data_chunk is None:
                return
            data.append(data_chunk)
            # Consume from the buffer any data left
            while True:
                try:
                    data_chunk = self.buffer.get(block=False)
                    if data_chunk is None:
                        return
                    data.append(data_chunk)
                except queue.Empty:
                    break
            yield b"".join(data)


# Code partially adapted from documentation:
# https://cloud.google.com/speech-to-text/docs/transcribe-streaming-audio
class Transcribe:

    def __init__(self):
        self.language_code = 'en-UK'
        self.rate = 16000
        self.diar_config = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=2,
            max_speaker_count=2
        )
        self.config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=self.rate,
        language_code=self.language_code,
        diarization_config=self.diar_config
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config, interim_results=True
        )
        self.dialogue = Queue()
        # Could be refactored - use in creation of client instead
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "zeta-buckeye-377214-7075b17aba9f.json"

    def start_trans(self):
        audio_stream = MicrophoneStream()
        client = speech.SpeechClient()
        with audio_stream as stream:
            audio_generator = stream.generator()
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )
            responses = client.streaming_recognize(self.streaming_config, requests)
            self.print_responses_testing(responses)

    def print_responses_testing(self, api_responses):
        current_speaker = 1
        dialog = Queue()
        for response in api_responses:
            #If no results continue
            if not response.results:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue
            speaker_sentence = ""
            dialog = []
            last_speaker = 1
            last_sentence = ""
            for word_info in result.alternatives[0].words:
                if current_speaker == word_info.speaker_tag:
                    speaker_sentence = speaker_sentence + " " + word_info.word
                # Speaker has changed - add dialogue to speakers containers
                else:
                    if speaker_sentence != "":
                        dialog.append("{}: {}".format(word_info.speaker_tag, speaker_sentence))
                    current_speaker = word_info.speaker_tag
                    speaker_sentence = ""
                last_speaker = word_info.speaker_tag
                last_sentence = speaker_sentence

            # Also add the last sentence on finalisation of response
            if last_sentence != "":
                dialog.append("{}: {}".format(last_speaker, last_sentence))

            for item in dialog:
                print(item)












