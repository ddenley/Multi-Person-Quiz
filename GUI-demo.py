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

flag_file = 'ad.png'
name_options = ["Place holder 1", "Place holder 2", "Place holder 3", "Place holder 4"]

__hostname = "127.0.0.1"
__port = 5006

code_names_df = pd.read_csv(code_names_csv)

def fromFilePathProduceOptions(filepath):
    # String array holding flag country options to present
    flag_options = []
    # Filepath conversion to code2 for code_names_csv
    filename = filepath.upper()
    filename = filename.split(".")[0]
    # Get correct country name
    dfx = code_names_df.index[code_names_df['code2']==filename].tolist()[0]
    actual_country_name = code_names_df.loc[dfx, 'name']
    flag_options.append(actual_country_name)
    # Randomly select another 3 country names
    i = 0
    while(i <= 2):
        random_name = code_names_df['name'].sample().tolist()[0]
        if random_name not in flag_options:
            flag_options.append(random_name)
            i += 1
    random.shuffle(flag_options)
    return flag_options

@app.route('/')
def home():
    global flag_file
    global name_options
    flag_file_path = flag_dataset_source + flag_file
    return render_template("index-demo.html", flag_image=flag_file_path, name_options=fromFilePathProduceOptions(flag_file))

@app.post('/update')
def update():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    print(data)
    # Update the current flag_file
    global flag_file
    flag_file = data[0]['file_path']
    print(flag_file)
    # Update the current name_options
    # Refresh the home page
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5006, debug=True)
    fromFilePathProduceOptions("ad.png")
