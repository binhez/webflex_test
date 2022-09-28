from flask import Flask, jsonify, request, send_file

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home_view():
    return "<h1>Hello World</h1>"
