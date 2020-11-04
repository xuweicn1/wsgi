from flask import Flask,request
import time
import requests

app = Flask(__name__)


@app.route('/')
def index():
    delay = float(request.args.get('delay') or 1)

    url = 'http://127.0.0.1:5200/?delay={}'.format(delay)

    resp = requests.get(url)
    return 'Hi there! ' + resp.text