import sys
import json
import requests

__hostname = "127.0.0.1"
__port = 5006

file_path = 'static/data/img/sad.jpeg'
answer = 'test'

conv = [{'file_path': file_path}]
s = json.dumps(conv)
res = requests.post("http://127.0.0.1:5006/update", json=s).json()
#print(res['escalate'])