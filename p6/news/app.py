from flask import Flask

app=Flask(__name__)

@app.route('/')
def index():
    pass

@app.route('/files/<filename>')
def file(filename):
    pass


