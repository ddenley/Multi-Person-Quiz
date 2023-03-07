import random

from flask import Flask, render_template, redirect, url_for, request
from flask_restful import reqparse
import json
import pandas as pd

# Development notes:
# Will receive requests of "filepaths" - for this simply give the flag file name e.g. ai.png
# At the moment users can cheat by refreshing page multiple times

app = Flask(__name__)
flag_dataset_source = 'static/data/Flags Dataset/'
code_names_csv = 'static/data/codes_names.csv'

flag_file_path = 'static/data/Flags Dataset/ad.png'
name_options = ["Place holder 1", "Place holder 2", "Place holder 3", "Place holder 4"]

__hostname = "127.0.0.1"
__port = 5006

@app.route('/')
def home():
    global flag_file
    global name_options
    return render_template("index-demo.html", flag_image=flag_file_path, name_options=name_options)

@app.post('/update')
def update():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    print(data)
    # Update the current flag_file
    global flag_file_path
    flag_file_path = data[0]['file_path']
    # Update the current name_options
    global name_options
    name_options = data[0]['options']
    # Refresh the home page



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5006, debug=True)
