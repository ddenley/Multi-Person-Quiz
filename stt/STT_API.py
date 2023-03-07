from flask import Flask
from flask_api import status
from threading import Thread
import STT
import requests

__hostname = "127.0.0.1"
__tts_port = 5001

app = Flask(__name__)

# Transcription object - will contain the queue to pull from
transcribe = STT.Transcribe()


# Get request must return sentence from STT_Module queue
@app.get("/incoming_speech")
def return_speech():
    contents = transcribe.get_from_queue()
    if contents is None:
        return {"text": "None", "player": "None"}, status.HTTP_204_NO_CONTENT
    else:
        return contents


def basic_queue_testing():
    queue_contents = transcribe.get_from_queue()
    print(queue_contents)


def run_trans(obj):
    obj.start_trans()


if __name__ == "__main__":
    trans_thread = Thread(target=run_trans, args=(transcribe,))
    trans_thread.start()
    app.run(debug=True, port=__tts_port, host=__hostname)


# Defunct Testing code

# if __name__ == "__main__":
#     user_choice = input("1: Run Sever 2: Test Queue Pulling\n")
#     if user_choice == '2':
#         trans_thread = Thread(target=run_trans, args=(transcribe,))
#         trans_thread.start()
#         while True:
#             user_input = input("Any key to get")
#             basic_queue_testing()
#     else:
#         # Start STT thread for constant listening and appending to dialogue queue
#         trans_thread = Thread(target=transcribe.start_trans)
#         trans_thread.start()
#         app.run(debug=True, port=__tts_port, host=__hostname)
