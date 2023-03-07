import sys
import json
import requests
import os, random

__hostname = "127.0.0.1"
__port = 5006

# To test randomly select a flag image file
flag_dataset_source = 'static/data/Flags Dataset/'
file_path = random.choice(os.listdir(flag_dataset_source))

print(file_path)

conv = [{'file_path': file_path}]
s = json.dumps(conv)
res = requests.post("http://127.0.0.1:5006/update", json=s).json()
#print(res['escalate'])