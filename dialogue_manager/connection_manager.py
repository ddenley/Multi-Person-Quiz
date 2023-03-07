# Author:   Andy Edmondson
# Date:     16 Feb 2023
# Purpose:  Provide functions for communication to the Flask and Rasa servers.
#
# Contains: tts_post        - POST for tts Flask API
#           stt_get         - GET for stt_tts Flask API
#           rasa_nlu_post   - POST for Rasa NLU module HTTP API
#           gui_post        - POST for GUI Flask API
import json

import requests
from typing import Tuple


# Variables required for the connections
__hostname = "127.0.0.1"
__tts_port = 5004
__stt_port = 5001
__gui_port = 5006
__rasa_port = 5005


def tts_post(message: str) -> int:
    """Sends a message to the text to speech server and returns the response code as an int."""
    response = requests.post(url=f"http://{__hostname}:{__tts_port}/tts", json={'text': message})
    # TODO - Add some proper error correction.
    return response.status_code


def stt_get() -> Tuple[str, int, int]:
    """Requests a diarized conversation turn from the stt_tts module."""
    response = requests.get(f"http://{__hostname}:{__stt_port}/incoming_speech")
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


def gui_post(img_path: str, choices: list) -> int:
    """POST to gui server. Returns the response code as an int."""
    data = json.dumps({'file_path': img_path,
                                   'options': choices})
    response = requests.post(url=f"http://{__hostname}:{__gui_port}/update",
                             json=data,
                             headers={'Content-Type': 'application/json'}
                             )
    return response.status_code


def rasa_nlu_post(text: str, message_id: str = "placeholder"):
    """Connect with rasa server to get intents and entities. Returns full response, e.g:
    {
'text': "Sure, let's guess Malaysia.",
'intent':
{
    'name': 'give_answer',
    'confidence': 0.9895011782646179
},
'entities':
[
    {
        'entity': 'answer',
        'start': 18,
        'end': 26,
        'confidence_entity': 0.9995859265327454,
        'value': 'Malaysia',
        'extractor': 'DIETClassifier'
    }
],
'text_tokens': [[0, 4], [6, 9], [10, 11], [12, 17], [18, 26]],
'intent_ranking':
[
    {'name': 'give_answer','confidence': 0.9895011782646179},
    {'name': 'greet','confidence': 0.010290027596056461},
    {'name': 'goodbye', 'confidence': 0.0001419934123987332},
    {'name': 'concur', 'confidence': 6.475452391896397e-05},
    {'name': 'contest', 'confidence': 1.9672743292176165e-06}
]
}
    """
    # https://rasa.com/docs/rasa/pages/http-api/#operation/parseModelMessage
    return requests.post(url=f"http://{__hostname}:{__rasa_port}/model/parse",
                         json={"text": text, "message_id": message_id})


if __name__ == "__main__":
    gui_post("../static/data/img/happy.jpg", ["Option1", "Option2", "Option3", "Option4"])
