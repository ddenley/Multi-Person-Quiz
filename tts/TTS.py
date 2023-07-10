import io

from google.cloud import texttospeech
import os
import wave
import pyaudio


def speech_to_text(text):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_api_credentials.json"

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-UK", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    decoded = response.audio_content

    wav_stream = io.BytesIO(decoded)
    wav_file = wave.open(wav_stream, 'rb')
    audio = pyaudio.PyAudio()

    stream = audio.open(format=audio.get_format_from_width(wav_file.getsampwidth()),
                        channels=wav_file.getnchannels(),
                        rate=wav_file.getframerate(),
                        output=True)

    data = wav_file.readframes(1024)
    while data:
        stream.write(data)
        data = wav_file.readframes(1024)

    stream.close()
    audio.terminate()
