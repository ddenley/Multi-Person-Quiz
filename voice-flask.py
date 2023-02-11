# Author:   Andy Edmondson
# Date:     4 Feb 2023
# Purpose:  Proof of concept for voice to text using flask-server.
#           Conversations are stored in a dicts queue until requested by the dialogue manager.
#
# Contains: incoming_speech endpoint as proof of concept for using flask api for connection.
#
# To GET on cli:
# curl -v -H "Content-Type: application/json" -X GET http://127.0.0.1:5001/incoming_speech
#
# Based on https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f

from flask import Flask
from typing import Tuple


app = Flask(__name__)
count = 0


@app.route('/incoming_speech', methods=['GET'])
def get_next_turn() -> Tuple[dict, int]:
    """Let the DM get the next line of chat."""
    global count
    global concept_data
    turn_text = concept_data[count]
    count = (count + 1) % len(concept_data)                 # Use like a circular buffer
    return turn_text, 200  # return data and 200 OK code


# Create a queue of test data for the test DM to get.
# Should be defined as dicts so client can use .json() to easily recover the data.
concept_data = [
        {"text": "Hi", "player": 1},
        {"text": "yes, we can play", "player": 2},
        {"text": "can you repeat that?", "player": 2},
        {"text": "I think it might be Mongolia", "player": 1},
        {"text": "No way, that's definitely Zimbabwe", "player": 2},
        {"text": "You always say Zimbabwe", "player": 1},
        {"text": "I live in hope.", "player": 2},
        {"text": "Maybe it's Malaysia, shall we say Malaysia?", "player": 1},
        {"text": "Sure, let's guess Malaysia.", "player": 2},
        {"text": "Malaysia!", "player": 1}
    ]


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001)
