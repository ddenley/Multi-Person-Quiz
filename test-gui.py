import sys
import json
import requests
import os, random

__hostname = "127.0.0.1"
__port = 5006

# To test randomly select a flag image file
file_path = 'static/data/Flags Dataset/jm.png'
options = ["Option 1", "Option 2", "Option 3", "Option 4"]

print(file_path)

conv = [{'file_path': file_path, 'options': options}]
s = json.dumps(conv)
res = requests.post("http://127.0.0.1:5006/update", json=s).json()
#print(res['escalate'])