from flask import Flask
from flask import render_template as render
import os
import json

app=Flask(__name__)

@app.route('/')
def index():
    return os.walk('../files/')

@app.route('/files/<filename>')
def file(filename):
    filename+=".json"
    if os.path.isfile(filename):
        return render("404.html")
    else:
        return "Find the file"


