from flask import Flask
from flask import render_template,abort

app=Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

@app.route('/')
def index():
    pass

@app.route('/files/<filename>')
def file(filename):
    pass


