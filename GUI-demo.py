from flask import Flask, render_template, redirect, url_for, request
from flask_restful import reqparse
import json


app = Flask(__name__)
flag_dataset_source = ''
flag_file = 'static/data/img/happy.jpg'
name_options = ["Place holder 1", "Place holder 2", "Place holder 3", "Place holder 4"]

__hostname = "127.0.0.1"
__port = 5006

@app.route('/')
def home():
    global flag_file
    global name_options
    return render_template("index-demo.html", flag_image=flag_file, name_options=name_options)

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