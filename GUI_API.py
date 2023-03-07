from flask import Flask, render_template, redirect, url_for, request, json
from flask_restful import reqparse
import json


# curl -v -H "Content-Type: application/json" -X POST -d '{"filePath":"static/data/img/sad.jpeg"}' http://127.0.0.1:5006/update_flag

app = Flask(__name__)
flag_dataset_source = ''
flag_file = 'static/data/img/happy.jpg'
name_options = [" ", " ", " ", " "]

__hostname = "127.0.0.1"
__port = 5006


@app.route('/', methods=['GET', 'POST'])
def home():
    data = [flag_file, name_options]
    # return "Welcome in the quiz"
    return render_template("index_with_refresh.html", data=data)


@app.route('/update',methods=['GET', 'POST'])
def update():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    # Update the current flag_file
    global flag_file
    flag_file = data['file_path']
    # Update the current name_options
    global name_options
    name_options = data['options']
    # Refresh the home page
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5006, debug=True)
