# Author:   Andy Edmondson
# Date:     5 Feb 2023
# Purpose:  Proof of concept for text to speech using flask-server.
#           Instead of tts, this will just output to console.
#
# Contains: tts endpoint as proof of concept for using flask api for connection.
#
# To POST on cli:
# curl -v -H "Content-Type: application/json" -X POST -d '{"text": "Say this"}' http://127.0.0.1:5004/tts

from flask import Flask
from flask_restful import reqparse
from typing import Tuple

app = Flask(__name__)


@app.route('/tts', methods=['POST'])
def say_text() -> Tuple[dict, int]:
    """Let the DM get the next line of chat."""
    parser = reqparse.RequestParser()  # initialize
    parser.add_argument('text', required=True)  # add arguments
    args = parser.parse_args()
    text_to_say = args['text']
    tts_function(text_to_say)
    return {"text": text_to_say}, 200  # return data and 200 OK code


def tts_function(tts_text):
    """Text to speech functionality"""
    print(tts_text)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5004)
