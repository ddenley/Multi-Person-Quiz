# Author:   Andy Edmondson
# Date:     4 Feb 2023
# Purpose:  Proof of concept for dialogue manager connecting to other services.
#
# Contains: Simulated dialogue manager with a simple loop through the modules
#
# Use of response based on https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request

import requests
from flag_quiz import FlagQuiz


def voice_client(host, port):
    """Connect to the voice server and get the next diarised turn."""
    response = requests.get(f"http://{host}:{port}/incoming_speech")
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

    return text, speaker


def tts_client(host, port, text):
    """Turn the text into audible speech."""
    # https://data-flair.training/blogs/python-text-to-speech/
    response = requests.post(url=f"http://{host}:{port}/tts", json={'text': text})
    # TODO - Deal with errors etc.


def display_client(host, port, image_path):
    """Set the flag on the display for the next question."""
    response = requests.post(url=f"http://{host}:{port}/update_flag", json={'filePath': image_path})
    # TODO - Deal with errors etc.


def rasa_client(host, port, text):
    """Connect with rasa server to get intents and entities."""
    # https://rasa.com/docs/rasa/pages/http-api/#operation/parseModelMessage
    return requests.post(url=f"http://{host}:{port}/model/parse",
                         json={"text": text, "message_id": "b2831e73-1407-4ba0-a861-0f30a42a2a5a"})


# TODO - Replace with a better example from latest model
""" RASA INTENT & ENTITY RETURN 
{
    'text': "Sure, let's guess Malaysia.", 
    'intent': {'name': 'greet', 'confidence': 0.9880393147468567}, 
    'entities': [], 
    'text_tokens': [[0, 4], [6, 9], [10, 11], [12, 17], [18, 26]], 
    'intent_ranking':[
        {'name': 'greet', 'confidence': 0.9880393147468567}, 
        {'name': 'bot_challenge', 'confidence': 0.0044221277348697186}, 
        {'name': 'affirm', 'confidence': 0.0023878375068306923}, 
        {'name': 'answer', 'confidence': 0.0019169427687302232}, 
        {'name': 'discussion', 'confidence': 0.0010989013826474547}, 
        {'name': 'inform', 'confidence': 0.000635469623375684}, 
        {'name': 'deny', 'confidence': 0.0005948932375758886}, 
        {'name': 'challenge', 'confidence': 0.0004594403726514429}, 
        {'name': 'give_city_answer', 'confidence': 0.00043493194971233606}, 
        {'name': 'goodbye', 'confidence': 1.0103047316079028e-05}
    ], 
    'response_selector':{
        'all_retrieval_intents': [], 
        'default': {
            'response': {
                'responses': None, 'confidence': 0.0, 'intent_response_key':None, 'utter_action': 'utter_None'
            }, 
            'ranking': []
        }
    }
}

"""

if __name__ == "__main__":

    default_image_path = "./img/happy.jpg"

    voice_port = 5001
    tts_port = 5004
    rasa_port = 5005
    display_port = 5006

    rasa_host = "127.0.0.1"
    flask_host = "127.0.0.1"

    quiz = FlagQuiz()

    # Set the default image
    # display_client(hostname, display_port, default_image_path)

    # Conversation loop for 2 questions of 5 turns
    for question in range(2):
        flag_path, options, answer = quiz.get_new_question()
        print(f"The flag path is {flag_path} and the country is {answer}.")
        display_client(flask_host, display_port, flag_path)
        for turn in range(5):
            turn_text, player = voice_client(flask_host, voice_port)
            print(f"{turn_text}  - said by player {player}")
            returnedData = rasa_client(rasa_host, rasa_port, turn_text)
            print(returnedData.json())
        # Say something
        tts_client(flask_host, tts_port, f"This is the flag of {answer}.")
