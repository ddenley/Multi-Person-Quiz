import STTV3

# Method to test if audio byte data streamed
def test_audio_stream():
    audio_stream = STTV3.MicrophoneStream()
    with audio_stream as stream:
        audio_generator = stream.generator()
        for content in audio_generator:
            print(content)
            print(len(content))

#test_audio_stream()

# Method to test transcription
def test_trans():
    trans = STTV3.Transcribe()
    trans.start_trans()

test_trans()