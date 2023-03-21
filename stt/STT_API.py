from flask import Flask, request
from threading import Thread
import STT
import json
import logging

__hostname = "127.0.0.1"
__tts_port = 5001



app = Flask(__name__)

# Transcription object - will contain the queue to pull from
transcribe = STT.Transcribe()
mute_flag = False

# Get request must return sentence from STT_Module queue
@app.route('/incoming_speech',methods=['GET'])
def return_speech():
    contents = transcribe.get_from_queue()
    if mute_flag is True:
        # print(f"Muted, not sending data back. {contents}")
        return {"text": "None", "player": "None"}, 204
    elif contents is None:
        return {"text": "None", "player": "None"}, 204
    else:
        print(f"Open line, sending back: {contents}")
        return contents
    
@app.route('/mute',methods=['POST'])
def mute():
    # jsondata = request.get_json()
    # data = json.loads(jsondata)
    data = request.get_json()
    global mute_flag
    if data['mute'] == 'mute':
        print("Muting the microphone.")
        mute_flag = True
    if data['mute'] == 'unmute':
        print("Unmuting the microphone.")
        mute_flag = False
    return {"code":200}

def basic_queue_testing():
    queue_contents = transcribe.get_from_queue()
    print(queue_contents)


def run_trans(obj):
    obj.start_trans()


if __name__ == "__main__":
    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
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
