import os
import json
from flask import Flask
from flask import render_template , abort

app= Flask(__name__)
filespath='../files'

def getfiles(path):
    # 返回所有文件名(带后缀)
    # files =os.listdir(path)
    # 返回所有文件名(不带后缀)
    files=[fname[:fname.index('.')] for fname in os.listdir(path)]
    return files


@app.route('/')
def index():
    return render_template('index.html',files=getfiles(filespath))

@app.route('/files/<filename>')
def showjson(filename):
    if filename not in getfiles(filespath):
        abort(404)
    with open(f"../files/{filename}.json",'r') as file:
        content=json.loads(file.read())
    return render_template('file.html',content=content)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404



if __name__ == '__main__':
    app.run()

