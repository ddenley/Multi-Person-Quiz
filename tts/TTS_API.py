# Author:   Andy Edmondson
# Date:     7 Mar 2023
# Purpose:  TTS Flask API.
#
# Contains: tts endpoint as proof of concept for using flask api for connection.
#
# To POST on cli:
# curl -v -H "Content-Type: application/json" -X POST -d '{"text": "Say this"}' http://127.0.0.1:5004/tts

from flask import Flask
import requests
from flask_restful import reqparse
from typing import Tuple
import TTS
import time
from threading import Thread
import multiprocessing as mp
from queue import Queue, Empty



ptq = Queue()
text_q = mp.Queue()
    
# app = Flask(__name__)

def create_app(q):
    app = Flask(__name__)
    app.config['text_q'] = q
    return app

app = create_app(text_q)


@app.route('/tts', methods=['POST'])
def say_text() -> Tuple[dict, int]:
    """Let the DM get the next line of chat."""
    parser = reqparse.RequestParser()  # initialize
    parser.add_argument('text', required=True)  # add arguments
    args = parser.parse_args()
    time.sleep(0.3)
    text_to_say = args['text']    
    #ptq.put(text_to_say)
    print(f"Adding {text_to_say} to queue.")
    app.config['text_q'].put(text_to_say)
    print(f"Size of q is {text_q.qsize()}")
    # mute_mic()
    # TTS.speech_to_text(text_to_say)
    # unmute_mic()
    return {"text": text_to_say}, 200  # return data and 200 OK code


def speak_some_text(_q):
    """Get the next item to say and say it."""
    while True:
        text_to_say = _q.get()
        mute_mic()
        print(f"Sending {text_to_say}")
        TTS.speech_to_text(text_to_say)
        unmute_mic()


__hostname = "127.0.0.1"
__stt_port = 5001


def mute_mic():
    """Mutes the mic so that the speech to text stream doesn't listen while the tts is talking. AE 12 mar"""
    print("Muting the mic")
    data = {'mute': 'mute'}
    response = requests.post(url=f"http://{__hostname}:{__stt_port}/mute", 
                             json=data, 
                             headers={'Content-Type': 'application/json'})


def unmute_mic():
    """Unmutes the mic so that the speech to text stream starts to listen again. AE 12 Mar"""
    print("Unmuting the mic")
    data = {'mute': 'unmute'}
    response = requests.post(url=f"http://{__hostname}:{__stt_port}/mute",
                             json=data, 
                             headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    
    # mp.set_start_method('fork')
    #text_q = mp.Queue()
    
    #app = create_app(text_q)
    
    p = mp.Process(target=speak_some_text, args=(text_q,))
    p.start()
    
    
    
    #p.close()
    #p.join()
    
    #ttst = Thread(target=speak_some_text, args=(ptq,))
    #ttst.start()
    
    app.run(host="127.0.0.1", port=5004)
    p.join()
    
