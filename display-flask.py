# Author:   Andy Edmondson
# Date:     4 Feb 2023
# Purpose:  Serve the flag image files to web browser.
#
#           Expects image files to be in ./static
#           Expects html template files to be in ./templates
#
# Contains: / endpoint using flask api.
#
# TODO:     Add ability to update the web page image dynamically.
#
# To update the file on cli:
# curl -v -H "Content-Type: application/json" -X POST -d '{"filePath":"static/data/img/sad.jpeg"}' http://127.0.0.1:5005/update_flag
# curl -v -H "Content-Type: application/json" -X POST -d '{"filePath":"static/data/img/happy.jpeg"}' http://127.0.0.1:5005/update_flag
#
# Update with ajax from:
# https://stackoverflow.com/questions/26070335/dynamically-update-image-using-python-flask-ajax

from base64 import b64encode
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
# from flask_socketio import SocketIO, emit


app = Flask(__name__)
flag_file = 'static/data/img/happy.jpg'


@app.route('/update', methods=['GET'])
def update():
    global flag_file
    text = "New Text or options"
    return render_template("index.html", flag_image=flag_file, flag_text=text)


@app.route("/update_flag", methods=['POST'])
def update_flag():
    global flag_file
    parser = reqparse.RequestParser()  # initialize
    parser.add_argument('filePath', required=True)  # add arguments
    args = parser.parse_args()
    flag_file = args['filePath']
    new_text = "This is some new text"
    return jsonify({'flag_image': flag_file, 'flag_text': new_text})
    # return render_template("index.html", flag_image=flag_file, flag_text=new_text)  # This line needs to force refresh


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5006)

