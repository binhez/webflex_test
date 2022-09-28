import configparser
from flask import Flask, jsonify, request, send_file
import pandas as pd
from utils.sqlutil import SqlConn
import datetime
app = Flask(__name__)


@app.route('/')
def home_view():
    return "<h1>Hello World</h1>"

# web_flex_tracking()