import queue
import pyaudio
from google.cloud import speech
import os
from queue import Queue, Empty
import numpy as np

volume = 100

# This class will handle the stream of audio data to be transcribed
# Acts as a generator method
# REFERENCE OF CODE:
# The code for this class has been taken and adapted from the following documentation:
# https://cloud.google.com/speech-to-text/docs/transcribe-streaming-audio
# Set instance variable instance.closed = True to end when ready
class MicrophoneStream:

    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../google_api_credentials.json"
        self.rate = 16000
        #Potentiall alyter chuck size to reduce latency
        self.chunk = int(self.rate / 10)
        # self.chunk = 4800
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
        return None, pyaudio.paContinue

    def audio_datalist_set_volume(self, datalist):
        """ Change value of list of audio chunks 
        https://stackoverflow.com/questions/36664121/modify-volume-while-streaming-with-pyaudio"""
        global volume
        for i in range(len(datalist)):
            chunk = np.fromstring(datalist[i], np.int16)
            chunk = chunk * volume
            datalist[i] = chunk.astype(np.int16)

    # Yields the audio data as bytes for later use in the API calls
    def generator(self):
        global volume
        # Keep yielding until instance is closed via instance.close = True
        while not self.closed:
            data = []
            data_chunk = self.buffer.get()
            # If chunk is none end iteration of the generator
            if data_chunk is None:
                return
            if volume == 0:
                data_chunk *= 0
            data.append(data_chunk)
            # Consume from the buffer any data left
            while True:
                try:
                    data_chunk = self.buffer.get(block=False)
                    if data_chunk is None:
                        return
                    if volume == 0:
                        data_chunk *= 0
                    data.append(data_chunk)
                except queue.Empty:
                    break
            yield b"".join(data)


# Code partially adapted from documentation:
# https://cloud.google.com/speech-to-text/docs/transcribe-streaming-audio
class Transcribe:

    def __init__(self):

        lines = []
        with open("stt/phrases.txt") as file:
            lines = [line.rstrip() for line in file]
        phrase_list = lines

        self.transcription_queue = Queue()
        self.language_code = 'en-US'
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
        diarization_config=self.diar_config,
        speech_contexts=[
            speech.SpeechContext(dict(
                phrases=phrase_list
            ))
        ]
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config, interim_results=False
        )
        self.dialogue = Queue()
        # Could be refactored - use in creation of client instead
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../google_api_credentials.json"

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
            self.alternative_method(responses)

    def print_responses_testing(self, api_responses):
        prev_dialog_len = 0

        for response in api_responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue
            if not result.is_final:
                pass

            else:
                dialog = []
                for word_info in result.alternatives[0].words:
                    dialog.append([word_info.word, word_info.speaker_tag])
                dialog = dialog[prev_dialog_len:]
                prev_dialog_len = prev_dialog_len + len(dialog)
                print(dialog)
                # self.transcription_queue.put(dialog)
                # Implementing turn logic for queue
                previous_speaker = None
                current_speaker = None
                first_word = True
                turn_string = ""
                word_index = 1
                for word_speaker in dialog:
                    current_speaker = word_speaker[1]
                    word = word_speaker[0]
                    if first_word:
                        previous_speaker = current_speaker
                        first_word = False
                    if previous_speaker == current_speaker:
                        turn_string = turn_string + word + " "
                    elif previous_speaker != current_speaker:
                        self.transcription_queue.put({
                            "text": turn_string,
                            "player": previous_speaker
                        })
                        # print("Appended :" + str(previous_speaker) + turn_string)
                        turn_string = word + " "
                        previous_speaker = current_speaker
                    if word_index == len(dialog):
                        self.transcription_queue.put({
                            "text": turn_string,
                            "player": current_speaker
                        })
                        # print("Appended :" + str(current_speaker) + turn_string)
                    word_index += 1

    def get_from_queue(self):
        try:
           contents = self.transcription_queue.get(block=False)
        except Empty:
            contents = None
        return contents

    def mute_mic(self, vol=0):
        global volume
        volume = vol
