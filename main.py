import json
import random
import time
from datetime import datetime
from flask import Flask, render_template
import threading
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()  # magic stuff, makes thread work like thread
socketio = SocketIO()
# app = Flask(__name__, static_url_path='/static')
app = Flask(__name__)
app.debug = True
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
socketio.init_app(app)

random.seed()  # Initialize the random number generator

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/line')
def line():
    labels = ["January", "February", "March",
              "April", "May", "June", "July", "August"]
    first = [100, 900, 800, 700, 600, 400, 700, 800]
    second = [2500, 1350, 980, 1800, 690, 1200, 2800, 2000]
    return render_template('line.html', first=first, second=second, labels=labels)


@app.route('/bars')
def bars():
    labels = ["January", "February", "March",
              "April", "May", "June", "July", "August"]
    first = [100, 900, 800, 700, 600, 400, 700, 800]
    second = [2500, 1350, 980, 1800, 690, 1200, 2800, 2000]
    return render_template('bars.html', first=first, second=second, labels=labels)


@app.route('/feed')
def chart():
    return render_template('feed.html', async_mode=socketio.async_mode)


@socketio.on('connect', namespace='/test')
def test_connect():
    print("Socket session started")
    x = threading.Thread(target=send, daemon=True)
    x.start()


def send():
    while True:
        json_data = json.dumps(
            {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
        data_to_send = {'data': json_data}
        socketio.emit('dataemit', data_to_send, namespace='/test')
        time.sleep(1)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9999, use_reloader=False)
