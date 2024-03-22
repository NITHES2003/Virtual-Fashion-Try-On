from flask import Flask, render_template, request, Response
import threading
import os
import signal
from replace import run_script as shirtreplace
from size import run_script as shirtsize
from assessory import run_script as acceso

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_script', methods=['POST'])
def start_script():
    global stop_flag
    stop_flag = False
    thread = threading.Thread(target=shirtreplace)
    thread.start()
    return 'Script started'

@app.route('/start_scripts', methods=['POST'])
def start_scripts():
    global stop_flag
    stop_flag = False
    thread = threading.Thread(target=shirtsize)
    thread.start()
    return 'Script started'

@app.route('/start_scriptss', methods=['POST'])
def start_scriptss():
    global stop_flag
    stop_flag = False
    thread = threading.Thread(target=acceso)
    thread.start()
    return 'Script started'

@app.route('/stop_server', methods=['POST'])
def stop_server():
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server stopped'

if __name__ == '__main__':
    app.run(debug=True)