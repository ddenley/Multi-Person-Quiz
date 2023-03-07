import requests
from typing import Tuple

__hostname = "127.0.0.1"
__tts_port = 5004

def stt_get() -> Tuple[str, int, int]:
    """Requests a diarized conversation turn from the stt_tts module."""
    response = requests.get(f"http://{__hostname}:{__tts_port}/incoming_speech")
    if response.status_code == 200:
        text = response.json()['text']
        speaker = response.json()['player']
    elif response.status_code == 401:
        print("Handle the error")
        text = "401 Error"
        speaker = 0
    else:
        text = "Unknown Error"
        speaker = 0

    return text, speaker, response.status_code

while True:
    user_input = input("Any key to send get request")
    print(stt_get())