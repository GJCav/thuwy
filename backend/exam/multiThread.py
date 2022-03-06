import time
import threading
from flask import Flask, request, session, redirect
import requests as R
import json as Json
import os

app = Flask(__name__)
app.secret_key = "abcd222 de------"


@app.route("/")
def index():
    return "hello, world"


@app.route("/sleep/")
def slp():
    time.sleep(5)
    tid = threading.current_thread()

    return f"week up, at {tid.name}"


app.run(debug=True)
app.run
